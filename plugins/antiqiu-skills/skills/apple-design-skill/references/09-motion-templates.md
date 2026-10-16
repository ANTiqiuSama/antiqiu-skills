# Apple Motion Templates

本文件是 Apple 风格前端动画模板库。它把 Apple HIG、Apple.com 产品叙事、Liquid Glass、SwiftUI / UIKit / AppKit 行为转成 Web / Client / Mobile 可落地模式。

不要把这些模板理解为 Apple 官方提供的 CSS 动画。它们是前端实现模板：设计目标来自 Apple 官方文档，工程参数来自 [07-motion.md](07-motion.md)。

## 1. How to use

每次实现动画前先选择一个模板，再套用 motion token：

1. 先判断动画目的：feedback、continuity、hierarchy、loading、storytelling。
2. 从本文件选择 1 个主模板，最多 1 个辅助模板。
3. 使用 [07-motion.md](07-motion.md) 中的 duration/easing/property。
4. 写出 reduced motion alternative。
5. 只动画 `opacity` 和 `transform`；`filter/backdrop-filter/blur` 只做小范围、短时、可关闭效果。

## Cross-platform guardrails

本模板库服务跨平台前端。Apple 独有模板要先判断是否真的适用：

| Template family | Applicability | Rule |
|---|---|---|
| Press, hover, sheet, modal, popover, search, loading, list reorder | Core transferable | 可直接用于 Web / Client / Mobile，按目标平台调整密度和输入方式 |
| Apple.com scroll storytelling, Liquid Glass-inspired material | Platform-informed transferable | 可用于营销页/展示页，但必须有 reduced motion 和 reduced transparency fallback |
| tvOS focus parallax | Scenario inspiration | 仅用于 TV、kiosk、remote、gamepad 或 keyboard focus grid，不用于普通鼠标/触控页面 |
| visionOS depth reveal | Scenario inspiration / Apple-only when targeting visionOS | 只抽取 depth comfort 和层级原则，不复刻 visionOS 系统窗口或 gaze UI |
| watchOS glance transition | Scenario inspiration | 只用于小组件/状态卡片，不把 watch UI 搬到常规 Web/app |
| Dynamic Island / Live Activity | Apple-only / concept transferable | 只抽取“持续任务的紧凑状态”原则；跨平台用 status chip/task bar，不克隆系统胶囊 |

Liquid Glass 相关动画先读 `14-liquid-glass-adoption.md`；如果是按钮、工具栏、分段控件、开关、滑块、搜索、badge 或 popover/sheet 控件，再读 `15-liquid-glass-controls.md`；如果需要 SwiftUI/UIKit/AppKit/Web 示例代码、`GlassEffectContainer` morph、scroll-edge、色彩或 Dark Mode，读取 `16-liquid-glass-api-motion-color.md`，最后选择本文件第 8 节模板。

## 2. Template selector

| 需求 | 首选模板 |
|---|---|
| 按钮点击、控件确认 | Press feedback, Haptic sync |
| hover / pointer / keyboard focus | Pointer lift, Focus parallax |
| tab / segmented control | Segmented pill glide, Tab content crossfade |
| 菜单、popover、tooltip | Anchor reveal, Menu cascade |
| sheet / modal / alert | Edge sheet, Modal dissolve-scale, Alert dissolve |
| 页面跳转、卡片详情 | Source-to-destination, Card-to-detail morph |
| 列表排序、过滤、插入 | FLIP reorder, Group insertion |
| 搜索、筛选 | Search expansion, Results crossfade |
| loading | Skeleton dissolve, Progress morph |
| Apple.com 产品页 | Hero reveal, Scroll scrub, Foreground/background speed split |
| Liquid Glass | Glass materialize, Glass merge/split, Toolbar glass drift |
| tvOS / remote focus | Focus parallax; only for TV/kiosk/remote/focus-grid contexts |
| visionOS / spatial surface | Depth reveal; use as depth-comfort inspiration, not OS chrome |
| Dynamic Island / Live Activity | Pill expand / live activity morph; cross-platform fallback is status chip/task bar |

## 3. Core feedback templates

### 3.1 Press feedback

Use for: buttons, icon buttons, list rows, cards with immediate activation.

Motion:
- down: `scale(0.98)` or `translateY(1px)` for 50-100ms
- up: return to `scale(1)` for 100-150ms
- optional: background or opacity change for tactile confirmation

Reduced motion:
- no scale; keep pressed background/outline for 100ms

