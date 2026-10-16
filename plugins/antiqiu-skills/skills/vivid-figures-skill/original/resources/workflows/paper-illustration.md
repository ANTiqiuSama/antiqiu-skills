# Modeling paper-illustration workflow

执行下列工作流；公共配置与检查规则由入口统一加载。

1. Run `python scripts/bootstrap.py --workspace <active-project-root> --profile modeling-competition --capability paper-illustration`.
2. Read `references/paper-illustration.md` completely and follow it as the authoritative prompt for visual design, chart/diagram construction, templates, export quality, review, and iteration.
3. Use the executable paths in `<active-project-root>/.vivid/runtime.json`.

规划、对账与绘图要求从所选工作流加载；检查规则只维护在 review-policy.md。


宿主图像生成工具 execution adapter:

- Preserve the original optimized image prompt, review rubric, and iteration loop.
- Use 宿主图像生成工具 exclusively for rendering. 依赖由宿主提供或由用户配置。 Do not call any external image provider or custom HTTP endpoint.
- The active reference implements every planning, layout, style, strict-review, and iteration stage directly with 当前助手 and built-in ImageGen.


Never paraphrase or weaken the loaded drawing instructions, visual standards, recipes, or review threshold.
