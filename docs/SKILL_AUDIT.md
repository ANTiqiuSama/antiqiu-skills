# Personal Skill audit

## 审计边界

本次审计以 2026-08-13 本机文件为准。

| 层级 | 发现结果 | 处理方式 |
| --- | ---: | --- |
| `~/.codex/skills` 中启用的个人 Skill | 11 | 10 个通用 Skill 逐项分析；`hatch-pet` 按用户要求排除 |
| 同目录中的 `SKILL.md.disabled` | 7 | 保留停用，不重新发布为启用项 |
| `~/.agents/skills` 的可发现 Skill | 16 | 字节内部或通用工具依赖，只审计边界，不复制 |
| Codex 系统 Skill | 6 | OpenAI 维护，不修改 |
| 插件缓存中的 Skill 文件 | 93 | 各插件维护，不修改；实际暴露还受插件配置和版本影响 |

外部层数量只是磁盘快照，不代表每个 Skill 都在每次任务中启用。插件配置、产品版本和上下文预算会改变最终列表。

## 结论

纳入总库的通用个人层从 10 个收敛为 7 个。三组合并均发生在职责连续且重复加载成本真实存在的地方：

```text
brainstorming + writing-plans
  → plan-work

executing-plans + verification-before-completion
  → execute-work

receiving-code-review + systematic-debugging
  → diagnose-work
```

没有继续合并 `refine-text`、`human-writing` 和 `write-action-first`。三者表面上都碰文字，实际产物不同：第一个改已有材料，第二个创作自然中文作品，第三个只整理聊天回复。把它们合在一起会让中文文风规则误伤技术文档，也会让“行动优先”擅自改写用户原文。

`hatch-pet` 是 Codex 宠物制作专用工具链，与通用工作流没有重复。它不进入本仓库、不参与统计，也不会在本地同步时被修改或停用。

## 逐项分析

### 1. `brainstorming`

- **原作用**：处理目标、约束或方案空间不清的研究与产品任务，先发散再收敛。
- **真实价值**：阻止 Agent 在问题还没定清时直接进入实现，也避免为了澄清而无限追问。
- **重复**：收敛后的执行 brief 与 `writing-plans` 的 Outcome、Constraints、Approach 和 Steps 高度重复。
- **潜在冲突**：在目标已经明确的任务中仍生成多个方案，会延迟直接修改。
- **处理**：并入 `plan-work` 的“目标不清或真实取舍”分支。明确任务直接跳过发散。

### 2. `writing-plans`

- **原作用**：为多依赖、跨系统或高风险工作生成精简实施计划。
- **真实价值**：让步骤包含产物、依赖、触及范围和最小验证，而不是写一份抽象待办清单。
- **重复**：前半段与 `brainstorming` 的收敛产物重复，后半段容易和 `executing-plans` 同时触发。
- **潜在冲突**：对一两个可逆动作也写正式计划，形成流程替代执行。
- **处理**：并入 `plan-work`。保留按风险选择“无计划、短清单、详细计划”的判断。

### 3. `executing-plans`

- **原作用**：按已接受计划持续工作，一次推进一个真实步骤，证据变化时更新计划。
- **真实价值**：减少每一步都重新请求批准和机械执行过期计划的问题。
- **重复**：每个步骤后的检查与 `verification-before-completion` 的完成门重复。
- **潜在冲突**：如果 `writing-plans` 同时被加载，Agent 可能边执行边持续重写计划。
- **处理**：与完成验证合并为 `execute-work`。方向未定时不触发。

### 4. `verification-before-completion`

- **原作用**：在宣称完成前，用当前证据运行与风险相称的新检查。
- **真实价值**：避免“已经改了”被误报成“已经可用”，同时反对每次都跑全量测试。
- **重复**：`executing-plans`、`systematic-debugging` 和 `keep-task-in-scope` 都有比例验证表述。
- **潜在冲突**：作为宽泛隐式 Skill 容易在任何修改任务中额外加载，即使上层执行流程已经包含验证。
- **处理**：并入 `execute-work` 的完成阶段。诊断流程只负责复现与回归，范围控制只引用完成验证，不再复制整套门。

### 5. `receiving-code-review`

- **原作用**：把评审意见当作待验证假设，分类为接受、调整、延后或拒绝。
- **真实价值**：同时避免盲从 reviewer 和为了反对而反对。
- **重复**：核对代码、要求、兼容性和测试，本质上和 debugging 的证据定位相同。
- **潜在冲突**：评审指出真实 Bug 时，两个 Skill 可能先后重复读代码和测试。
- **处理**：并入 `diagnose-work` 的“评审反馈”入口，共享证据收集和最小修复阶段。

### 6. `systematic-debugging`