Rules:
- Never delay the action until the press animation completes.
- Avoid bounce on destructive actions; make them calm and clear.

### 3.2 Pointer lift

Use for: cards, toolbar buttons, desktop hover targets.

Motion:
- `translateY(-2px)` + mild shadow for 100-150ms
- foreground content can move 1px faster than the card shell

Reduced motion:
- no movement; use border/outline/contrast.

Rules:
- Do not use hover-only affordances on touch-first layouts.
- Large cards should lift less than small controls.

### 3.3 Focus parallax

Use for: tvOS-inspired grids, keyboard focus galleries, remote-control UIs.

Motion:
- focused card: `scale(1.03)` to `scale(1.06)`
- image layer: translate 2-6px opposite pointer/focus direction
- shadow/outline: strengthen after scale settles

Reduced motion:
- static focus ring and elevated z-index only.

Rules:
- Focus movement must be spatially predictable.
- Keep the focused item anchored; do not make the whole grid drift.

### 3.4 Haptic sync

Use for: native shells, React Native, mobile web wrapped by native containers.

Motion:
- visual press begins immediately
- haptic fires at confirmation point
- success checkmark or state snap appears 50-100ms after haptic

Reduced motion:
- keep haptic and static state; remove scale/slide.

Rules:
- Haptic and visual feedback must represent the same state.
- Never use haptic for decorative hover-like effects.

## 4. Control templates

### 4.1 Toggle thumb glide

Use for: switch controls, binary settings.

Motion:
- thumb translates across track in 150-200ms
- track color changes in 100-150ms
- optional thumb scale from `1` to `0.96` while dragging

Reduced motion:
- snap thumb position; keep semantic color/label.

Rules:
- Text label must make the state clear; do not rely on color alone.

### 4.2 Segmented pill glide

Use for: segmented controls, filters, tab-like local mode switches.

Motion:
- selected pill moves with `translateX` for 200-300ms
- pill width morphs to target label width
- content area fades/offsets by 4-8px

Reduced motion:
- selected state jumps instantly; content crossfades or switches.

Rules:
- Pill motion should be behind text, not moving text itself.
- Keep focus order independent from animation.

### 4.3 Tab underline morph

Use for: website nav, category bars, horizontal tabs.

Motion:
- underline x/width morphs in 200-300ms
- label color changes in 100ms
- content panel fades for 200ms

Reduced motion:
- underline snaps; panel direct switch or fade only.

Rules:
- Underline should follow measured text width, not equal-width slots unless the design uses equal tabs.

### 4.4 Search field expansion

Use for: navigation search, table filtering, command palette triggers.

Motion:
- field width/clip expands from trigger area in 250-350ms
- background chrome dims or blurs slightly
- placeholder/text cursor appears after 100ms

Reduced motion:
- show final search field directly; keep focus placement.

Rules:
- Focus the input immediately.
- Provide Escape/cancel and preserve previous query when appropriate.

### 4.5 Validation nudge

Use for: form errors, missing required fields.

Motion:
- small x-axis nudge 4-6px for 150-200ms
- error text fades in below control
- focus ring or border color updates immediately

Reduced motion:
- no nudge; use error text and focus ring.

Rules:
- Nudge once only. Repeated shaking feels punitive.

## 5. Presentation templates

### 5.1 Anchor reveal

Use for: tooltips, popovers, menus, help bubbles.

Motion:
- originate near trigger: `translateY(4-8px)` or side offset
- opacity 0 -> 1 in 150-200ms
- transform-origin points to trigger

Reduced motion:
- fade only or instant.

Rules:
- Anchor geometry matters more than dramatic motion.
- Do not reveal from screen center unless the trigger is central.

### 5.2 Menu cascade

Use for: context menus, dropdown menus, command menus.

Motion:
- container fades/translates 4-8px
- menu items stagger by 12-24ms, max 80ms total

Reduced motion:
- no stagger; fade or instant.

Rules:
- Keep total delay tiny; menus are operational UI.

### 5.3 Edge sheet

Use for: bottom sheets on mobile, side sheets on desktop, drawers.

Motion:
- enter from closest edge in 300-350ms
- backdrop opacity follows slightly behind sheet
- drag-to-dismiss tracks finger/pointer directly

Reduced motion:
- dissolve backdrop and show sheet in final position.

Rules:
- Direction should match spatial source.
- Sheet content must be interactive before the animation fully ends.

### 5.4 Modal dissolve-scale

Use for: blocking dialogs, focused task panels.

Motion:
- backdrop fade 150-250ms
- dialog `scale(0.98) -> 1` + opacity in 300-350ms

