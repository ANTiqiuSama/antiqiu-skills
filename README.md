# ANTiqiu Skills

一套经过收敛和回归测试的个人 Agent Skills。它覆盖规划、执行、诊断、范围控制、既有 Agent 指令精简、文本炼化、中文技术文档、自然中文写作和行动优先输出。

## 这次整理解决了什么

整理前有 11 个启用的个人 Skill。`hatch-pet` 是独立的 Codex 宠物制作工具链，按用户要求排除；其余 10 个通用 Skill 中有三组会在同一阶段重复触发：

- `brainstorming` 与 `writing-plans` 都会把问题变成计划；
- `executing-plans` 与 `verification-before-completion` 都会控制交付末段；
- `receiving-code-review` 与 `systematic-debugging` 都要求先核验证据再改代码。

现在它们分别合并为 `plan-work`、`execute-work` 和 `diagnose-work`。其余 Skill 保留独立边界，没有为了减少数量而做成一个无所不包的大 Skill。

在 2026-08-13 的合并快照中：

| 指标 | 整理前 | 整理后 | 变化 |
| --- | ---: | ---: | ---: |
| 纳入通用总库的个人 Skill 数 | 10 | 7 | -30.0% |
| 启动时的名称与描述字节数 | 3,784 | 2,368 | -37.4% |
| 三组重叠工作流的 `SKILL.md` 行数 | 186 | 105 | -43.5% |
| 诊断按需支持材料 | 5 文件 / 636 行 | 2 文件 / 63 行 | 行数 -90.1% |

这些指标证明启动和匹配阶段需要读取的个人元数据更少，也证明同一任务不再需要加载两份相邻流程；深度诊断时需要读取的按需材料也显著缩短。它们不等价于固定的端到端耗时承诺，模型、网络、工具和任务本身仍会影响实际速度。

2026-08-14 新增的 `trim-agent-instructions` 是一个此前不存在的专项能力，不是把旧 Skill 拆回来。当时总包有 8 个 Skill，启动名称与描述共 2,789 字节。

2026-08-28 又评估了 Antigravity 中安装的 `ste-cn`。本机发现的 4 份副本内容相同，但都没有上游地址或许可证文件；其职责也与 `refine-text` 的技术文档改写高度重叠。因此总库没有复制原文或新增第 9 个 Skill，而是把可复用的受控中文写作方法独立重写为 `refine-text` 的按需参考。当前仍是 8 个 Skill，只有处理中文技术材料时才加载这部分规则；启动名称与描述共 2,828 字节，仍比整理前的 10 个减少 25.3%。

详细逐项审计见 [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md)，测试证据见 [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md)。

## 当前 8 个 Skills

| Skill | 负责什么 | 典型触发 |
| --- | --- | --- |
| [`plan-work`](plugins/antiqiu-skills/skills/plan-work/SKILL.md) | 澄清目标、比较真实方案、生成精简执行路径 | 目标不清、存在真实取舍、多系统或多依赖计划 |
| [`execute-work`](plugins/antiqiu-skills/skills/execute-work/SKILL.md) | 按已定方向持续实施，并用新证据验证完成 | “按计划继续”“执行下面步骤”“做到完成” |
| [`diagnose-work`](plugins/antiqiu-skills/skills/diagnose-work/SKILL.md) | 定位非显然故障，或判断评审意见是否成立 | Bug、回归、性能、偶现测试、模糊或冲突的 review comment |
| [`keep-task-in-scope`](plugins/antiqiu-skills/skills/keep-task-in-scope/SKILL.md) | 约束长期任务和可选流程，防止主交付物被挤走 | 持续优化、SOTA、冻结、哈希、审计、迁移、宽测和新基础设施 |
| [`trim-agent-instructions`](plugins/antiqiu-skills/skills/trim-agent-instructions/SKILL.md) | 审计并精简已有 Agent 指令链，保留真正改变行为的规则 | AGENTS.md、AGENTS.override.md、CLAUDE.md 等指令去重、删旧、缩写和纠冲突 |
| [`refine-text`](plugins/antiqiu-skills/skills/refine-text/SKILL.md) | 保留事实、立场和不确定性的文本炼化，以及清晰一致的中文技术文档 | 润色、压缩、扩写、重组、总结、README、运行手册、API 文档和技术方案 |
| [`human-writing`](plugins/antiqiu-skills/skills/human-writing/SKILL.md) | 写出有材料、有说话位置和自然中文韵律的作品 | 中文长帖、文章、叙事、故事、口播和明确的去 AI 味改稿 |
| [`write-action-first`](plugins/antiqiu-skills/skills/write-action-first/SKILL.md) | 把聊天回复整理成先结果、易扫描、可执行的形状 | 仅显式调用，或用户明确要求行动优先、ADHD-friendly、不要铺垫 |

