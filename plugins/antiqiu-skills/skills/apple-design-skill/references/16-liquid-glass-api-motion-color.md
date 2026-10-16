# Liquid Glass API, Motion, Color, and Code Recipes

Use this reference when a task needs Liquid Glass implementation detail, animation/transition design, color behavior, Dark Mode handling, UIKit/AppKit material fallbacks, or concrete sample code. Read `14-liquid-glass-adoption.md` for adoption strategy and `15-liquid-glass-controls.md` for control-level recipes first. Read `17-liquid-glass-deep-link-map.md` when you need to open official related links or classify platform-specific APIs.

## 1. Source coverage

### Explicit source set

| Source | Category | Local use |
|---|---|---|
| Adopting Liquid Glass | Adoption, navigation, controls, windows, search, platform checks | Migration audit and implementation checklist |
| HIG Materials: Liquid Glass | Material hierarchy | Functional layer, regular/clear choice, standard material boundary |
| Applying Liquid Glass to custom views | SwiftUI API and motion | Custom shapes, containers, unions, morphs, transitions, performance |
| `Glass.regular` / `Glass.clear` | Variant choice | Readable default vs rich-media overlay |
| HIG Color: Liquid Glass color | Color and contrast | Accent placement, monochrome labels, light/dark/high-contrast variants |
| HIG Color: System colors | Semantic color | Prefer dynamic system colors; define custom variants for light/dark/high contrast |
| UIKit native menu button route | UIKit API / system menu transition | Prefer `UIButtonConfiguration.glassButtonConfiguration` + `UIButton.menu` + `showsMenuAsPrimaryAction` + `UIMenu`/`UIAction` when the interaction is a menu |
| SwiftUI `Material` | Standard material fallback | Content-layer blur/vibrancy, not Liquid Glass |
| UIKit `UIBlurEffect` / `UIVibrancyEffect` | UIKit standard material fallback | Blur behind `UIVisualEffectView`; vibrant foreground labels/icons |
| AppKit `NSVisualEffectView.BlendingMode` | macOS standard material fallback | Blend behind window or within current window |
| Liquid Glass deep related-link crawl | HIG and API link routing | Use `17-liquid-glass-deep-link-map.md` to choose the next official page and separate Apple-only APIs from transferable principles |

### Additional HIG pages with Liquid Glass implications

| HIG page | What it adds | Cross-platform rule |
|---|---|---|
| Layout | Content should extend to edges; controls float above content; use background extension and scroll-edge separation | Build a content layer and a functional layer; do not put important content under translucent controls |
| Motion | Liquid Glass reacts more strongly to direct touch and more subtly to pointer/trackpad | Tune motion by input type; keep motion optional and cancelable |
| Scroll views / Status bars | Scroll-edge effects protect controls and status bars over scrolling content | Use one contrast-preserving edge treatment per scroll region |
| Toolbars / Navigation bars | Reduce custom toolbar backgrounds, group actions, use symbols, use one prominent action | Let content influence toolbar appearance; group related controls into clear clusters |
| Tab bars | Tab bars float over content and can minimize while scrolling | Use scroll-minimized bottom bars only when navigation remains recoverable |
| Sidebars | Visually rich content can extend beneath sidebars through background extension or horizontal scrolling | Extend media/background only; keep readable content and controls outside sidebar glass |
| Buttons | Avoid label/background color collisions; toolbar buttons can adopt Liquid Glass | Primary action gets one prominent treatment; destructive actions need semantic clarity |
| App icons | Layered icons receive Liquid Glass-like highlights/refraction/translucency | Use layered source artwork; let platform export apply final effects |
| Widgets | Clear/tinted appearances and glass texture need contrast-safe foreground groups | Treat widgets as platform-specific; keep primary content legible in monochrome/tinted modes |
| Images | Feathered glass behind spatial-photo text is visionOS-specific | Use only as a spatial-photo readability technique, not as generic Web blur |

