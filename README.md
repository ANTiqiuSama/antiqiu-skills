# ANTiqiu Skills

一套经过收敛和回归测试的个人 Agent Skills。它覆盖规划、执行、诊断、范围控制、文本炼化、自然中文写作和行动优先输出。

这不是把所有见过的 Skill 收进一个目录。仓库只维护 ANTiqiuSama 当前使用并有权修改的个人 Skills。Codex 内置 Skills、插件缓存和字节内部平台 Skills 仍由各自来源维护，不复制、不改名，也不在这里制造第二份版本。

## 这次整理解决了什么

整理前有 11 个启用的个人 Skill。`hatch-pet` 是独立的 Codex 宠物制作工具链，按用户要求排除；其余 10 个通用 Skill 中有三组会在同一阶段重复触发：

- `brainstorming` 与 `writing-plans` 都会把问题变成计划；
- `executing-plans` 与 `verification-before-completion` 都会控制交付末段；
- `receiving-code-review` 与 `systematic-debugging` 都要求先核验证据再改代码。

现在它们分别合并为 `plan-work`、`execute-work` 和 `diagnose-work`。其余 Skill 保留独立边界，没有为了减少数量而做成一个无所不包的大 Skill。

在 2026-08-13 的本机快照中：

| 指标 | 整理前 | 整理后 | 变化 |
| --- | ---: | ---: | ---: |
| 纳入通用总库的个人 Skill 数 | 10 | 7 | -30.0% |
| 启动时的名称与描述字节数 | 3,784 | 2,368 | -37.4% |
| 三组重叠工作流的 `SKILL.md` 行数 | 186 | 105 | -43.5% |
| 诊断按需支持材料 | 5 文件 / 636 行 | 2 文件 / 63 行 | 行数 -90.1% |

这些指标证明启动和匹配阶段需要读取的个人元数据更少，也证明同一任务不再需要加载两份相邻流程；深度诊断时需要读取的按需材料也显著缩短。它们不等价于固定的端到端耗时承诺，模型、网络、工具和任务本身仍会影响实际速度。

详细逐项审计见 [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md)，测试证据见 [`docs/TEST_RESULTS.md`](docs/TEST_RESULTS.md)。

## 当前 7 个 Skills

| Skill | 负责什么 | 典型触发 |
| --- | --- | --- |
| [`plan-work`](plugins/antiqiu-skills/skills/plan-work/SKILL.md) | 澄清目标、比较真实方案、生成精简执行路径 | 目标不清、存在真实取舍、多系统或多依赖计划 |
| [`execute-work`](plugins/antiqiu-skills/skills/execute-work/SKILL.md) | 按已定方向持续实施，并用新证据验证完成 | “按计划继续”“执行下面步骤”“做到完成” |
| [`diagnose-work`](plugins/antiqiu-skills/skills/diagnose-work/SKILL.md) | 定位非显然故障，或判断评审意见是否成立 | Bug、回归、性能、偶现测试、模糊或冲突的 review comment |
| [`keep-task-in-scope`](plugins/antiqiu-skills/skills/keep-task-in-scope/SKILL.md) | 约束长期任务和可选流程，防止主交付物被挤走 | 持续优化、SOTA、冻结、哈希、审计、迁移、宽测和新基础设施 |
| [`refine-text`](plugins/antiqiu-skills/skills/refine-text/SKILL.md) | 保留事实、立场和不确定性的文本炼化 | 润色、压缩、扩写、重组、总结、综合已有材料 |
| [`human-writing`](plugins/antiqiu-skills/skills/human-writing/SKILL.md) | 写出有材料、有说话位置和自然中文韵律的作品 | 中文长帖、文章、叙事、故事、口播和明确的去 AI 味改稿 |
| [`write-action-first`](plugins/antiqiu-skills/skills/write-action-first/SKILL.md) | 把聊天回复整理成先结果、易扫描、可执行的形状 | 仅显式调用，或用户明确要求行动优先、ADHD-friendly、不要铺垫 |

## 怎么选择

先选当前阶段，只用一个主工作流：

1. 方向还没定，使用 `$plan-work`。
2. 方向已定，要持续完成，使用 `$execute-work`。
3. 原因不清或收到可疑评审，使用 `$diagnose-work`。

随后按产物选择最多一个领域 Skill。已有文本一般用 `$refine-text`；自然中文作品用 `$human-writing`。

`$keep-task-in-scope` 只在长期循环或额外流程可能挤占主任务时叠加。`$write-action-first` 只改变回复形状，不改变代码、结论或原始文稿，因此默认禁止隐式调用。

如果多个 Skill 同时命中，按下面的顺序处理：

```text
用户明确格式与安全边界
  → 领域事实与产物规则
  → 当前工作阶段
  → 长期范围约束
  → 回复呈现方式
```

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

运行 7 个 Skill 加一组综合路由的独立 Codex 行为回归：

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
