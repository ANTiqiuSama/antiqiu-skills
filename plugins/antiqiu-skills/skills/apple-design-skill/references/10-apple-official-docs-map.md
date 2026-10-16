# Apple Official Docs Crawl Map

Crawled snapshot: 2026-07-15. Source scope: Apple Human Interface Guidelines, Apple Design Resources, Apple Fonts, SF Symbols, Apple Style Guide, and selected Apple Developer documentation for Liquid Glass, materials, color, motion, menus, and navigation transitions.

This file is the routing map. It lists where Apple official material lives and which local reference to load before implementing a frontend. It intentionally stores titles, URLs, and frontend routing notes rather than long copied passages from Apple docs.

## 1. How Codex should use this map

1. Identify the task class: visual system, motion, component, platform, input, technology brand, or resource/license.
2. Load the local reference shown in the **Local extraction** column.
3. Use the Apple URL only for verification or deeper detail.
4. Convert Apple platform behavior to Web / Client / Mobile patterns; do not copy Apple assets or private implementation.
5. When motion is involved, always pair the category file with [07-motion.md](07-motion.md) and [09-motion-templates.md](09-motion-templates.md).
6. Check the **cross-platform applicability level** before using Apple-only platforms or technologies.

## 2. Cross-platform applicability levels

| Level | Meaning | Examples | Rule |
|---|---|---|---|
| Core transferable | Useful across Web, desktop client, mobile app, and enterprise UI | color semantics, layout rhythm, typography hierarchy, loading, feedback, accessibility, buttons, forms, sheets | Use freely after adapting to target platform and brand |
| Platform-informed transferable | Useful when the target has similar screen size, density, input, or task model | iOS touch patterns, iPadOS split view, macOS sidebar/toolbar, Apple.com storytelling | Use as a reference model, not as native imitation |
| Scenario inspiration | Useful only for analogous scenarios | watchOS glanceability, tvOS focus grid, visionOS depth comfort, CarPlay low-distraction UI | Extract constraints/principles; do not copy surface UI by default |
| Apple-only / brand-gated | Requires Apple platform support, official assets, or strict brand rules | Apple Pay, Sign in with Apple, Wallet, HealthKit, SF Symbols, Product Bezels, Apple Fonts, Dynamic Island, Live Activities | Use only when supported and licensed; otherwise design neutral fallback |

## 3. Local reference routing

| Task class | Start here | Then load | Use when |
|---|---|---|---|
| Apple-style landing / product page | `00-philosophy.md` | `01-tokens.md`, `03-patterns.md`, `09-motion-templates.md` | Product storytelling, Apple.com-like layouts, hero sections |
| Official docs lookup | `10-apple-official-docs-map.md` | relevant category below | Need to find which Apple doc/page applies |
| Foundations: color, layout, typography, materials | `11-hig-foundations-patterns.md` | `01-tokens.md`, `03-patterns.md` | Visual system, semantic tokens, hierarchy, copy |
| Patterns: loading, search, privacy, onboarding | `11-hig-foundations-patterns.md` | `04-accessibility.md`, `09-motion-templates.md` | Flow design and system states |
| Components and inputs | `12-hig-components-inputs.md` | `02-components.md`, `07-motion.md`, `15-liquid-glass-controls.md` | Buttons, sheets, menus, tables, forms, keyboard/pointer/touch, Liquid Glass controls |
| Platform adaptation | `13-platform-resources-technologies.md` | `03-patterns.md`, `04-accessibility.md` | Apply platform references with transferability filter |
| Apple resources and brand technologies | `13-platform-resources-technologies.md` | `06-fonts.md`, `01-tokens.md` | Use Apple-only resources only when licensed/supported; provide fallback |
| Liquid Glass / materials / motion | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | `07-motion.md`, `09-motion-templates.md`, `01-tokens.md` | Adoption audit, controls, API examples, color/Dark Mode, glass material, morph, scroll-edge scenes, official deep-link routing |

## 4. Liquid Glass

Liquid Glass has a standalone route because it crosses foundations, controls, motion, accessibility, SwiftUI APIs, and platform-specific materials. Load this section before treating any blur/translucency as an Apple-style design decision. For linked-page exploration and API routing, load `17-liquid-glass-deep-link-map.md`.