## 怎么选择

先选当前阶段，只用一个主工作流：

1. 方向还没定，使用 `$plan-work`。
2. 方向已定，要持续完成，使用 `$execute-work`。
3. 原因不清或收到可疑评审，使用 `$diagnose-work`。

随后按产物选择最多一个领域 Skill。已有 Agent 指令用 `$trim-agent-instructions`；普通已有文本和中文技术文档用 `$refine-text`；文章、叙事等自然中文作品用 `$human-writing`。

`$keep-task-in-scope` 只在长期循环或额外流程可能挤占主任务时叠加。`$write-action-first` 只改变回复形状，不改变代码、结论或原始文稿，因此默认禁止隐式调用。

如果多个 Skill 同时命中，按下面的顺序处理：

```text
用户明确格式与安全边界
  → 领域事实与产物规则
  → 当前工作阶段
  → 长期范围约束
  → 回复呈现方式
```

## 怎么使用中文技术文档模式

不需要安装或调用单独的 `ste-cn`。直接让 `$refine-text` 处理已有中文技术材料：

```text
使用 $refine-text 重写这份运行手册。
保留现有事实、条件、命令和不确定性；统一术语，把有独立失败或重试方式的动作拆成步骤。
这是增量更新，请同时检查受影响的旧章节，修正已经过时或互相矛盾的内容。
```

它会在通用的“保真、逻辑、结构、表达”流程之后，按需读取 [`plain-technical-chinese.md`](plugins/antiqiu-skills/skills/refine-text/references/plain-technical-chinese.md)。这部分主要做四件事：

- 一个概念使用一个稳定名称，产品名、字段名、命令、路径和错误文本保持原样；
- 条件放在它约束的动作前，责任不清时才明确执行者，不凭空补负责人；
- 有不同失败、重试、回滚或验证方式的动作分开写，紧密耦合的动作不机械拆分；
- 删除没有证据的“充分保障”“显著提升”等自证表达，同时保留原文的限制和不确定性。

这不是固定句长、段落数或清单分数驱动的模板。中文没有必要照搬英文词数规则；是否拆句，以读者能否准确理解、执行和验证为准。它也不是 [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) 的中文版、实现或认证。

`$refine-text` 与 `$human-writing` 的边界不变：README、运行手册、API 文档、错误信息和工程方案走前者；论坛长文、叙事、口播或明确要求自然中文韵律的作品走后者。若用户只要求写新代码，不要因为代码里有注释就触发文本炼化。

## 怎么使用 `trim-agent-instructions`

这个 Skill 处理的是“仓库里已经存在一套 Agent 指令，但越积越重”的问题。它不以删到某个行数为目标，而是逐条判断：没有这条规则时，Agent 的进入条件、取证、动作或验证会不会发生有价值的变化。

最直接的用法是：

```text
使用 $trim-agent-instructions 审计并精简这个仓库实际生效的 AGENTS.md 指令链。
删除重复和已经失效的规则，缩短有价值但过长的规则，修正冲突或含糊表达；
直接修改并做与风险相称的验证，不要追求固定删减比例。
```

只想先看分析、不改文件时，要把只读边界写明：

```text
使用 $trim-agent-instructions 只读分析根目录到 packages/api 的 Agent 指令链。
给出 keep、delete-obvious、delete-stale、shorten、improve 五类结论和关键依据，暂不修改。
```

它会按下面的顺序工作：

