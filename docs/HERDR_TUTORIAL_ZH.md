# Herdr 多 Agent 编排教程

这份教程面向需要长期使用 Codex、Claude Code 和 Antigravity/Gemini 的人。
它既讲第一次启动，也讲论文、代码和长任务怎么分工。

示例使用 Herdr 0.8.2 的本机命令面。不同版本可能变化。运行命令前，先以
`herdr --skill` 和各命令组的帮助为准。

## 1. 先理解 Herdr 的边界

Herdr 管理终端布局和 Agent 生命周期。它能创建 workspace、tab 和 pane，
也能识别 Agent 是空闲、工作、卡住还是完成。

Herdr 不负责以下事情：

- 它不是模型网关。
- 它不会自动选择模型。
- 它不会替你配置 Claude Relay。
- 它不会证明任务已经交付。
- Antigravity 集成不会安装 `agy` 命令。

因此要分开看三层状态：

| 层 | 要回答的问题 | 可用证据 |
| --- | --- | --- |
| 进程 | Agent 是否还在运行 | `herdr agent list/get` |
| 路由 | Agent 实际用了哪个模型 | Agent 状态栏、端点日志 |
| 交付 | 任务是否达到目标 | 产物、Git diff、构建和验收命令 |

`idle` 或 `done` 只说明 Agent 已经停下来。它不等于论文已经改好，也不等于
测试已经通过。

## 2. workspace、tab、pane 和 Agent

Herdr 的层级是：

```text
workspace
└── tab
    └── pane
        └── Agent 或普通 Shell 进程
```

- workspace 表示一个项目或一项独立任务。
- tab 表示一个长期角色，例如 `claude-review`。
- pane 是真实终端。
- Agent 是 pane 中被 Herdr 识别的 CLI 进程。

一个 pane 退出 Codex 后，会回到 Shell。此时 Shell 不是 `chair`。`chair` 只是
Agent 名或 tab 标签。用下面的命令判断 Agent 是否仍在：

```bash
herdr agent list
```

如果只看到类似 `host:dir user$` 的提示符，说明 pane 前台是 Shell。不要因为
tab 仍叫 `chair`，就认为 Codex 还在运行。

## 3. 不要把项目根目录写成系统根目录

教程中的“项目根目录”是仓库或论文工程目录，例如：

```text
/Users/me/Documents/paper-project
```

它不是系统根目录 `/`。把所有 Agent 的 `cwd` 设为 `/` 会扩大读取范围，
也会让相对路径、Git 仓库和验收命令失去明确边界。

需要访问多个目录时，给每个任务明确目录。Codex 还可以按需使用 `--add-dir`。
不要用 `/` 代替权限设计。

## 4. 安装后先做四项检查

macOS 或 Linux 可以使用 Herdr 官方安装器：

```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

Windows PowerShell 使用官方 Windows 安装器：

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://herdr.dev/install.ps1 | iex"
```

安装脚本会执行远程代码。使用前先确认域名和脚本内容符合你的环境策略。

```bash
herdr --version
herdr --skill
herdr integration status
command -v codex claude agy
```

按需安装集成：

```bash
herdr integration install codex
herdr integration install claude
herdr integration install antigravity-cli
```

集成显示 `current` 只证明钩子存在。它不证明对应 Agent 已启动。

再检查 Antigravity：

```bash
agy --version
agy models
```

如果 `agy` 不存在，要单独安装 Antigravity CLI。只安装桌面应用或 Herdr 集成
不会得到这个命令。

## 5. 第一次启动：先让一个 Codex 成为协调者

进入项目目录，再启动 Herdr：

```bash
cd /path/to/project
herdr
```

在 Herdr 的一个 Shell tab 中启动 Codex：

```bash
codex --profile herdr
```

Codex 启动后，先让它检查：

```bash
test "${HERDR_ENV:-}" = 1
printf '%s\n' "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
```

如果 `HERDR_ENV` 为空，不要让这个 Codex 控制当前 Herdr 会话。退出它，在
Herdr 管理的 Shell 中重新启动。

如果 Codex 看不到 `HERDR_*`，建立一个只给 Herdr 使用的配置：

```toml
# ~/.codex/herdr.config.toml
[shell_environment_policy]
inherit = "all"
```

然后用 `codex --profile herdr` 启动。这个配置会把父进程环境传给 Codex。
只在可信的 Herdr tab 中使用，不要在排障输出中打印令牌。

## 6. 选择编排拓扑

先按“任务”拆，再按“角色”开 Agent。

### 6.1 独立写任务

一个独立写任务使用一个 Git worktree 和一个 workspace。这样两个任务可以
并行修改，不会踩同一批文件。

