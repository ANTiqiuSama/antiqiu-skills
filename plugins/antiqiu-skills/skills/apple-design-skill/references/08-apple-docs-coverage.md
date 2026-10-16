# Apple Official Docs Coverage

本文件是 Apple 官方设计文档的覆盖地图。它不替代 [07-motion.md](07-motion.md) 或组件规范，而是告诉 Codex 在不同任务中应该优先读取哪些 Apple 来源、如何把平台规范翻译成 Web / Client / Mobile 的实现决策。

## 1. Source hierarchy

优先级从高到低：

1. **Apple Human Interface Guidelines (HIG)**: 设计原则、平台差异、组件行为、输入方式、无障碍。
2. **Apple Design Resources**: 官方 UI kits、模板、字体、SF Symbols、产品 bezels、技术品牌素材。
3. **Apple Developer Documentation**: SwiftUI / UIKit / AppKit / visionOS 等 API 文档，用于理解系统控件的行为与运动，不直接照搬私有实现。
4. **Apple Style Guide**: 命名、文案、大小写、产品术语和编辑规范。
5. **Apple.com / WWDC design sessions**: 观察产品页叙事、滚动动效、空间节奏、材料表达；只能提炼模式，不复制资产。

当 Apple 官方文档和第三方设计系统冲突时，以 Apple 官方文档为准。第三方来源只用于补足前端工程 token、性能和可访问性实现。

## 1.1 Cross-platform applicability

本 skill 默认只迁移 Apple 设计中的通用原则。Apple 独有平台和技术需要单独归类：

| 类型 | 示例 | 使用方式 |
|---|---|---|
| 可跨平台复用 | 色彩语义、排版层级、布局节奏、反馈、加载、无障碍、按钮/表单/弹层 | 直接转成 Web / Client / Mobile 规则 |
| 平台启发 | iOS touch、iPadOS split view、macOS sidebar/toolbar、Apple.com scroll storytelling | 目标输入/屏幕/任务相似时使用 |
| 场景启发 | watchOS glanceability、tvOS focus grid、visionOS depth comfort、CarPlay low-distraction | 只抽取约束，不复制平台外观 |
| Apple 独有 / 品牌受限 | SF Symbols、Apple Fonts、Product Bezels、Apple Pay、Sign in with Apple、Wallet、Dynamic Island、Live Activities | 仅在平台支持和授权允许时使用；跨平台提供中性 fallback |

## 2. Task-to-doc routing

| 用户任务 | 先读本 skill | 再查 Apple 官方文档 |
|---|---|---|
| Apple 风格页面 / landing page | `00-philosophy.md`, `01-tokens.md`, `03-patterns.md` | HIG: Layout, Color, Typography, Materials; Apple Design Resources |
| 组件库 / design system | `01-tokens.md`, `02-components.md`, `05-tailwind-config.md`, `15-liquid-glass-controls.md` | HIG: Components, Inputs; SF Symbols; Design Resources UI Kits; Liquid Glass controls |
| 动画 / 转场 / 滚动叙事 | `07-motion.md`, `09-motion-templates.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md` | HIG: Motion, Loading, Materials, Accessibility; SwiftUI Liquid Glass docs |
| Liquid Glass / 毛玻璃 | `14-liquid-glass-adoption.md`, `15-liquid-glass-controls.md`, `16-liquid-glass-api-motion-color.md`, `17-liquid-glass-deep-link-map.md`, `01-tokens.md`, `07-motion.md`, `09-motion-templates.md` | HIG: Materials/Color/Layout/Motion/Scroll views/Toolbars/Sidebars/Tab bars; Adopting Liquid Glass; SwiftUI/UIKit/AppKit glass/material docs |
| 中文字体统一 | `06-fonts.md`, `01-tokens.md` | Apple Fonts; HIG Typography; Apple Style Guide |
| 官方文档查找 / URL 路由 | `10-apple-official-docs-map.md` | HIG / Design Resources / Developer Documentation URL map |
| HIG Foundations / Patterns | `11-hig-foundations-patterns.md` | HIG: Accessibility, Color, Layout, Loading, Searching, Privacy, Modality |
| HIG Components / Inputs | `12-hig-components-inputs.md` | HIG: Buttons, Toolbars, Sheets, Lists, Menus, Text fields, Keyboards, Pointers |
| iOS / iPadOS / macOS 适配 | `13-platform-resources-technologies.md`, `03-patterns.md`, `04-accessibility.md` | HIG: Designing for iOS / iPadOS / macOS |
| tvOS / watchOS / visionOS 启发 | `13-platform-resources-technologies.md`, `07-motion.md`, `09-motion-templates.md` | HIG: Designing for tvOS / watchOS / visionOS; Focus, Spatial design |
| 图标 / symbol / 空状态 | `01-tokens.md`, `02-components.md` | HIG: Icons, SF Symbols; SF Symbols app/resources |
| 文案 / 产品命名 / 按钮文字 | `04-accessibility.md` | Apple Style Guide; HIG Writing |
| Apple Pay / Sign in / Wallet / Health 等技术品牌 | `13-platform-resources-technologies.md`, `02-components.md`, `03-patterns.md` | Apple Design Resources: Technologies and brand templates |