Crawl note: HIG pages such as Game controls and Touchscreen gestures can surface Liquid Glass through shared page metadata or overview-card imagery, but their primary guidance is input design rather than Liquid Glass. Route those pages through `12-hig-components-inputs.md`, not this Liquid Glass reference, unless the task explicitly concerns glassy game/touch overlays.

## 2. Design rule taxonomy

### Material hierarchy

- Liquid Glass is the functional layer for controls and navigation. Use it for bars, sidebars, floating toolbars, badges, media controls, compact status, and contextual actions.
- Standard materials are the content-structure layer. Use them for panels, backgrounds, grouped lists, dense text, and app surfaces beneath glass.
- Clear glass is a special case for visually rich media. If the background is bright, add a dimming layer; Apple gives 35% dark opacity as a useful reference.
- Regular glass is the default for text-heavy, control-heavy, or unpredictable backgrounds.
- Never use blur as decoration. The effect must improve hierarchy, continuity, or readability.

### Motion and transition

- Treat Liquid Glass motion as material continuity: shapes can merge, split, materialize, or morph between related controls.
- Use direct manipulation for sliders/toggles and pressed controls. The active part can become glass-like while the rest of the form remains standard.
- Prefer `GlassEffectContainer` for multiple glass shapes so the system can optimize rendering and coordinate shape interaction.
- Use stable IDs for morphing shapes. A morph without stable identity reads as a random dissolve.
- For native menus on iOS/iPadOS 26+, do not re-create the bubble-to-menu expansion with custom scale, spring, or blur timing. Use a system `UIButton` with a `UIMenu`; UIKit owns the menu presentation, optical thickening, refraction/lensing, shadow, accessibility, and dismissal behavior.
- Use matched geometry when elements are close enough to feel spatially related; use materialize/dissolve for elements that appear from unrelated positions.
- Do not animate blur continuously. Animate position, scale, opacity, clip, radius, and state changes; let platform material rendering update discretely.
- Respect reduced motion: replace morphs, parallax, and scroll-linked stretch with fade or instant layout changes.
- Tune feedback by input. Touch can use stronger compression/lift because the finger supplies tactile context; pointer/trackpad should stay subtler.

### Color and Dark Mode

- Liquid Glass has no fixed color by default; it reflects the content behind it.
- Use color sparingly on the material or foreground. For primary actions, tint the material/background, not just the icon or label.
- Do not tint every item in a toolbar or tab bar. A single prominent action is usually the maximum.
- Over colorful content, use monochrome toolbar/tab labels unless the accent has clear contrast against likely backgrounds.
- For custom colors, provide light, dark, and increased-contrast variants. A single fixed color can fail when glass adapts.
- Prefer semantic/system colors for text, fills, separators, and states. They adapt to appearance, contrast, and vibrancy contexts.
- In Dark Mode, avoid pure white glowing content and pure black glass. Use elevated semantic surfaces and test with Reduce Transparency plus Increase Contrast.
- visionOS glass is not Dark Mode; it adapts to surroundings. Treat visionOS-specific glass as Apple-only unless the target is spatial UI.

### Layout and scroll edge

- Content may extend under the glass layer only when it is background/media. Do not place tappable controls or essential text behind translucent bars.
- Use scroll-edge effects when scrolling content passes behind controls, pinned headers, status bars, or bars with text outside glass controls.
- Prefer automatic scroll-edge styling. Use hard for dense controls/text and soft only after contrast testing.
- Apply one edge effect per scroll region; split panes may each own one aligned edge effect.
- Use background extension for sidebars/inspectors when media should feel edge-to-edge without actually moving text under the panel.

### Platform scope