```bash
herdr worktree create \
  --cwd "$PROJECT" \
  --branch agent/paper-polish \
  --base main \
  --label paper-polish \
  --no-focus
```

从 JSON 返回值读取 workspace、checkout 和 root pane ID。不要猜 ID。

### 6.2 只读任务

文献查证、代码阅读和方案评审不写项目文件时，可以共用项目 workspace。
没有必要为每个只读问题创建 worktree。

### 6.3 同一任务内的多个角色

一个长期 Agent 使用一个 tab。不要把多个 Agent 挤进窄分屏。需要同时写文件时，
让它们串行，或给出互不重叠的可写路径。

## 7. 创建 Claude 和 Antigravity tab

下面的命令由 Herdr 内的协调者执行。

先创建 Claude tab：

```bash
PROJECT=$(pwd -P)
CLAUDE_TAB=$(herdr tab create \
  --workspace "$HERDR_WORKSPACE_ID" \
  --label claude-review \
  --cwd "$PROJECT" \
  --no-focus)

CLAUDE_PANE=$(printf '%s\n' "$CLAUDE_TAB" | jq -r '.result.root_pane.pane_id')

herdr agent start paper-claude-review \
  --kind claude \
  --pane "$CLAUDE_PANE"
```

再创建 Antigravity tab：

```bash
AGY_TAB=$(herdr tab create \
  --workspace "$HERDR_WORKSPACE_ID" \
  --label gemini-writer \
  --cwd "$PROJECT" \
  --no-focus)

AGY_PANE=$(printf '%s\n' "$AGY_TAB" | jq -r '.result.root_pane.pane_id')

herdr agent start paper-gemini-writer \
  --kind agy \
  --pane "$AGY_PANE"
```

`agent start` 不会创建 pane。它只能在已有的空闲 Shell pane 中启动 Agent。

先做最小连通测试：

```bash
herdr agent prompt paper-claude-review \
  '只回复 CLAUDE_READY，不读取或修改文件。' \
  --wait --timeout 55000

herdr agent prompt paper-gemini-writer \
  '只回复 GEMINI_READY，不读取或修改文件。' \
  --wait --timeout 55000
```

测试成功后，再发送真实任务。

## 8. Claude 使用自定义 Relay

自定义 Relay 的环境必须在 `tab create --env` 时注入。不要把变量写在
`herdr agent start` 前面。Herdr daemon 不保证把调用方的临时环境传给目标 pane。

凭据只保存在本机安全位置。Skill、Git 仓库、prompt 和日志只写变量名，
不写令牌值。

```bash
MODEL='<provider>/<model-id>'

CLAUDE_TAB=$(herdr tab create \
  --workspace "$HERDR_WORKSPACE_ID" \
  --label claude-review \
  --cwd "$PROJECT" \
  --no-focus \
  --env "ANTHROPIC_BASE_URL=<relay-url>" \
  --env "ANTHROPIC_AUTH_TOKEN=$RELAY_TOKEN" \
  --env "ANTHROPIC_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_OPUS_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_SONNET_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_HAIKU_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_FABLE_MODEL=$MODEL" \
  --env "CLAUDE_CODE_SUBAGENT_MODEL=$MODEL" \
  --env "CLAUDE_CODE_MAX_CONTEXT_TOKENS=<verified-window>" \
  --env "CLAUDE_CODE_EFFORT_LEVEL=<supported-effort>" \
  --env "CLAUDE_CODE_ATTRIBUTION_HEADER=0")
```

启动后读取状态栏：

```bash
herdr agent read paper-claude-review \
  --source recent-unwrapped --lines 20
```

只有显示的模型与预期路由一致，才算切换完成。一次 HTTP 请求成功只证明
Relay 可达。`agent start` 返回 `idle` 只证明进程启动。

改了 Relay、模型、上下文或 effort 后，要重建 tab。旧 tab 的根 Shell 已经
继承了旧环境，重启 Agent 不会补上新变量。

## 9. 给 Agent 的任务说明

长背景写入一份 brief。所有参加评审的 Agent 读取同一份 brief。

每条任务说明至少写清七项：

```markdown
**结果** 要得到什么可观察结果
**先读** brief、论文、代码或数据路径
**可读** 允许读取的路径和系统
**可写** 仅允许写入的路径
**约束** 禁止事项、事实边界和审批边界
**验收** 可执行命令或可检查条件
**返回** 完整结果写到哪个文件，只回复路径与 done/blocked
```

示例：

```markdown
**结果** 找出论文中心论点最缺的三项证据。
**先读** `artifacts/herdr-paper/polish/brief.md` 和 `paper/main.tex`。
**可读** 论文、引用文献、现有实验日志和代码。
**可写** 仅 `artifacts/herdr-paper/polish/round-01-claude.md`。
**约束**
- 区分事实、推导和建议。
- 不编造引用、结果或统计显著性。
- 不修改论文，不继续委托。
**验收** 每项问题都给出对应 claim、现有证据和最小补救动作。
**返回** 写入指定文件，只回复路径与 done/blocked。
```