Reduced motion:
- dissolve only.

Rules:
- Avoid large zoom. Modal motion should reduce surprise, not perform a trick.

### 5.5 Alert dissolve

Use for: system-like confirmation or destructive decisions.

Motion:
- fade/scale `0.99 -> 1` in 200-300ms
- destructive button should not bounce or overshoot

Reduced motion:
- instant/fade.

Rules:
- Alerts need clarity and restraint; spectacle fights comprehension.

### 5.6 Toast / flag slide

Use for: non-blocking status, save success, sync info.

Motion:
- enter from nearby edge by 8-16px in 250-350ms
- auto-dismiss only when low-risk and pauseable

Reduced motion:
- fade only; keep manual dismissal.

Rules:
- If a toast updates data, ensure screen readers receive a live-region update.

## 6. Navigation and continuity templates

### 6.1 Source-to-destination transition

Use for: card -> detail, thumbnail -> gallery, row -> inspector.

Motion:
- source element becomes destination shell through measured transform
- background fades/settles behind it
- detail content fades after shell reaches 70-80% progress

Reduced motion:
- direct navigation with crossfade.

Rules:
- Preserve source identity: image, title, or shape should visibly connect both states.
- Avoid when source and destination have no strong visual relationship.

### 6.2 Card-to-detail morph

Use for: Apple News/App Store-like cards, product feature cards.

Motion:
- card radius decreases/increases toward destination container
- image crops expand with `clip-path` or transform
- title repositions using transform, not layout animation

Reduced motion:
- static destination with shared hero image; fade.

Rules:
- Crop and radius changes are secondary; content continuity is primary.

### 6.3 Sticky large title collapse

Use for: Apple-style sections, settings/detail pages, long product pages.

Motion:
- title starts large/centered or large/top
- scroll progress maps to x/y/scale
- title pins at toolbar/section top before content ends
- background can shift from dark to light during the section

Reduced motion:
- title appears in final pinned location; no scroll scrub.

Rules:
- Pinning must end before the next section begins.
- Title should not cover interactive content.

### 6.4 Tab content crossfade

Use for: segmented content, tab panels, media/category switching.

Motion:
- old panel fades out 100-150ms
- new panel fades in + 4-8px translate 150-250ms

Reduced motion:
- fade only or direct switch.

Rules:
- Keep container height stable or animate height separately after content switch.

### 6.5 Breadcrumb / hierarchy return

Use for: desktop sidebars, nested settings, admin-style Apple-inspired apps.

Motion:
- forward: content slides 8-16px from right, fades in
- back: content slides from left
- sidebar selection updates immediately

Reduced motion:
- fade or direct switch.

Rules:
- Direction must match navigation hierarchy.

## 7. Data and content templates

### 7.1 FLIP reorder

Use for: sortable lists, filtered cards, grouped results.

Motion:
- measure First and Last positions
- invert with transform
- play transform to zero in 200-300ms

Reduced motion:
- direct reorder; optionally highlight changed rows.

Rules:
- Do not FLIP huge tables; use highlight or pagination instead.

### 7.2 Group insertion

Use for: adding cards, chat messages, notifications.

Motion:
- new item fades + translates 8px
- surrounding items use FLIP, not layout transitions

Reduced motion:
- new item appears with static highlight.

Rules:
- Insertions should not push the user's current reading target unexpectedly.

### 7.3 Results crossfade

Use for: search results, filters, category switching.

Motion:
- pending state: subtle skeleton or progress
- final state: old results fade down, new results fade up
- keep scroll position when user intent suggests refinement

Reduced motion:
- direct replacement and count update.

Rules:
- Empty state should animate less than successful content; clarity first.

### 7.4 Numeric delta tick

Use for: dashboards, metrics, financial/patent analytics.

Motion:
- number increments over 300-500ms only for meaningful changes
- color/arrow explains direction

Reduced motion:
- final number plus changed-state highlight.

Rules:
- Never animate numbers if precision or trust is critical during live updates.

### 7.5 Skeleton dissolve

Use for: loading cards, lists, details.

Motion:
- skeleton shimmer only after 100ms delay
- real content replaces skeleton with 150-250ms dissolve

Reduced motion:
- static placeholder; direct content replacement.

Rules:
- Do not show skeleton for near-instant loads.

### 7.6 Progress morph

Use for: uploads, analysis, generation, long-running tasks.

Motion:
- unknown state: small indeterminate indicator
- known progress: morph into determinate bar/steps
- completion: bar becomes success state, then content appears

