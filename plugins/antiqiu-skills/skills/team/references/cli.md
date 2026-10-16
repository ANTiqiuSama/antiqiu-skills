# 隔离 CLI

Grok 对抗审查通过 `scripts/run_agent.py grok` 在隔离 CLI 运行，不是 Codex 子任务。运行前将允许外发的最小审查包交给调用器，并显式传入 `--context-class public|sanitized|synthetic`；该参数只是调用者声明，不会脱敏。不得发送仓库、私有业务资料、凭据或完整对话。Grok 仅审查，不能浏览仓库或写入文件。

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$python = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$runner = Join-Path $env:USERPROFILE '.codex/skills/team/scripts/run_agent.py'
$revision = 'sha256:<immutable-review-packet-hash>'
$taskText | & $python -B $runner grok --context-class sanitized --revision $revision --output "$pwd\work\grok-review.json"
```

请求模型固定 `grok-4.7`，推理强度固定 `xhigh`，审查模式使用 runner 默认 debate。CLI 的 `--reasoning-effort` 支持值已由本机 Grok help、model cache 和 headless 文档确认，且 `grok-4.7` 列有 `xhigh`。默认 `timeout=0` 表示不限总时长，`idle_timeout=0` 表示不因无流输出超时。有限总时限或 idle timeout 只允许来自任务包中明确预算，并须通过 `--budget` 说明；不自动套用 120 秒限制。

`--revision` 必须是本次提交包的不可变身份；runner 会把它和 runner 退出码写入原始 JSON 回执，真实进程退出码另记录在 timing 诊断中。回执记录 `requested_reasoning_effort`、`launch_reasoning_effort`、`actual_reported_reasoning_effort` 和 `effort_evidence`。服务未回显实际 effort 时，`effort_evidence=launch_argument` 只证明实际 CLI 参数；若服务回显，则必须与 XHigh 一致。返回后调用者必须读取实际 JSON 回执，按 [review-packet.md](review-packet.md) 检查模型、effort、状态、runner 退出码、隔离、工具清单、结果和 revision。先前 High 回执、对话摘要、布尔标志或 exit 0 单独都不能证明当前审查有效。

默认实施和监看使用 `gpt-6-luna`、`low`。显式用户要求 Gemini 时用隔离 Antigravity CLI，模型按 runner 支持配置；MiMo 只按用户明确覆盖的 Codex 执行路径使用。任何指定模型不可用、失败或被硬限流都返回 blocked，不自动换模型；额度低只作提示。

```powershell
& $python -B -m unittest discover -s scripts -p "test_*.py"
```
