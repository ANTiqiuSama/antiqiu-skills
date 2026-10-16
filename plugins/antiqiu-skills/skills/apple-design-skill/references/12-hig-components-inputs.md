# HIG Components and Inputs Extraction

This file converts Apple HIG Components and Inputs into semantic frontend behavior. Use [02-components.md](02-components.md) for visual recipes, [09-motion-templates.md](09-motion-templates.md) for animation templates, [15-liquid-glass-controls.md](15-liquid-glass-controls.md) when the component needs a Liquid Glass control treatment, and [16-liquid-glass-api-motion-color.md](16-liquid-glass-api-motion-color.md) when implementation code, transition behavior, color, or Dark Mode is involved.

## 1. Component decision map

| Need | Use | Avoid |
|---|---|---|
| Immediate action | Button | Link-looking control that submits data |
| Navigation | Link / navigation item | Primary button styling unless the action is a CTA |
| Binary setting | Toggle | Button that hides current state |
| Local mutually exclusive mode | Segmented control | Top-level tab bar or random pills |
| Long/finite choice | Picker / menu | Free text when choices are known |
| Contextual commands | Menu / context menu | Hiding primary actions |
| Lightweight contextual content | Popover | Long workflows in tiny surfaces |
| Scoped task | Sheet | Full page if user must keep context visible |
| Critical interruption | Alert | Routine success messages |
| Dense structured data | List/table/outline | Card grid when scanning values matters |
| Rich visual collection | Collection/card grid | Dense table when visuals are primary |
| Long operation | Progress indicator | Fake determinate progress |

## 2. Controls

### Buttons

- Use buttons for instant actions.
- One primary action per task region is usually enough.
- Destructive actions must be explicit and visually separated.
- Buttons provide immediate pressed/disabled/loading states.
- Do not wait for the press animation to finish before executing.

Motion: Press feedback, Haptic sync.

### Links

- Use links for navigation, external resources, or document locations.
- Keep visited/focus/hover states accessible.
- Do not use a link role for destructive commands.

### Segmented controls

- Use for local mode switches in the same view.
- Keep segment labels short and parallel.
- Do not change global navigation or deep route unexpectedly.
- The selected indicator may glide; text should stay stable.

Motion: Segmented pill glide, Tab content crossfade.

### Toggles

- Use for immediate on/off states.
- Label describes the enabled state or the setting being controlled.
- Do not use for actions that require confirmation or have more than two states.

Motion: Toggle thumb glide.

### Sliders, steppers, pickers

- Slider: continuous range with live value feedback.
- Stepper: small incremental changes.
- Picker: finite choices, especially on mobile.
- Always provide keyboard and screen reader value states.

### Text and search fields

- Keep labels visible; placeholder is not a label.
- Show errors near affected fields.
- Preserve typed input after validation failure.
- Search fields need clear/cancel, result count, and no-results recovery.

Motion: Search field expansion, Validation nudge, Results crossfade.

## 3. Navigation and chrome

### Toolbars and navigation bars

- Use for frequent commands, navigation, search, and contextual actions.
- Group commands by function and risk.
- Keep chrome stable while content scrolls.
- Material/blur expresses hierarchy, not decoration.

Motion: Toolbar glass drift, Material contrast swap.

### Tab bars

- Use for stable top-level destinations.
- Keep order stable.
- Avoid more destinations than users can scan comfortably.
- Do not use tab bars for wizard steps.

### Sidebars and split views

- Use for desktop/tablet hierarchy, collections, folders, settings categories.
- Preserve selection and scroll state.
- Collapse gracefully on narrow screens.

Motion: iPadOS sidebar adapt, Breadcrumb / hierarchy return.

### Menu bar and menus

- Use menu bar behavior as a macOS reference for command organization.
- Menus are compact command containers, not primary task hiding places.
- Context menus must only expose actions related to the selected object.
- Provide visible alternatives for touch and keyboard.

Motion: Menu cascade, Anchor reveal.

## 4. Transient surfaces

### Popovers

- Anchor to a trigger or object.
- Keep content lightweight and contextual.
- Dismiss with Escape/outside click and return focus.
- Avoid long forms or multi-step flows.

### Sheets

- Use for scoped tasks related to the current context.
- Mobile: bottom sheet/full-height sheet when appropriate.
- Desktop: side sheet or inspector when it supports comparison.
- Avoid nested sheets.

### Alerts

- Reserve for critical immediate decisions or information.
- Copy must be short and specific.
- Buttons should make outcomes clear.
- Avoid decorative motion; use calm dissolve.

## 5. Content components

### Lists, tables, and outlines

- Use lists/tables for dense structured data.
- Keep rows scannable and selection state clear.
- Preserve scroll after filtering/sorting where possible.
- Use outline/tree behavior for hierarchical data.

Motion: FLIP reorder only for small/medium lists; highlight changes for large tables.

### Cards and collections

- Use cards for visual summaries, products, dashboards, or galleries.
- If the whole card is clickable, make the destination clear.
- Do not bury unrelated actions inside one card.

Motion: Card-to-detail morph, Source-to-destination.

### Images, charts, maps, web views

- Images need responsive sizing and alt text.
- Charts should keep axes stable and labels readable.
- Maps need visible controls, attribution, and fallback states.
- Web views need loading/error states and focus boundaries.

Motion: Numeric delta tick only when the change benefits comprehension.

## 6. Status and feedback components

### Progress indicators

- Use determinate progress when known.
- Use indeterminate only for unknown short waits.
- For long tasks, show state text and cancellation/background options.

### Badges and labels

- Badges supplement, not replace, primary labels.
- Labels should be readable and copyable where useful.
- Counts need accessible descriptions.

### Toasts and flags

- Use for nonblocking status.
- Critical or recoverable errors should appear inline or in a persistent surface.
- Auto-dismiss only low-risk information.

## 7. Inputs

### Touch and gestures

- Minimum comfortable target: 44px+ with spacing.
- Gesture actions need visible alternatives.
- Drag needs preview, target affordance, and cancellation.

### Keyboard

- Every interactive element is reachable.
- Enter/Space activate controls appropriately.
- Escape dismisses transient surfaces.
- Arrow keys work for segmented controls, menus, sliders, lists, and grids when expected.

### Pointing devices

- Hover is additive; focus/touch alternatives still required.
- Avoid large layout jumps on pointer hover.
- Pointer lift should be subtle and reversible.

### Focus and remote input

- Directional focus must be predictable.
- Focused item is unmistakable.
- tvOS-like parallax applies only to the active item and only when the target UI actually has remote, kiosk, gamepad, or keyboard-grid navigation.

### Haptics

- Sync haptic with real state confirmation.
- Do not use haptics for decorative motion.
- Provide visual/text feedback for users who do not receive haptics.

### Eyes and Digital Crown

- Eyes and Digital Crown are Apple-specific input models.
- Use visionOS gaze/attention only for visionOS, gaze-like hardware, or as a general lesson in stable targets and comfortable depth.
- Use Digital Crown only as inspiration for continuous scroll/adjustment controls; do not invent a crown-like UI on ordinary Web/app screens.

## 8. Component QA checklist

- [ ] Is the component role correct before styling?
- [ ] Does it work with touch, keyboard, pointer, screen reader, and reduced motion?
- [ ] Does every surface originate from and return to its context?
- [ ] Are primary, secondary, destructive, and disabled states distinct?
- [ ] Is loading/progress honest and recoverable?
- [ ] Are menu/sheet/popover actions scoped and not overloaded?
- [ ] Do dense data components preserve scanability and scroll state?
- [ ] Are animations selected from `09-motion-templates.md` and not improvised?
