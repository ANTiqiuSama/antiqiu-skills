# Liquid Glass Adoption and Landmarks Case Study

Use this reference when a task mentions Liquid Glass, glass materials, translucent navigation, toolbar grouping, sidebar/inspector overlays, scroll-edge readability, or Apple-style app icons. It consolidates Apple 2026 guidance from the official adoption article, the SwiftUI Landmarks Liquid Glass article, linked Landmarks topic pages, and the local sample archive at `/Users/lukesong/Downloads/LandmarksBuildingAnAppWithLiquidGlass.zip`. For detailed control-level recipes, read `15-liquid-glass-controls.md`; for API, motion/transition, color/Dark Mode, UIKit/AppKit, and Web code examples, read `16-liquid-glass-api-motion-color.md`; for official related-link routing, read `17-liquid-glass-deep-link-map.md`.

## Source map

| Source | Use for | Skill route |
|---|---|---|
| HIG Materials: Liquid Glass | Core material definition, functional-layer rule, regular/clear variants, standard-material boundary | Start here for material choice and hierarchy |
| HIG Color: Liquid Glass color | Accent/tint rules, monochrome controls over colorful content, primary action emphasis | Use before adding color to glass controls |
| HIG Layout / Motion / Scroll views / Toolbars / Sidebars / Tab bars / Buttons / App icons / Widgets | Additional Liquid Glass design implications across layout, motion, scroll-edge readability, bars, icon layers, and widget appearances | Use `16-liquid-glass-api-motion-color.md` for categorized extraction/code and `17-liquid-glass-deep-link-map.md` for URL routing |
| SwiftUI custom Liquid Glass docs | API behavior: glassEffect, regular/clear, interactive, container, union, IDs, transitions, performance | Use for Apple API translation and Web/client analogs |
| UIKit/AppKit material docs | `UIGlassEffect`, `UIBlurEffect`, `UIVibrancyEffect`, `NSGlassEffectView`, `NSVisualEffectView.BlendingMode` | Use when translating to native clients or standard-material fallbacks |
| Adopting Liquid Glass | Migration checklist across visual refresh, icons, controls, navigation, toolbars, modals, layout, search, and platforms | Start here for audit or redesign tasks |
| Landmarks: Building an app with Liquid Glass | Concrete SwiftUI case study for iOS, iPadOS, and macOS | Use for implementation pattern extraction |
| Landmarks background extension topic | Media bleeding under sidebar/inspector without moving foreground content | Use for hero media, split view, inspector layouts |
| Landmarks horizontal scrolling topic | Scroll content that can pass under sidebars/inspectors | Use for carousels and horizontal collections |
| Landmarks toolbar topic | System toolbar glass and action grouping | Use for toolbars/action bars |
| Landmarks badges topic | Custom glass elements, IDs, and morphing | Use for custom functional glass overlays; see `15-liquid-glass-controls.md` for controls |
| Local sample zip | Source-level confirmation of APIs, spacing constants, and file organization | Use when exact sample structure matters |

## Cross-platform boundary

Liquid Glass is an Apple system material. For Web, Android, Windows, enterprise clients, or marketing pages, translate it as a set of principles rather than cloning the OS surface.

- Use glass as a functional layer for navigation, controls, inspector panels, contextual actions, or status surfaces.
- Do not use blur as generic decoration; it must clarify hierarchy, preserve content focus, or communicate continuity.
- Prefer native or design-system components before custom glass. If the target platform has no equivalent material, use a readable translucent surface with contrast, reduced-transparency fallback, and normal opaque fallback.
- Apple-only APIs such as `glassEffect`, `GlassEffectContainer`, `backgroundExtensionEffect`, `UIBackgroundExtensionView`, `NSGlassEffectView`, and Icon Composer are implementation references, not cross-platform requirements.
- Always test reduced motion, reduced transparency, high contrast, dark/light appearance, and busy or high-chroma backgrounds.

## HIG Materials extraction

HIG Materials defines Liquid Glass as the functional layer for controls and navigation, not as a general content material.

### Functional layer rule

