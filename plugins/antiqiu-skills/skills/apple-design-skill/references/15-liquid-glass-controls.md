# Liquid Glass Controls

Use this reference when a task asks for Liquid Glass-style controls, glass buttons, floating toolbars, segmented controls, toggles, sliders, search fields, badges, status chips, contextual menus, or action palettes. Read `14-liquid-glass-adoption.md` first for adoption boundaries and Landmarks sample routing, then use this file for concrete control design decisions. For API examples, motion/transition code, color/Dark Mode variants, and UIKit/AppKit/Web fallbacks, also read `16-liquid-glass-api-motion-color.md`. For HIG/API linked-page routing, read `17-liquid-glass-deep-link-map.md`.

## Design intent

Liquid Glass controls sit in the top functional layer of an interface. They should make actions easier to find while letting content remain the visual focus.

- Use glass for controls that float over rich content, control navigation, trigger contextual actions, or show compact status.
- Avoid glass for dense form fields, long text containers, data tables, destructive confirmations, or any element that needs maximum contrast.
- Prefer native/platform controls when available; custom glass controls are for high-value moments and need accessibility fallbacks.
- Keep glass groups sparse. One well-placed glass action cluster is stronger than many competing translucent controls.
- Motion must explain state, grouping, or continuity; do not animate glass just because it can shimmer.

## HIG Materials control rules

### Functional layer first

Liquid Glass controls belong in the functional layer above content. Use them for navigation controls, toolbar actions, floating media controls, inspectors, contextual actions, status chips, and direct-manipulation controls. Do not turn content cards, app backgrounds, long text panels, or dense form regions into Liquid Glass just for style.

A content-layer exception exists for controls that become transiently interactive. Sliders and toggles can take on a Liquid Glass appearance during activation because the material highlights direct manipulation. In Web/client implementations, translate this as a stronger active thumb/track or switch thumb treatment, not as a permanently glassy form row.

### Regular and clear selection

| Control context | Prefer | Reason |
|---|---|---|
| Text-heavy popover, alert, sidebar, inspector | Regular | Background blur/luminosity adjustment protects labels and icons |
| Toolbar/tab bar over unpredictable app content | Regular or opaque fallback | Legibility matters more than immersion |
| Media controls over photo/video | Clear, with contrast check | Rich content should remain visible |
| Bright media behind controls | Clear plus dark dimming layer | Apple's clear-glass guidance uses dimming to preserve legibility |
| Dark media or native media controls | Clear may not need extra dimming | Existing darkness or native control treatment can provide contrast |
| Dense data, forms, tables | Standard material or solid surface | Liquid Glass adds noise and harms scan speed |

### Color placement

- Default glass should inherit from the content behind it rather than introduce brand color everywhere.
- Use colored glass for a single primary action, prominent status, or high-value emphasis.
- For primary actions, tint the glass background; do not rely on colored icon/text alone.
- Avoid coloring every toolbar item. Multiple tinted glass controls dilute hierarchy and can hurt readability.
- On colorful backgrounds, keep toolbar/tab labels monochrome unless the accent color is clearly distinct.
- Check both resting and scrolled states so content colors do not collide with control colors.


## Control anatomy

A Liquid Glass-inspired control has five layers:

| Layer | Role | Frontend translation |
|---|---|---|
| Backdrop sample | Connects control to content behind it | blur, saturation, tint, optional edge reflection |
| Material body | Defines tappable/control surface | translucent fill, border highlight, inner glow |
| Elevation ring | Separates the control from busy content | soft shadow plus subtle top/edge stroke |
| Content | Label, icon, value, or status | semantic color, high contrast, no low-opacity text |
| State overlay | Press, hover, focus, selected, disabled | opacity, scale, ring, tint, or grouped morph |

Minimum requirements:

- The content layer must stay readable without blur.
- Keyboard focus must be visible even when the glass surface is subtle.
- Reduced transparency must produce an opaque surface.
- Reduced motion must replace morph/slide/parallax with opacity or instant state changes.

## Material tokens

These are cross-platform starting points, not Apple API values. Treat `regular` as the default readable material and `clear` as a special media/rich-background variant.

