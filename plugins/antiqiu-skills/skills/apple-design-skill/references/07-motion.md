# Motion System

Apple 风格前端动画规范。本文只定义 motion: timing、easing、property、触发、降级和可访问性策略。色彩、字体、间距、圆角、阴影、毛玻璃等视觉样式继续放在 [01-tokens.md](01-tokens.md)，组件结构放在 [02-components.md](02-components.md)，布局样式放在 [03-patterns.md](03-patterns.md)。

## 1. 调研来源

| 来源 | 可采用的标准 |
|---|---|
| [Apple HIG Motion](https://developer.apple.com/design/human-interface-guidelines/motion) | 动效必须有目的，帮助表达状态、反馈、空间关系；不要为了装饰添加动画；必须让 motion optional |
| [Apple HIG Loading](https://developer.apple.com/design/human-interface-guidelines/loading) | 加载时优先尽快显示内容；超过一两秒再显示进度；知道进度用 determinate，不知道进度用 indeterminate |
| [Apple HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials) | 材料表达层级和背景关系；半透明、模糊和 vibrancy 必须服务于可读性 |
| [Apple Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/liquid-glass) | Liquid Glass 是动态材料系统，强调适应性、层级、触控响应和连续形变 |
| [SwiftUI GlassEffectContainer](https://developer.apple.com/documentation/swiftui/glasseffectcontainer) | 多个 glass 元素可以作为容器化材料组来协调运动和 morph |
| [SwiftUI GlassEffectTransition](https://developer.apple.com/documentation/swiftui/glasseffecttransition) | glass 元素的进入、退出和状态变化应保持材料连续性 |
| [SwiftUI navigationTransition](https://developer.apple.com/documentation/swiftui/view/navigationtransition%28_%3A%29) | 导航转场可以保留 source 和 destination 的空间关系 |
| [Apple Support Reduce Motion](https://support.apple.com/en-us/111781) | Reduce Motion 会将缩放/滑动类转场替换为 dissolve，关闭视差和部分应用动画 |
| [Material Design Motion](https://m1.material.io/motion/material-motion.html) | motion 用来表达空间关系、功能和意图；动画要快速、精准、自然 |
| [Material Duration & Easing](https://m1.material.io/motion/duration-easing.html) | 按距离、速度、表面变化动态调整时长；进入用 deceleration，离开用 acceleration，常规移动用 standard curve |
| [Fluent 2 Motion](https://fluent2.microsoft.design/motion) | motion 要 functional、natural、consistent、appealing；时长按元素尺寸和移动距离调整 |
| [Carbon Motion](https://carbondesignsystem.com/elements/motion/overview/) | 区分 productive motion 和 expressive motion；组件内微交互可快，系统级提示可更有表现力 |
| [Atlassian Motion](https://atlassian.design/foundations/motion) | 每个 motion event 由 duration、easing curve、property 三项定义；交互 50-150ms，转场 150-400ms |
| [Spectrum Motion](https://spectrum.adobe.com/page/motion/) | motion 应 purposeful、intuitive、seamless；微动画 130-250ms，宏动画 300-500ms |
| [WCAG 2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) | 自动开始且超过 5 秒的移动、闪烁、滚动或自动更新内容必须可暂停、停止或隐藏 |
| [WCAG 2.2 Animation from Interactions](https://www.w3.org/TR/wcag/#animation-from-interactions) | 交互触发的 motion animation 必须可禁用，除非动画对功能或信息表达必不可少 |
| [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/%40media/prefers-reduced-motion) | 通过 `prefers-reduced-motion` 检测用户是否希望减少非必要运动；大面积缩放和位移可能触发不适 |

## 2. Motion 原则

1. **Purpose before delight**: 动画必须解释变化、确认反馈、维持空间关系或降低等待感；没有信息价值就缩短或移除。
2. **Fast enough to operate**: 高频交互不等待动画完成。hover、press、toggle 必须接近即时；页面级转场也不要阻塞下一步操作。
3. **Spatial continuity**: 进入、退出、展开、收起要从触发点或关联元素出发，方向与用户预期一致。
4. **Natural but restrained**: 使用加速、减速、惯性和轻微 scale 表达真实感；避免夸张弹性、旋转、漂浮、连续视差。
5. **One change, one cue**: 一个状态变化不要同时使用大位移、大缩放、强透明度和颜色闪烁。首选一个主属性加一个辅助属性。
6. **Accessible by default**: 所有非必要动画都要响应 `prefers-reduced-motion`；自动循环动画超过 5 秒要提供暂停/停止/隐藏。
7. **Performance is part of design**: 首选 `opacity` 和 `transform`；避免动画驱动 layout、paint-heavy shadow、filter blur 或 large backdrop-filter。

## 3. Token 模型

### 3.1 Duration

| Token | 值 | 用途 |
|---|---:|---|
| `motion-duration-immediate` | 50ms | press feedback、selection tick、极小状态确认 |
| `motion-duration-instant` | 100ms | hover、active、link color、switch thumb 微交互 |
| `motion-duration-fast` | 150ms | tooltip、popover 小面积进入、菜单项反馈 |
| `motion-duration-standard` | 200ms | dropdown、accordion、小组件展开收起 |
| `motion-duration-content` | 300ms | tab panel、列表过滤、局部内容替换 |
| `motion-duration-modal` | 350ms | modal、sheet、toast、drawer 的常规进入退出 |
| `motion-duration-large` | 500ms | 大面板、跨屏位移、复杂重排 |
| `motion-duration-hero` | 600ms | hero reveal、页面首屏揭示，低频使用 |
| `motion-duration-loop` | 1200-1500ms | skeleton、indeterminate progress，仅加载态使用 |

使用规则:

- 交互反馈控制在 50-150ms。
- 常规 UI 转场控制在 150-400ms。
- 只有低频、大面积、需要用户理解空间关系的 motion 才允许 500-600ms。
- 元素越大、移动距离越长、层级变化越明显，时长可以更长；离开屏幕通常比进入屏幕更短。

### 3.2 Easing

| Token | CSS | 用途 |
|---|---|---|
| `motion-ease-linear` | `linear` | 色彩、opacity 的极短微反馈；连续旋转进度 |
| `motion-ease-standard` | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Apple.com 常规 ease，适合展开、状态切换 |
| `motion-ease-emphasized` | `cubic-bezier(0.4, 0, 0.2, 1)` | Material standard，适合元素在屏幕内移动 |
| `motion-ease-enter` | `cubic-bezier(0, 0, 0.2, 1)` | 进入屏幕: 快速出现，柔和停下 |
| `motion-ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | 离开屏幕: 加速离场，减少等待 |
| `motion-ease-productive` | `cubic-bezier(0.2, 0, 0.38, 0.9)` | Carbon productive 风格，适合高频业务组件 |
| `motion-ease-expressive` | `cubic-bezier(0.4, 0.14, 0.3, 1)` | Carbon expressive 风格，适合通知、成功反馈、低频高可见度状态 |
| `motion-ease-spring` | `cubic-bezier(0.175, 0.885, 0.32, 1.275)` | 轻微回弹，仅用于小面积确认反馈 |

使用规则:

- 进入使用 ease-out/deceleration；退出使用 ease-in/acceleration；屏幕内位置变化使用 ease-in-out/standard。
- 线性不用于大位移，因为匀速移动不自然。
- spring 只用于小元素和短距离反馈，不用于页面、modal、drawer。

### 3.3 Properties

| 属性 | 推荐度 | 说明 |
|---|---|---|
| `opacity` | 首选 | 最安全，适合 fade、toast、skeleton 降级 |
| `transform: translate/scale` | 首选 | GPU 友好，适合位移、展开、按压反馈 |
| `clip-path` | 谨慎 | 可用于 reveal，但要测试性能和 reduced motion |
| `height/width/top/left` | 避免 | 会触发布局，改用 transform 或容器尺寸状态 |
| `box-shadow/filter/backdrop-filter` | 谨慎 | paint 成本高，只做短时小范围过渡 |
| `color/background` | 可用 | 100-150ms，通常 linear 即可 |

## 4. Pattern Matrix

本节定义基础 motion 场景。更完整的 Apple 风格模板库见 [09-motion-templates.md](09-motion-templates.md)，包括 Liquid Glass morph、source-to-destination、Dynamic Island pill、tvOS focus parallax、visionOS depth reveal 等模板。

| 场景 | 属性 | 时长 | 曲线 | reduced motion |
|---|---|---:|---|---|
| Button hover | background/opacity | 100ms | linear | 允许颜色变化，禁用 scale |
| Button press | scale `0.98` | 50-100ms | standard | 用静态 pressed 样式替代 |
| Link hover | color/underline opacity | 100ms | linear | 保留颜色/下划线 |
| Toggle | thumb translate | 150-200ms | standard | 直接切换位置，不滑动 |
| Tooltip | opacity + translateY 4px | 150ms | enter/exit | fade only 或直接出现 |
| Dropdown | opacity + translateY 6-8px | 150-200ms | enter/exit | fade only |
| Accordion | opacity + grid-template-rows | 200-300ms | standard | 直接展开，保留焦点顺序 |
| Tabs | opacity + translateX 8px | 200-300ms | standard | fade only 或直接切换 |
| Modal | opacity + scale 0.98 -> 1 | 300-350ms | emphasized | dissolve/fade |
| Sheet/Drawer | translate from edge | 300-350ms | enter/exit | fade or instant |
| Toast/Flag | opacity + translateY 8px | 250-350ms | expressive | fade only |
| Page reveal | opacity + translateY 16-24px | 500-600ms | standard | 内容直接可见 |
| List reorder | transform translate | 200-300ms | emphasized | 直接重排 |
| Drag feedback | transform + shadow | 100-200ms | productive | 保留 outline/selected 状态 |
| Skeleton shimmer | background-position | 1200-1500ms loop | linear | 静态占位色 |
| Progress spinner | rotation | 800-1200ms loop | linear | 可保留小型 spinner；大面积 loader 改静态/进度条 |
| Scroll-linked visual | transform/opacity | scroll progress | none | 禁用 scrub，显示关键帧或静态图 |
| Parallax | translate/scale depth | scroll progress | none | 默认禁用，除非对叙事必要且有开关 |

## 5. CSS Variables

```css
:root {
  --apple-motion-duration-immediate: 50ms;
  --apple-motion-duration-instant: 100ms;
  --apple-motion-duration-fast: 150ms;
  --apple-motion-duration-standard: 200ms;
  --apple-motion-duration-content: 300ms;
  --apple-motion-duration-modal: 350ms;
  --apple-motion-duration-large: 500ms;
  --apple-motion-duration-hero: 600ms;
  --apple-motion-duration-loop: 1500ms;

  --apple-motion-ease-linear: linear;
  --apple-motion-ease-standard: cubic-bezier(0.25, 0.1, 0.25, 1);
  --apple-motion-ease-emphasized: cubic-bezier(0.4, 0, 0.2, 1);
  --apple-motion-ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --apple-motion-ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --apple-motion-ease-productive: cubic-bezier(0.2, 0, 0.38, 0.9);
  --apple-motion-ease-expressive: cubic-bezier(0.4, 0.14, 0.3, 1);
  --apple-motion-ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

## 6. Tailwind Extension

只把 motion token 加到 motion utilities，不要把它们混入 color、spacing、radius 等视觉 token 说明中。

```js
export const appleMotion = {
  transitionDuration: {
    immediate: '50ms',
    instant: '100ms',
    fast: '150ms',
    standard: '200ms',
    content: '300ms',
    modal: '350ms',
    large: '500ms',
    hero: '600ms',
    loop: '1500ms',
  },
  transitionTimingFunction: {
    'apple-linear': 'linear',
    'apple-standard': 'cubic-bezier(0.25, 0.1, 0.25, 1)',
    'apple-emphasized': 'cubic-bezier(0.4, 0, 0.2, 1)',
    'apple-enter': 'cubic-bezier(0, 0, 0.2, 1)',
    'apple-exit': 'cubic-bezier(0.4, 0, 1, 1)',
    'apple-productive': 'cubic-bezier(0.2, 0, 0.38, 0.9)',
    'apple-expressive': 'cubic-bezier(0.4, 0.14, 0.3, 1)',
    'apple-spring': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
  },
};
```

## 7. Reduced Motion Contract

### 7.1 CSS baseline

```css
@media (prefers-reduced-motion: reduce) {
  html:focus-within {
    scroll-behavior: auto;
  }

  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  [data-motion="parallax"],
  [data-motion="scroll-scrub"],
  [data-motion="large-scale"] {
    animation: none !important;
    transform: none !important;
  }
}
```

### 7.2 Prefer reduced alternatives

不要只做全局 `animation: none`。每个关键组件要定义 reduced motion alternative:

| 原动画 | Reduced motion 替代 |
|---|---|
| 页面 slide/zoom | fade 或 instant |
| modal scale | dissolve |
| sheet translate | fade 或 instant |
| parallax | 静态背景 |
| scroll reveal | 内容初始可见 |
| skeleton shimmer | 静态 placeholder |
| loading spinner | determinate progress 或静态 loading text |
| confetti/celebration | icon/state text/toast |

### 7.3 JavaScript hook

```js
export function useReducedMotion() {
  const query = '(prefers-reduced-motion: reduce)';
  const [reduced, setReduced] = React.useState(() =>
    typeof window !== 'undefined' && window.matchMedia(query).matches
  );

  React.useEffect(() => {
    const media = window.matchMedia(query);
    const update = () => setReduced(media.matches);
    update();
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
  }, []);

  return reduced;
}
```

## 8. Loading Motion

1. 0-100ms: 不显示 loader，避免闪一下。
2. 100-1000ms: 可显示 skeleton 或轻量占位。
3. >1000ms: 显示明确进度、步骤、可取消或可继续操作的状态。
4. 已知进度: 用 determinate progress；未知进度: 用 indeterminate progress，但避免全屏长时间循环动画。
5. Loading 动画不应伪造进度；如果无法估计，用状态文本和后台执行降低焦虑。

## 9. Frontend Implementation Rules

- CSS transition 必须显式列出属性，不使用 `transition: all`。
- 组件默认状态必须完整可读，动画只增强理解，不承担唯一信息表达。
- 高级动效先做 reduced motion 版本，再实现 full motion。
- 交互后不要因为动画阻塞点击、输入、滚动或导航。
- 对 `filter`、`backdrop-filter`、大面积 shadow、scroll-linked animation 做性能测试。
- scroll reveal 只能用于低密度内容，不用于表格、表单、密集仪表盘核心数据。
- 同一个 viewport 内同时运动的主元素不超过 2 个。
- 大面积 `scale` 不超过 `0.98 -> 1` 或 `1 -> 1.02`。
- 页面级 motion 禁止无限循环；循环只用于明确的 loading/progress。
- 闪烁、频闪、快速反复颜色变化默认禁止。

## 10. QA Checklist

- [ ] 每个动画能回答: 解释了什么变化或反馈？
- [ ] duration 是否符合交互 50-150ms、转场 150-400ms、低频大动画 500-600ms？
- [ ] easing 是否按进入、退出、屏幕内移动区分？
- [ ] 是否只动画 `opacity`/`transform` 等低成本属性？
- [ ] 是否避免 `transition: all`？
- [ ] reduced motion 下是否没有大位移、大缩放、视差、scroll scrub？
- [ ] 自动循环或滚动内容超过 5 秒时是否可暂停、停止或隐藏？
- [ ] 动画禁用后信息是否仍然完整？
- [ ] 组件能否在动画未结束时继续响应输入？
- [ ] desktop、mobile、低性能设备是否都完成视觉检查？