- Use Liquid Glass to separate controls/navigation from content. Typical Apple examples include tab bars, sidebars, toolbars, floating controls, sheets, and popovers.
- Content may scroll or peek beneath this layer, but the controls on top must remain legible.
- Do not use Liquid Glass as a generic content-layer background. For app backgrounds, content cards, and structural surfaces, prefer standard materials or solid semantic surfaces.
- Exception: some content-layer controls can temporarily take on Liquid Glass while active, such as sliders and toggles, to emphasize direct manipulation.
- Custom Liquid Glass should be sparse and reserved for important functional elements.

### Regular vs clear variants

| Variant | Use for | Avoid |
|---|---|---|
| Regular | Alerts, sidebars, popovers, text-heavy or control-dense surfaces, backgrounds that may harm legibility | Rich media overlays where the control should reveal visual detail |
| Clear | Floating media controls over photos/videos or visually rich backgrounds where immersion matters | Text-heavy controls, bright backgrounds without dimming, complex content behind labels |

Regular glass blurs and adjusts background luminosity to preserve text/icon legibility. Scroll-edge effects can further protect contrast when content moves beneath controls.

Clear glass is more transparent. Use it only when the background is visually rich and the content behind the control should stay prominent. If the background is bright, add a dark dimming layer behind clear glass; Apple guidance gives 35% opacity as a useful reference point. If the background is already dark or a native media control provides its own dimming, extra dimming may be unnecessary.

### Color on Liquid Glass

- Liquid Glass has no inherent color by default; it picks up color from the content behind it.
- Color can be applied to the material for stained-glass emphasis, or to symbols/text on top of the material.
- Use color sparingly. Reserve colored glass for true emphasis such as primary actions or status indicators.
- For primary actions, prefer tinting the glass background rather than only tinting the icon/text.
- Do not tint many controls in the same toolbar or tab bar; one emphasized action is usually enough.
- Over colorful backgrounds, prefer monochrome toolbar/tab-bar labels or choose an accent with strong visual separation.
- Check the default/resting content position, not only scrolling edge cases, to avoid similar content colors sitting behind similarly colored controls.

### Standard materials boundary

Use standard materials and effects for content structure beneath Liquid Glass:

- Choose material by semantic use and required separation, not by the apparent color it creates.
- Use system/vibrant colors on top of materials for legibility.
- Thicker, more opaque materials improve contrast for text and fine details.
- Thinner, more translucent materials preserve more background context.
- In cross-platform UI, this maps to choosing between solid surfaces, low-transparency panels, and high-transparency panels based on readability and hierarchy.

### SwiftUI/API behavior to translate

- `glassEffect(_:in:)` applies the material behind a view and foreground effects over the view; the default is regular glass in a capsule-like shape.
- Apply `glassEffect` after modifiers that define the view appearance, so the final visual shape is captured correctly.
- `interactive()` makes a custom glass view react like standard glass buttons to touch and pointer input.
- Use `GlassEffectContainer` when multiple glass shapes coexist. It improves rendering performance and lets nearby shapes blend/morph.
- Container spacing controls when shapes start blending; larger spacing makes shapes merge sooner.
- Use `glassEffectUnion` when multiple views should contribute to one unified glass shape at rest.
- Use `glassEffectID` with a shared namespace when shapes need to morph during transitions.
- Too many glass containers or too many standalone glass effects can degrade performance.


## Adoption principles

### Visual refresh

- Start by rebuilding with the latest SDK and reviewing the existing app before redesigning everything.
- Let system frameworks carry bars, sheets, popovers, controls, split views, tab bars, and toolbars where possible.
- Remove custom backgrounds that fight system bars, scroll-edge effects, or Liquid Glass surfaces.
- Limit custom glass to the most important functional elements; too many glass controls create visual noise.
- Treat the material as adaptive: overlap, focus state, accessibility settings, and platform can change appearance.

### Controls

- Avoid hard-coded control dimensions; updated controls may become rounder, larger, or more spacious.
- Keep color use restrained in controls and navigation; prefer semantic/system colors with light, dark, and increased-contrast variants.
- Avoid crowding and overlapping glass controls. Give every glass surface a clear hit target and readable background relationship.
- For content scrolling under controls, provide a scroll-edge readability layer: native scroll-edge effect on Apple platforms, gradient/mask/opaque fallback elsewhere.
- Use concentric corner logic: nested controls should echo the surrounding container/window curvature instead of mixing unrelated radii.