| Apple doc | URL | Applicability | Local extraction | Frontend use |
|---|---|---|---|---|
| HIG Materials: Liquid Glass | https://developer.apple.com/cn/design/human-interface-guidelines/materials#Liquid-Glass | Core transferable principles / Apple material behavior | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `01-tokens.md` | Functional-layer rule, regular/clear variant choice, scroll-edge readability, content-layer boundary |
| HIG Materials: Standard materials | https://developer.apple.com/cn/design/human-interface-guidelines/materials#Standard-materials | Core transferable principles | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `01-tokens.md` | Use standard/opaque materials for content structure under glass; map to SwiftUI Material, UIKit blur/vibrancy, AppKit visual effects |
| HIG Color: Liquid Glass color | https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color | Core transferable principles | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `01-tokens.md` | Tint sparingly, emphasize primary actions with material tint, keep controls monochrome over colorful content |
| HIG Color: System colors | https://developer.apple.com/design/human-interface-guidelines/color#System-colors | Core transferable principles | `16-liquid-glass-api-motion-color.md`, `01-tokens.md` | Semantic foreground/background colors that adapt to light, dark, vibrancy, and increased contrast |
| HIG Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility | Core transferable | `04-accessibility.md`, `14-liquid-glass-adoption.md` | Reduced transparency, increased contrast, legibility checks |
| HIG Dark Mode | https://developer.apple.com/design/human-interface-guidelines/dark-mode | Core transferable | `01-tokens.md`, `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md` | Light/dark/high-contrast variants for adaptive glass surfaces |
| HIG Sliders | https://developer.apple.com/design/human-interface-guidelines/sliders | Component exception | `12-hig-components-inputs.md`, `15-liquid-glass-controls.md` | Direct-manipulation controls may take on glass while active; translate as active thumb/track feedback |
| HIG Toggles | https://developer.apple.com/design/human-interface-guidelines/toggles | Component exception | `12-hig-components-inputs.md`, `15-liquid-glass-controls.md` | Binary controls may use transient glass emphasis; preserve clear on/off state |
| Liquid Glass overview | https://developer.apple.com/documentation/technologyoverviews/liquid-glass | Platform-informed transferable | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Material hierarchy, continuity, platform differences, fallback planning |
| Adopting Liquid Glass | https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass | Core transferable / Apple-specific APIs inside | `14-liquid-glass-adoption.md` | Migration checklist for controls, navigation, toolbars, modals, layout, search, and icons |
| SwiftUI View styles: Styling views with Liquid Glass | https://developer.apple.com/documentation/swiftui/view-styles | Apple API index | `17-liquid-glass-deep-link-map.md`, `16-liquid-glass-api-motion-color.md` | Check the complete SwiftUI Liquid Glass view-style list from the docs sidebar |
| Landmarks: Building an app with Liquid Glass | https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass | SwiftUI sample / pattern extraction | `14-liquid-glass-adoption.md`, `09-motion-templates.md` | Background extension, toolbar grouping, horizontal scroll under sidebars, custom badges, app icon layers |
| Applying Liquid Glass to custom views | https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views | Apple API behavior / transferable grouping model | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Custom glass shape, grouping, morph, performance, accessibility fallback |
| SwiftUI `glassEffect(_:in:)` | https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:) | Apple API behavior | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md` | Apply material after appearance-defining modifiers; translate to one final composited control shape |
| SwiftUI `Glass.regular` | https://developer.apple.com/documentation/SwiftUI/Glass/regular | Variant model | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md` | Default readable glass for text-heavy, control-dense, or unpredictable backgrounds |
| SwiftUI `Glass.clear` | https://developer.apple.com/documentation/SwiftUI/Glass/clear | Variant model | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md` | Rich media overlays; add dimming on bright backgrounds when contrast needs it |
| SwiftUI `Glass.interactive(_:)` | https://developer.apple.com/documentation/SwiftUI/Glass/interactive(_:) | Interaction model | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Touch/pointer reaction for custom glass controls |
| SwiftUI `GlassEffectContainer` | https://developer.apple.com/documentation/swiftui/glasseffectcontainer | Motion/performance model | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Group related glass shapes, enable blend/morph, avoid excessive containers |
| SwiftUI `glassEffectUnion` | https://developer.apple.com/documentation/SwiftUI/View/glassEffectUnion(id:namespace:) | Grouping model | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Combine multiple views into one resting material shape |
| SwiftUI `glassEffectID` | https://developer.apple.com/documentation/SwiftUI/View/glassEffectID(_:in:) | Continuity model | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Stable IDs for morphing glass elements between states |
| SwiftUI `GlassEffectTransition` | https://developer.apple.com/documentation/swiftui/glasseffecttransition | Transition model | `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Entry/exit continuity for glass surfaces |
| UIKit `UIButtonConfiguration.glassButtonConfiguration` | https://developer.apple.com/documentation/UIKit/UIButtonConfiguration/glassButtonConfiguration | Apple API behavior / native menu trigger support | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Objective-C/UIKit glass button configuration; useful for React Native/Flutter bridges |
| UIKit `UIButton.menu` | https://developer.apple.com/documentation/UIKit/UIButton/menu | Apple API behavior / system menu presentation | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Attach a `UIMenu` to the triggering button so UIKit owns anchored menu presentation |
| UIKit `UIButton.showsMenuAsPrimaryAction` | https://developer.apple.com/documentation/UIKit/UIButton/showsMenuAsPrimaryAction | Apple API behavior / trigger behavior | `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Tap opens the assigned menu directly; avoid custom tap-to-menu animation |
| UIKit `UIMenu` / `UIAction` | https://developer.apple.com/documentation/UIKit/UIMenu | Apple API behavior / menu hierarchy | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Preserve submenus, inline sections, images, selected/checkmark state, disabled state, and destructive actions |
| UIKit `UIAction` | https://developer.apple.com/documentation/UIKit/UIAction | Apple API behavior / leaf command | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Model menu leaves as semantic actions with title, image, state, attributes, and handler |
| UIKit menu options/states | https://developer.apple.com/documentation/UIKit/UIMenu/Options-swift.struct/displayInline | Apple API behavior / menu semantics | `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Route inline sections, single-selection groups, selected state, disabled state, and destructive actions to native menu semantics |
| UIKit `UIBlurEffect` | https://developer.apple.com/documentation/UIKit/UIBlurEffect | Standard-material fallback | `16-liquid-glass-api-motion-color.md` | Blur content behind a visual-effect view; not a full Liquid Glass replacement |
| UIKit `UIVibrancyEffect` | https://developer.apple.com/documentation/UIKit/UIVibrancyEffect | Standard-material fallback | `16-liquid-glass-api-motion-color.md` | Improve foreground label/icon vividness above blur |
| AppKit `NSVisualEffectView.BlendingMode` | https://developer.apple.com/documentation/AppKit/NSVisualEffectView/BlendingMode-swift.enum | Standard-material fallback | `16-liquid-glass-api-motion-color.md` | Choose behind-window vs within-window blending for macOS material surfaces |
| SwiftUI `Material` | https://developer.apple.com/documentation/SwiftUI/Material | Standard-material fallback | `16-liquid-glass-api-motion-color.md` | Content-layer material and vibrancy behavior beneath glass |
| SwiftUI glass button styles | https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glass | Apple API behavior / control styling | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md` | Default glass button behavior and states |
| SwiftUI glass prominent button style | https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glassProminent | Apple API behavior / control emphasis | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md` | Prominent glass primary actions; use one emphasized action per local group |
| SwiftUI `GlassButtonStyle` | https://developer.apple.com/documentation/swiftui/glassbuttonstyle | Apple API concrete type | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | API parity for standard glass buttons; prefer semantic `.glass` guidance |
| SwiftUI `GlassProminentButtonStyle` | https://developer.apple.com/documentation/swiftui/glassprominentbuttonstyle | Apple API concrete type | `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | API parity for prominent glass buttons; keep emphasis sparse |
| SwiftUI `DefaultGlassEffectShape` | https://developer.apple.com/documentation/swiftui/defaultglasseffectshape | Apple API concrete type | `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | Default capsule shape for glass effects; override shape deliberately |
| Liquid Glass deep related-link map | HIG + SwiftUI/UIKit/AppKit links from Liquid Glass seed pages | Routing / classification | `17-liquid-glass-deep-link-map.md` | Pick the next official page to open; separate transferable guidance from Apple-only APIs |

