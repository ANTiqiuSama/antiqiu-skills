# 组件规范 — Apple 风格 UI 组件

> 来源：Apple.com 实际组件 CSS 分析、HIG 组件规范、Apple Design Resources。
> 所有尺寸和样式值均来自 Apple 官方源码或设计资源。

---

## 1. 按钮（Buttons）

### 1.1 按钮类型总览

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  主要按钮（Primary）    蓝色填充 + 白色文字 + 全圆角         │
│  ┌──────────────────┐                                      │
│  │  立即购买         │  bg: #0071E3                        │
│  └──────────────────┘  text: #FFF                          │
│                        radius: 980px (全圆角/药丸形)        │
│                        padding: 8px 16px                    │
│                        font: 14px / 400                     │
│                                                             │
│  次要按钮（Secondary）  蓝色文字 + 箭头 → + 无边框           │
│  进一步了解 →           text: #0071E3                       │
│                        font: 21px / 400                     │
│                        hover: underline                     │
│                                                             │
│  文字链接              蓝色文字 + 下划线                     │
│  进一步了解             text: #0071E3                       │
│                        hover: underline                     │
│                        font: 继承父级                       │
│                                                             │
│  深色背景按钮          白色文字 + 白色边框（半透明）         │
│  ┌──────────────────┐                                      │
│  │  观看影片  ▶      │  text: rgba(255,255,255,0.8)        │
│  └──────────────────┘  border: 1px solid rgba(255,255,255,0.8) │
│                        hover: border/text 全不透明           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 主要按钮（Primary Button）

```css
.btn-primary {
  display: inline-block;
  padding: 8px 16px;
  font-family: var(--font-system);
  font-size: 14px;
  font-weight: 400;
  line-height: 1;
  color: #FFFFFF;
  background: #0071E3;
  border: none;
  border-radius: 980px;  /* 全圆角 — Apple 标志性按钮形状 */
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  white-space: nowrap;
  transition: background 100ms linear;
}

.btn-primary:hover {
  background: #0077ED;
}

.btn-primary:active {
  background: #006EDB;
}

/* 大号主按钮 */
.btn-primary-lg {
  padding: 12px 24px;
  font-size: 17px;
}

/* Focus Ring */
.btn-primary:focus-visible {
  outline: 2px solid #0071E3;
  outline-offset: 4px;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.2);
}
```

### 1.3 次要按钮（Secondary / CTA Link）

Apple.com 最常见的 CTA 样式，是文字链接 + 箭头组合：

```css
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-system);
  font-size: 21px;
  font-weight: 400;
  line-height: 1;
  color: #0071E3;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
  transition: color 100ms linear;
}

.btn-secondary:hover {
  text-decoration: underline;
}

.btn-secondary:active {
  color: #006EDB;
}

/* 箭头字符 */
.btn-secondary .arrow::after {
  content: ' →';
  font-size: 0.85em;
}

/* 小号次要按钮 */
.btn-secondary-sm {
  font-size: 14px;
}

/* Focus Ring */
.btn-secondary:focus-visible {
  outline: 2px solid #0071E3;
  outline-offset: 4px;
  border-radius: 4px;
}
```

### 1.4 深色背景按钮

用于深色/图片背景上的按钮：

```css
.btn-on-dark {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-family: var(--font-system);
  font-size: 14px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.8);
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 980px;
  cursor: pointer;
  text-decoration: none;
  transition: all 100ms linear;
}

.btn-on-dark:hover {
  color: #FFFFFF;
  border-color: #FFFFFF;
}

.btn-on-dark:focus-visible {
  outline: 2px solid #FFFFFF;
  outline-offset: 4px;
}
```

### 1.5 按钮组合

Apple.com 常见的按钮排列方式：

```html
<!-- 水平排列：主按钮 + 次要按钮 -->
<div class="flex items-center justify-center gap-6 mt-6">
  <a href="#" class="btn-primary">立即购买</a>
  <a href="#" class="btn-secondary">
    进一步了解 <span class="arrow"></span>
  </a>
</div>

<!-- 只有次要按钮（常见于产品卡片） -->
<a href="#" class="btn-secondary">
  进一步了解 <span class="arrow"></span>
</a>

<!-- 深色背景上的按钮组 -->
<div class="flex items-center justify-center gap-4 mt-6">
  <a href="#" class="btn-primary">立即购买</a>
  <a href="#" class="btn-on-dark">
    观看影片 <span aria-hidden="true">▶</span>
  </a>
</div>
```

---

## 2. 导航栏（Navigation Bar）