### Navigation and layout

- Separate navigation from content as a distinct functional layer above the content layer.
- Prefer adaptive tab-to-sidebar patterns for wide contexts; use split views for sidebar plus detail plus inspector workflows.
- Audit safe areas around sidebars, inspectors, title bars, window controls, and bottom bars.
- Extend visual content beneath sidebars/inspectors when it improves edge-to-edge continuity, but do not put actionable text or controls under translucent panels.
- For iOS-like tab bars, consider scroll-minimize behavior only when it increases content focus and does not hide primary navigation unexpectedly.

### Toolbars and menus

- Group toolbar actions by function instead of letting every item share one glass capsule.
- Use fixed separators/spacers to create readable action groups.
- Prefer standard icons for common actions, but always provide accessible labels.
- Do not mix text and icons inside a group unless the whole group has a consistent rule.
- Hide the entire toolbar item, not only its inner view, to avoid empty glass slots.
- Align contextual menu top actions with equivalent swipe actions for predictability.

### Windows, modals, sheets, and popovers

- Support arbitrary window sizes and continuous resizing; do not design only for fixed breakpoints.
- Use split-view primitives for fluid column resizing where available.
- Respect safe areas and layout guides so window controls/title bars do not collide with content.
- Check sheet edges: inside content should not crowd rounder corners; outside content peeking through should feel intentional.
- Remove custom visual-effect backgrounds from sheets/popovers when the platform already supplies the material.
- Anchor action sheets or contextual dialogs to their initiating control rather than defaulting to a bottom-edge sheet on every platform.

### Lists, forms, and search

- Lists, tables, and forms should breathe more: larger row height, padding, and rounder sections.
- Section headers should use readable title-style capitalization, not all-caps by default.
- Use grouped form/list styles to inherit platform metrics where available.
- Place search according to device convention: toolbar/trailing on wider layouts, bottom/keyboard-aware on phone, semantic search tab when search is a primary tab.

### App icons

- Liquid Glass-era Apple icons use layered, dynamic, expressive composition. Cross-platform icon work can borrow the layering model, not the Apple mask/brand treatment.
- Build foreground, middle, and background layers intentionally so lighting, highlight, shadow, and transparency effects have depth.
- Use optically balanced, centered artwork that survives rounded-rectangle, square, and circular masks.
- Prefer simplified filled shapes and controlled translucency over thin outlines and complex detail.
- On Apple platforms, preview light, dark, clear, and tinted appearances and updated grids in Icon Composer or official templates.

## Landmarks sample extraction

The local sample is useful because it shows where Apple places Liquid Glass in a real app, not just the APIs.

| File | Pattern extracted | Cross-platform translation |
|---|---|---|
| `Views/Landmarks Split View/LandmarksSplitView.swift` | `NavigationSplitView`, global search, inspector, badges over content | Responsive shell with sidebar/detail/inspector and global search layer |
| `Views/Landmarks/Landmarks View/LandmarksView.swift` | Full-bleed scroll container, flexible header, title removed from toolbar | Hero-led content that starts under top chrome and owns visual hierarchy |
| `Views/Landmarks/Landmarks View/LandmarkFeaturedItemView.swift` | Background extension on image before overlay | Extend media only; keep text/CTA above the glass-safe foreground layer |
| `Views/Landmarks/Landmark Detail/LandmarkDetailView.swift` | Detail hero image, grouped toolbar, inspector button | Detail page with media continuity and grouped contextual actions |
| `Views/Landmarks/Landmarks View/LandmarkHorizontalListView.swift` | Horizontal scroll touches edges, leading spacer restores content alignment | Carousel can pass under sidebar/inspector while cards remain aligned |
| `Views/Badges/BadgesView.swift` | `GlassEffectContainer`, custom `glassEffect`, `glassEffectID`, animated expand/collapse | Custom status/action cluster that morphs as one material group |
| `Views/Landmarks/FlexibleHeader.swift` | Scroll geometry stretches a hero image when pulling beyond top bounds | Scroll-linked hero extension; disable or simplify for reduced motion |
| `Resources/Landmarks App Icon.icon/icon.json` | Layered icon groups, glass flags, translucency, lighting, shadow | Layered icon source model; platform-specific export handles final effects |

