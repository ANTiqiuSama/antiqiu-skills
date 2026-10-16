# 无障碍（Accessibility）

> 基于 [WCAG 2.2](https://www.w3.org/TR/WCAG22/)、[Apple Accessibility](https://developer.apple.com/cn/accessibility/) 和 Apple.com 实际实现提炼。目标是 **让所有用户都能顺畅使用**，同时保持 Apple 的视觉风格。

---

## 1. 色彩对比度

### 1.1 WCAG 标准要求

| 元素 | 最低对比度 (AA) | 推荐对比度 (AAA) | 说明 |
|---|---|---|---|
| 正文（<18px） | 4.5:1 | 7:1 | 小字需要更高对比度 |
| 大文字（≥18px 或 ≥14px bold） | 3:1 | 4.5:1 | 大字可以适当降低 |
| 图标/图形元素 | 3:1 | — | 非文本内容 |
| 焦点指示器 | 3:1 | — | 必须与背景有足够区分 |
| 占位符文字 | — | — | 建议不低于 2.5:1（非强制） |

### 1.2 Apple.com 实测对比度验证

以下为 Apple.com 主要文字/背景组合的实测对比度：

| 组合 | 前景色 | 背景色 | 对比度 | 等级 |
|---|---|---|---|---|
| 主文字 @ 白背景 | `#1D1D1F` | `#FFFFFF` | 15.4:1 | AAA |
| 次要文字 @ 白背景 | `#6E6E73` | `#FFFFFF` | 4.6:1 | AA |
| 辅助文字 @ 白背景 | `#86868B` | `#FFFFFF` | 3.3:1 | 仅大字 AA |
| 链接蓝 @ 白背景 | `#0071E3` | `#FFFFFF` | 4.5:1 | AA |
| 主文字 @ 灰背景 | `#1D1D1F` | `#F5F5F7` | 13.7:1 | AAA |
| 深色链接 @ 黑背景 | `#2997FF` | `#000000` | 4.6:1 | AA |
| 浅文字 @ 黑背景 | `#F5F5F7` | `#000000` | 16.8:1 | AAA |

> **注意**：`#86868B`（辅助文字）在白背景上对比度仅 3.3:1，对于小于 18px 的正文 **不满足 AA 标准**。Apple 官网将其用于辅助说明文字（通常字号较大或用户关注度较低的场景）。建议在关键信息场景中使用 `#6E6E73` 或更深的灰色。

### 1.3 对比度不达标的常见修正

```css
/* 问题：辅助文字在白背景上对比度不足 */
.bad { color: #86868B; /* 3.3:1，小字不达标 */ }
.good { color: #6E6E73; /* 4.6:1，满足 AA */ }

/* 深色模式下同样注意 */
@media (prefers-color-scheme: dark) {
  .bad { color: #6E6E73; /* 在黑背景上 3.6:1 */ }
  .good { color: #A1A1A6; /* 在黑背景上 6.4:1 */ }
}
```

---

## 2. 动态字体

### 2.1 使用相对单位

```css
/* 正确：使用 rem/em，尊重用户字体偏好 */
html {
  font-size: 106.25%; /* 基准 17px，但会随用户偏好缩放 */
}

h1 { font-size: 3rem; }   /* 约 51px @17px 基准 */
h2 { font-size: 2.25rem; } /* 约 38px */
p  { font-size: 1rem; }    /* 17px */

/* 错误：使用固定 px，忽略用户偏好 */
/* h1 { font-size: 51px; } */  /* 不要这样做 */
```

### 2.2 响应 prefers-contrast

```css
/* 增强对比度模式 — 系统辅助功能设置 */
@media (prefers-contrast: more) {
  :root {
    --color-text-primary:   #000000;   /* 加深主文字 */
    --color-text-secondary: #424245;   /* 加深次要文字 */
    --color-text-tertiary:  #515154;   /* 加深辅助文字 */
    --color-border:         #86868B;   /* 加深边框 */
  }

  /* 增强按钮对比度 */
  .btn-primary {
    background: #0058B0;  /* 更深的蓝色，与白字对比度更高 */
  }

  /* 增强边框可见性 */
  .card {
    border: 1px solid var(--color-border);
  }
}

/* 降低对比度模式 — 较少见，但应保持可读 */
@media (prefers-contrast: less) {
  :root {
    --color-text-primary:   #424245;
    --color-text-secondary: #6E6E73;
  }
}
```

---

## 3. Focus 管理

### 3.1 Apple 的蓝色聚焦环策略

Apple 在所有平台上使用统一的蓝色聚焦环（Focus Ring）作为键盘导航的视觉指示：

- **键盘导航**：显示 `outline: 2px solid #0071E3`
- **鼠标点击**：隐藏 outline
- **触屏操作**：隐藏 outline

### 3.2 完整实现（CSS + JS）

#### CSS 部分

```css
/* 基础 Focus Ring 样式 */
*:focus {
  outline: 2px solid #0071E3;
  outline-offset: 2px;
}

/* 鼠标/触屏聚焦时隐藏 outline */
*:focus:not(:focus-visible) {
  outline: none;
}

/* 对于不支持 :focus-visible 的浏览器，使用 data 属性降级 */
*:focus[data-focus-method="mouse"]:not(input):not(textarea):not(select),
*:focus[data-focus-method="touch"]:not(input):not(textarea):not(select) {
  outline: none;
}

/* 表单元素始终显示聚焦环 */
input:focus,
textarea:focus,
select:focus {
  outline: 2px solid #0071E3;
  outline-offset: 2px;
}

/* 自定义聚焦样式（如卡片、按钮） */
.btn-primary:focus-visible {
  outline: 2px solid #0071E3;
  outline-offset: 4px;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.2);
}

/* 跳过导航链接（Skip Link） */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 8px 16px;
  background: #0071E3;
  color: #FFF;
  font-size: 14px;
  z-index: 10000;
  border-radius: 0 0 8px 0;
}
.skip-link:focus {
  top: 0;
}
```

#### JS 部分 — 输入方式检测

```js
/**
 * Apple 风格 Focus 管理
 * 检测用户输入方式（键盘/鼠标/触屏），仅在键盘操作时显示聚焦环
 */

;(function () {
  let lastFocusMethod = null;

  // 键盘输入 — 显示聚焦环
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Tab' || e.key === 'ArrowLeft' || e.key === 'ArrowRight' ||
        e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      lastFocusMethod = 'keyboard';
      document.documentElement.setAttribute('data-focus-method', 'keyboard');
      document.documentElement.classList.add('keyboard-nav');
    }
  });

  // 鼠标输入 — 隐藏聚焦环
  document.addEventListener('mousedown', function () {
    lastFocusMethod = 'mouse';
    document.documentElement.setAttribute('data-focus-method', 'mouse');
    document.documentElement.classList.remove('keyboard-nav');
  });

  // 触屏输入 — 隐藏聚焦环
  document.addEventListener('touchstart', function () {
    lastFocusMethod = 'touch';
    document.documentElement.setAttribute('data-focus-method', 'touch');
    document.documentElement.classList.remove('keyboard-nav');
  });
})();
```

### 3.3 焦点陷阱（模态框）

```js
/**
 * 焦点陷阱 — 模态框打开时限制焦点在模态框内循环
 */
function trapFocus(element) {
  const focusableSelectors = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(', ');

  const focusable = element.querySelectorAll(focusableSelectors);
  const firstFocusable = focusable[0];
  const lastFocusable = focusable[focusable.length - 1];

  element.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      // Shift+Tab：到达第一个元素时跳到最后一个
      if (document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      }
    } else {
      // Tab：到达最后一个元素时跳到第一个
      if (document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
  });

  // 打开时聚焦到第一个可交互元素
  firstFocusable?.focus();
}
```

---

## 4. 动画减弱

### 4.1 prefers-reduced-motion 实现

```css
/**
 * 动画减弱 — 尊重用户的系统辅助功能设置
 * 减少或替换非必要运动，保留可理解的状态变化
 * 完整 motion 规范见 references/07-motion.md
 */

@media (prefers-reduced-motion: reduce) {
  /* 全局缩短非必要动画 */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* 禁用视差效果 */
  .parallax-element {
    transform: none !important;
  }

  /* 禁用自动播放的 GIF/视频 */
  .auto-play-media {
    display: none;
  }
  .auto-play-media + .static-fallback {
    display: block;
  }
}

/* 反之：用户偏好动画时可以适当增强 */
@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: transform 200ms ease, box-shadow 200ms ease;
  }

  .hero-element {
    animation: fadeInUp 600ms ease;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 4.2 动画减弱的最佳实践

| 做法 | 说明 |
|---|---|
| 减少或替换非必要运动 | 大位移、缩放、视差、scroll scrub 优先替换为 fade 或静态状态 |
| 提供静态降级方案 | 每个动画元素都有无动画或少动画的展示方式 |
| 不要依赖动画传递信息 | 信息应在动画前就已可见 |
| 尊重 `prefers-reduced-motion` | 使用 `@media (prefers-reduced-motion: reduce)` |
| 循环动画可控 | 自动移动、闪烁、滚动或更新超过 5 秒时提供暂停、停止或隐藏 |

---

## 5. ARIA 标注

### 5.1 常用 ARIA 属性列表

| 属性 | 用途 | 示例 |
|---|---|---|
| `aria-label` | 为元素提供不可见的文字标签 | `<button aria-label="关闭">✕</button>` |
| `aria-labelledby` | 用另一个元素的文字作为标签 | `aria-labelledby="title-id"` |
| `aria-describedby` | 关联描述文字 | 表单输入关联错误提示 |
| `aria-hidden` | 对屏幕阅读器隐藏装饰元素 | `aria-hidden="true"` |
| `aria-expanded` | 表示展开/折叠状态 | 菜单、手风琴 |
| `aria-selected` | 表示选中状态 | 标签页、列表选项 |
| `aria-live` | 宣布动态内容变化 | `aria-live="polite"` |
| `aria-current` | 表示当前项 | 导航高亮项 |
| `role` | 定义元素语义角色 | `role="navigation"` |
| `aria-disabled` | 表示禁用状态（保留焦点能力） | `aria-disabled="true"` |

### 5.2 Apple 风格的 ARIA 使用示例

#### 导航栏

```html
<nav aria-label="全局导航">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/" aria-current="page">商店</a>
    </li>
    <li role="none">
      <a role="menuitem" href="/mac">Mac</a>
    </li>
    <li role="none">
      <a role="menuitem" href="/ipad">iPad</a>
    </li>
  </ul>
</nav>
```

#### 产品卡片

```html
<article aria-labelledby="product-title" aria-describedby="product-desc">
  <h3 id="product-title">iPhone 16 Pro</h3>
  <p id="product-desc">钛金属设计，A18 Pro 芯片</p>
  <a href="/iphone-16-pro" aria-label="进一步了解 iPhone 16 Pro">
    进一步了解 <span aria-hidden="true">→</span>
  </a>
</article>
```

#### 模态框

```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-desc">
  <h2 id="modal-title">确认购买</h2>
  <p id="modal-desc">您即将购买 iPhone 16 Pro，价格 ¥7999 起。</p>
  <button>确认</button>
  <button aria-label="关闭对话框">✕</button>
</div>
```

#### 购物车徽章

```html
<a href="/bag" aria-label="购物袋，2 件商品">
  <svg aria-hidden="true"><!-- 购物袋图标 --></svg>
  <span aria-hidden="true">2</span>
</a>
```

#### 动态价格更新

```html
<div aria-live="polite" aria-atomic="true">
  <span>总价：¥15,998</span>
</div>
```

---

## 6. 屏幕阅读器

### 6.1 VoiceOver 兼容性

VoiceOver 是 Apple 平台的内建屏幕阅读器，以下是兼容性要点：

| 要点 | 说明 |
|---|---|
| 语义化 HTML | 使用正确的 HTML 元素（`<nav>`、`<main>`、`<article>` 等） |
| 图片替代文字 | 所有有意义的图片必须有 `alt` 属性 |
| 表单标签 | 使用 `<label>` 或 `aria-label` |
| 标题层级 | 保持合理的标题层级（h1 → h2 → h3），不跳级 |
| 链接文字 | 避免使用"点击这里"，使用描述性文字 |
| 动态内容 | 使用 `aria-live` 宣布变化 |
| 表格数据 | 使用 `<th>` + `scope` 属性 |

### 6.2 语义化 HTML

```html
<!-- ✅ 正确：语义化结构 -->
<body>
  <a href="#main" class="skip-link">跳到主要内容</a>

  <header>
    <nav aria-label="全局导航">
      <!-- 导航链接 -->
    </nav>
  </header>

  <main id="main">
    <section aria-labelledby="hero-title">
      <h1 id="hero-title">iPhone 16 Pro</h1>
      <p>你好，Apple Intelligence。</p>
    </section>

    <section aria-labelledby="features-title">
      <h2 id="features-title">功能亮点</h2>
      <article aria-labelledby="feature-1">
        <h3 id="feature-1">A18 Pro 芯片</h3>
        <p>前所未有的性能表现。</p>
      </article>
    </section>
  </main>

  <footer>
    <nav aria-label="页脚导航">
      <!-- 页脚链接 -->
    </nav>
  </footer>
</body>

<!-- ❌ 错误：div 滥用 -->
<body>
  <div class="nav">...</div>
  <div class="content">
    <div class="title">iPhone 16 Pro</div>
    <div class="subtitle">你好，Apple Intelligence。</div>
    <div class="features">
      <div class="feature">
        <div class="feature-title">A18 Pro 芯片</div>
      </div>
    </div>
  </div>
</body>
```

### 6.3 图片处理

```html
<!-- 有意义的图片 — 需要 alt -->
<img src="iphone-16-pro.jpg" alt="iPhone 16 Pro 钛金属外观，显示全新的相机控制按钮" />

<!-- 纯装饰图片 — 隐藏 -->
<img src="decorative-pattern.png" alt="" role="presentation" />

<!-- 图标 — 使用 aria-hidden -->
<button aria-label="搜索">
  <svg aria-hidden="true" focusable="false">
    <!-- 搜索图标 -->
  </svg>
</button>

<!-- 复杂图表 — 使用详细描述 -->
<figure>
  <img src="performance-chart.png" alt="性能对比柱状图" />
  <figcaption>
    A18 Pro 相比上一代性能提升 20%，能效提升 30%。
    详细数据见下方表格。
  </figcaption>
</figure>
```

---

## 7. 无障碍检查清单

以下是实施 Apple 风格界面时的 **10 条无障碍要点**：

- [ ] **1. 色彩对比度**：正文 ≥ 4.5:1（AA），推荐 7:1（AAA）；大文字 ≥ 3:1
- [ ] **2. 键盘可导航**：所有交互元素可通过 Tab/Shift+Tab/Enter/Space/Esc 操作
- [ ] **3. Focus Ring 可见**：键盘导航时显示 `2px solid #0071E3` 聚焦环
- [ ] **4. 动画可关闭**：尊重 `prefers-reduced-motion: reduce`，提供静态降级
- [ ] **5. 语义化 HTML**：使用 `<nav>`、`<main>`、`<article>`、`<section>` 等语义元素
- [ ] **6. 图片有替代文字**：有意义图片有描述性 `alt`，装饰图片用 `alt=""`
- [ ] **7. 表单可访问**：每个输入有 `<label>` 或 `aria-label`，错误信息用 `aria-describedby` 关联
- [ ] **8. 标题层级合理**：h1 → h2 → h3 逐级递进，不跳级
- [ ] **9. 响应用户偏好**：支持 `prefers-color-scheme`、`prefers-contrast`、`prefers-reduced-motion`
- [ ] **10. ARIA 正确使用**：不过度使用 `role`，优先用原生 HTML 元素；动态内容用 `aria-live` 宣布

---

## 8. 参考资源

| 资源 | 链接 |
|---|---|
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ |
| Apple Accessibility | https://developer.apple.com/cn/accessibility/ |
| Apple Accessibility 设计指南 | https://developer.apple.com/cn/design/accessibility/ |
| VoiceOver 测试指南 | https://developer.apple.com/accessibility/vision/ |
| WebAIM 对比度检测器 | https://webaim.org/resources/contrastchecker/ |
| ARIA 实践模式 | https://www.w3.org/WAI/ARIA/apg/ |