### 2.1 导航栏规格

```
┌──────────────────────────────────────────────────────────────┐
│  ◬  商店  Mac  iPad  iPhone  Watch  AirPods  ...    🔍 🛒  │
│──────────────────────────────────────────────────────────────│
│  ↑ 毛玻璃背景                                               │
│  高度: 44px（桌面）/ 48px（移动端）                          │
│  背景: rgba(255,255,255,0.72) + blur(20px) + saturate(180%) │
│  文字: 12px / 400 / opacity 0.8 → hover 1.0                │
│  底部: 1px border rgba(0,0,0,0.08)                          │
│  最大宽度: 980px（内容区域）                                  │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 完整实现

```css
.navbar {
  position: sticky;
  top: 0;
  z-index: 9999;
  height: 44px;
  background: rgba(255, 255, 255, 0.72);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.navbar-inner {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 8px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.navbar-logo svg {
  width: 18px;
  height: 18px;
  fill: var(--color-text-primary);
}

/* 导航链接 */
.navbar-link {
  font-size: 12px;
  font-weight: 400;
  color: var(--color-text-primary);
  opacity: 0.8;
  text-decoration: none;
  transition: opacity 100ms linear;
  padding: 0 8px;
}

.navbar-link:hover {
  opacity: 1.0;
}

/* 搜索/购物袋图标 */
.navbar-action {
  opacity: 0.8;
  transition: opacity 100ms linear;
}

.navbar-action:hover {
  opacity: 1.0;
}

/* Focus Ring */
.navbar-link:focus-visible,
.navbar-action:focus-visible {
  outline: 2px solid #0071E3;
  outline-offset: 2px;
  border-radius: 4px;
}

/* 移动端 */
@media (max-width: 734px) {
  .navbar {
    height: 48px;
  }

  .navbar-links {
    display: none; /* 移动端隐藏，使用汉堡菜单 */
  }
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .navbar {
    background: rgba(29, 29, 31, 0.72);
    border-bottom-color: rgba(255, 255, 255, 0.08);
  }

  .navbar-logo svg {
    fill: #F5F5F7;
  }

  .navbar-link {
    color: #F5F5F7;
  }
}
```

### 2.3 HTML 结构

```html
<header class="navbar" role="banner">
  <div class="navbar-inner">
    <a href="/" class="navbar-logo" aria-label="Apple 首页">
      <svg aria-hidden="true"><!-- Apple Logo --></svg>
    </a>

    <nav aria-label="全局导航">
      <ul class="navbar-links" role="menubar">
        <li role="none"><a class="navbar-link" role="menuitem" href="/store">商店</a></li>
        <li role="none"><a class="navbar-link" role="menuitem" href="/mac">Mac</a></li>
        <li role="none"><a class="navbar-link" role="menuitem" href="/ipad">iPad</a></li>
        <li role="none"><a class="navbar-link" role="menuitem" href="/iphone">iPhone</a></li>
        <li role="none"><a class="navbar-link" role="menuitem" href="/watch">Watch</a></li>
        <li role="none"><a class="navbar-link" role="menuitem" href="/airpods">AirPods</a></li>
      </ul>
    </nav>

    <div class="navbar-actions">
      <button class="navbar-action" aria-label="搜索">
        <svg aria-hidden="true"><!-- 搜索图标 --></svg>
      </button>
      <a href="/bag" class="navbar-action" aria-label="购物袋">
        <svg aria-hidden="true"><!-- 购物袋图标 --></svg>
      </a>
    </div>
  </div>
</header>
```

---

## 3. 卡片（Cards）

### 3.1 产品卡片

Apple.com 最常见的卡片类型，用于产品展示：

```css
.card-product {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: var(--color-bg-secondary);
  text-align: center;
  transition: transform 200ms ease,
              box-shadow 200ms ease;
}

.card-product:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

/* 卡片内容区域 */
.card-product-content {
  padding: 40px 24px 0;
}

/* 卡片标题 */
.card-product-title {
  font-size: 40px;
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.015em;
  color: var(--color-text-primary);
}

/* 卡片副标题 */
.card-product-subtitle {
  font-size: 21px;
  font-weight: 400;
  line-height: 1.33;
  color: var(--color-text-secondary);
  margin-top: 8px;
}

/* 卡片 CTA */
.card-product-cta {
  margin-top: 16px;
}

/* 卡片图片 */
.card-product-image {
  width: 100%;
  margin-top: 20px;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .card-product {
    background: #1D1D1F;
  }
}
```

### 3.2 特性卡片

用于展示产品特性：

```css
.card-feature {
  border-radius: 20px;
  overflow: hidden;
  background: var(--color-bg-primary);
  padding: 48px 32px;
}

.card-feature-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
}

.card-feature-title {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.21;
  letter-spacing: -0.015em;
  color: var(--color-text-primary);
}

.card-feature-desc {
  font-size: 17px;
  font-weight: 400;
  line-height: 1.33;
  color: var(--color-text-secondary);
  margin-top: 12px;
}
```

### 3.3 统计卡片

用于展示数据/统计：

```css
.card-stat {
  text-align: center;
  padding: 32px 24px;
}

.card-stat-value {
  font-size: 56px;
  font-weight: 300;
  line-height: 1.05;
  letter-spacing: -0.022em;
  color: var(--color-text-primary);
}

.card-stat-label {
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-secondary);
  margin-top: 8px;
}
```

---

## 4. 表单（Forms）

### 4.1 输入框

```css
.input {
  width: 100%;
  padding: 11px 16px;
  font-family: var(--font-system);
  font-size: 17px;
  font-weight: 400;
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  outline: none;
  transition: border-color 100ms linear,
              box-shadow 100ms linear;
}