## 5. Foundations

| Apple doc | URL | Local extraction | Frontend use |
|---|---|---|---|
| Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility | `04-accessibility.md`, `11-hig-foundations-patterns.md` | Contrast, focus, screen reader, reduced motion/transparency |
| Inclusion | https://developer.apple.com/design/human-interface-guidelines/inclusion | `11-hig-foundations-patterns.md` | Respectful copy, inclusive defaults, user-first presentation |
| App icons | https://developer.apple.com/design/human-interface-guidelines/app-icons | `11-hig-foundations-patterns.md` | App icon production cues; do not copy Apple icons |
| Icons | https://developer.apple.com/design/human-interface-guidelines/icons | `11-hig-foundations-patterns.md` | Icon clarity, consistency, semantic use |
| Color | https://developer.apple.com/design/human-interface-guidelines/color | `01-tokens.md`, `11-hig-foundations-patterns.md` | Semantic colors, contrast, brand blue discipline |
| Dark Mode | https://developer.apple.com/design/human-interface-guidelines/dark-mode | `01-tokens.md`, `11-hig-foundations-patterns.md` | Dark palettes, elevated surfaces, images in dark UI |
| Layout | https://developer.apple.com/design/human-interface-guidelines/layout | `03-patterns.md`, `11-hig-foundations-patterns.md` | Adaptive grids, safe areas, readable width |
| Materials | https://developer.apple.com/design/human-interface-guidelines/materials | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `01-tokens.md`, `07-motion.md`, `09-motion-templates.md` | Glass/material hierarchy, blur/transparency readability |
| Motion | https://developer.apple.com/design/human-interface-guidelines/motion | `07-motion.md`, `09-motion-templates.md` | Purposeful motion, continuity, reduced motion |
| Typography | https://developer.apple.com/design/human-interface-guidelines/typography | `01-tokens.md`, `06-fonts.md`, `11-hig-foundations-patterns.md` | Font stacks, hierarchy, readability |
| Writing | https://developer.apple.com/design/human-interface-guidelines/writing | `04-accessibility.md`, `11-hig-foundations-patterns.md` | Concise labels, action copy, error/help text |
| SF Symbols | https://developer.apple.com/design/human-interface-guidelines/sf-symbols | `11-hig-foundations-patterns.md`, `13-platform-resources-technologies.md` | Symbol weight/scale, icon fallback, license awareness |

