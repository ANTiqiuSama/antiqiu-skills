# 大任务用量与低额度报告

长期 Goal、跨轮次研究、多 worker 或多阶段实施，在结束或交接时仅为达到展示阈值的用量附一行汇总。小改动和无变化的监控唤醒不强制报告。统计直接复用已有回执或状态，不为取数生成额外模型调用，也不因统计缺失停下可继续的工作。

## 取数与口径

- 1 B = 1,000,000,000 tokens；面向用户只保留一位小数，按四舍五入显示。小于 0.05 B、显示为 0.0 B 的用量直接省略，不逐项列根任务／worker 小数，也不补充“用量很少”。原始整数计数保留在内部记录；token 用量不等于计费金额。
- 本任务计数优先于整个历史会话计数。累计快照用结束总量减开始总量；没有开始快照时，明确只能报告会话累计，不能标成本任务消耗。同一请求／会话区间只能计数一次；不要把根任务已汇总的 worker 消耗再加一遍。
- 优先读取服务返回的 `total_tokens`／明确的总量字段。缓存输入和推理输出若已包含在输入／输出中，不能重复相加。字段语义不清、计数器重置、记录缺失时标为未知或部分统计，不用字符数、耗时或额度百分比反推 token。
- Codex：协调者与 GPT-6 Luna 共用当前 Codex 账户额度。用户显式指定 MiMo 时也读取同一账户。有实际 Goal 时可读取 `get_goal` 的范围内用量；没有 Goal 不为统计创建一个。也可读取当前任务的本地会话 `token_count` 中 `total_token_usage`，以前后快照作差。`get_usage_limits` 只代表 Codex 账户额度，不代表 Grok／Gemini，也不能换算为 token。
- Grok CLI：复用调用回执的 `model_usage`；需要会话汇总且确有该 CLI 会话 ID 时，使用已安装 CLI 的 `grok usage <SESSION_ID>`。Codex 任务 ID 不能当作 Grok CLI 会话 ID。通过其他宿主调用 Grok 时，使用那个宿主实际提供的用量；不要假设一定有 CLI 记录。
- Gemini：复用 Antigravity 回执的 `model_usage` 或当前接入方提供的用量数据。缺少明确总量就保留原始字段并报告部分统计，不猜输入是否包含缓存。
- 保留来源、供应商、模型、统计范围和截至时点；没有读到当前回执或接口的字段就写“未知”，不能让 worker 自述的估算冒充实测。

## 剩余额度

本任务实际使用 Codex、Grok 或 Gemini 时，在已有回执、已支持的只读额度接口或用户提供的当前额度中取值。任一已知窗口剩余 **严格低于 30%**，报告供应商／模型、窗口、剩余百分比及已知重置时间；恰好 30% 不触发低额提醒。多窗口分别判断，不平均，也不混用供应商。

若供应商只给 `usedPercent`，剩余为 `max(0, min(100, 100 - usedPercent))`。未提供额度接口或字段就写“Codex／Grok／Gemini 剩余额度未知”。未使用的供应商无需查询或播报。账户余额、请求次数、上下文余量、Goal token budget 与限流百分比是不同指标，保留其原始名称和单位。

低额度提醒只负责告知，不自动暂停 Goal、降低质量、切换模型或购买／兑换额度。只有用户设置的预算、服务实际硬限制或用户明确指令约束后续执行。不要为了满足报告读取凭据、逆向认证接口或调用模型询问它自己的额度。

## 汇总工具与输出

`scripts/usage_report.py` 可对已有的标准化 JSON 做确定性汇总，或读取当前 Codex 会话。标准化数据的 `records` 每项包含唯一 `measurement_id`、`provider`、明确的 `total_tokens`（未知为 null）、`source`，可附 `model`、`scope`、`as_of`；`quotas` 每项包含 `provider`、`window`、`remaining_percent` 或 `used_percent`，可附 `reset_at`。`used_providers` 只列本任务实际使用者。不要同时传入相互重叠的会话和 worker 总量。

```text
python usage_report.py --input <normalized-usage.json>
python usage_report.py --codex-session <current-session.jsonl> --request-text <unique-user-request-text>
```

示例结尾：`本任务已记录用量 0.2 B；Grok 5 小时窗口剩余 24%。` 小用量场景完全省略 token 一项；额度低于 30% 的提醒独立保留。汇总脚本的 `report_tokens=false` 表示不展示 token 用量，`measured_total_tokens` 仅供内部核算。 若统计不全，写 `已记录部分用量 … B；Gemini 总用量／剩余额度未知`。报告时不得承诺覆盖尚未记入日志的最终答复。
