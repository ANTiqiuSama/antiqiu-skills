# Modeling mermaid-diagram workflow

执行下列工作流；公共配置与检查规则由入口统一加载。

1. Run `python scripts/bootstrap.py --workspace <active-project-root> --profile modeling-competition --capability mermaid-diagram`.
2. Read `references/mermaid-diagram.md` completely and follow it as the authoritative prompt for visual design, chart/diagram construction, templates, export quality, review, and iteration.
3. Use the executable paths in `<active-project-root>/.vivid/runtime.json`.

规划、对账与绘图要求从所选工作流加载；检查规则只维护在 review-policy.md。


Use the runtime's `render_mermaid.py`; it selects the working system Chrome and supports SVG, PNG, and PDF without Puppeteer's incompatible bundled browser.


Never paraphrase or weaken the loaded drawing instructions, visual standards, recipes, or review threshold.