## 6. Platform design

| Apple doc | URL | Applicability | Local extraction | Frontend use |
|---|---|---|---|---|
| Designing for iOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-ios | Platform-informed transferable | `13-platform-resources-technologies.md` | Phone-first touch layouts, navigation stacks, tab bars, sheets |
| Designing for iPadOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados | Platform-informed transferable | `13-platform-resources-technologies.md` | Split views, sidebars, toolbars, drag/drop, pointer/keyboard |
| Designing for macOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-macos | Platform-informed transferable | `13-platform-resources-technologies.md` | Dense desktop workflows, menus, inspectors, multi-pane layouts |
| Designing for watchOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos | Scenario inspiration | `13-platform-resources-technologies.md` | Extract glanceable/compact constraints; do not mimic watch UI by default |
| Designing for tvOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos | Scenario inspiration | `13-platform-resources-technologies.md`, `12-hig-components-inputs.md` | Use focus-grid ideas only for TV/kiosk/remote/keyboard contexts |
| Designing for visionOS | https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos | Scenario inspiration / Apple-only when targeting visionOS | `13-platform-resources-technologies.md`, `09-motion-templates.md` | Extract depth comfort and material hierarchy; do not fake spatial OS chrome |
| Spatial layout | https://developer.apple.com/design/human-interface-guidelines/spatial-layout | Scenario inspiration / Apple-only when targeting visionOS | `13-platform-resources-technologies.md` | Use depth principles only when the target UI has spatial/layered needs |

## 7. Patterns

