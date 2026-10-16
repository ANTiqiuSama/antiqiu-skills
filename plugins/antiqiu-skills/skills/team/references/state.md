# 状态与适配器接口

`scripts/monitor_policy.py` 使用 Python 3.10+ 标准库。每个真实作业保留一个状态文件和一个写入入口；固定 Luna 任务持有会话、状态、日志和结果。脚本不运行模型、任意命令、实验或调度器。现有 version=1 状态与命令可直接沿用，新增执行身份首次出现时重新取样，不清空已有交接记录。事件派发与处理完成分开记录。

## 观测输入

```json
{
  "job_id": "attempt_example_01",
  "execution_id": "boot-id:1379:4226529",
  "observed_at": "2026-09-12T08:00:00Z",
  "status": "running",
  "phase": "evaluation",
  "alive": true,
  "identity_verified": true,
  "completed": 20,
  "total": 100,
  "progress_comparable": true
}
```

- `job_id` 标识当前作业，不同 attempt 使用不同状态；`execution_id` 标识同一作业的当前执行实例，由真实身份推导。可观测执行身份时提供，切勿为了保留旧速率省略它。
- `observed_at` 含时区且晚于前次实际观测。`status` 只接受 running / unknown / succeeded / failed / needs_decision；明确终态来自作业证据，不能按计数推定。
- `alive` 是 true / false / null，`identity_verified` 缺省 false；无法观测与确认消失不同。`phase` 非空且 `progress_comparable=true` 才允许同单位估时。`completed`、`total` 同时缺省/null 或同时为非负有限数，前者不能大于后者。
- 事件使用稳定 `event_key` 与简短事实 `detail`，不要把每秒变化的时间戳、整份日志或秘密放进事件身份。unknown 连续三次触发无法观测事件；明确失败或决策需求直接触发。

有生产端历史时增加 `progress_samples`：

```json
{
  "job_id": "attempt_example_01",
  "execution_id": "boot-id:1379:4226529",
  "phase": "evaluation",
  "total": 100,
  "source": "completed_event_file_mtime",
  "points": [
    {"at": 1789199760, "completed": 18},
    {"at": 1789199880, "completed": 19},
    {"at": 1789200000, "completed": 20}
  ]
}
```

这是字段值，外层仍需观测字段。身份/阶段/总量匹配，提供 3–64 个时间和计数严格增加的点，且不超过本次观测。`source` 是非空来源名，不能冒用保留名 `wake_observations`。取样语义及 ETA 失效规则见 [progress.md](progress.md)。

## 调用与动作

```text
python monitor_policy.py observe --snapshot SNAPSHOT.json --state STATE.json
python monitor_policy.py dispatched --state STATE.json --event-id EVENT --worker-id ACTUAL_AGENT_ID
python monitor_policy.py resume --state STATE.json --event-id EVENT
python monitor_policy.py handled --state STATE.json --event-id EVENT
```

`observe` 可加 `--min-minutes`、`--initial-minutes`、`--max-minutes`，保存后沿用。JSON 解析或身份错误应报告并检查当前绑定，不能删状态重试。写入为单文件替换，不支持多个并发写入者。持久状态保留最新观测、有限历史、策略和交接证据；不保存完整会话。

| action | 含义与下一步 |
| --- | --- |
| wait | 根据 interval_minutes 更新原 heartbeat，确认后结束本轮 |
| escalate | 已有 pending 证据，尚未派发；交给大模型，取得真实 id 后 dispatched |
| wait_for_worker | 已派发；等同一 agent 的完成事件，补充事实也交给它 |
| stop | 该监控已完成；暂停原计划 |
| rearm | 大模型明确交回等待；执行一次新观测后恢复原计划 |

`interval_minutes`、`proposed_next_check_at`、阶段 ETA 和 `schedule_basis` 是建议；`scheduled=false` 表示本脚本没有调用调度器。使用实际工具配置证明调度生效，不能修改这一字段来代替调度。

## 交接不重复

`pending` 保留原始触发快照，后续新问题保存在 `latest_incident`；不会因一次恢复健康就遗失尚未处理的问题。`event_id` 指实际交接事件，`observed_event_id` 可表示本次另一个问题。模型派发响应不确定时先查已有 agent，不能直接重试。

取得真实 id 后才 `dispatched`；相同 id 可确认，不得改派第二个 id。通过 `send_message_to_thread` 交接时保存目标任务 ID、发送时间及可取得的目标轮次 ID，并核对发送后的对应结果。消息成功回执和 `handoff_sent=true` 都只证明派发；旧适配器把事件加入 `handled_event_ids` 也不能替代处理凭据。目标轮次失败时保留未解决事件并报告交接故障，不能把它记成完成。大模型实际完成且决定继续等同一作业时 `resume`，状态变为 `released`，同一执行实例的相同问题暂不重复派发；确认恢复健康或核实新的 execution_id 后，允许独立复发。执行身份缺失和 unknown 不算重启/恢复，不要求稀疏检查必须先看到健康中间态才能识别新实例的失败。

只有实际结果证据证明接收任务已处理，才可 `handled`；此状态保持停止，包括随后迟到的错误观测。需要新作业时先确认身份并创建新作业状态。脚本不能核实 agent 的真实完成，ack 命令必须以实际完成事件和结果为依据。停止请求、失败或 unknown 都不构成恢复授权。

自动恢复须由项目适配器在调用前验证原 attempt、协议、输入、配置/权重身份全部一致，checkpoint 有效、旧进程已确认退出、事故此前未恢复，并将恢复计数持久化；最多一次。同一状态/事故不得因句柄失效或派发不确定重复启动。未满足全部条件时交给协调者。

## 项目入口

适配器只持有项目身份、只读探针、超时和策略边界；通用估时与去重调用本 Skill。启动探针前先检查 `pending_decision(state)`，若返回待交接/已派发/已结束动作，直接处理动作，无需再次读作业。正常情况下采集一次 snapshot，格式无效的观测转为本作业的 unknown 以累计无法观测次数；作业身份不匹配仍是必须核查绑定的显式错误，不能改写成另一作业的观测。随后 `observe` 并保存，禁止在入口中循环等待。

在任务 `work/task-monitor/CONTEXT.md` 保留后续唤醒真正需要的少量运行信息：实际目标任务与计划 ID、入口命令/可用运行时、作业绑定与输出路径、模型设置以及唯一目标 SSoT 的入口。授权、判断边界和验收条件从当前目标 prompt 引用，不在 CONTEXT 另存会漂移的目标摘要。绑定可增加 `goal_prompt_pointer` / `goal_prompt_pointer_windows` 指向同一文档入口；版本变化时重新解析，派发时传实际版本，不把绑定时的旧版本永久写死。频率从 state 和实际计划读取，不复制会过时的分钟数；保持一个入口，不建立通用守护进程或重复任务。