### Pattern 1: background extension

Use when a high-value image, video, map, or product render sits next to a sidebar or inspector.

- Align the media view to the leading and trailing edges of its container.
- Apply the extension to the media layer only.
- Add title, badges, buttons, and captions after the extension layer so they do not blur or slide beneath the sidebar.
- For Web, simulate with a clipped media bleed, mirrored/blurred edge strip, or a background layer behind the panel; keep the readable foreground separate.
- Avoid this pattern for dense forms, tables, or text-heavy panels where blur would reduce scannability.

### Pattern 2: horizontal scroll under sidebars

Use when a carousel or horizontal collection sits beside a translucent sidebar/inspector.

- Let the scroll container touch the window/content edges so the system or layout can continue beneath the panel.
- Add an inner spacer/padding to align the first visible card with section titles.
- Keep scroll indicators and focus rings visible above glass; do not hide affordances under the panel.
- For Web, use an edge-to-edge scroll rail with safe-area padding and a panel overlay mask.

### Pattern 3: toolbar glass grouping

Use when a toolbar has multiple unrelated actions.

- Put standalone actions in their own group.
- Combine closely related actions, such as favorite plus collection, into one group.
- Use fixed gaps between groups and flexible spacing to place the toolbar where platform conventions expect it.
- Use icons for common actions only if every icon has a text label for assistive tech and a visible text fallback where needed.

### Pattern 4: custom glass badges and morph

Use for a small, functional status/action cluster that benefits from material continuity.

- Wrap related glass items in one container so the material can merge/split as a group.
- Give every morphing item a stable ID in the shared namespace.
- Trigger state changes through a single animation transaction.
- Keep dimensions modest: the Landmarks badge cluster uses a narrow frame, small icon surfaces, and clear spacing.
- For Web, implement as a grouped overlay with transform/clip-path/opacity continuity; if reduced motion is enabled, replace morph with a dissolve or instant layout change.

## Web/client adaptation recipes

| Apple concept | Web/client equivalent | Required fallback |
|---|---|---|
| Liquid Glass material | translucent surface with blur/saturation/tint plus content-aware shadow | opaque semantic surface if blur/transparency is reduced or unsupported |
| Scroll edge effect | top/bottom gradient scrim, mask, or elevated bar that increases contrast over scrolling content | solid bar when contrast is insufficient |
| Background extension effect | media bleed or mirrored/blurred side strip beneath sidebar/inspector | plain background color/image crop when performance or readability fails |
| GlassEffectContainer morph | grouped motion container with shared geometry, transform, opacity, border-radius interpolation | static regrouping or fade when reduced motion is active |
| ToolbarSpacer grouping | action-group capsules separated by fixed gaps | visible separators or grouped buttons without glass |
| Icon Composer layers | layered source artwork with controlled opacity and masks | normal platform icon export without Apple-only glass metadata |

## Decision checklist

Before adding Liquid Glass to a frontend, answer these in order:

1. Is this a functional layer, or only decoration?
2. Can native/design-system controls provide the effect without custom glass?
3. Does the content behind the glass stay legible in light, dark, high contrast, and busy backgrounds?
4. Does reduced transparency produce an intentional opaque fallback?
5. Does reduced motion remove morphing, parallax, and scroll-linked extension?
6. Are toolbar/menu actions grouped by meaning?
7. Are sidebars, inspectors, sheets, and popovers using safe areas and edge content intentionally?
8. Are platform-only behaviors labeled as Apple-only or translated to neutral equivalents?

## Source links

- https://developer.apple.com/cn/design/human-interface-guidelines/materials#Liquid-Glass
- https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass
- https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color
- https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
- https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:)
- https://developer.apple.com/documentation/SwiftUI/Glass/regular
- https://developer.apple.com/documentation/SwiftUI/Glass/clear
- https://developer.apple.com/documentation/SwiftUI/Glass/interactive(_:)
- https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectUnion(id:namespace:)
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectID(_:in:)
- https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Applying-a-background-extension-effect
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Extending-horizontal-scrolling-under-a-sidebar-or-inspector
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Refining-the-system-provided-glass-effect-in-toolbars
- https://developer.apple.com/documentation/SwiftUI/Landmarks-Displaying-custom-activity-badges