## 10. 正确使用并行

并行单位是互不等待的任务，不是 Agent 数量。

错误做法：

```text
安排 Claude → 等完 → 安排 Codex → 等完 → 安排 Gemini
```

正确做法：

```text
安排 Claude ─┐
安排 Codex ──┼→ 统一等待 → 收集产物 → 处理分歧
安排 Gemini ─┘
```

先把所有独立任务发出去，再等待。写同一篇论文的任务不独立。评审可以并行，
正文修改必须交给一个写入者。

## 11. 论文工作流：Codex 与 Claude 辩论，Gemini 写作

如果当前 Codex 已经是 chair，把下面的 prompt 直接发给它。不要再创建第二个
chair，也不要从 chair 自己所在的 pane 对自己调用 `herdr agent prompt`。

```text
使用 $herdr-orchestrator。你是当前 Herdr workspace 的协调者，不要创建第二个
协调者，也不要修改论文。

项目目录：<project-root>
论文入口：<paper-file>
目标 venue：<venue>
构建命令：<build-command>
产物目录：<artifact-root>
允许使用的代码、数据和算力：<limits>

先检查 HERDR_ENV、当前 workspace、现有 Agent 和集成状态。复用已存在且空闲的
Agent。建立以下角色：
- 一个独立 Codex reviewer，检查方法、复现和 claim-evidence 关系；
- 一个 Claude reviewer，做对抗评审、理论与定位检查；
- 一个 kind=agy 的 Gemini writer，只落实已接受的正文和图片修改。

第一阶段只做最小连通测试。报告每个 Agent 的名称、kind、pane ID、实际模型证据
和连通状态。不要读取或修改论文。

连通后再执行论文流程：两位 reviewer 先独立评审，再只围绕分歧辩论一轮；把
接受、拒绝、待用户决定和需要证据的事项写入 decisions.md；Gemini writer 是
该轮唯一的论文写入者。任何 Agent 都不得编造引用、实验结果或统计显著性。

任务完成以产物、论文构建、实际 diff 和独立复核为准。idle、done 或 --wait
超时都不能单独证明完成。遇到 blocked 时把原问题和 tab 位置交给我，不要替我
回答审批。
```

推荐使用四个 Agent：

| Agent | 职责 |
| --- | --- |
| Codex chair | 编排、证据门、验收和汇报 |
| Codex reviewer | 方法、复现、claim-evidence 审查 |
| Claude reviewer | 对抗评审、理论、定位和缺失对照 |
| Gemini writer | 落实已接受修改，生成正文和图片产物 |

这样 chair 不参加正文修改，也不审查自己的观点。如果只开三个 Agent，Codex
chair 可以兼任一方 reviewer，但要标明这份评审不独立。

### 11.1 第一轮：独立评审

Codex 与 Claude 读取同一版论文和同一份 brief。两者分别落盘，第一轮不能
互看对方答案。

```text
round-01-codex.md
round-01-claude.md
```

### 11.2 第二轮：只辩论分歧

chair 从两份评审中提取：

- 互相冲突的结论；
- 缺失证据；
- 不兼容的修改建议。

第二轮只发送这份分歧清单。每方回答三个问题：

1. 是否改变原判断？
2. 什么证据能改变判断？
3. 最小的正文或实验修改是什么？

不要让第二轮重新评审整篇论文。

### 11.3 决策记录

每个问题写成以下状态之一：

- 接受；
- 拒绝；
- 等用户决定；
- 需要证据。

分歧不能被模型平均掉。涉及论文方向、昂贵实验或不确定引用时，由用户决定。

### 11.4 Gemini 修改正文和图片

Gemini 只收到已接受的决策。它是当前轮唯一的论文写入者。

```markdown
**结果** 生成落实已接受决策的新论文版本。
**先读** `brief.md`、`decisions.md` 和当前论文。
**可读** 论文工程和已接受的证据。
**可写** 仅论文文件、指定图片路径和构建所需文件。
**约束**
- 不编造引用、数值、实验和显著性。
- 缺证据的 claim 降低强度或删除。
- 数据图必须保留数据源和绘图脚本。
- 生成式图片必须标记为 schematic。
- 不覆盖评审记录，不继续委托。
**验收** 论文构建通过，变更日志覆盖全部已接受决策。
**返回** 回复论文、图片和变更日志路径。
```

### 11.5 补实验的门槛

每个实验任务必须包含：

- 假设；
- 现有 baseline；
- 唯一变化因素；
- 指标；
- 数据与算力限制；
- 停止条件；
- 结果文件路径。

