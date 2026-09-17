---
name: native-hybrid-agents
description: 用本机 Antigravity 和 Grok CLI 委派独立文本任务、方案辩论与实现建议，主 agent 整合验收；不依赖代理服务。
---

# 本机双模型协作

主 agent 负责拆分、判断、落地与验收，通过随包脚本启动独立 CLI 工作进程。它们不属于宿主 App 的原生子 agent。本机启动仍会把提示词发送给模型服务，不是离线推理。

## 分工与边界

- Antigravity：简单文本、整理改写、总结、格式转换与速度优先的简单任务。固定 `gemini-3.8-flash-high`、high 推理，不自动降级。
- Grok：优先 debate、独立质疑、实现方案、代码生成、调试与修复建议。使用 `grok-4.6`、high 推理；实现模式返回文本或代码，由主 agent 应用和验证。
- 用户指定执行者、只读或数据范围时遵守原要求。零碎任务直接完成，独立任务可并行，同一任务不重复启动。失败如实报告，不静默换模型。

只传完成任务所需且允许外发的材料。非公开代码、技术实现、业务信息、凭据、内部链接和原始办公资料不得交给外部模型；改名不等于消除敏感信息。不能安全抽象的任务留在允许的数据环境中处理，不传完整对话、原始日志或仓库。

## 准备与调用

需要 macOS 或 Linux、Python 3.11+，以及已分别安装并登录的官方 `agy` 与 `grok` CLI。脚本从 `PATH` 查找可执行文件，找不到时检查 `~/.local/bin/`。只复用当前用户已有的默认登录缓存；不随包分发凭据、不自动登录或安装 CLI。

Antigravity 默认登录位置为 `~/.gemini/antigravity-cli/antigravity-oauth-token`，Grok 为 `~/.grok/auth.json`。隔离参数已在 Antigravity 1.2.5 与 Grok Build 1.0.34 使用过；其他版本需按下述方式检查，不承诺所有版本兼容。遇到不兼容的隔离状态，停止调用，不删除限制来强行继续。

从当前 Skill 的实际安装目录解析 `scripts/run_agent.py`，使用绝对路径，不依赖个人全局启动器。下面命令在该 Skill 目录执行，任务文件必须先经过外发检查：

```bash
python3 -B scripts/run_agent.py antigravity --context-class sanitized < /path/to/text-task.txt
python3 -B scripts/run_agent.py grok --context-class sanitized < /path/to/debate.txt
python3 -B scripts/run_agent.py grok --task-mode implement --context-class sanitized < /path/to/implementation.txt
```

`--context-class` 必填：`public` 表示公开材料，`sanitized` 表示经过语义脱敏，`synthetic` 表示虚构测试。由调用 agent 审核后声明，它不是自动脱敏证明。任务写明目标、事实、假设、输出形式和验收条件；不授予 worker 文件写入、工具执行或嵌套委派权限。

Antigravity 默认总时限 300 秒。Grok 默认 `--timeout 0 --idle-timeout 0`，推理总时长与无进展时长均不设截止时间，保留进度提示及手动取消。只有用户指定时限或运行有明确时限的诊断时才设正数。使用执行工具分段等待，每次不超过 30 秒；返回运行中的 session ID 不等于失败，不因此重复启动或截断任务。

成功回执必须有 `status=success` 和非空结果。核对实际模型、`model_usage`、`isolation_verified` 与工具使用情况，再整合结果；代码仍需主 agent 检查、应用和验证。登录失败、限流、超时、工具调用、模型不符和未完成输出都不是成功。Grok 单次输出上限见 [scripts/grok.toml](scripts/grok.toml)，较大实现应拆成独立可验收的任务。

## 自动 debate

遇到会影响决策的方案取舍、关键证据冲突、连续失败后准备换路线，或用户明确要求辩论时，主 agent 在已有授权和数据边界内调用 Grok。简单编辑或已有直接证据的问题不额外辩论。

1. 主 agent 提供自己的初判、候选方案的合理理由、可外发事实、假设和待质疑点。
2. Grok 提出关键反例、成立条件及能区分方案的最小检查；不要求它必须反对。
3. 主 agent 核查异议。通常一轮；仍有关键分歧且有新增材料时最多再复辩一轮。按证据裁决，保留未解决的问题，不按票数判断。

worker 可返回 `DEBATE_REQUEST`，由主 agent 判断相关性、准备脱敏材料并发起；worker 不自行调用其他进程。实现任务使用 `--task-mode implement`，不强制套用辩论格式，也不声称代码已写入或测试已通过。

## 隔离与检查

两个入口均创建临时空工作目录与专用配置，结束后清理；清理本地文件不代表服务端零留存，也不代表调用免费。

- Antigravity：禁止继承个人定制，关闭默认组件；回读文件、命令、网络、MCP 权限与专用 `PreToolUse` 拦截，再核对初始化模型、agent 和目录后发送文本。CLI 可能仍列出内置工具，不能把其声明列表当作实际权限；出现工具或子 agent 步骤即拒绝结果。
- Grok：使用随包的专用配置，禁用工具、网页、子 agent、记忆及项目上下文；保留已有本机部署策略并在临时配置收紧 MCP。发送任务前运行 `inspect` 验证隔离。只有完整 `end_turn`、匹配的模型用量和无工具调用才接受结果。

安装后先运行不联网的检查：

```bash
python3 -B -m unittest discover -s scripts -p 'test_*.py'
```

需要验证实际登录与版本兼容性时，对两个入口分别传入简短虚构文本，使用 `--context-class synthetic --timeout 55`，并检查 JSON 回执；每项诊断少于 60 秒。这一诊断时限不改变日常 Grok 的无限时限。无本机执行工具的云端对话无法直接使用这些入口。
