---
name: team
description: 用户明确说出 /team、$team、“混动”，或明确要求操作 Herdr、在 Herdr 标签页间协调 Codex/Claude Code/Antigravity/Gemini 时使用：按变更范围做 Grok 隔离审查、协调裁决，默认由 GPT-6 Luna Low 实施和监看；Herdr 模式负责多 Agent 拓扑、工件验收与有界恢复。普通单模型任务或进程内委派不触发。
---

# 混动团队

仅在用户明确要求 `/team`、`$team`、“混动”或 Herdr 编排时启用。当前选定模型协调、裁决和验收；默认由 `gpt-6-luna` / `low` 实施及监看，用户明确覆盖优先。普通单模型任务不进入此流程。

## 审查与实施

新项目或影响方案、执行身份、输入或主张的实质变化，先用隔离 Grok 4.7 XHigh CLI 对抗审查。匹配当前修订的有效回执可复用，不逐命令重审。Grok 只读最小允许外发的审查包，不访问或写入仓库。

按 [CLI](references/cli.md) 调用，并按 [审查与执行包](references/review-packet.md) 核原始回执、实际模型/effort、退出状态、隔离、工具清单和 revision。成功审查不等于接受；协调者作同修订裁决。实施前，回执、接受裁决及完整十项执行包须绑定同一规范哈希，并有当前步授权和准确 executor 绑定。缺项逐项报告；科学字段不适用时明确写 `not_applicable`。

`scripts/route_task.py` 提供 `route(request)` 与 JSON CLI；`canonical_execution_revision()` 生成规范包身份。只读 review/judgment 返回协调者，不构成实施授权。计划模式只读，不启动实施。未知协调模型保持 `null`；Gemini/MiMo 仅按用户明确覆盖使用。指定模型不可用或硬限流则报告具体阻塞，不静默换模型；低额度仅提醒。

## 长作业与验收

只有身份核实的真实作业才监看。复用用户授权的固定任务与附着 heartbeat；同项目避免重复任务或临时 cron。稳定状态、日志与结果用于检查，不能依赖跨任务终端 ID。无行动价值变化保持安静；派发不等于处理完成。

动态间隔、去重与恢复条件按 [状态](references/state.md)、[长等待](references/wait.md) 和 [运行时](references/runtime.md)。不擅自暂停 Goal 或恢复用户停止的作业。未知状态、科学失败、身份不符或 checkpoint 无效时交给协调者；符合原作业身份、旧进程退出和同事故未恢复等条件时才允许一次恢复。

协调者以代码、程序、作品或真实实验结果验收实施任务；工程完成与科学 pass/fail/inconclusive 分开。审查包和回执保留必要机器字段，不扩写成额外长报告。交付简述成果入口、验证与实质缺口；指标和协议留在项目包，用量按 [用量报告](references/usage-reporting.md)，不因余额改模型。

## Herdr 模式

用户要求操作 Herdr、检查 Herdr fleet，或在 Herdr 标签页间组织跨厂商辩论与执行时，Herdr 作为终端与生命周期控制面。仅解释、检查 fleet 时不需 Grok 审查；实施类变更仍按上文审查、裁决与验收，用户指定的 Agent 与模型优先。先读 [Herdr 模式](references/herdr.md)：确认 `HERDR_ENV=1` 并先运行 `herdr --skill`，一个可写任务对应一个 worktree 与 workspace，派发全部独立任务后再等待，以工件和验收命令而非 `done` 状态判定完成，不代用户回答审批。

按需加载：模型与端点配置读 [providers](references/herdr-providers.md)；论文审稿、跨模型辩论、图表与实验缺口读 [paper workflow](references/herdr-paper-workflow.md)；超时、`unknown`、消失或无工件回到 idle 读 [recovery](references/herdr-recovery.md)。单个小任务不建 fleet。