1. 先确认当前 Agent 产品真正使用的文件名、继承范围和优先级，不假定所有工具都遵循同一套规则。
2. 只读取会影响目标目录的父级到当前目录指令链；只有子目录继承也在审计范围内时，才继续向下读。
3. 对每条规则判断现实依据和行为差异，分为保留、删除显然项、删除过时项、缩短或改进。
4. 路径已消失、内容完全重复或只是空泛口号时，静态证据就够了。只有高影响且结论不确定，并且测试结果真的会改变决定时，才做一次隔离的新会话对照。
5. 修改后重新读取有效指令链，检查仍被引用的路径和命令；优先复用仓库已有检查。只有发现范围或优先级发生实质变化时，才增加路由或加载验证。

这里刻意不要求固定评分表、固定数量的子代理演练、每条规则都做盲测，也不要求先删掉某个百分比。盲测如果仍会自动加载待测指令，就只能算辅助观察，不能当作独立证据。用户已经明确授权修改时，也不会再为每一批删除反复索要确认；只有行为选择会显著改变结果、超出范围或难以撤销时才暂停。

它和相邻 Skill 的边界是：`$refine-text` 负责在含义已经确定后优化措辞，`$trim-agent-instructions` 先决定规则本身该留、该删还是该改；审计开始扩张成宽泛治理时叠加 `$keep-task-in-scope`，方向已定且需要多步落实时可配合 `$execute-work`。从零设计一套新指令不属于它的默认范围。

## 安装完整包

推荐把仓库作为插件市场源加入 Codex：

```bash
codex plugin marketplace add ANTiqiuSama/antiqiu-skills
codex plugin marketplace list
```

重启 ChatGPT / Codex 桌面端，在 Plugins Directory 里选择 `ANTiqiu Skills`，安装 `antiqiu-skills`。插件清单位于 [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json)，插件入口位于 [`plugins/antiqiu-skills/.codex-plugin/plugin.json`](plugins/antiqiu-skills/.codex-plugin/plugin.json)。

只想安装一个 Skill 时，可以让 `$skill-installer` 从本仓库对应目录安装。例如：

```text
使用 $skill-installer 安装 ANTiqiuSama/antiqiu-skills 仓库中
plugins/antiqiu-skills/skills/refine-text 目录下的 Skill。
```

Codex 能自动发现 Skill 变更；如果列表没有刷新，重新启动任务或 Codex。

## 从旧名称迁移

| 旧 Skill | 新 Skill |
| --- | --- |
| `brainstorming` | `plan-work` |
| `writing-plans` | `plan-work` |
| `executing-plans` | `execute-work` |
| `verification-before-completion` | `execute-work` |
| `receiving-code-review` | `diagnose-work` |
| `systematic-debugging` | `diagnose-work` |

`human-writing`、`keep-task-in-scope`、`refine-text` 和 `write-action-first` 名称不变。`hatch-pet` 不属于本总库，本地安装保持原样。旧目录可以保留为 `SKILL.md.disabled` 备份，但不要让新旧名称同时启用，否则又会恢复重复匹配。

## 验证与开发

静态和结构回归不需要模型调用：

```bash
python3 tests/audit_skills.py
```

运行 8 个 Skill 的独立 Codex 行为回归和综合路由用例：

```bash
python3 tests/run_behavior_tests.py --model gpt-5.6-terra --jobs 3
```

完整验证还包括插件清单校验、`human-writing` 检查脚本冒烟测试、临时安装后 Skill 发现测试和全新 Codex 会话路由测试。当前结果记录在 [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md)。

## 仓库结构

```text
antiqiu-skills/
├── .agents/plugins/marketplace.json
├── AGENTS.md
├── docs/
├── licenses/
├── plugins/antiqiu-skills/
│   ├── .codex-plugin/plugin.json
│   └── skills/
└── tests/
```

## 来源与许可

仓库自有内容采用 MIT License。各 Skill 内已有的 MIT 文件继续生效。第三方来源、修改关系和对应许可证见 [`NOTICE.md`](NOTICE.md) 与 [`licenses/`](licenses/)。