Reduced motion:
- static progress bar and text.

Rules:
- Never fake determinate progress.

## 8. Liquid Glass and material templates

Native menu exception: when an iOS/iPadOS 26+ button opens a menu or command list, prefer UIKit's native `UIButton` + `UIMenu` route and let the system perform the Liquid Glass bubble-to-menu transition. Use the templates below for custom glass groups, Web/Android/older-iOS fallbacks, or interactions that cannot be represented by standard controls.

### 8.1 Glass materialize

Use for: floating controls, toolbars, cards over rich backgrounds.

Motion:
- opacity appears first
- blur/saturation/border highlight increase over 250-350ms
- foreground content appears after material is readable

Reduced motion:
- show final material immediately or use opaque fallback.

Rules:
- Text contrast must pass before the animation completes.
- If backdrop-filter is expensive, use semi-opaque fallback.

### 8.2 Glass merge / split

Use for: grouped toolbar controls, segmented actions, floating palettes.

Motion:
- nearby glass elements share container rhythm
- gap closes, radii morph, highlight travels across merged edge
- split reverses with shorter exit

Reduced motion:
- no morph; swap to final grouped state.

Rules:
- Merge only when controls are conceptually related.
- Do not merge unrelated actions just because it looks cool.

### 8.3 Toolbar glass drift

Use for: sticky nav over scrolling content.

Motion:
- toolbar opacity/blur/shadow respond to scroll threshold
- background brightness informs text color/token switch
- controls stay stable; only material changes

Reduced motion:
- threshold-based state change without scrub.

Rules:
- Avoid continuous blur updates on low-performance devices.

### 8.4 Foreground/background speed split

Use for: showing glass over dark/light scenes, product storytelling, feature demos.

Motion:
- background moves at 0.35-0.65x speed
- foreground glass/card moves at 1x speed
- specular highlight can move at 1.2x for material response

Reduced motion:
- show 2-3 static keyframes or a simple dissolve.

Rules:
- Always include reference objects so users can perceive relative movement.

### 8.5 Material contrast swap

Use for: dark-to-light sections, glass over images, adaptive nav.

Motion:
- background tone changes over section progress
- glass material shifts opacity and border color
- text token switches at the contrast-safe threshold

Reduced motion:
- switch at section boundary.

Rules:
- Never cross through a low-contrast midpoint.

## 9. Product storytelling templates

### 9.1 Hero product reveal

Use for: marketing pages, product launches, feature intros.

Motion:
- copy appears in staggered layers
- product visual reveals through light sweep, mask, or translate
- CTA appears after primary message is readable

Reduced motion:
- static hero, optional fade.

Rules:
- Do not animate every line. Pick one dominant reveal.

### 9.2 Scroll scene scrub

Use for: Apple.com-like chapters, product details, capability demos.

Motion:
- scroll progress controls product transform or scene state
- text changes at clear chapter thresholds
- background and foreground move at different rates

Reduced motion:
- convert to stacked static keyframes.

Rules:
- Scrubbed motion must be reversible and understandable at slow scroll speed.

### 9.3 Feature spotlight

Use for: one feature at a time, dashboard/analytics product tours.

Motion:
- inactive content dims or slides back
- active feature receives scale/opacity focus
- callout line or highlight follows target

Reduced motion:
- static highlight and anchored callout.

Rules:
- Avoid moving labels away from their target.

### 9.4 Compare before / after

Use for: product improvements, visual transformations, performance comparisons.

Motion:
- slider/reveal mask tracks input
- labels remain fixed
- optional value counter updates with progress

Reduced motion:
- side-by-side static comparison.

Rules:
- Do not auto-play before/after for long periods without controls.

## 10. System-state templates

### 10.1 Dynamic Island pill expand

Use for: compact task state, voice/upload/recording/sync status.

Motion:
- compact pill expands into panel in 300-500ms
- corners stay pill-like
- icon anchors left; details fade in after expansion starts

Reduced motion:
- replace compact state with panel via fade.

Rules:
- Use only for ongoing state, not random notifications.

### 10.2 Live activity morph

Use for: timers, uploads, background jobs, status chips.

Motion:
- persistent capsule changes width/content gradually
- progress or time moves continuously only when meaningful
- completion compresses to success chip then dismisses

Reduced motion:
- static state updates with text.

Rules:
- Live state should remain glanceable; do not force users to watch animation.

### 10.3 Permission just-in-time reveal

Use for: location/camera/microphone/data permission explanations.