| Token | Default | Notes |
|---|---:|---|
| `--glass-fill` | `rgba(255,255,255,.62)` | Increase opacity over busy backgrounds |
| `--glass-fill-dark` | `rgba(28,28,30,.58)` | Use dark semantic surface, not pure black |
| `--glass-blur` | `18px` | 12-24px is usually enough for controls |
| `--glass-saturate` | `1.4` | Lower if colors become noisy |
| `--glass-stroke` | `rgba(255,255,255,.42)` | Pair with darker bottom border if needed |
| `--glass-shadow` | `0 18px 48px rgba(0,0,0,.18)` | Reduce for small inline controls |
| `--glass-radius-sm` | `12px` | Small icon/action buttons |
| `--glass-radius-md` | `18px` | Segmented/action groups |
| `--glass-radius-lg` | `26px` | Floating palettes / badges cluster |
| `--glass-radius-pill` | `999px` | Pills, search, compact status |

Token rules:

- Use semantic text tokens from `01-tokens.md`; do not make labels translucent to imply glass.
- Use radius hierarchy from the container inward. Nested controls should feel concentric.
- If blur is unavailable, keep the same radius and spacing but use a solid semantic surface.
- The blur layer is performance-sensitive; keep animated properties to opacity and transform where possible.

## State model

| State | Visual behavior | Motion behavior | Accessibility note |
|---|---|---|---|
| Rest | Clear material, low shadow, readable label | none | Contrast passes without hover |
| Hover | Slight lift or highlight | 80-140ms ease-out | Do not rely on hover on touch |
| Press | Compress 1-2%, highlight dims or tightens | 50-100ms ease-out | Action should not wait for animation end |
| Focus | Strong ring outside glass edge | immediate or 80ms fade | Ring must be visible on busy content |
| Selected | Stronger fill/tint, selected indicator or thumb | 150-250ms glide/morph | Selected state must not be color-only |
| Disabled | More opaque, lower content contrast but still legible | none | Avoid transparent disabled controls over content |
| Loading | Replace content with progress or optimistic state | progress morph or subtle fade | Respect pause/stop/reduced motion |
| Error | Solid semantic error surface or message below | short nudge only if useful | Error text and icon required |

## Control recipes

### 1. Glass button

Use for primary or contextual actions over media/content.

Structure:

- pill or rounded-rectangle surface
- icon optional; text required unless the icon is universally understood
- minimum 44px touch target on mobile, 32px compact desktop target only for dense toolbars
- one primary glass button per local region

Behavior:

- rest surface is translucent but label is opaque
- press compresses slightly and reduces shadow
- focus ring appears outside the material, not inside the blur
- prominent variant uses a stronger fill or semantic tint, not excessive glow

Avoid:

- destructive action as clear glass only
- text-only glass button on busy imagery
- multiple primary glass buttons in one cluster

### 2. Icon button

Use for toolbar items, floating media controls, map controls, and compact inspectors.

Structure:

- square or circular hit target with icon centered optically
- optional label for visible text on desktop; always provide accessible label
- selected/favorite state uses filled icon plus surface change

Behavior:

- hover lift is tiny; press is immediate
- icon should not swim or parallax separately from the button
- selected state can tint the icon, but shape/fill must also change

Avoid:

- unlabeled custom icons
- icon-only groups where each icon has a different visual language
- mixing icon-only and text buttons inside the same glass capsule without a clear reason

### 3. Glass button group / toolbar cluster

Use for related actions in a toolbar or floating action palette.

Structure:

- group related actions in shared capsules
- separate unrelated groups with fixed gaps
- keep group width as small as functionally possible
- align clusters with platform expectations: bottom on phone when thumb reach matters, top/trailing on tablet/desktop when paired with content tools

Behavior:

- material can respond to scroll threshold, but individual controls should remain spatially stable
- use group-level hover/focus only for palettes; individual focus remains visible
- hidden actions remove the whole toolbar item, not only inner content

Cross-platform translation:

- Web toolbar: grouped rounded surfaces with fixed gaps and a solid fallback
- Desktop client: lower blur, stronger border, more compact density
- Mobile app: larger hit targets, fewer groups, avoid placing under system gestures

### 4. Segmented control

Use for local mode switching, filters, view mode changes, and short mutually exclusive choices.

Structure:

- one shared glass track
- selected segment has a stronger pill/thumb or fill
- labels should be short; icons optional but not required

Behavior:

- selected thumb glides 150-250ms using transform
- content switches with crossfade or fast slide, not with large page movement
- selected state must include text/shape change, not color alone

Avoid:

- more than 5 segments
- using segmented control as global navigation
- glass over high-frequency table filters where a solid chip group is clearer

### 5. Toggle / switch

Use for binary settings and feature enablement.