| Platform/surface | Transferability | Rule |
|---|---|---|
| Web / enterprise UI | Transfer principles only | Use readable translucent controls, solid fallbacks, and CSS reduced-motion/transparency handling |
| SwiftUI apps | Direct API use | Prefer system controls, `glassEffect`, `GlassEffectContainer`, button styles, scroll-edge APIs |
| UIKit apps | Direct API use where available | Prefer standard bars/buttons/menus; use `UIGlassEffect`, glass button configurations, and `UIMenu` before custom rendering |
| AppKit apps | Direct API use where available | Prefer `NSGlassEffectView` for glass and `NSVisualEffectView` for standard materials |
| tvOS | Focus-specific | Liquid Glass appears on focus/navigation; avoid copying TV focus UI to regular Web |
| widgets/icons | Apple-specific | Use as platform guidance only; do not generalize widget/icon rendering to app content |
| visionOS | Mostly Apple-specific | Extract comfort/readability rules; avoid fake spatial OS chrome in normal apps |

## 3. API mapping

| Need | SwiftUI | UIKit | AppKit | Web/client translation |
|---|---|---|---|---|
| Standard glass button | `.buttonStyle(.glass)` / `GlassButtonStyle` | `UIButton.Configuration.glass()` | `NSButton.BezelStyle.glass` | Rounded translucent button with solid fallback |
| Prominent primary glass | `.buttonStyle(.glassProminent)` / `GlassProminentButtonStyle` | `.prominentGlass()` / `.prominentClearGlass()` | Use platform prominent/control style | One tinted primary surface per local group |
| Menu from a glass trigger | Prefer `Menu`/system control before custom glass | `UIButtonConfiguration.glassButtonConfiguration`, `UIButton.menu`, `showsMenuAsPrimaryAction`, `UIMenu`, `UIAction` | Native menu where available | Native menu bridge first; fallback to anchored command menu with semantic parity |
| Custom glass shape | `.glassEffect(_:in:)`; default shape is `DefaultGlassEffectShape` | `UIGlassEffect` | `NSGlassEffectView` | CSS backdrop-filter surface with contrast-safe fill; pill/capsule default |
| Multiple glass shapes | `GlassEffectContainer(spacing:)` | Prefer standard controls; custom grouping if needed | Prefer standard controls; custom grouping if needed | One grouped layer; animate transforms and radius |
| Resting union | `glassEffectUnion(id:namespace:)` | N/A | N/A | Shared wrapper/background spanning related items |
| Transition identity | `glassEffectID(_:in:)` | N/A | N/A | Stable IDs for shared-element animation |
| Add/remove transition | `glassEffectTransition(_:)` | N/A | N/A | Matched-geometry or materialize/fade pattern |
| Content under sidebar | `backgroundExtensionEffect()` | `UIBackgroundExtensionView` | `NSBackgroundExtensionView` | Mirrored/blurred media strip behind panel |
| Scroll-edge readability | `scrollEdgeEffectStyle` with a safe-area bar/inset | `UIScrollEdgeEffect` APIs | `NSScrollEdgeEffectStyle` | Sticky scrim/blur edge tied to scroll region |
| Content-layer material | `.regularMaterial`, `.thinMaterial` | `UIBlurEffect` + `UIVibrancyEffect` | `NSVisualEffectView` | Standard translucent panel, not Liquid Glass |

## 4. SwiftUI examples

These examples are implementation sketches. Prefer system controls first; custom glass should be sparse.

### Regular glass control

```swift
struct GlassToolbarButton: View {
    var body: some View {
        Button {
            // perform action
        } label: {
            Label("Share", systemImage: "square.and.arrow.up")
                .labelStyle(.iconOnly)
        }
        .buttonStyle(.glass)
        .accessibilityLabel("Share")
    }
}
```

Use this for normal toolbar actions. Do not tint every button in the toolbar.

### Clear glass over bright media

```swift
struct MediaOverlayButton: View {
    var body: some View {
        Label("Flag", systemImage: "flag.fill")
            .font(.headline)
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
            .background(.black.opacity(0.35), in: Capsule())
            .glassEffect(.clear, in: Capsule())
            .accessibilityLabel("Flag media")
    }
}
```

Use clear glass only when rich content should remain visible. Add the dimming layer when bright content can sit behind the control.

### Tinted primary action