Motion:
- context card appears near related action
- permission CTA appears after reason is readable

Reduced motion:
- direct content reveal.

Rules:
- Animation must not pressure the user. Give clear cancel/skip.

### 10.4 Error recovery transition

Use for: failed uploads, invalid forms, recoverable network errors.

Motion:
- error state fades in near affected area
- retry affordance becomes the strongest action
- previous content remains visible if helpful

Reduced motion:
- direct error state and focus move.

Rules:
- Do not use playful motion for serious or destructive errors.

## 11. Spatial and platform-inspired templates

### 11.1 visionOS depth reveal

Use for: spatial dashboards, immersive marketing demos, layered glass panels.

Motion:
- foreground panel appears before background detail
- z-depth is implied with scale, blur, opacity, and shadow
- cursor/focus movement affects only small highlight layers

Reduced motion:
- flat layered composition.

Rules:
- Avoid large z-axis zoom; it can feel uncomfortable.

### 11.2 watchOS glance transition

Use for: compact widgets, status cards, mobile summaries.

Motion:
- tiny scale/opacity transitions, 100-200ms
- content density stays low

Reduced motion:
- direct switch.

Rules:
- Watch-inspired UI should be glanceable, not miniature desktop UI.

### 11.3 macOS inspector slide

Use for: desktop side panels, property inspectors, advanced settings.

Motion:
- inspector slides from trailing edge by 16-24px
- main content may resize only after panel starts

Reduced motion:
- instant panel with focus placement.

Rules:
- Keyboard focus should move predictably into the panel only when user requested it.

### 11.4 iPadOS sidebar adapt

Use for: responsive apps crossing tablet/desktop widths.

Motion:
- sidebar collapses to icon rail or overlay
- content column uses FLIP rather than layout jump

Reduced motion:
- breakpoint state changes instantly.

Rules:
- Do not hide primary navigation without a stable replacement.

## 12. Implementation snippets

### 12.1 CSS motion attributes

```css
[data-apple-motion] {
  transition-property: opacity, transform;
  transition-duration: var(--apple-motion-duration-content);
  transition-timing-function: var(--apple-motion-ease-standard);
}

[data-apple-motion="press"]:active {
  transform: scale(0.98);
  transition-duration: var(--apple-motion-duration-immediate);
}

[data-apple-motion="anchor-reveal"][data-state="open"] {
  opacity: 1;
  transform: translate3d(0, 0, 0) scale(1);
}

[data-apple-motion="anchor-reveal"][data-state="closed"] {
  opacity: 0;
  transform: translate3d(0, 6px, 0) scale(0.99);
}
```

### 12.2 Reduced motion baseline

```css
@media (prefers-reduced-motion: reduce) {
  [data-apple-motion] {
    animation: none !important;
    transition-duration: 0.01ms !important;
    transform: none !important;
  }

  [data-apple-motion="anchor-reveal"],
  [data-apple-motion="modal"],
  [data-apple-motion="toast"] {
    transition-property: opacity !important;
  }
}
```

### 12.3 FLIP helper

```js
export function animateFlip(nodes, mutate, options = {}) {
  const first = new Map(nodes.map((node) => [node, node.getBoundingClientRect()]));
  mutate();

  requestAnimationFrame(() => {
    for (const node of nodes) {
      const start = first.get(node);
      const end = node.getBoundingClientRect();
      const dx = start.left - end.left;
      const dy = start.top - end.top;

      node.animate(
        [
          { transform: `translate(${dx}px, ${dy}px)` },
          { transform: 'translate(0, 0)' },
        ],
        {
          duration: options.duration ?? 250,
          easing: options.easing ?? 'cubic-bezier(0.4, 0, 0.2, 1)',
        }
      );
    }
  });
}
```

## 13. QA checklist

- [ ] 选中的模板是否能解释状态变化，而不是只增加“高级感”？
- [ ] 是否一个场景只使用一个主模板？
- [ ] 是否避免同时大位移、大缩放、强 blur 和强 opacity 变化？
- [ ] 是否给 source-to-destination / card morph 提供真实视觉锚点？
- [ ] Liquid Glass 是否表达层级，而不是普通透明装饰？
- [ ] scroll scrub 是否有静态关键帧降级？
- [ ] reduced motion 是否保留任务路径？
- [ ] reduced transparency / high contrast 是否仍然可读？
- [ ] 所有动画结束前是否仍可点击、输入、滚动或取消？
- [ ] 低性能设备是否禁用连续 blur、parallax 和大面积 shadow？