.input::placeholder {
  color: var(--color-text-tertiary);
}

.input:focus {
  border-color: #0071E3;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}

/* 错误态 */
.input-error {
  border-color: #FF3B30;
}

.input-error:focus {
  border-color: #FF3B30;
  box-shadow: 0 0 0 3px rgba(255, 59, 48, 0.15);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .input {
    background: #1D1D1F;
    border-color: #424245;
    color: #F5F5F7;
  }

  .input:focus {
    border-color: #2997FF;
    box-shadow: 0 0 0 3px rgba(41, 151, 255, 0.15);
  }
}
```

### 4.2 搜索框

Apple.com 风格搜索框：

```css
.search-input {
  width: 100%;
  padding: 10px 16px 10px 40px;
  font-family: var(--font-system);
  font-size: 17px;
  font-weight: 400;
  color: var(--color-text-primary);
  background: rgba(255, 255, 255, 0.85);
  -webkit-backdrop-filter: blur(40px);
  backdrop-filter: blur(40px);
  border: none;
  border-radius: 8px;
  outline: none;
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  opacity: 0.5;
}
```

### 4.3 标签/芯片

```css
.chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 400;
  color: var(--color-text-primary);
  background: var(--color-bg-elevated);
  border: none;
  border-radius: 980px; /* 全圆角 */
  cursor: pointer;
  transition: background 100ms linear;
}

.chip:hover {
  background: var(--color-border-subtle);
}

.chip-active {
  background: var(--color-text-primary);
  color: var(--color-bg-primary);
}
```

---

## 5. 分隔线（Dividers）

```css
.divider {
  border: none;
  border-top: 1px solid var(--color-border-subtle);
  margin: 24px 0;
}

.divider-strong {
  border-top-color: var(--color-border);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .divider {
    border-top-color: #333336;
  }
  .divider-strong {
    border-top-color: #424245;
  }
}
```

---

## 6. 标签页（Tabs）

### 6.1 水平标签页

```css
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid var(--color-border-subtle);
}

.tab-item {
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-secondary);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all 100ms linear;
}

.tab-item:hover {
  color: var(--color-text-primary);
}

.tab-item-active {
  color: var(--color-text-primary);
  border-bottom-color: #0071E3;
  font-weight: 500;
}
```

### 6.2 药丸标签页（Pill Tabs）

Apple.com 产品页常见的标签切换：

```css
.pill-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pill-tab {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-secondary);
  background: var(--color-bg-elevated);
  border: none;
  border-radius: 980px;
  cursor: pointer;
  transition: all 100ms linear;
}

.pill-tab:hover {
  color: var(--color-text-primary);
}

.pill-tab-active {
  color: #FFFFFF;
  background: var(--color-text-primary);
}
```

---

## 7. 模态框（Modal）

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 3000;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 350ms ease;
}

.modal-overlay-open {
  opacity: 1;
}

.modal-content {
  background: var(--color-bg-primary);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.16);
  max-width: 520px;
  width: calc(100% - 32px);
  max-height: calc(100vh - 80px);
  overflow-y: auto;
  transform: scale(0.95) translateY(10px);
  transition: transform 350ms ease;
}

.modal-overlay-open .modal-content {
  transform: scale(1) translateY(0);
}

.modal-header {
  padding: 24px 24px 0;
}

.modal-title {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.21;
  color: var(--color-text-primary);
}

.modal-body {
  padding: 16px 24px;
}

.modal-footer {
  padding: 0 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .modal-overlay {
    background: rgba(0, 0, 0, 0.6);
  }

  .modal-content {
    background: #1D1D1F;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  }
}
```