## 3. HIG coverage map

### 3.1 Getting started and platform design

| Apple 文档区域 | 前端落地 |
|---|---|
| Designing for iOS | mobile-first navigation, large touch targets, safe areas, sheets, tab bars |
| Designing for iPadOS | adaptive columns, sidebars, split views, pointer/keyboard, drag and drop |
| Designing for macOS | dense controls, menu bars/toolbars, window chrome, keyboard-first workflows |
| Designing for watchOS | glanceable content, minimal text, quick state transitions |
| Designing for tvOS | focus-driven navigation, parallax cards, overscan-safe layout |
| Designing for visionOS | depth, spatial hierarchy, indirect input, motion comfort |

**Rule:** 平台页不是让 Web 伪装成原生系统，而是用来决定密度、导航层级、输入反馈和 motion comfort。

### 3.2 Foundations

| HIG foundation | 本 skill 落点 | 前端检查 |
|---|---|---|
| Accessibility | `04-accessibility.md` | contrast, focus, keyboard, screen reader, reduced motion, reduced transparency |
| Inclusion | `04-accessibility.md` | 文案避免排他，状态不只靠颜色表达 |
| App icons | `01-tokens.md`, `02-components.md` | icon radius、光影和品牌识别不要复制 Apple 图标 |
| Color | `01-tokens.md` | semantic color, dark mode, contrast, blue for action only |
| Layout | `03-patterns.md` | safe area, readable width, adaptive grids, generous whitespace |
| Materials | `01-tokens.md`, `09-motion-templates.md` | glass/translucency 表达层级，不能牺牲可读性 |
| Motion | `07-motion.md`, `09-motion-templates.md` | purpose, continuity, optional motion, no decorative overload |
| Typography | `01-tokens.md`, `06-fonts.md` | optical hierarchy, SF/PingFang fallback, dynamic type-inspired scaling |
| Writing | `04-accessibility.md` | concise labels, action-first buttons, user-centered copy |
| Icons / SF Symbols | `01-tokens.md`, `02-components.md` | symbol scale, stroke weight, filled/outlined consistency |

### 3.3 Patterns

| HIG pattern | 前端模板 |
|---|---|
| Navigation | tab bar, sidebar, toolbar, breadcrumb-like hierarchy, source-to-destination transition |
| Searching | expanding search field, scoped filters, empty results, keyboard submit |
| Loading | skeleton, determinate progress, cancellable long task, content-first reveal |
| Onboarding | short staged reveal, permission timing, skip path |
| Settings | grouped lists, disclosure rows, destructive action separation |
| Notifications | toast/flag/live activity style state, no modal spam |
| Privacy | just-in-time prompts, explicit data purpose, reversible choices |
| Collaboration / sharing | contextual share controls, activity state, permissions clarity |
| Drag and drop | lifted preview, target affordance, drop confirmation |
| Charts / data | stable axes, animated deltas only when they clarify change |

