# Provider setup and verification

Read this file only when the task needs provider selection, a custom endpoint,
or provider-specific recovery.

## Select by role, then by provider

Choose the capability needed before choosing the CLI. Prefer different model
families for implementation and adversarial review when independence matters.
Two CLIs that route to the same underlying model are not independent evidence.

Do not silently substitute a provider the user excluded. Record who pays for a
route when quota or cost affects the choice.

## Claude Code with a custom compatible endpoint

Keep credentials outside the Skill, repository, prompt, and logs. Store only the
name of the credential variable in a local provider note. On a single-user macOS
machine, a non-interactive Zsh startup file can export the token; protect that
file with mode `600`. Prefer an OS secret manager on a shared machine.

Do not export both `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN` unless the
provider explicitly requires it. The API key can take precedence and route a
request somewhere unexpected.

For a custom backend, create the Herdr tab with its complete environment. The
`agent start` command has no `--env`, and the caller's temporary environment is
not a reliable substitute.

```bash
MODEL='<provider>/<model-id>'
PANE=$(herdr tab create \
  --workspace "$HERDR_WORKSPACE_ID" \
  --label claude-review \
  --cwd "$PROJECT" \
  --no-focus \
  --env "ANTHROPIC_BASE_URL=<endpoint>" \
  --env "ANTHROPIC_AUTH_TOKEN=$RELAY_TOKEN" \
  --env "ANTHROPIC_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_OPUS_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_SONNET_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_HAIKU_MODEL=$MODEL" \
  --env "ANTHROPIC_DEFAULT_FABLE_MODEL=$MODEL" \
  --env "CLAUDE_CODE_SUBAGENT_MODEL=$MODEL" \
  --env "CLAUDE_CODE_MAX_CONTEXT_TOKENS=<verified-window>" \
  --env "CLAUDE_CODE_EFFORT_LEVEL=<supported-effort>" \
  --env "CLAUDE_CODE_ATTRIBUTION_HEADER=0" \
  | jq -r '.result.root_pane.pane_id')

herdr agent start paper-claude-review --kind claude --pane "$PANE"
```

The example maps every Claude Code model alias to one backend model. Remove a
mapping only when the installed Claude Code version does not support it. Never
guess a context window or effort ceiling.

After startup, read the agent status line and verify that the displayed model
matches the intended provider/model identifier. `agent start` returning `idle`
only proves that a process started. A successful HTTP request only proves
transport; neither proves that the live session changed models.

When custom endpoint settings change, rebuild the tab. Restarting the agent in
the old root shell does not change the tab's inherited environment.

## Codex

Install the Herdr integration, then read the current CLI and model cache before
selecting model or effort:

```bash
herdr integration install codex
codex --help
```

Pass model arguments after `--`:

```bash
herdr agent start paper-codex-review --kind codex --pane "$PANE" -- \
  --model <model> -c model_reasoning_effort=high
```

If a Codex session launched by Herdr cannot see `HERDR_*`, use an opt-in profile
instead of weakening the global policy:

```toml
# ~/.codex/herdr.config.toml
[shell_environment_policy]
inherit = "all"
```

Launch that worker with `--profile herdr`. This exposes the parent environment
to that Codex process, so use the profile only in a trusted Herdr tab and never
print secrets while diagnosing it.

## Antigravity and Gemini

Herdr's Antigravity integration installs lifecycle hooks; it does not install
the standalone `agy` executable. Verify both layers:

```bash
command -v agy
agy --version
agy models
herdr integration install antigravity-cli
herdr integration status
```

Start Antigravity with kind `agy`:

```bash
herdr agent start paper-gemini-writer --kind agy --pane "$PANE"
```

Use native kind `gemini` only when the user asked for the Gemini CLI rather than
Antigravity. A desktop application, a Herdr integration, and a CLI executable
are separate components; verify the one the workflow actually uses.

For figure generation, require a target path and a caption/source note. If the
figure encodes data, require the data and rendering script or notebook. Never
let a generative image silently stand in for experimental evidence.