| Apple doc | URL | Local extraction | Frontend use |
|---|---|---|---|
| Launching | https://developer.apple.com/design/human-interface-guidelines/launching | `11-hig-foundations-patterns.md` | Fast startup, avoid unnecessary splash/loading |
| Onboarding | https://developer.apple.com/design/human-interface-guidelines/onboarding | `11-hig-foundations-patterns.md` | Quick start, skip path, just-in-time education |
| Loading | https://developer.apple.com/design/human-interface-guidelines/loading | `07-motion.md`, `09-motion-templates.md`, `11-hig-foundations-patterns.md` | Skeletons, progress, content-first loading |
| Searching | https://developer.apple.com/design/human-interface-guidelines/searching | `12-hig-components-inputs.md`, `11-hig-foundations-patterns.md` | Search fields, scoped filters, empty results |
| Settings | https://developer.apple.com/design/human-interface-guidelines/settings | `11-hig-foundations-patterns.md`, `12-hig-components-inputs.md` | Grouped settings, disclosure, defaults |
| Privacy | https://developer.apple.com/design/human-interface-guidelines/privacy | `11-hig-foundations-patterns.md`, `13-platform-resources-technologies.md` | Just-in-time permission, clear data purpose |
| Notifications | https://developer.apple.com/design/human-interface-guidelines/notifications | `11-hig-foundations-patterns.md`, `09-motion-templates.md` | Timely status, non-blocking feedback, live regions |
| Collaboration and sharing | https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing | `11-hig-foundations-patterns.md` | Share controls, permissions, presence/activity |
| Drag and drop | https://developer.apple.com/design/human-interface-guidelines/drag-and-drop | `12-hig-components-inputs.md`, `09-motion-templates.md` | Drag preview, targets, keyboard alternatives |
| Entering data | https://developer.apple.com/design/human-interface-guidelines/entering-data | `12-hig-components-inputs.md` | Forms, validation, input assistance |
| Feedback | https://developer.apple.com/design/human-interface-guidelines/feedback | `12-hig-components-inputs.md`, `09-motion-templates.md` | State feedback, recovery, confirmations |
| Going full screen | https://developer.apple.com/design/human-interface-guidelines/going-full-screen | `13-platform-resources-technologies.md` | Immersive media/work modes, exit clarity |
| Managing accounts | https://developer.apple.com/design/human-interface-guidelines/managing-accounts | `11-hig-foundations-patterns.md`, `13-platform-resources-technologies.md` | Account walls, sign-in timing, privacy |
| Modality | https://developer.apple.com/design/human-interface-guidelines/modality | `12-hig-components-inputs.md` | Modal/sheet decision and focus management |
| Multitasking | https://developer.apple.com/design/human-interface-guidelines/multitasking | `13-platform-resources-technologies.md` | Multi-window, split screen, responsive persistence |
| Playing audio | https://developer.apple.com/design/human-interface-guidelines/playing-audio | `11-hig-foundations-patterns.md` | Media controls, interruptions, background state |
| Playing video | https://developer.apple.com/design/human-interface-guidelines/playing-video | `11-hig-foundations-patterns.md` | Video controls, captions, fullscreen |
| Printing | https://developer.apple.com/design/human-interface-guidelines/printing | `12-hig-components-inputs.md` | Print dialogs, preview, system handoff |
| Ratings and reviews | https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews | `11-hig-foundations-patterns.md` | Prompt timing, respectful review requests |
| Undo and redo | https://developer.apple.com/design/human-interface-guidelines/undo-and-redo | `12-hig-components-inputs.md` | Reversible actions, destructive alternatives |

## 8. Components

