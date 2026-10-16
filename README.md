# ANTiqiu Skills

个人 Agent Skills 集合，覆盖科研、写作、设计、逆向分析、知乎和 Agent 协作。

当前插件共 **29 个 Skill**，版本 **1.6.0**：2026-10-16 从本机用户级目录同步的 17 个、仓库原有的 9 个，以及 1.6.0 新增的 3 个 Claude 风格设计 Skill。同步保留正文、脚本、参考材料、模板、图片和许可证，不收录系统 Skill、插件缓存、Python 缓存或本机账号配置。

## Claude 风格设计 Skills（1.6.0）

| Skill | 来源 | 用途 |
| --- | --- | --- |
| [frontend-design](plugins/antiqiu-skills/skills/frontend-design/SKILL.md) | Anthropic 官方 [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design)，Apache-2.0，原文收录 | 为新 UI 选择有辨识度的视觉方向，避开模板化默认样式 |
| [claude-design](plugins/antiqiu-skills/skills/claude-design/SKILL.md) | 参照公开流传的 Claude Design 工作方式重新撰写，未逐字收录其提示词 | HTML 原生的幻灯片、原型、文档、海报、邮件和多方案画布 |
| [frontend-app-builder](plugins/antiqiu-skills/skills/frontend-app-builder/SKILL.md) | 改写自 OpenAI `build-web-apps:frontend-app-builder`（MIT） | 前端应用与网站：先做 token 方案、以代码实现，Image Gen 概念图改为可选，验收只看一次 |

路由：视觉方向用 `frontend-design`；独立 HTML 交付物用 `claude-design`；仓库内的应用或网站用 `frontend-app-builder`；Apple 风格用 `apple-design-skill`；中英文排版检查用 `apply-design-typography-standards`；科研图表用 `vivid-figures-skill`。

同时安装了 OpenAI 的 Build Web Apps 插件时，请在 Codex 中停用其自带的 `frontend-app-builder`，避免两个同名 Skill 同时触发。

## 本次同步的 Skills

| Skill | 用途 |
| --- | --- |
| [academic-humanizer](plugins/antiqiu-skills/skills/academic-humanizer/SKILL.md) | 学术与专业文本润色，保留事实、数字、引用和作者声音 |
| [apple-design-skill](plugins/antiqiu-skills/skills/apple-design-skill/SKILL.md) | Apple 设计语言与 HIG 参考；1.6.0 起不再附带 Apple 专有字体文件 |
| [apply-design-typography-standards](plugins/antiqiu-skills/skills/apply-design-typography-standards/SKILL.md) | 中英文排版与设计规范检查 |
| [audit-research-release](plugins/antiqiu-skills/skills/audit-research-release/SKILL.md) | 只读审查研究材料、证据和发布条件 |
| [build-project-wiki](plugins/antiqiu-skills/skills/build-project-wiki/SKILL.md) | 基于源码证据建立、维护和查询项目 Wiki |
| [designing-studies](plugins/antiqiu-skills/skills/designing-studies/SKILL.md) | 设计可执行的前瞻实验、评估和仿真协议 |
| [discovering-literature](plugins/antiqiu-skills/skills/discovering-literature/SKILL.md) | 可复现的文献检索与筛选 |
| [game-the-llm-reviewer](plugins/antiqiu-skills/skills/game-the-llm-reviewer/SKILL.md) | 对已完成论文做保持含义的有限措辞调整 |
| [refine-text](plugins/antiqiu-skills/skills/refine-text/SKILL.md) | 学术和专业文本转交 academic-humanizer，其他文本按请求编辑 |
| [reverse-engineer-anything](plugins/antiqiu-skills/skills/reverse-engineer-anything/SKILL.md) | 使用 REA 分析原生、托管、JavaScript、固件和浏览器目标 |
| [rolling-goal-prompt](plugins/antiqiu-skills/skills/rolling-goal-prompt/SKILL.md) | 明确要求时维护可恢复的跨会话目标记录 |
| [run-research-program](plugins/antiqiu-skills/skills/run-research-program/SKILL.md) | 持续研究项目的状态、实验执行和证据管理 |
| [team](plugins/antiqiu-skills/skills/team/SKILL.md) | 显式调用的混动团队路由、隔离实施和监看 |
| [vivid-figures-skill](plugins/antiqiu-skills/skills/vivid-figures-skill/SKILL.md) | 科研图表、143 个源码配方、组合模板和绘图资源 |
| [write-research-paper](plugins/antiqiu-skills/skills/write-research-paper/SKILL.md) | 基于可追溯研究证据起草或实质修改论文 |
| [zhihu](plugins/antiqiu-skills/skills/zhihu/SKILL.md) | 知乎开放平台搜索、热榜、直答和本人内容读取 |
| [zhihu-public-reader](plugins/antiqiu-skills/skills/zhihu-public-reader/SKILL.md) | 读取指定公开知乎回答并检查正文完整性 |