实验可以分为“中心论点必需”“能裁决分歧”“可选补充”和“当前不可执行”。
没有数据、算力或授权时，只能给实验设计，不能把它写成已有证据。

### 11.6 图片的证据门

每张图片至少保留：用途、支撑的 claim、数据源或 `schematic` 标签、生成脚本
或 prompt、单位与样本量、最终文件和 caption 来源。

图片变漂亮不等于证据变强。缺数据时先保留 figure spec，等实验完成后再画。

## 12. 为什么 Claude 和 Antigravity 看不到变化

先按下面的顺序排查：

| 现象 | 常见原因 | 检查 |
| --- | --- | --- |
| Agent 是 `idle` | 只启动了 Agent，还没有派任务 | 查看 `agent read` 和任务记录 |
| `agent prompt --wait` 超时 | 监听超时，任务可能仍在运行 | `agent get`，不要重发 prompt |
| Agent 已完成，项目没变化 | 任务要求只写临时产物 | 检查返回的产物路径 |
| Claude 回答正常但模型不对 | Relay 环境没有注入 tab | 读取状态栏，重建 tab |
| Antigravity tab 没反应 | `agy` 不存在或会话未启动 | `command -v agy`、`agy models` |
| 状态为 `unknown` | Herdr 无法识别覆盖层后的界面 | `agent explain --format text` |
| Agent 回到空闲但没有产物 | 请求截断、目标错误或提前退出 | 读取末尾输出，从已有进度续跑 |

## 13. 等待、超时和审批

`agent prompt --wait` 等的是生命周期状态，不是某一条消息的可靠回执。

```bash
herdr agent get <name>
herdr agent read <name> --source recent-unwrapped --lines 40
herdr agent explain <name> --format text
```

超时后不要重发原任务。先看 Agent 是否还在工作，再看产物是否变化。

`blocked` 表示 Agent 正在等待人类。不要用 `send-keys` 替用户回答审批。
把问题和 tab 位置告诉用户，由用户进入该 tab 决定。

## 14. 验收和停止条件

任务只有同时满足以下条件才通过：

1. 产物存在；
2. 产物非空；
3. 产物时间晚于派活时间；
4. 验收命令通过；
5. 已要求独立评审时，评审没有未解决阻塞项。

出现以下任一情况就停止并汇报：

- 同一非瞬时失败出现两次；
- 两轮纠正没有实质进展；
- 十分钟没有产物，也没有状态变化；
- 无人值守时 Agent 等待审批。

网络、限流和后端抖动可以退避重试。鉴权、模型不存在、参数错误和权限错误
必须先改配置。不要原样重复。

## 15. 状态汇报模板

汇报任务，不要只罗列进程：

| 事项 | 状态 | 位置 | 证据 |
| --- | --- | --- | --- |
| 方法评审 | 进行中 | paper / codex-review | review 文件仍在更新 |
| 对抗评审 | 已完成 | paper / claude-review | 产物非空，时间有效 |
| 正文改写 | 待开始 | paper / gemini-writer | 等决策清单 |

需要用户决定的事项另列：

| # | 分歧 | 用户要决定什么 |
| --- | --- | --- |
| 1 | 两位 reviewer 对主实验充分性判断不同 | 是否追加消融实验 |

## 16. Mac 与远程开发机

服务端代码、数据处理和训练更适合远程开发机。本机只保留显示和输入：

```bash
herdr --remote <ssh-host>
```

先单独验证 `ssh <ssh-host>`。iOS、macOS、模拟器、签名和本机设备任务应留在
Mac。Android 编译可以远程，真机操作通常仍在本机。

远程连接断开不等于任务停止。重新连接后，要重新读取 Agent 和产物状态，
不能把旧侧边栏当作当前证据。

## 17. 清理

只关闭本次创建的 Agent、tab 和 workspace。不要运行 `herdr server stop` 来清理
单个任务，因为它会终止该 session 中所有 pane 进程。

清理前先确认：

- 产物已复制到持久目录；
- Git 改动已提交或明确保留；
- 没有后台实验或构建仍在运行；
- 用户不再需要查看 Agent 对话。

## 18. 安装本仓库 Skill

把本仓库添加为 Codex 插件市场：

```bash
codex plugin marketplace add ANTiqiuSama/antiqiu-skills
codex plugin marketplace list
```

安装 `antiqiu-skills` 后，使用：

```text
使用 $herdr-orchestrator，在当前 Herdr workspace 中建立 Codex、Claude 和
Antigravity 的论文工作流。先检查环境与连通性，不修改论文。
```

随后再发送论文路径、目标 venue、允许写入的目录、构建命令、算力限制和
实验审批边界。
