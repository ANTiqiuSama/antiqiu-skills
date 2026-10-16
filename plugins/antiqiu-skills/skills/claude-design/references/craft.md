# Craft rules

Use the sections the artifact needs. These rules fill gaps. They never override the user or an existing design system.

## Contents

- Subject and treatment
- Typography
- Colour and themes
- Layout and spacing
- Repeated elements and cards
- Charts and data
- Interfaces, dashboards and tools
- Copy inside the design
- Clean build checklist

## Subject and treatment

- Define one concrete subject, its audience and the page's single job. Distinctive choices come from the subject's own materials, instruments, units and terms of art. Include at least one detail that only this subject would have, as content and not ornament.
- Choose the treatment before you design. Plans, memos, reports and demos get a utilitarian treatment: real hierarchy, considered spacing and a proper palette, without a big hero. Landing pages, games, launch decks and keepsake tools get an editorial treatment and one real aesthetic risk. When you are unsure, a well-composed page is always acceptable. An over-designed identity sometimes is not.
- Make the page complete at rest. Content must be readable on the first frame without scrolling animations. Size a hero to its content, not to `100vh`. Tools open in a realistic working state with example data labelled as examples.

## Typography

- Use one family or two clearly different ones. Assign the roles display, body and utility (captions or data).
- Keep running text near 65 characters wide, and under 80. Serif body text gets slightly more line height.
- Set a type scale and stick to it. Use `font-variant-numeric: tabular-nums` wherever digits line up.
- Typical Chinese stack: system `PingFang SC` → `"Noto Sans SC"` or `"Source Han Sans SC"` → `sans-serif`. Load webfonts only from a host the target allows, and always declare a real fallback stack.
- Avoid these generated-page tells: one accented word in a headline, all-caps labels everywhere, and decorative labels above content.

## Colour and themes

- Choose neutrals deliberately. A grey with a slight hue toward the accent looks intentional. A pure mid-grey looks inherited.
- Semantic colours (good, warning, critical) are separate from the accent.
- When the host can be light or dark, design both themes at the token level:
  - Bare `:root` holds the full light palette.
  - `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }` redefines only tokens.
  - `:root[data-theme="dark"] { … }` repeats the dark tokens. Set `color-scheme: dark` wherever the dark palette applies.
  - Components read tokens only. `body` sets an explicit token background.
  - Declare every token in bare `:root` first.
- A deliberately single-world design (neon arcade, letterpress) can stay single-theme, but it must set its background and every colour explicitly.

## Layout and spacing

- Use flex or grid with `gap`, not per-element margins. Use `minmax(0, 1fr)` tracks, `max-width` rather than fixed `width`, and no `nowrap` or fixed heights on boxes that hold text.
- Keep a side gutter of at least 16 px at every width, safe-area aware: `padding-inline: max(16px, env(safe-area-inset-left, 0px)) max(16px, env(safe-area-inset-right, 0px))`. Stack to one column around 400 px.
- Only wide tables, code and diagrams may scroll sideways, each inside its own `overflow-x: auto` container.
- Watch selector specificity. Type-based and element-based classes that both set spacing cancel each other out without warning.

## Repeated elements and cards

- Siblings share edges, baselines and inner padding. A recurring element sits in the same place on each sibling.
- Let content set the height. Choose a column count that the items actually fill, so nothing sits alone in a row.
- Borders, fills, radii and shadows mark an object as separate. Apply them by role, not to every block. Use big-number tiles only when the numbers are the point of the page.
- Structure is information. Use numbering, eyebrows and dividers only when they encode something true. For example, use 01/02/03 only for a real sequence.

## Charts and data

1. Choose the form from the data's job: magnitude, identity, polarity, change over time, or a single headline number. Sometimes the right answer is a stat or a table.
2. Assign colour by job. Categorical hues go in a fixed order and follow the entity, not its rank. Sequential scales use one hue from light to dark. Diverging scales use two hues around a neutral.
3. Use one y-axis. Never use dual axes. Use small multiples or an indexed common base instead.
4. Draw to scale. Every label must name a value the chart actually reaches. Keep marks and labels inside the viewBox and clear of each other.
5. Use a legend for two or more series. Label up to four series directly. Never encode identity by colour alone. Offer a table view for dense data.
6. Web charts get a hover tooltip. Charts that must render in both themes take text colour from tokens.
7. Scientific and publication figures go to `vivid-figures-skill`.

## Interfaces, dashboards and tools

- Put the summary before the detail. Encode state in form as well as numbers (chip, stripe, pill) so items that need attention stand out at a glance.
- Interactive elements look interactive. Focus is visible, and controls have explicit typography, never browser-default 16 px.
- Every control works on local state. Do not ship inert buttons or fake progress.

## Copy inside the design

- Write from the user's side: "notifications", not "webhook config". Use active voice. A button says what happens ("Save changes"), and the toast echoes it ("Saved").
- Errors say what went wrong and how to fix it, without apologising. An empty state invites the first action.
- Use sentence case and plain verbs, and give each element one job. Name the artifact like a product with a short specific noun phrase, without an explanatory tail.

## Clean build checklist

- Close every element, double-quote attributes and give each form control a stable `id`.
- Respect `prefers-reduced-motion`. Use one orchestrated motion moment rather than scattered effects. Motion that responds to a user action is welcome.
- Use Canvas or WebGL for generative graphics, not long hand-written SVG paths.
- Check for overlap, cascade collisions and silent font fallback before handoff.