`team` 等 Skill 的脚本需要相应本机 CLI 或服务；同步代码不包含登录态、令牌或服务配置。具体依赖和入口见各 Skill 正文。

## 保留的既有 Skills

为保留既有使用入口，本次没有删除以下仓库原有 Skill：

| Skill | 用途 |
| --- | --- |
| [plan-work](plugins/antiqiu-skills/skills/plan-work/SKILL.md) | 澄清目标和比较实施方案 |
| [execute-work](plugins/antiqiu-skills/skills/execute-work/SKILL.md) | 持续执行并验证交付 |
| [diagnose-work](plugins/antiqiu-skills/skills/diagnose-work/SKILL.md) | 故障诊断和评审意见核验 |
| [keep-task-in-scope](plugins/antiqiu-skills/skills/keep-task-in-scope/SKILL.md) | 控制长期任务与可选流程的范围 |
| [trim-agent-instructions](plugins/antiqiu-skills/skills/trim-agent-instructions/SKILL.md) | 审查并精简已有 Agent 指令链 |
| [human-writing](plugins/antiqiu-skills/skills/human-writing/SKILL.md) | 自然中文文章与叙事 |
| [write-action-first](plugins/antiqiu-skills/skills/write-action-first/SKILL.md) | 显式调用的行动优先回复模式 |
| [herdr-orchestrator](plugins/antiqiu-skills/skills/herdr-orchestrator/SKILL.md) | Herdr 跨厂商 Agent 编排 |
| [native-hybrid-agents](plugins/antiqiu-skills/skills/native-hybrid-agents/SKILL.md) | 原有 Antigravity/Grok CLI 协作入口 |

这些保留项不表示本机当前仍安装或使用它们。优先遵循本轮用户指令和对应 Skill 的适用范围；`team` 仅在显式请求混动时使用。

## 安装

仓库继续使用现有插件市场结构：[市场清单](.agents/plugins/marketplace.json)、[插件入口](plugins/antiqiu-skills/.codex-plugin/plugin.json)。通过支持该市场的 Codex 客户端添加 `ANTiqiuSama/antiqiu-skills`，然后安装 `antiqiu-skills`。

只安装一个 Skill 时，使用 Skill 安装器指定对应目录，例如：

```text
使用 $skill-installer 安装 ANTiqiuSama/antiqiu-skills 仓库中的
plugins/antiqiu-skills/skills/refine-text
```

## 验证与历史记录

本地静态检查不调用外部模型：

```bash
python tests/audit_skills.py
```

检查 Skill 集合、名称和描述、许可证、文档相对链接、Python 语法、插件清单，以及是否误带 Apple 专有字体。既有工作流的收敛预算单独计算，不把新增的领域 Skill 算成历史预算回归。`agents/openai.yaml` 对本次同步项按原安装状态保留，不为上传额外生成。

`tests/run_behavior_tests.py` 和 `tests/behavior_cases.json` 保留既有工作流的模型行为用例；它们不构成新增 17 个 Skill 的完整模型验收。本次同步不自动发起付费模型调用。

历史材料保留在 [docs/](docs/)，包括 [原审查记录](docs/SKILL_AUDIT.md)、[原测试记录](docs/TEST_RESULTS.md) 和 [Herdr 教程](docs/HERDR_TUTORIAL_ZH.md)。其中旧版计数、模型和行为结论仅对应记录当时的版本。

## 来源与许可

仓库自有内容采用 [MIT](LICENSE)，各 Skill 与附带资源的许可证单独生效，见 [NOTICE.md](NOTICE.md)。第三方版权声明、许可证和来源说明保留原文。

**`vivid-figures-skill` 不适用本仓库的 MIT 许可。** 仓库所有者于 2026-10-16 确认已取得作者对此次公开上传的书面授权。其 [原许可证](plugins/antiqiu-skills/skills/vivid-figures-skill/LICENSE) 仍保留原有限制；此次上传不向其他使用者授予修改或再次分发的通用权利。