Structure:

- track can be glass; thumb should remain solid enough to read state
- on/off state uses thumb position plus color/label/icon
- label sits outside the switch for readability

Behavior:

- thumb glide 150-220ms
- press target includes label where platform allows
- avoid morphing the whole switch into a different shape; state clarity matters more than spectacle

Avoid:

- tiny glass switch over photo/video
- using blur to indicate disabled state
- relying on green alone for on state

### 6. Slider

Use for continuous values such as media, brightness-like settings, map zoom, or creative controls.

Structure:

- track can be translucent, but filled progress and thumb need strong contrast
- value label or preview appears near the thumb only when helpful
- large values need precise keyboard/pointer support

Behavior:

- thumb can become more glass-like during drag, but should not obscure the value
- track fill updates immediately
- haptic-like visual feedback should be subtle and tied to meaningful stops

Avoid:

- low-contrast track over busy content
- animated blur on every pointer move
- hiding exact value when precision matters

### 7. Search field

Use when search is primary or global.

Structure:

- pill-shaped field with solid text and clear placeholder
- search icon, clear button, and optional scope chips
- on phone, respect keyboard movement and bottom placement when platform convention requires it

Behavior:

- expansion should be anchored to its starting position
- search results crossfade; avoid moving the field unpredictably
- if search is a tab, use a semantic search tab model rather than a generic tab with search icon

Avoid:

- glass placeholder that fails contrast
- large blur field over text-heavy content
- global search hidden inside a decorative glass capsule

### 8. Floating status chip / badge

Use for compact status, earned badge, ongoing task, sync state, or notification count.

Structure:

- small glass or solid badge surface with icon plus value/label
- if it is actionable, make the hit target larger than the visible chip
- status color uses semantic meaning, not decoration

Behavior:

- status updates can use numeric tick, fade, or small morph
- related badge plus toggle can be placed in one material group
- collapse/expand should preserve source/destination relationship

Avoid:

- badge cluster covering primary content
- auto-playing badge animations without user action
- using Apple-only system capsule shapes for unrelated platforms

### 9. Popover / menu trigger

Use when a button opens a menu, picker, or inspector.

Structure:

- trigger and popover should feel materially related
- popover arrow/anchor points to the source control where platform supports it
- menu items use standard icons for common commands when available
- on iOS/iPadOS 26+, if the interaction is a menu or command list, prefer a native `UIButton` + `UIMenu` route before custom glass animation
- icon menu triggers can use a glass button; title/picker triggers can use a plain button with the system popup indicator

Behavior:

- menu reveals from the trigger, not from an unrelated edge
- native UIKit menus should use `UIButton.menu` and `showsMenuAsPrimaryAction`; let the system own the bubble-to-menu Liquid Glass transition
- destructive actions need separation and semantic styling
- top menu actions should match swipe/contextual actions where applicable

Avoid:

- bottom sheets for every menu on desktop/tablet
- menu blur so strong that item text loses contrast
- decorative icons on every menu item
- custom spring/scale/blur timelines that imitate a system menu when a native menu can represent the same hierarchy

### 10. Sheet and inspector controls

Use for task-focused panels, side inspectors, and modal controls.

Structure:

- sheet background can be glass/material, but inner controls should not all be glass
- keep controls away from rounder sheet corners
- inspector controls should align to the content they affect

Behavior:

- half sheet can be more translucent; full sheet should become more opaque for task focus
- inspector opening should preserve detail context
- content behind the panel can peek through only when it aids orientation

Avoid:

- placing important text behind a translucent sheet edge
- nested glass inside glass inside glass
- custom background effects that fight platform sheets/popovers

## Interaction and motion mapping

| Control | Primary motion | Duration | Reduced motion |
|---|---|---:|---|
| Button | press compress / highlight | 50-100ms | color/fill state only |
| Icon button | small lift or press | 80-140ms | instant state change |
| Segmented control | thumb glide | 150-250ms | crossfade selected fill |
| Toggle | thumb glide | 150-220ms | instant thumb position |
| Slider | direct thumb tracking | direct | direct, no extra effects |
| Toolbar cluster | material drift on scroll threshold | 150-300ms | opacity/fill swap |
| Badge group | merge/split morph | 250-450ms | fade/instant regroup |
| Popover/menu | anchor reveal | 150-250ms | dissolve |
| Sheet/inspector | edge reveal / opacity | 200-350ms | dissolve or instant |