```swift
struct PrimaryDoneButton: View {
    var body: some View {
        Button("Done") {
            // commit changes
        }
        .buttonStyle(.glassProminent)
        .tint(.accentColor)
    }
}
```

Use one prominent action per local toolbar or modal region. Destructive actions should use destructive semantics, not a beautiful tinted glass style.

### Custom shape and modifier order

```swift
struct GlassStatusChip: View {
    let count: Int

    var body: some View {
        Label("\(count)", systemImage: "bell.fill")
            .font(.callout.weight(.semibold))
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .foregroundStyle(.primary)
            .glassEffect(.regular.interactive(),
                         in: .rect(cornerRadius: 18, style: .continuous))
    }
}
```

Apply appearance-defining modifiers before `glassEffect` so the final padded shape is what the material captures.

### Container morph

```swift
struct MorphingToolCluster: View {
    @State private var expanded = false
    @Namespace private var glassNamespace

    var body: some View {
        VStack(spacing: 16) {
            GlassEffectContainer(spacing: 28) {
                HStack(spacing: 12) {
                    Image(systemName: "pencil")
                        .frame(width: 44, height: 44)
                        .glassEffect()
                        .glassEffectID("edit", in: glassNamespace)

                    if expanded {
                        Image(systemName: "eraser")
                            .frame(width: 44, height: 44)
                            .glassEffect()
                            .glassEffectID("erase", in: glassNamespace)
                            .glassEffectTransition(.matchedGeometry)
                    }
                }
            }

            Button(expanded ? "Collapse" : "Expand") {
                withAnimation(.snappy(duration: 0.28)) {
                    expanded.toggle()
                }
            }
            .buttonStyle(.glass)
        }
    }
}
```

Use a morph only when the two states are semantically related and spatially close. Otherwise use materialize/fade.

### Unioned resting group

```swift
struct WeatherGlassGroup: View {
    @Namespace private var groupNamespace
    private let symbols = ["cloud.rain.fill", "bolt.fill", "wind"]

    var body: some View {
        GlassEffectContainer(spacing: 18) {
            HStack(spacing: 8) {
                ForEach(symbols, id: \.self) { symbol in
                    Image(systemName: symbol)
                        .frame(width: 36, height: 36)
                        .glassEffect()
                        .glassEffectUnion(id: "weather-tools", namespace: groupNamespace)
                }
            }
        }
    }
}
```

Use a union when several small controls should read as one resting material shape.

### Scroll-edge custom bar

```swift
struct ScrollEdgeExample: View {
    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 18) {
                ForEach(0..<40) { index in
                    Text("Row \(index)")
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                }
            }
        }
        .scrollEdgeEffectStyle(.automatic, for: .top)
        .safeAreaInset(edge: .top) {
            HStack {
                Text("Library")
                    .font(.headline)
                Spacer()
                Button("Filter") { }
                    .buttonStyle(.glass)
            }
            .padding(.horizontal)
        }
    }
}
```

Use this when custom top content floats above a scroll view. Avoid decorative edge effects when no content scrolls beneath the control layer.

### Background extension beneath sidebar

```swift
struct SidebarExtensionExample: View {
    @State private var inspectorOpen = true

    var body: some View {
        NavigationSplitView {
            List(["Mount Fuji", "Rainier", "Denali"], id: \.self) { Text($0) }
        } detail: {
            HeroImage()
                .backgroundExtensionEffect()
                .overlay(alignment: .bottomLeading) {
                    Text("Mount Fuji")
                        .font(.largeTitle.bold())
                        .padding()
                }
        }
        .inspector(isPresented: $inspectorOpen) {
            Text("Metadata")
                .padding()
        }
    }
}
```

Apply the extension to media/background, not to readable foreground text.

### Semantic color and Dark Mode

