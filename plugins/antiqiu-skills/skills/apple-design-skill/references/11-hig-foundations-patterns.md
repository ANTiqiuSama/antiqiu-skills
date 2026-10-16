# HIG Foundations and Patterns Extraction

This file converts Apple HIG Foundations and Patterns into frontend decisions. Use it after [10-apple-official-docs-map.md](10-apple-official-docs-map.md) identifies the official Apple page to verify.

## 1. Foundations routing

| Need | Apple source | Local implementation |
|---|---|---|
| Visual tokens | Color, Dark Mode, Materials, Typography, Layout | `01-tokens.md`, `03-patterns.md`, `05-tailwind-config.md` |
| Accessibility | Accessibility, Inclusion | `04-accessibility.md` |
| Copy and labels | Writing, Apple Style Guide | `04-accessibility.md`, product copy rules in this file |
| Icons | Icons, SF Symbols, App icons | `01-tokens.md`, `02-components.md`, `13-platform-resources-technologies.md` |
| Motion | Motion, Loading, Materials | `07-motion.md`, `09-motion-templates.md` |

## 2. Foundation extraction rules

### Accessibility and inclusion

- Design the default path for keyboard, screen reader, reduced motion, reduced transparency, high contrast, and larger text.
- Do not rely on color, motion, or icon-only states as the sole information channel.
- Keep labels human, specific, and respectful; avoid blaming users in error states.
- Ask for sensitive permissions just in time and explain purpose before the system prompt.

### Color and Dark Mode

- Use semantic roles first: text, secondary text, background, elevated background, separator, action, destructive, success, warning.
- Apple blue remains an interaction color, not a decorative brand wash.
- Dark Mode is not simple inversion: reduce pure-white glare, preserve hierarchy, and retune shadows/materials.
- Check contrast at every material state, especially during glass/blur transitions.

### Layout

- Respect safe areas, browser chrome, status bars, and device cutouts.
- Use adaptive columns: phone stack, tablet split/sidebar, desktop multi-pane.
- Keep content width readable; Apple-style spaciousness comes from hierarchy and rhythm, not empty padding alone.
- Avoid nested scroll traps unless the content model clearly needs them.

### Materials and Liquid Glass

- Use materials to express depth and hierarchy between foreground and background.
- Glass is not generic blur decoration; it must improve context, continuity, or chrome stability.
- Text must remain readable before, during, and after material transitions.
- Provide reduced transparency fallback with opaque/elevated surfaces.

### Typography and writing

- Use large, clear hierarchy; avoid too many weights.
- Keep labels concise and action-oriented.
- Error copy should explain recovery, not merely state failure.
- Apple product and technology names should follow Apple Style Guide capitalization and spelling.

### Icons and SF Symbols

- Pair icon weight with adjacent text weight.
- Filled symbols usually indicate selected/emphasized state; do not mix filled/outlined randomly.
- Functional icons need accessible names; decorative icons should be hidden from assistive tech.
- On non-Apple Web, use licensed fallback icons instead of bundling restricted Apple symbols.

## 3. Pattern extraction rules

### Launching

- Show useful content as soon as possible.
- Avoid decorative splash screens that delay the task.
- Preserve previous state when returning to a workflow.

### Onboarding

- Teach only what is needed to start.
- Let users skip nonessential education.
- Move permission prompts to the moment of value.

### Loading

- 0-100ms: show nothing special if content arrives quickly.
- 100-1000ms: show skeleton or subtle placeholder.
- >1000ms: show progress, state text, cancellation, or background continuation.
- Use determinate progress when progress is knowable; do not fake percentages.

### Searching

- Keep search scope visible.
- Provide clear empty states and recovery suggestions.
- Preserve query until the user clears or changes it.
- Debounce expensive searches and cancel stale requests.

### Settings

- Prefer sensible defaults.
- Group settings by user goal, not internal system architecture.
- Separate destructive or privacy-sensitive choices.
- Use disclosure rows for advanced details.

### Privacy

- Explain why data is needed before asking.
- Make deny/skip paths available where possible.
- Show sync, sharing, and retention state clearly.
- Avoid manipulative motion or urgency around privacy choices.

### Notifications and feedback

- Notify only when information is timely and useful.
- Use inline feedback for recoverable local errors.
- Use toast/flag for nonblocking status.
- Use alert only when immediate attention is necessary.

### Collaboration and sharing

- Show who can access what.
- Make permission changes explicit and reversible.
- Keep activity/presence subtle and relevant.
- Avoid surprising broadcast actions.

### Drag and drop

- Provide a visible drag affordance or clear object behavior.
- Show a preview and valid drop targets.
- Offer keyboard/menu alternatives.
- Confirm destructive or cross-boundary drops when needed.

### Entering data

- Keep labels visible.
- Validate near the affected field.
- Preserve user input after errors.
- Use pickers/steppers/toggles where structured input reduces errors.

### Feedback

- Feedback should answer: what happened, why, and what can I do next?
- Match feedback intensity to consequence.
- Avoid playful motion for serious errors, payments, health, identity, or privacy.

### Modality

- Use modal surfaces for focused tasks that must be completed/dismissed before returning.
- Prefer sheets/popovers when the task is scoped to the current context.
- Avoid nesting modal surfaces.
- Always return focus to the trigger or next logical element.

### Multitasking

- Preserve state across windows, panes, split views, and responsive breakpoints.
- Do not assume one fullscreen viewport.
- Keep core commands available when the window narrows.

### Media patterns

- Keep media controls discoverable and keyboard accessible.
- Provide captions/transcripts where applicable.
- Do not hide exits from fullscreen/immersive modes.
- Handle interruptions and background states visibly.

### Undo and redo

- Prefer reversible actions over confirmation spam.
- Provide undo for risky but common operations.
- Use confirmation only when action is destructive, expensive, or hard to reverse.

## 4. Pattern-to-motion map

| Pattern | Motion template |
|---|---|
| Loading | Skeleton dissolve, Progress morph |
| Search | Search field expansion, Results crossfade |
| Notifications | Toast / flag slide, Live activity morph |
| Drag and drop | FLIP reorder, Group insertion, Haptic sync |
| Modality | Edge sheet, Modal dissolve-scale, Alert dissolve |
| Multitasking | Sidebar adapt, macOS inspector slide |
| Product storytelling | Hero product reveal, Scroll scene scrub, Sticky title collapse |

## 5. QA checklist

- [ ] Did the flow start with useful content rather than decoration?
- [ ] Are permissions asked only after value is clear?
- [ ] Is loading honest, cancellable, or backgroundable when long?
- [ ] Is search scope and empty state obvious?
- [ ] Are settings grouped by user intention?
- [ ] Does feedback explain next action?
- [ ] Is every modal/sheet/popover scoped and dismissible?
- [ ] Does the layout survive phone, tablet, desktop, and split windows?
- [ ] Are text, icons, and colors semantic rather than decorative?
- [ ] Are reduced motion/transparency alternatives defined?