See `09-motion-templates.md` for detailed templates: Press feedback, Segmented pill glide, Search field expansion, Menu cascade, Edge sheet, Glass materialize, Glass merge/split, Toolbar glass drift, and iPadOS sidebar adapt.

## Accessibility and fallback requirements

- Contrast: text and icons meet normal contrast over the final composited surface, not just against the nominal fill.
- Reduced transparency: swap blur/translucency for an opaque semantic background.
- Reduced motion: remove morph, parallax, large sliding, scroll-linked stretch, and shimmer.
- Increased contrast: increase fill opacity, border contrast, and focus ring strength.
- Keyboard: every interactive glass control has logical focus order and visible focus ring.
- Screen reader: icon-only controls need labels; selected/expanded/pressed states need semantic state.
- Pointer/touch: target sizes follow platform expectations; hover-only affordances need touch equivalents.
- Performance: avoid animating blur; animate transform/opacity or switch classes at thresholds.

## Implementation starter CSS

This is a platform-neutral starting point for Web prototypes. Tune per brand, background, and accessibility requirements.

```css
.lg-control {
  --lg-fill: rgba(255, 255, 255, .62);
  --lg-stroke: rgba(255, 255, 255, .44);
  --lg-shadow: 0 18px 48px rgba(0, 0, 0, .18);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .45rem;
  min-height: 44px;
  padding: 0 16px;
  color: var(--color-text, #1d1d1f);
  background: var(--lg-fill);
  border: 1px solid var(--lg-stroke);
  border-radius: 999px;
  box-shadow: var(--lg-shadow);
  -webkit-backdrop-filter: blur(18px) saturate(1.4);
  backdrop-filter: blur(18px) saturate(1.4);
  transition: transform 120ms ease, box-shadow 160ms ease, background-color 160ms ease;
}

.lg-control:hover {
  transform: translateY(-1px);
}

.lg-control:active {
  transform: scale(.985);
  box-shadow: 0 10px 28px rgba(0, 0, 0, .14);
}

.lg-control:focus-visible {
  outline: 2px solid var(--color-link, #0071e3);
  outline-offset: 3px;
}

@media (prefers-reduced-transparency: reduce) {
  .lg-control {
    background: var(--color-bg-elevated, #fff);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .lg-control {
    transition: none;
  }
  .lg-control:hover,
  .lg-control:active {
    transform: none;
  }
}
```

## QA checklist

- [ ] Does every glass control have a functional reason to be glass?
- [ ] Are related toolbar actions grouped and unrelated actions separated?
- [ ] Does the control remain readable over the busiest expected background?
- [ ] Does reduced transparency produce a deliberate opaque version?
- [ ] Does reduced motion remove morphing and scroll-linked movement?
- [ ] Are icon-only controls labeled for assistive tech?
- [ ] Are selected, disabled, loading, and error states distinguishable without color alone?
- [ ] For iOS/iPadOS 26+ menu triggers, did you use native `UIButton` + `UIMenu` before building a custom glass menu?
- [ ] Are touch targets, focus rings, and keyboard order correct?
- [ ] Is the blur layer static or threshold-based rather than continuously animated?

## Source links

- https://developer.apple.com/cn/design/human-interface-guidelines/materials#Liquid-Glass
- https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color
- https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass
- https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:)
- https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectID(_:in:)
- https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glass
- https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glassProminent
- https://developer.apple.com/documentation/swiftui/glassbuttonstyle
- https://developer.apple.com/documentation/swiftui/glassprominentbuttonstyle
- https://developer.apple.com/documentation/UIKit/UIButtonConfiguration/glassButtonConfiguration
- https://developer.apple.com/documentation/UIKit/UIButton/menu
- https://developer.apple.com/documentation/UIKit/UIButton/showsMenuAsPrimaryAction
- https://developer.apple.com/documentation/UIKit/UIMenu
- https://developer.apple.com/documentation/UIKit/UIAction
- https://developer.apple.com/documentation/UIKit/UIMenuElementState/on
- https://developer.apple.com/documentation/UIKit/UIMenuElementAttributes/disabled
- https://developer.apple.com/documentation/UIKit/UIMenuElementAttributes/destructive
- https://developer.apple.com/documentation/SwiftUI/Glass/regular
- https://developer.apple.com/documentation/SwiftUI/Glass/clear
- https://developer.apple.com/documentation/SwiftUI/Glass/interactive(_:)
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectUnion(id:namespace:)