- **原作用**：复现、定位首个偏差、建立可证伪假设，再改根因。
- **真实价值**：防止把多个猜测补丁叠在一起，并为深调用链、条件等待和防御层提供按需参考。
- **重复**：和评审处理都要求先验证主张；完成后的回归又与执行验证相邻。
- **潜在冲突**：原因已经显然时仍强行跑完整诊断流程，会增加无效步骤。
- **处理**：并入 `diagnose-work`。把 5 个、636 行的支持材料收敛成“根因追踪”和“基于条件等待”两个通用参考；删除要求每层都加校验的绝对规则、项目专属 TypeScript 示例、npm 专用污染脚本和不可复核的案例数字。明确显然错误直接修，不触发本 Skill。

### 7. `keep-task-in-scope`

- **作用**：约束长期优化、冻结、审计、迁移、宽测和新基础设施，防止辅助流程挤走主交付物。
- **真实价值**：区分探索、确认和发布，并给可选工作设置 Evidence、Consequence、Decision impact 和 Proportion 四道门。
- **重复**：原文包含一段完成验证，与旧 `verification-before-completion` 重复；正式规划又可能与旧 `writing-plans` 重合。
- **潜在冲突**：如果对普通直接改动也触发，会把“防过度流程”本身变成额外流程。
- **处理**：保留独立名称，只用于长期循环和真实范围决策；删除重复验证流程，改为衔接 `plan-work` 和 `execute-work`。

### 8. `refine-text`

- **作用**：保真地润色、压缩、扩写、重组和综合已有材料。
- **真实价值**：先锁定事实、约束、立场、引用和不确定性，再优化逻辑、结构和表达。
- **重复**：与 `human-writing` 都能处理中文改稿，与 `write-action-first` 都强调结论靠前。
- **潜在冲突**：如果自然中文风格规则先于保真处理，可能改变原意；如果行动优先规则作用于文稿本身，可能破坏文体。
- **处理**：保留。描述明确限定“已有文本和保真变换”；自然中文作品在完成含义与结构阶段后才交给 `human-writing`；`write-action-first` 只整理外围回复。

### 9. `human-writing`

- **作用**：创作和深度改写自然、有材料、有中文韵律的文章与叙事。
- **真实价值**：现实写作先做材料门，虚构写作守人物与因果，并通过按需参考和检查脚本减少模型腔。
- **重复**：旧描述把教程、评测、润色等范围写得过宽，容易抢到普通技术文档和一般改稿。
- **潜在冲突**：冒号、破折号和翻案句式禁令适合成稿，不适合代码、机器字段、结构化报告和普通聊天。
- **处理**：保留完整领域能力，把启动描述从 1,158 字节缩到 420 字节；明确普通校对、技术文档和报告走 `refine-text`。用户格式、事实与引用高于文风规则。

### 10. `write-action-first`

- **作用**：让聊天回复先出现结果、答案、状态、阻塞项或用户真正需要执行的动作。
- **真实价值**：减少铺垫、支线、无依据时间估算和把 Agent 能做的工作推回用户。
- **重复**：与全局 AGENTS.md 的“结论优先”和 `refine-text` 的读者导向存在局部重复。
- **潜在冲突**：自动命中所有状态更新和说明文时，会把解释压得过短，或擅自给已完成任务制造下一步。
- **处理**：保留为显式输出模式，并设置 `allow_implicit_invocation: false`。它只改变聊天呈现，不改变产物和判断。

## 停用目录

以下 7 项已经没有有效 `SKILL.md`，本次不重新启用：

- `apply-design-typography-standards`
- `build-project-wiki`
- `dispatching-parallel-agents`
- `finishing-a-development-branch`
- `using-git-worktrees`
- `using-superpowers`
- `validate-prompt-before-execution`

它们有的已被当前系统能力替代，有的触发过宽，有的依赖用户显式授权。保留 `.disabled` 文件比重新打包兼容别名更安全，也不会占 Skill 列表。

## 外部 Skills

- **Codex 系统 Skills**：例如 `skill-creator`、`plugin-creator` 和 `openai-docs`，由 OpenAI 随产品更新。本仓库不复制，避免版本分叉。
- **插件 Skills**：文档、表格、浏览器、数据分析等能力随插件安装和版本变化。本仓库不接管。
- **字节内部 Skills**：`bytedcli`、Codebase、Lark、日志与 APM 等依赖内部命令、权限和服务。本仓库是公开库，复制它们既会造成维护分叉，也可能泄露内部契约，因此完全排除。

## 组合规则

一次任务默认只选一个阶段型 Skill：`plan-work`、`execute-work` 或 `diagnose-work`。

领域 Skill 可以和阶段型 Skill 配合，但职责不交叉。例如“分析并重写一篇中文报告”可以先用 `refine-text` 锁定事实，再在用户明确要求自然中文作品时使用 `human-writing`；不需要同时让两个 Skill各自重新分析全文。

`keep-task-in-scope` 是长期任务的范围门，不是第四个常规阶段。`write-action-first` 是显式呈现层，不参与实现决策。
