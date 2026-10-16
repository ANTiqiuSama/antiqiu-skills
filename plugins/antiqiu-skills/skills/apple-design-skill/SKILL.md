---
name: apple-design-skill
description: Apply Apple design language or HIG guidance when requested or relevant to an existing Apple-style interface; keep the product design system primary.
license: MIT
metadata:
  version: 1.2.1
  category: productivity
  tags:
    - frontend
    - docs
    - planning
    - analysis
  namespace: "@LukeSONG2000"
  description_zh: 在明确需要 Apple 风格或 HIG 参考时，按需提供样式、动效和平台边界；以目标产品的设计系统为准。
  author: LukeSONG2000
  homepage: https://github.com/LukeSONG2000/apple-design-skill
  compatibility:
    claude_code: true
    codex: true
  claude:
    legacy_name: apple-design
    auto_activate: false
---

# Apple Design Language

Use Apple design guidance when requested or when it is already the product's design language. Keep user choices and the existing design system primary. Ordinary frontend work does not automatically load this skill; use [frontend-design](../frontend-design/SKILL.md) for non-Apple visual direction and [claude-design](../claude-design/SKILL.md) for HTML artifacts.

Transfer hierarchy, spacing, semantic color, readable type, feedback, motion and accessibility across platforms. Apple-only hardware, interactions and resources require real platform support and appropriate rights; otherwise use a neutral fallback. Do not treat Apple.com's token values as universal rules.

## Load only the needed reference

- Foundations: [philosophy](references/00-philosophy.md), [tokens](references/01-tokens.md), [components](references/02-components.md), [page patterns](references/03-patterns.md).
- Implementation: [accessibility](references/04-accessibility.md), [Tailwind/CSS](references/05-tailwind-config.md), [fonts and licensing](references/06-fonts.md). Never bundle SF Pro or PingFang files.
- Motion: [motion tokens](references/07-motion.md) and [examples](references/09-motion-templates.md); respect reduced-motion settings.
- Official guidance: [coverage map](references/08-apple-docs-coverage.md), [official links](references/10-apple-official-docs-map.md), [HIG foundations/patterns](references/11-hig-foundations-patterns.md), [HIG components/inputs](references/12-hig-components-inputs.md).
- Platform, resources and branding: [platform boundaries](references/13-platform-resources-technologies.md).
- Liquid Glass: [adoption](references/14-liquid-glass-adoption.md), [controls](references/15-liquid-glass-controls.md), [API/motion/color](references/16-liquid-glass-api-motion-color.md), [deep links](references/17-liquid-glass-deep-link-map.md).

Resources include Apple public styles, HIG, Design Resources and platform documentation plus maintained cross-platform examples. Distinguish extracted patterns from official requirements. Check the affected states, keyboard/focus behavior, contrast and actual rendering; read unrelated platform chapters only when the task needs them.