```swift
struct AdaptiveGlassLabel: View {
    @Environment(\.colorScheme) private var colorScheme
    @Environment(\.accessibilityContrast) private var contrast

    var body: some View {
        Label("Synced", systemImage: "checkmark.icloud.fill")
            .font(.callout.weight(.semibold))
            .foregroundStyle(.primary)
            .tint(.accentColor)
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
            .glassEffect(.regular, in: Capsule())
            .overlay {
                if contrast == .increased {
                    Capsule().stroke(.primary.opacity(colorScheme == .dark ? 0.7 : 0.45), lineWidth: 1)
                }
            }
    }
}
```

Use semantic foreground styles and system accent colors before inventing fixed glass colors. Add explicit contrast help only when the system setting or product surface requires it.

## 5. UIKit and AppKit examples

### UIKit glass button

```swift
let doneButton = UIButton(configuration: .prominentGlass())
doneButton.setTitle("Done", for: .normal)
doneButton.addAction(UIAction { _ in
    // commit changes
}, for: .primaryActionTriggered)
```

Use `glass()`, `prominentGlass()`, `clearGlass()`, or `prominentClearGlass()` for buttons instead of hand-building button blur. On tvOS, these styles apply glass even outside focus, so test focus and unfocused states.

### UIKit native menu from a glass trigger

Use this route when a glass button opens a menu, command list, picker, or nested action set. It matches the official model more closely than a custom React Native/Web animation because UIKit presents the menu from the button and owns the Liquid Glass expansion.

Control choice:

- Use `glassButtonConfiguration` for icon-only or compact floating menu triggers.
- Use `plainButtonConfiguration` with the system popup indicator for title/picker triggers that should stay visually quiet until the menu opens.
- Use SF Symbols at the surrounding control weight; `regular` is usually the right default for compact menu triggers.
- Assign `menu` and `showsMenuAsPrimaryAction` in both cases so the trigger, menu, accessibility behavior, and dismissal remain system-owned.

```objc
UIButtonConfiguration *configuration = nil;
if (@available(iOS 26.0, *)) {
  configuration = [UIButtonConfiguration glassButtonConfiguration];
} else {
  configuration = [UIButtonConfiguration borderedButtonConfiguration];
}

configuration.cornerStyle = UIButtonConfigurationCornerStyleCapsule;
configuration.image = [UIImage systemImageNamed:@"plus"];
configuration.preferredSymbolConfigurationForImage =
  [UIImageSymbolConfiguration configurationWithPointSize:17
                                                  weight:UIImageSymbolWeightRegular];

UIButton *button = [UIButton buttonWithConfiguration:configuration primaryAction:nil];
UIAction *newItem = [UIAction actionWithTitle:@"New"
                                        image:[UIImage systemImageNamed:@"doc.badge.plus"]
                                   identifier:nil
                                      handler:^(__kindof UIAction *action) {
  // Handle selection.
}];
button.menu = [UIMenu menuWithChildren:@[newItem]];
button.showsMenuAsPrimaryAction = YES;
```

Menu semantics to preserve when bridging from React Native, Flutter, or another client layer:

- Convert hierarchical data to `UIMenu` for submenus and `UIAction` for leaf actions.
- Use SF Symbols/system images when available; keep icon weight aligned with surrounding button symbols.
- Map selected items to the menu element "on" state, disabled items to disabled attributes, and destructive operations to destructive attributes.
- Use inline menu sections and single-selection options when the structure is a grouped command set rather than a deeper navigation step.
- On iOS 26+ prefer this native route for menu triggers; on iOS 25 and below, Android, and Web, use a semantic anchored menu fallback with reduced-motion and reduced-transparency handling. Do not claim the fallback is a full Liquid Glass material.

Use SwiftUI `GlassEffectContainer`, `glassEffectID`, and custom matched geometry only for custom glass view groups that cannot be represented by a system menu or standard control.

### UIKit standard material fallback

```swift
let blur = UIBlurEffect(style: .systemMaterial)
let backgroundView = UIVisualEffectView(effect: blur)
backgroundView.layer.cornerCurve = .continuous
backgroundView.layer.cornerRadius = 18
backgroundView.clipsToBounds = true

let vibrancy = UIVibrancyEffect(blurEffect: blur, style: .label)
let contentView = UIVisualEffectView(effect: vibrancy)
backgroundView.contentView.addSubview(contentView)
```