### 3.4 Components

| HIG component family | 本 skill 文件 | Motion template |
|---|---|---|
| Buttons, links, controls | `02-components.md` | press feedback, hover lift, haptic sync |
| Search fields, text fields | `02-components.md` | search field expansion, validation nudge |
| Menus, context menus | `02-components.md` | anchored menu reveal, small cascade |
| Toolbars, tab bars, sidebars | `02-components.md`, `03-patterns.md` | toolbar glass drift, segmented pill, source transition |
| Sheets, popovers, alerts | `02-components.md` | edge sheet, anchored popover, alert dissolve |
| Progress indicators | `02-components.md`, `07-motion.md` | progress morph, skeleton dissolve |
| Lists, tables, outlines | `02-components.md`, `03-patterns.md` | FLIP reorder, grouped insertion, selection transition |
| Cards, collections, grids | `02-components.md`, `03-patterns.md` | card lift, source-to-detail, focus parallax |

### 3.5 Inputs and feedback

| Input | 前端行为 |
|---|---|
| Touch | 44px+ target, immediate pressed state, no hover-only affordance |
| Pointer | subtle hover, focus ring, no large jumps on pointer move |
| Keyboard | visible focus order, Enter/Space activation, Escape dismissal |
| Game controller / remote | focus parallax, large target regions, predictable directional movement |
| Gestures | visible alternatives for hidden gestures; drag shows preview and destination |
| Haptics | sync visual feedback timing with haptic event when native shell supports it |
| Voice / accessibility input | no motion-only or color-only state; labels and roles are complete |

## 4. Apple Design Resources coverage

Use Apple Design Resources when the user asks for fidelity, platform-specific measurements, official templates, or brand integrations.

| Resource group | Use for |
|---|---|
| iOS & iPadOS UI Kits | native-like mobile layouts, status/navigation/tab bars, controls |
| macOS UI Kits | desktop density, toolbar/window/sidebar conventions |
| tvOS UI Kits | focus and media-card layout |
| watchOS UI Kits | glanceable micro-layouts |
| visionOS UI Kits | depth, scale, glass, spatial surfaces |
| Product Bezels | screenshots and marketing mocks; respect usage terms |
| Fonts | SF Pro, SF Compact, SF Mono, New York; do not redistribute Apple fonts without permission |
| SF Symbols | symbol naming/weight/scale/reference; implement with licensed alternatives on Web if needed |
| Technology templates | Apple Pay, Wallet, Sign in with Apple, Health, HomeKit, AirPlay, Siri/App Shortcuts, Live Activities |

## 5. Developer Documentation coverage

Developer docs are useful when a frontend needs to mimic native behavior without becoming platform-specific.

| Apple API / topic | Transferable behavior |
|---|---|
| SwiftUI `glassEffect` / `GlassEffectContainer` / `GlassEffectTransition` | glass elements can group, morph, and transition as a material system; see `14-liquid-glass-adoption.md` for Landmarks extraction and `16-liquid-glass-api-motion-color.md` for code recipes |
| SwiftUI `navigationTransition` | navigation can preserve source/destination continuity |
| SwiftUI matched geometry concepts | cards, thumbnails, and controls can animate across layout contexts |
| UIKit/AppKit presentation controllers | sheets, popovers, menus, and modals originate from context |
| ScrollView / safe area APIs | scroll-linked chrome changes and safe-area-aware layout |
| Focus engine / tvOS docs | focus movement should be spatially predictable |
| visionOS volumes/windows | depth cues and motion comfort matter more than spectacle |