---

## 8. Toast / 通知

```css
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.6);
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-primary);
  z-index: 4000;
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
  transition: opacity 350ms ease,
              transform 350ms ease;
}

.toast-visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .toast {
    background: rgba(29, 29, 31, 0.6);
    color: #F5F5F7;
  }
}
```

---

## 9. 页脚（Footer）

Apple.com 风格页脚：

```css
.footer {
  background: var(--color-bg-secondary);
  padding: 20px 0;
  font-size: 12px;
  color: var(--color-text-tertiary);
  line-height: 1.47;
}

.footer-inner {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 页脚导航 */
.footer-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 16px 0;
  border-top: 1px solid var(--color-border-subtle);
}

.footer-nav-column {
  flex: 1;
  min-width: 140px;
}

.footer-nav-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.footer-nav-link {
  display: block;
  font-size: 12px;
  color: var(--color-text-secondary);
  text-decoration: none;
  padding: 4px 0;
}

.footer-nav-link:hover {
  text-decoration: underline;
  color: var(--color-text-primary);
}

/* 页脚底部 */
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--color-border-subtle);
}

.footer-legal {
  font-size: 12px;
  color: var(--color-text-tertiary);
}
```

---

## 10. 列表项（List Items）

### 10.1 设置列表

Apple 风格的设置列表（类似 iOS Settings app）：

```css
.list-group {
  background: var(--color-bg-primary);
  border-radius: 12px;
  overflow: hidden;
}

.list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  min-height: 44px; /* 最小触摸目标 */
  text-decoration: none;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border-subtle);
}

.list-item:last-child {
  border-bottom: none;
}

.list-item-label {
  font-size: 17px;
  font-weight: 400;
}

.list-item-value {
  font-size: 17px;
  color: var(--color-text-tertiary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.list-item-chevron::after {
  content: '';
  display: inline-block;
  width: 7px;
  height: 7px;
  border-top: 1.5px solid var(--color-text-tertiary);
  border-right: 1.5px solid var(--color-text-tertiary);
  transform: rotate(45deg);
}
```

### 10.2 开关（Toggle）

```css
.toggle {
  position: relative;
  width: 51px;
  height: 31px;
  appearance: none;
  -webkit-appearance: none;
  background: var(--color-border);
  border-radius: 980px;
  cursor: pointer;
  transition: background 200ms ease;
}

.toggle::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 27px;
  height: 27px;
  background: #FFFFFF;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: transform 200ms ease;
}

.toggle:checked {
  background: #34C759;
}

.toggle:checked::before {
  transform: translateX(20px);
}

.toggle:focus-visible {
  outline: 2px solid #0071E3;
  outline-offset: 2px;
}
```

---

## 11. 进度指示器

### 11.1 线性进度条

```css
.progress-bar {
  width: 100%;
  height: 4px;
  background: var(--color-border-subtle);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: #0071E3;
  border-radius: 2px;
  transition: width 350ms ease;
}
```

### 11.2 骨架屏（Skeleton）

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-elevated) 25%,
    var(--color-bg-tertiary) 50%,
    var(--color-bg-elevated) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease infinite;
  border-radius: 8px;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 骨架屏形状 */
.skeleton-text {
  height: 17px;
  margin-bottom: 8px;
}

.skeleton-text-short {
  width: 60%;
}

.skeleton-title {
  height: 32px;
  width: 40%;
  margin-bottom: 16px;
}

.skeleton-image {
  width: 100%;
  aspect-ratio: 16/10;
}

/* 尊重减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: var(--color-bg-elevated);
  }
}
```

---

## 12. 组件状态速查

所有可交互组件应支持以下状态：

| 状态 | 触发 | 视觉表现 |
|---|---|---|
| Default | 默认 | 标准样式 |
| Hover | 鼠标悬停 | 轻微视觉增强（颜色加深/透明度变化） |
| Active | 按下 | 轻微缩小 `scale(0.97)` 或颜色加深 |
| Focus | 键盘聚焦 | 蓝色聚焦环 `outline: 2px solid #0071E3` |
| Disabled | 禁用 | 降低透明度 `opacity: 0.32`，禁止交互 |
| Loading | 加载中 | 骨架屏或 spinner |
| Error | 错误 | 红色边框/文字 `#FF3B30` |
| Success | 成功 | 绿色指示 `#34C759` |