Use this for standard material/content-layer surfaces or older OS fallbacks. Content added to the visual effect view content view is not blurred by the blur effect; vibrancy sits above blur to keep labels/icons readable.

### AppKit standard material fallback

```swift
let effectView = NSVisualEffectView()
effectView.material = .sidebar
effectView.blendingMode = .withinWindow
effectView.state = .active
effectView.wantsLayer = true
effectView.layer?.cornerRadius = 18
```

Use `.withinWindow` when the material should blend with content behind it inside the same window. Use `.behindWindow` only when the design intentionally samples desktop/other-window content, which is rarely appropriate for cross-platform apps.

## 6. Web/client examples

### CSS glass with accessibility fallbacks

```css
.lg-surface {
  --lg-bg: color-mix(in srgb, Canvas 70%, transparent);
  --lg-border: color-mix(in srgb, CanvasText 18%, transparent);
  color: CanvasText;
  background: var(--lg-bg);
  border: 1px solid var(--lg-border);
  border-radius: 999px;
  box-shadow: 0 16px 44px rgb(0 0 0 / 18%);
  -webkit-backdrop-filter: blur(18px) saturate(1.35);
  backdrop-filter: blur(18px) saturate(1.35);
  transition:
    transform 140ms ease,
    background-color 180ms ease,
    box-shadow 180ms ease;
}

.lg-surface:hover {
  transform: translateY(-1px);
}

.lg-surface:active {
  transform: scale(.985);
}

.lg-surface:focus-visible {
  outline: 2px solid Highlight;
  outline-offset: 3px;
}

@media (prefers-color-scheme: dark) {
  .lg-surface {
    --lg-bg: rgb(28 28 30 / 62%);
    --lg-border: rgb(255 255 255 / 20%);
    box-shadow: 0 18px 48px rgb(0 0 0 / 42%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .lg-surface {
    transition: none;
  }
  .lg-surface:hover,
  .lg-surface:active {
    transform: none;
  }
}

@media (prefers-contrast: more) {
  .lg-surface {
    background: Canvas;
    border-color: CanvasText;
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}
```

### Scroll-edge scrim for Web

```css
.scroll-shell {
  position: relative;
  overflow: auto;
}

.scroll-shell::before {
  content: "";
  position: sticky;
  top: 0;
  z-index: 2;
  display: block;
  height: 56px;
  margin-bottom: -56px;
  pointer-events: none;
  background: linear-gradient(
    to bottom,
    color-mix(in srgb, Canvas 88%, transparent),
    color-mix(in srgb, Canvas 0%, transparent)
  );
  -webkit-backdrop-filter: blur(14px);
  backdrop-filter: blur(14px);
}
```

Use this only when controls or status text sit above the scroll region. Remove it if it becomes visual decoration.

### Matched glass group with reduced-motion fallback

```css
.lg-cluster {
  display: inline-grid;
  grid-auto-flow: column;
  gap: 8px;
  padding: 6px;
  border-radius: 24px;
}

.lg-item {
  inline-size: 44px;
  block-size: 44px;
  border-radius: 18px;
  transition:
    transform 220ms cubic-bezier(.2, .8, .2, 1),
    border-radius 220ms cubic-bezier(.2, .8, .2, 1),
    opacity 180ms ease;
}

.lg-item[data-active="true"] {
  transform: translateX(4px) scale(1.04);
}

@media (prefers-reduced-motion: reduce) {
  .lg-item {
    transition: opacity 120ms ease;
    transform: none;
  }
}
```

For complex Web morphs, use shared-layout animation only if the source and destination represent the same object or control group.

## 7. QA checklist