| Apple doc | URL | Local extraction | Frontend use |
|---|---|---|---|
| Buttons | https://developer.apple.com/design/human-interface-guidelines/buttons | `12-hig-components-inputs.md`, `02-components.md` | Instant actions, primary/secondary/destructive states |
| Toolbars | https://developer.apple.com/design/human-interface-guidelines/toolbars | `12-hig-components-inputs.md`, `03-patterns.md` | Frequent commands, search, contextual actions |
| Navigation bars | https://developer.apple.com/design/human-interface-guidelines/navigation-bars | `12-hig-components-inputs.md`, `03-patterns.md` | Top chrome/navigation behavior; currently aliases toolbar-like docs |
| Tab bars | https://developer.apple.com/design/human-interface-guidelines/tab-bars | `12-hig-components-inputs.md`, `03-patterns.md` | Top-level mobile navigation |
| Sidebars | https://developer.apple.com/design/human-interface-guidelines/sidebars | `12-hig-components-inputs.md`, `13-platform-resources-technologies.md` | Desktop/tablet navigation and collections |
| The menu bar | https://developer.apple.com/design/human-interface-guidelines/the-menu-bar | `13-platform-resources-technologies.md` | macOS menu model, commands, discoverability |
| Menus | https://developer.apple.com/design/human-interface-guidelines/menus | `12-hig-components-inputs.md` | Compact commands and options |
| Edit menus | https://developer.apple.com/design/human-interface-guidelines/edit-menus | `12-hig-components-inputs.md` | Text/object edit commands |
| Context menus | https://developer.apple.com/design/human-interface-guidelines/context-menus | `12-hig-components-inputs.md` | Object-specific actions |
| Popovers | https://developer.apple.com/design/human-interface-guidelines/popovers | `12-hig-components-inputs.md` | Anchored contextual surfaces |
| Sheets | https://developer.apple.com/design/human-interface-guidelines/sheets | `12-hig-components-inputs.md` | Scoped tasks, bottom/side sheets |
| Alerts | https://developer.apple.com/design/human-interface-guidelines/alerts | `12-hig-components-inputs.md` | Critical immediate information |
| Activity views | https://developer.apple.com/design/human-interface-guidelines/activity-views | `12-hig-components-inputs.md` | Share/action sheets and activity flows |
| Windows | https://developer.apple.com/design/human-interface-guidelines/windows | `13-platform-resources-technologies.md` | Desktop/spatial windows and workspaces |
| Split views | https://developer.apple.com/design/human-interface-guidelines/split-views | `13-platform-resources-technologies.md` | Master-detail and multi-pane layouts |
| Scroll views | https://developer.apple.com/design/human-interface-guidelines/scroll-views | `12-hig-components-inputs.md` | Scroll behavior and nested scroll caution |
| Lists and tables | https://developer.apple.com/design/human-interface-guidelines/lists-and-tables | `12-hig-components-inputs.md` | Structured dense data |
| Outline views | https://developer.apple.com/design/human-interface-guidelines/outline-views | `12-hig-components-inputs.md` | Hierarchical data trees |
| Text fields | https://developer.apple.com/design/human-interface-guidelines/text-fields | `12-hig-components-inputs.md` | Short text input, labels, validation |
| Search fields | https://developer.apple.com/design/human-interface-guidelines/search-fields | `12-hig-components-inputs.md` | Search entry, cancel, clear, scope |
| Pickers | https://developer.apple.com/design/human-interface-guidelines/pickers | `12-hig-components-inputs.md` | Finite choices and native selection patterns |
| Sliders | https://developer.apple.com/design/human-interface-guidelines/sliders | `12-hig-components-inputs.md` | Continuous value selection |
| Steppers | https://developer.apple.com/design/human-interface-guidelines/steppers | `12-hig-components-inputs.md` | Increment/decrement controls |
| Toggles | https://developer.apple.com/design/human-interface-guidelines/toggles | `12-hig-components-inputs.md` | Binary state switching |
| Progress indicators | https://developer.apple.com/design/human-interface-guidelines/progress-indicators | `07-motion.md`, `12-hig-components-inputs.md` | Determinate/indeterminate progress |
| Labels | https://developer.apple.com/design/human-interface-guidelines/labels | `12-hig-components-inputs.md`, `04-accessibility.md` | Static readable text and labels |
| Images | https://developer.apple.com/design/human-interface-guidelines/images | `11-hig-foundations-patterns.md` | Responsive artwork, alt text, no layout shift |
| Charts | https://developer.apple.com/design/human-interface-guidelines/charts | `11-hig-foundations-patterns.md`, `09-motion-templates.md` | Clear data visualization |
| Maps | https://developer.apple.com/design/human-interface-guidelines/maps | `13-platform-resources-technologies.md` | Geographic context, controls, attribution |
| Web views | https://developer.apple.com/design/human-interface-guidelines/web-views | `12-hig-components-inputs.md` | Embedded web content and boundaries |
| Segmented controls | https://developer.apple.com/design/human-interface-guidelines/segmented-controls | `12-hig-components-inputs.md`, `09-motion-templates.md` | Local mode selection |
| Disclosure controls | https://developer.apple.com/design/human-interface-guidelines/disclosure-controls | `12-hig-components-inputs.md` | Expand/collapse related content |
| Page controls | https://developer.apple.com/design/human-interface-guidelines/page-controls | `12-hig-components-inputs.md` | Paged flat lists/carousels |
| Status bars | https://developer.apple.com/design/human-interface-guidelines/status-bars | `13-platform-resources-technologies.md` | Safe area and device/system status |

## 9. Inputs and feedback

| Apple doc | URL | Local extraction | Frontend use |
|---|---|---|---|
| Gestures | https://developer.apple.com/design/human-interface-guidelines/gestures | `12-hig-components-inputs.md` | Direct manipulation and visible alternatives |
| Touchscreen gestures | https://developer.apple.com/design/human-interface-guidelines/touchscreen-gestures | `12-hig-components-inputs.md` | Touch target and gesture rules |
| Keyboards | https://developer.apple.com/design/human-interface-guidelines/keyboards | `12-hig-components-inputs.md`, `04-accessibility.md` | Shortcuts, focus order, command discoverability |
| Pointing devices | https://developer.apple.com/design/human-interface-guidelines/pointing-devices | `12-hig-components-inputs.md` | Pointer/hover/focus behavior |
| Focus and selection | https://developer.apple.com/design/human-interface-guidelines/focus-and-selection | `12-hig-components-inputs.md` | tvOS/keyboard focus and selection distinction |
| Remotes | https://developer.apple.com/design/human-interface-guidelines/remotes | `12-hig-components-inputs.md`, `13-platform-resources-technologies.md` | Remote-first focus navigation |
| Game controls | https://developer.apple.com/design/human-interface-guidelines/game-controllers | `12-hig-components-inputs.md` | Controller mapping and hints |
| Playing haptics | https://developer.apple.com/design/human-interface-guidelines/playing-haptics | `12-hig-components-inputs.md`, `09-motion-templates.md` | Haptic/visual timing sync |
| Eyes | https://developer.apple.com/design/human-interface-guidelines/eyes | `13-platform-resources-technologies.md` | Apple-only input; use only for visionOS or gaze-like products |
| Digital Crown | https://developer.apple.com/design/human-interface-guidelines/digital-crown | `13-platform-resources-technologies.md` | Apple-only input; use only as a continuous adjustment metaphor |

