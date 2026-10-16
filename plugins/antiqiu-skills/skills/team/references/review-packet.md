# 审查、裁决与执行包

## 身份与回执

新项目或影响方案、执行身份、输入条件、协议、主张的实质变化先审查。执行包不可变；`canonical_execution_revision(execution_packet)` 以 UTF-8、排序键、紧凑 JSON、拒绝 NaN 的规范序列计算 `sha256:<hex>`，提交、回执与裁决均绑定此值。预期实施代码、产物和验证证据记为执行结果，不逐步重审；超出原包的实质变化另建新包，旧回执不授权新包。

读取原始 JSON 回执，核对 runner `status=success`、`exit_code=0`、请求及实际模型均为 `grok-4.7`、`requested_reasoning_effort="xhigh"`、`launch_reasoning_effort="xhigh"`、`effort_evidence` 为 `launch_argument` 或 `server_echo`、`isolation_verified=true`、`tools_available=[]`、`tools_used=[]`、非空 `result` 及匹配的 revision。`actual_reported_reasoning_effort` 若存在须为 `xhigh`；无服务回显时只报告 CLI 参数证据。缺失、不匹配、来源不明或 CLI 失败的回执不允许实施；摘要、旧 High 回执、布尔标志和单独 exit 0 均不能替代它。

Grok 仅对抗审查，不访问或写仓库；只发送明确允许外发且已脱敏的材料。当前选定模型结合意见与本地证据，写出同修订裁决（`accepted`、`rejected`、`needs_evidence`）及理由。仅 `accepted` 可进入实施。

## 执行包与授权

机器可读 `execution_packet` 包含以下具体、可核对的十项：

1. `attempt_protocol`：attempt ID、协议版本。
2. `objective_claims`：目标及论文/产品主张。
3. `inputs_identity`：数据、代码、配置、权重及版本/哈希。
4. `write_scope`：允许写入的精确路径和边界。
5. `command_environment`：命令、cwd、运行时、依赖身份。
6. `budget_stop`：时间/计算/成本预算和停止条件。
7. `metrics_aggregation`：指标、聚合、样本/seed 规则。
8. `engineering_completion`：工程完成的可观察条件。
9. `scientific_predicate`：科学 pass/fail/inconclusive 判定；非科学任务写 `not_applicable`。
10. `evidence_recovery_escalation`：结果、日志、checkpoint 位置，恢复和升级条件。

不适用字段说明原因，缺项按字段名报告。顶层必需字段不得仅为布尔值或空值，嵌套元数据允许布尔值。路由器的非空/哈希校验不代替调用者对包与原始证据的判断。项目协议、指标、阈值和具体主张留在项目包。

只读项目审查可绑定材料哈希。`task_kind:"review"`（缺省 `operation:"review"`）、显式 `operation:"review"` 或 `task_kind:"judgment"` 均回到协调者，不构成实施授权。实施须有完整包、有效回执、接受裁决、`current_step_authorized:true`、`executor_authorized:true` 及准确绑定的固定 Luna executor。复用任务已有授权，不逐步询问；授权或绑定失效时停止受影响实施。