- [ ] Is every glass surface in the functional layer, not the content layer?
- [ ] Did regular/clear variant choice follow background complexity and text density?
- [ ] Is color limited to primary actions or status, with semantic light/dark/high-contrast variants?
- [ ] Do toolbar/tab/sidebar labels remain readable over the resting content position?
- [ ] Does Dark Mode use elevated semantic surfaces rather than inverted light colors?
- [ ] Does Reduce Transparency produce an opaque fallback?
- [ ] Does Reduce Motion remove morph, parallax, scroll-linked stretch, and blur movement?
- [ ] Are multiple glass shapes grouped in one container or wrapper for performance and visual continuity?
- [ ] Does scroll-edge treatment exist only where scrolling content passes behind controls?
- [ ] Are Apple-only surfaces such as widgets, icons, visionOS glass, and spatial-photo glass labeled as platform-specific?

## Source links

- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass
- https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
- https://developer.apple.com/documentation/SwiftUI/Glass/regular
- https://developer.apple.com/documentation/SwiftUI/Glass/clear
- https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color
- https://developer.apple.com/design/human-interface-guidelines/color#System-colors
- https://developer.apple.com/design/human-interface-guidelines/dark-mode
- https://developer.apple.com/documentation/UIKit/UIBlurEffect
- https://developer.apple.com/documentation/UIKit/UIVibrancyEffect
- https://developer.apple.com/documentation/AppKit/NSVisualEffectView/BlendingMode-swift.enum
- https://developer.apple.com/documentation/SwiftUI/Material
- https://developer.apple.com/documentation/swiftui/view-styles
- https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:)
- https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectUnion(id:namespace:)
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectID(_:in:)
- https://developer.apple.com/documentation/SwiftUI/GlassEffectTransition
- https://developer.apple.com/documentation/SwiftUI/View/glassEffectTransition(_:)
- https://developer.apple.com/documentation/swiftui/glassbuttonstyle
- https://developer.apple.com/documentation/swiftui/glassprominentbuttonstyle
- https://developer.apple.com/documentation/swiftui/defaultglasseffectshape
- https://developer.apple.com/documentation/UIKit/UIGlassEffect
- https://developer.apple.com/documentation/UIKit/UIButtonConfiguration/glassButtonConfiguration
- https://developer.apple.com/documentation/UIKit/UIButton/menu
- https://developer.apple.com/documentation/UIKit/UIButton/showsMenuAsPrimaryAction
- https://developer.apple.com/documentation/UIKit/UIMenu
- https://developer.apple.com/documentation/UIKit/UIAction
- https://developer.apple.com/documentation/UIKit/UIMenu/Options-swift.struct/displayInline
- https://developer.apple.com/documentation/UIKit/UIMenu/Options-swift.struct/singleSelection
- https://developer.apple.com/documentation/UIKit/UIMenuElementAttributes/destructive
- https://developer.apple.com/documentation/UIKit/UIMenuElementAttributes/disabled
- https://developer.apple.com/documentation/UIKit/UIMenuElementState/on
- https://developer.apple.com/documentation/AppKit/NSGlassEffectView
- https://developer.apple.com/videos/play/wwdc2025/219/
- https://developer.apple.com/videos/play/wwdc2025/243/
- https://developer.apple.com/design/human-interface-guidelines/layout
- https://developer.apple.com/design/human-interface-guidelines/motion
- https://developer.apple.com/design/human-interface-guidelines/scroll-views
- https://developer.apple.com/design/human-interface-guidelines/toolbars
- https://developer.apple.com/design/human-interface-guidelines/navigation-bars
- https://developer.apple.com/design/human-interface-guidelines/sidebars
- https://developer.apple.com/design/human-interface-guidelines/tab-bars
- https://developer.apple.com/design/human-interface-guidelines/buttons
- https://developer.apple.com/design/human-interface-guidelines/status-bars
- https://developer.apple.com/design/human-interface-guidelines/app-icons
- https://developer.apple.com/design/human-interface-guidelines/widgets
- https://developer.apple.com/design/human-interface-guidelines/images