## 10. Technologies and brand-sensitive features

| Apple doc | URL | Applicability | Local extraction | Frontend use |
|---|---|---|---|---|
| AirPlay | https://developer.apple.com/design/human-interface-guidelines/airplay | Apple-only / analogous casting fallback | `13-platform-resources-technologies.md` | Media target selection and connection state |
| Apple Pay | https://developer.apple.com/design/human-interface-guidelines/apple-pay | Apple-only / brand-gated | `13-platform-resources-technologies.md` | Official button/template only when supported; otherwise neutral checkout |
| App Clips | https://developer.apple.com/design/human-interface-guidelines/app-clips | Apple-only / concept transferable | `13-platform-resources-technologies.md` | Extract lightweight task entry; do not mimic App Clip branding |
| Augmented reality | https://developer.apple.com/design/human-interface-guidelines/augmented-reality | Scenario inspiration | `13-platform-resources-technologies.md` | AR placement, safety, reset controls |
| CarPlay | https://developer.apple.com/design/human-interface-guidelines/carplay | Scenario inspiration / Apple-only when targeting CarPlay | `13-platform-resources-technologies.md` | Extract low-distraction constraints; do not use as generic desktop/mobile UI |
| Game Center | https://developer.apple.com/design/human-interface-guidelines/game-center | Apple-only / game-social model | `13-platform-resources-technologies.md` | Extract achievement/profile principles; use neutral game social fallback |
| Generative AI | https://developer.apple.com/design/human-interface-guidelines/generative-ai | Core transferable | `13-platform-resources-technologies.md` | AI transparency, control, correction, trust |
| HealthKit | https://developer.apple.com/design/human-interface-guidelines/healthkit | Apple-only / sensitive-data model | `13-platform-resources-technologies.md` | Extract consent and sensitive-data clarity; use neutral health-data UI |
| HomeKit | https://developer.apple.com/design/human-interface-guidelines/homekit | Apple-only / device-control model | `13-platform-resources-technologies.md` | Extract device state and safety confirmation; use neutral IoT UI |
| iCloud | https://developer.apple.com/design/human-interface-guidelines/icloud | Apple ecosystem / sync model | `13-platform-resources-technologies.md` | Extract sync/offline/conflict handling; use neutral cloud-sync UI |
| In-app purchase | https://developer.apple.com/design/human-interface-guidelines/in-app-purchase | Platform-specific commerce | `13-platform-resources-technologies.md` | Extract purchase clarity and recovery; use target-platform checkout |
| Live Activities | https://developer.apple.com/design/human-interface-guidelines/live-activities | Apple-only / concept transferable | `09-motion-templates.md`, `13-platform-resources-technologies.md` | Extract glanceable ongoing state; do not clone iOS system surface |
| Machine learning | https://developer.apple.com/design/human-interface-guidelines/machine-learning | Core transferable | `13-platform-resources-technologies.md` | Personalization transparency and correction |
| Maps | https://developer.apple.com/design/human-interface-guidelines/maps | Provider-specific / transferable | `13-platform-resources-technologies.md` | Map controls and attribution |
| Siri | https://developer.apple.com/design/human-interface-guidelines/siri | Apple-only / voice model | `13-platform-resources-technologies.md` | Extract action naming and confirmation; use neutral voice/command UI |
| Sign in with Apple | https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple | Apple-only / brand-gated | `13-platform-resources-technologies.md` | Official button only when offering Apple sign-in; otherwise neutral auth |
| SharePlay | https://developer.apple.com/design/human-interface-guidelines/shareplay | Apple-only / collaboration model | `13-platform-resources-technologies.md` | Extract shared-session presence and controls; use neutral collaboration UI |
| Wallet | https://developer.apple.com/design/human-interface-guidelines/wallet | Apple-only / analogous pass fallback | `13-platform-resources-technologies.md` | Add-to-wallet only when supported; otherwise neutral pass/export flow |
| Widgets | https://developer.apple.com/design/human-interface-guidelines/widgets | Concept transferable | `13-platform-resources-technologies.md` | Extract one-job glanceable summaries; use neutral dashboard/widget UI |
| Complications | https://developer.apple.com/design/human-interface-guidelines/complications | Apple-only / scenario inspiration | `13-platform-resources-technologies.md` | Extract glanceable micro-status; do not mimic watchOS complications |
| Watch faces | https://developer.apple.com/design/human-interface-guidelines/watch-faces | Apple-only | `13-platform-resources-technologies.md` | Only relevant for watchOS-specific design |

