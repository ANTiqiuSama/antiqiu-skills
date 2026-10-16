# Formats

Read only the section for the current deliverable.

## Slide deck

- Use a fixed 1920×1080 stage scaled to fit the window, with arrow, space and click navigation, a slide counter and one `<section>` per slide labelled `data-label="03 Pricing"` for feedback.
- Before building, plan the deck system: one layout per element class, one or two background colours for the whole deck, full-bleed slides when imagery is central and a varied rhythm of section starters.
- Text is never below 24 px and is usually much larger. Use one idea per slide, and put detail in speaker notes (`<aside class="notes">`) rather than on the slide.
- Text-heavy slides still commit to imagery from the system or to labelled placeholders.
- Export: print CSS with `@page { size: 1920px 1080px; margin: 0 }` and one slide per page, then Playwright `page.pdf()`. Freeze animations before export. Produce editable PPTX through the `pptx` skill or python-pptx when the user asks for it.

## Interactive prototype

- Build a working app with real state: navigation between screens, forms that validate, lists that add, edit and delete, and success and empty states. Seed realistic sample data and mark it as sample data.
- Put mobile designs in a device frame at real size, with 44 px touch targets. Keep desktop prototypes fluid.
- Label each screen or state so the user can refer to it. Put the flow the user cares about one click from the start.
- If the user wants a model call inside the prototype, read the provider credentials from the environment. Never hard-code keys.

## Landing page or site

- Follow `frontend-design`: hero with the most characteristic element of the subject, a deliberate type pairing, one bold move and quiet surroundings.
- Make it responsive down to phone width, with visible focus and reduced motion respected. For repository apps, follow `frontend-app-builder`.

## Document, report or one-pager

- Use flowing pages at Letter or A4, `@page` margins, a 12 pt print minimum, real heading hierarchy, running headers and footers, and avoid widows on headings (`break-after: avoid`).
- Tables use tabular numbers and right-aligned figures. Figures have captions.
- Export through Playwright `page.pdf({ preferCSSPageSize: true })`. Use the `docx` or `pdf` skill when the user needs a Word or editable PDF output.

## Poster, flier or social card

- Give the root element an explicit pixel `width` and `height`. Common sizes are 1080×1350 portrait social, 1080×1080 square, 1200×630 link card and A-series at 300 dpi for print.
- Ask in plain terms when the size or medium is unclear. Export PNG with an element screenshot at `deviceScaleFactor: 2`, and PDF at the page size.
- Use one dominant element, a strong type hierarchy and generous margins. Treat type as image.

## HTML email

- Use a 600 px table-based layout with inline styles, no JS and no external CSS. Web fonts need a safe fallback.
- Every image has alt text and explicit width and height. The email works with images off, has a dark-mode-safe palette and includes a plain-text alternative when sending.

## Animation or motion piece

- Drive a timeline with `requestAnimationFrame` or the Web Animations API. Provide play, pause and scrub controls and a deterministic seek for export.
- Respect `prefers-reduced-motion` in interactive contexts.
- Export video with Remotion, or with frame capture plus ffmpeg, only when asked.

## Wireframes and explorations

- Use greyscale boxes, real labels and annotations, and many ideas quickly. Put storyboards in sequence, three to eight frames per flow.
- Present explorations on the option canvas (rounds of `1a`, `1b` and so on) and let the user pick before any high-fidelity work.

## Design system or UI kit

- Extract or define tokens (colour, type, spacing, radius, elevation, motion) as CSS custom properties, then build a specimen page showing every component with its states (default, hover, focus, active, disabled, error, loading, empty).
- When extracting from code or Figma, copy values exactly. Do not round or snap them to a grid.

## Handoff to code

Deliver tokens, component inventory with states, layout rules, asset list, interaction notes and the source HTML. Point to the matching files in the target repository when one exists.