## 6. Coverage checklist

Before delivering an Apple-style frontend, check:

- [ ] Which Apple platform is the primary reference: iOS, iPadOS, macOS, watchOS, tvOS, visionOS, or Apple.com marketing?
- [ ] Did the design use semantic tokens instead of hard-coded decorative colors?
- [ ] Is motion tied to feedback, continuity, hierarchy, or loading clarity?
- [ ] Are motion templates selected from `09-motion-templates.md` and tokenized by `07-motion.md`?
- [ ] Are Liquid Glass effects used as hierarchy/material, not generic blur decoration?
- [ ] Does reduced motion still preserve information and task flow?
- [ ] Does reduced transparency / high contrast keep text readable?
- [ ] Are icons/SF Symbols proportions and weights consistent?
- [ ] Does platform density match the target device and input mode?
- [ ] Are official brand templates used for Apple Pay, Sign in with Apple, Wallet, Health, etc.?
- [ ] Is any Apple asset, font, icon, product image, or screenshot used only within its allowed license/usage terms?

## 7. Official links

- HIG root: https://developer.apple.com/design/human-interface-guidelines
- HIG Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- HIG Materials: https://developer.apple.com/design/human-interface-guidelines/materials
- HIG Loading: https://developer.apple.com/design/human-interface-guidelines/loading
- HIG Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- HIG Color: https://developer.apple.com/design/human-interface-guidelines/color
- HIG Typography: https://developer.apple.com/design/human-interface-guidelines/typography
- HIG Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- HIG SF Symbols: https://developer.apple.com/design/human-interface-guidelines/sf-symbols
- Apple Design Resources: https://developer.apple.com/design/resources/
- SF Symbols: https://developer.apple.com/sf-symbols/
- Apple Fonts: https://developer.apple.com/fonts/
- Apple Style Guide: https://support.apple.com/guide/applestyleguide/welcome/web
- Liquid Glass overview: https://developer.apple.com/documentation/technologyoverviews/liquid-glass
- Adopting Liquid Glass: https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass
- Landmarks Liquid Glass sample: https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass
- Applying Liquid Glass to custom views: https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views
- HIG Materials Liquid Glass: https://developer.apple.com/cn/design/human-interface-guidelines/materials#Liquid-Glass
- HIG Color Liquid Glass: https://developer.apple.com/design/human-interface-guidelines/color#Liquid-Glass-color
- HIG Scroll views scroll-edge effects: https://developer.apple.com/design/human-interface-guidelines/scroll-views
- SwiftUI GlassEffectContainer: https://developer.apple.com/documentation/swiftui/glasseffectcontainer
- SwiftUI GlassEffectTransition: https://developer.apple.com/documentation/swiftui/glasseffecttransition
- SwiftUI backgroundExtensionEffect: https://developer.apple.com/documentation/SwiftUI/View/backgroundExtensionEffect()
- SwiftUI scrollEdgeEffectStyle: https://developer.apple.com/documentation/SwiftUI/View/scrollEdgeEffectStyle(_:for:)
- UIKit UIGlassEffect: https://developer.apple.com/documentation/UIKit/UIGlassEffect
- AppKit NSGlassEffectView: https://developer.apple.com/documentation/AppKit/NSGlassEffectView
- SwiftUI navigationTransition: https://developer.apple.com/documentation/swiftui/view/navigationtransition%28_%3A%29
- UIKit UIBlurEffect: https://developer.apple.com/documentation/UIKit/UIBlurEffect
- UIKit UIVibrancyEffect: https://developer.apple.com/documentation/UIKit/UIVibrancyEffect
- AppKit NSVisualEffectView.BlendingMode: https://developer.apple.com/documentation/AppKit/NSVisualEffectView/BlendingMode-swift.enum
- SwiftUI Material: https://developer.apple.com/documentation/SwiftUI/Material
