# Third-party notices

ANTiqiu Skills includes adapted or redistributed third-party material. Each package retains its own license and any applicable authorization conditions.

| Package | Relationship | Upstream | License |
| --- | --- | --- | --- |
| `plan-work`, `execute-work`, `diagnose-work` | Rewritten and consolidated workflow concepts | [obra/superpowers](https://github.com/obra/superpowers) | MIT, copyright 2025 Jesse Vincent; see [`licenses/superpowers-MIT.txt`](licenses/superpowers-MIT.txt) |
| `keep-task-in-scope` | Independent extension of anti-overdefense concepts | [wanshuiyin/HERO-Anti-OverDefense](https://github.com/wanshuiyin/HERO-Anti-OverDefense) | MIT, copyright 2026 Ruofeng Yang; see [`licenses/hero-MIT.txt`](licenses/hero-MIT.txt) |
| `write-action-first` | Adapted response-shaping concepts | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | MIT, copyright 2026 Ayoub Ghriss; license retained inside the Skill |
| `human-writing` | Bundled from the separately maintained ANTiqiuSama project | [ANTiqiuSama/human-writing](https://github.com/ANTiqiuSama/human-writing) | MIT; license retained inside the Skill |
| `academic-humanizer` | Snapshot of the current local installation | AIScientists-Dev; upstream acknowledgments retained in the Skill's README | MIT; license retained inside the Skill |
| `frontend-design` | Verbatim copy of Anthropic's official skill (upstream commit `dbd4588`) | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Apache-2.0; `LICENSE.txt` retained inside the Skill. Only `agents/openai.yaml` was added |
| `frontend-app-builder` | Substantially modified version of OpenAI's Build Web Apps skill (upstream commit `0722921`) | [openai/plugins](https://github.com/openai/plugins/tree/main/plugins/build-web-apps/skills/frontend-app-builder) | MIT as declared by the upstream plugin manifest; see the Skill's `LICENSE` |
| `claude-design` | Original text by ANTiqiuSama. Its workflow is informed by public descriptions and community reconstructions of Anthropic's Claude Design product ([jiji262/claude-design-skill](https://github.com/jiji262/claude-design-skill), [Trystan-SA/claude-design-system-prompt](https://github.com/Trystan-SA/claude-design-system-prompt), [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)); no prompt text is reproduced | — | MIT (this repository) |
| `vivid-figures-skill` | Snapshot of the current local installation; repository owner confirmed prior written permission for this public upload on 2026-10-16 | yjz211; upstream notices retained inside the Skill | Personal Non-Commercial License, retained unmodified; this upload does not grant downstream redistribution or modification rights |

The upstream projects remain separate projects. Their names do not imply endorsement of this bundle.

The 2026-10-16 sync includes `vivid-figures-skill` based on the repository owner's confirmation of prior written permission for this public upload. Its original restrictions and third-party notices remain in effect; no general permission to redistribute or modify it is implied. System skills and plugin caches are outside this user-level snapshot. Version 1.6.0 removed `apple-design-skill` (replaced by the Claude-aligned design skills) together with its bundled PingFang SC font files, which are Apple-licensed and not redistributable under a third-party MIT declaration, removed `native-hybrid-agents` (superseded by `team`), and removed `herdr-orchestrator` so that multi-agent work uses the single `team` workflow. Existing per-Skill licenses take precedence over the repository's default MIT license.