## 11. Apple Design Resources

| Resource | URL | Applicability | Local extraction | Frontend use |
|---|---|---|---|---|
| Design Resources root | https://developer.apple.com/design/resources/ | Reference / license-sensitive | `13-platform-resources-technologies.md` | Official UI kits, bezels, fonts, symbols, technology assets |
| Apple Fonts | https://developer.apple.com/fonts/ | Apple-only / license-sensitive | `06-fonts.md`, `13-platform-resources-technologies.md` | SF/New York awareness; use system stack or legal fallback |
| SF Symbols | https://developer.apple.com/sf-symbols/ | Apple-only / license-sensitive | `13-platform-resources-technologies.md` | Apple-only symbol assets; use licensed fallback icons off Apple platforms |
| Apple Style Guide | https://support.apple.com/guide/applestyleguide/welcome/web | Core transferable for writing | `11-hig-foundations-patterns.md` | Product terms, writing style, capitalization |
| Liquid Glass overview | https://developer.apple.com/documentation/technologyoverviews/liquid-glass | Platform-informed transferable | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Extract material hierarchy and continuity; provide fallback |
| Adopting Liquid Glass | https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass | Core transferable / Apple-specific APIs inside | `14-liquid-glass-adoption.md` | Migration checklist for controls, navigation, toolbars, modals, layout, search, icons |
| Landmarks: Building an app with Liquid Glass | https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass | SwiftUI sample / pattern extraction | `14-liquid-glass-adoption.md`, `09-motion-templates.md` | Background extension, toolbar grouping, custom badges, app icon layers |
| Landmarks background extension | https://developer.apple.com/documentation/SwiftUI/Landmarks-Applying-a-background-extension-effect | Pattern extraction | `14-liquid-glass-adoption.md` | Extend media under sidebar/inspector; keep overlay content separate |
| Landmarks toolbar glass | https://developer.apple.com/documentation/SwiftUI/Landmarks-Refining-the-system-provided-glass-effect-in-toolbars | Pattern extraction | `14-liquid-glass-adoption.md` | Group toolbar actions with fixed spacers |
| Landmarks custom badges | https://developer.apple.com/documentation/SwiftUI/Landmarks-Displaying-custom-activity-badges | Pattern extraction | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `09-motion-templates.md` | GlassEffectContainer, stable IDs, morphing status cluster |
| SwiftUI glass button styles | https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glass | Platform-informed transferable | `15-liquid-glass-controls.md` | Glass button/control states, fallbacks, accessibility |
| SwiftUI glass prominent button style | https://developer.apple.com/documentation/SwiftUI/PrimitiveButtonStyle/glassProminent | Platform-informed transferable | `15-liquid-glass-controls.md` | Prominent glass actions; use sparingly |
| SwiftUI glassEffectID | https://developer.apple.com/documentation/SwiftUI/View/glassEffectID(_:in:) | Platform-informed transferable | `15-liquid-glass-controls.md`, `09-motion-templates.md` | Stable IDs for grouped morphing controls |
| Applying Liquid Glass to custom views | https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views | Platform-informed transferable | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Glass grouping/morph concepts; do not copy private rendering |
| SwiftUI GlassEffectContainer | https://developer.apple.com/documentation/swiftui/glasseffectcontainer | Platform-informed transferable | `14-liquid-glass-adoption.md`, `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Coordinated glass elements |
| SwiftUI GlassEffectTransition | https://developer.apple.com/documentation/swiftui/glasseffecttransition | Platform-informed transferable | `16-liquid-glass-api-motion-color.md`, `09-motion-templates.md` | Glass entry/exit continuity |
| SwiftUI navigationTransition | https://developer.apple.com/documentation/swiftui/view/navigationtransition%28_%3A%29 | Core transferable concept | `09-motion-templates.md` | Source/destination continuity |

## 12. Crawl maintenance

When updating this map:

1. Check Apple official URLs first; page paths can change.
2. Add only verified URLs returning valid Apple Developer pages.
3. Keep the map as title + URL + local extraction + frontend use.
4. Put implementation rules in category files, not in this map.
5. Avoid copying long Apple text; paraphrase behavior into frontend guidance.
