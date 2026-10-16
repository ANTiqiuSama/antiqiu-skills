---
name: frontend-app-builder
description: Build new frontend apps, dashboards, games, creative websites, hero sections and requested redesigns. Follows a Claude-aligned process: ground the design in the subject, plan tokens, build code-native UI, and check the rendered result once. Image Gen concepts are optional. Replaces the build-web-apps plugin version. Skip small fixes inside an existing design system.
---

# Frontend App Builder

Act first as a senior product designer, then as the engineer who builds that design. This is an adapted version of OpenAI's `build-web-apps:frontend-app-builder`. It replaces the original's mandatory image-first pipeline and open-ended fidelity loop with the Claude Design approach: design a system in code, build it faithfully and look at it once.

## Precedence

The user's words come first. The repository's existing framework, tokens and components come second. Read AGENTS.md, CLAUDE.md, theme files and existing styles before choosing anything. Your own choices come last. For visual direction, load [frontend-design](../frontend-design/SKILL.md). For craft rules (themes, layout, charts, copy), load [claude-design craft](../claude-design/references/craft.md).

## 1. Brief

- Pin down the subject, audience, primary job, required screens or sections, supplied copy and data fields, and any constraints. Ask one round of questions only when the answers change the build (see claude-design §1). Otherwise state your assumptions and continue.
- Keep the information architecture the user describes. Do not invent sections, metrics, claims or navigation.

## 2. Design plan

Write a compact plan before coding:

- 4–6 named colour tokens.
- Typefaces and their roles.
- Spacing and radius scale.
- A layout concept with an ASCII wireframe for the first viewport and the main screen.
- One sentence on what makes this design specific to the subject.

Review the plan against the brief. Revise any part that reads like the default you would produce for any similar product, then build the revised plan.

Default restraint: one memorable element, quiet surroundings and no decorative eyebrows, pills or badges above the hero. Use no fake metrics or filler cards. Use cards only where an object really is separate.

## 3. Image Gen concepts (optional)

Use the installed `imagegen` skill only when:

- the user asks for concepts or mood options first;
- the surface depends on bespoke raster imagery (product renders, scenes, illustrations, posters);
- a game needs sprites, tiles or parallax layers.

Generate readable concepts, one per major section or state when detail matters. Get approval when the user asked to review. Then treat the accepted concept as the spec: keep its copy, palette (white stays white), container model, icon style and section order. Record any intentional deviation.

Without these triggers, design in code. The token plan is the spec. Never ship a screenshot as UI. App text, controls, tables and HUDs stay code-native.

## 4. Build

- Follow the repository's stack. For a new complex app (dashboard, editor, multi-panel tool), use React + Vite unless told otherwise. Use a single HTML file for small static deliverables.
- Structure: an app shell, focused components, shared primitives for repeated controls, separate sample data and state helpers, and tokens in one place. Keep `App` as composition glue.
- Implement through the tokens. Similar elements share a component. Differences are explicit variants.
- Set typography on every control (buttons, tabs, inputs, sidebars, toolbars). Never rely on browser defaults.
- Icons come from the repository's set, or from Lucide when it matches. Otherwise draw a clean custom SVG with a proper `viewBox`, consistent stroke and `currentColor`.
- Make the core workflow real: local state, selected states, working filters and forms, create, edit and delete, and success and empty states. Seed realistic example data labelled as examples.
- Motion: one orchestrated moment, plus feedback on user actions. Respect `prefers-reduced-motion`.
- Quality floor: responsive down to phone width, visible keyboard focus, semantic markup, 4.5:1 text contrast and no horizontal page scroll. Run type, lint and test checks if the repository has them.
- For AI features, use the user's chosen provider credentials (for example `openai-developers:openai-platform-api-key` when installed). Never use fake keys.

## 5. Verify once

1. Run the app and open it in the Browser, or in Playwright when the Browser is unavailable (state the reason).
2. Capture the first viewport and one scrolled view at desktop width and at phone width. Click through the core workflow.
3. When a concept exists, put the concept and the render side by side with `view_image`. Compare copy, layout, palette, type scale, spacing, container model, icons and asset treatment.
4. Fix what is visibly wrong: clipped or overlapping content, accidental wrapping, mobile overflow, font fallback, inert controls, broken assets, contrast, and drift from the concept. Re-check only the areas you fixed.
5. Remove temporary QA artifacts.

Do not loop on taste once the hard checks pass. Further polish is the user's call.

## Final response

Keep it short: how to run the app, which viewports and flows you checked, any intentional deviations from the concept or plan, and remaining known issues. Do not recite the token values.
