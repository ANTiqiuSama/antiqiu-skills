# Modeling paper-technical-diagram workflow

执行下列工作流；公共配置与检查规则由入口统一加载。

1. Run `python scripts/bootstrap.py --workspace <active-project-root> --profile modeling-competition --capability paper-figure-drawio`.
2. Read `references/paper-technical-diagram.md` completely and follow it as the authoritative prompt for technical, engineering, physical, geometric, architecture, process, and network diagrams, including its Draw.io and TikZ sub-engines.
3. Use the executable paths in `<active-project-root>/.vivid/runtime.json`.

规划、对账与绘图要求从所选工作流加载；检查规则只维护在 review-policy.md。


Use the runtime's `export_drawio.py` to wait for detached Windows exports. In the general-paper variant, use the compatibility checker's `general` or `architecture` mode when the original roadmap/decision-flow checker would impose an unrelated shape requirement.


Never paraphrase or weaken the loaded drawing instructions, visual standards, recipes, or review threshold.
