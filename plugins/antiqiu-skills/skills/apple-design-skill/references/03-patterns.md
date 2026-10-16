# 页面布局模式 — Apple 风格页面结构

> 来源：Apple.com 页面结构分析（iPhone、Mac、iPad 产品页等）。
> 所有布局均基于 Apple.com 4 级断点系统（320/735/1068/1441px）。

---

## 1. 页面基础结构

### 1.1 标准 Apple.com 页面结构

```
┌─────────────────────────────────────────────────┐
│ 导航栏（sticky, 毛玻璃, 44px）                  │
├─────────────────────────────────────────────────┤
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ Hero 区                                     │ │
│ │ 产品名 + 副标题 + CTA + 产品图              │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ 特性双栏区                                   │ │
│ │ [卡片 A]  [卡片 B]                           │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ 全宽特性展示区                               │ │
│ │ 大图/视频 + 标题 + 描述                       │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│ │ 产品卡片 │ │ 产品卡片 │ │ 产品卡片 │        │
│ └──────────┘ └──────────┘ └──────────┘        │
│                                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ 对比/选购区                                  │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
├─────────────────────────────────────────────────┤
│ 页脚                                           │
└─────────────────────────────────────────────────┘
```

### 1.2 全局布局规则

```css
/* 页面基础 */
body {
  font-family: var(--font-system);
  font-size: 17px;
  line-height: 1.33;
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 内容容器 */
.container {
  max-width: 980px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 区块交替背景 */
.section-white { background: var(--color-bg-primary); }
.section-gray { background: var(--color-bg-secondary); }
```

---

## 2. Hero 区（首屏）

### 2.1 Hero 区布局模式

Apple.com 有两种主要 Hero 布局：

#### 模式 A：图片在上

```
┌──────────────────────────────────────┐
│           大标题（48-96px）           │
│          副标题（21-28px）           │
│      [主要按钮] [次要按钮 →]         │
│                                      │
│      ┌────────────────────┐          │
│      │                    │          │
│      │     产品图片        │          │
│      │                    │          │
│      └────────────────────┘          │
└──────────────────────────────────────┘
```

#### 模式 B：图片在下（深色背景）

```
┌──────────────────────────────────────┐
│ 背景色：深色/产品主题渐变             │
│                                      │
│      ┌────────────────────┐          │
│      │                    │          │
│      │     产品图片        │          │
│      │                    │          │
│      └────────────────────┘          │
│           大标题（白字）              │
│          副标题（白字）              │
│      [主要按钮] [次要按钮 →]         │
└──────────────────────────────────────┘
```

### 2.2 Hero 区实现

```css
.hero {
  text-align: center;
  padding: 80px 24px 0;
  overflow: hidden;
  position: relative;
}

.hero-title {
  font-size: clamp(40px, 7vw, 80px);
  font-weight: 300;
  line-height: 1.05;
  letter-spacing: -0.022em;
  color: var(--color-text-primary);
}

.hero-subtitle {
  font-size: clamp(21px, 2.5vw, 28px);
  font-weight: 400;
  line-height: 1.33;
  color: var(--color-text-secondary);
  margin-top: 12px;
}

.hero-price {
  font-size: 17px;
  font-weight: 400;
  color: var(--color-text-secondary);
  margin-top: 16px;
}

.hero-cta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-top: 20px;
}

.hero-image {
  max-width: 100%;
  margin-top: 40px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

/* 深色 Hero */
.hero-dark {
  background: #000000;
  color: #F5F5F7;
}

.hero-dark .hero-title {
  color: #F5F5F7;
}

.hero-dark .hero-subtitle {
  color: #A1A1A6;
}

/* 响应式 */
@media (max-width: 734px) {
  .hero {
    padding: 40px 16px 0;
  }

  .hero-cta {
    flex-direction: column;
    gap: 12px;
  }
}
```

---

## 3. 双栏特性展示

### 3.1 双栏布局

Apple.com 最经典的布局模式——两个等宽卡片并排：

```
┌─────────────────────┐ ┌─────────────────────┐
│                     │ │                     │
│   产品图/动画       │ │   产品图/动画       │
│                     │ │                     │
│   标题              │ │   标题              │
│   副标题            │ │   副标题            │
│   [了解更多 →]      │ │   [了解更多 →]      │
│                     │ │                     │
└─────────────────────┘ └─────────────────────┘
 桌面：两列等宽，间距 12px
 移动：单列堆叠，间距 12px
 卡片圆角 20px，深色/浅色背景可交替
```

### 3.2 双栏实现

```css
.section-dual {
  padding: 12px;
}

.dual-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  max-width: 980px;
  margin: 0 auto;
}

/* 响应式：移动端单列 */
@media (max-width: 734px) {
  .dual-grid {
    grid-template-columns: 1fr;
  }
}

/* 卡片内容 */
.dual-card {
  border-radius: 20px;
  overflow: hidden;
  background: var(--color-bg-secondary);
  text-align: center;
  padding: 40px 24px 0;
  min-height: 500px;
}

.dual-card-title {
  font-size: clamp(28px, 4vw, 40px);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.015em;
}

.dual-card-subtitle {
  font-size: 17px;
  font-weight: 400;
  color: var(--color-text-secondary);
  margin-top: 8px;
}

.dual-card-cta {
  margin-top: 16px;
}

.dual-card-image {
  width: 100%;
  margin-top: 20px;
}

/* 深色卡片变体 */
.dual-card-dark {
  background: #000000;
  color: #F5F5F7;
}

.dual-card-dark .dual-card-subtitle {
  color: #A1A1A6;
}
```

---

## 4. 三栏网格

### 4.1 三栏产品展示

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ 图片     │ │ 图片     │ │ 图片     │
│ 标题     │ │ 标题     │ │ 标题     │
│ 描述     │ │ 描述     │ │ 描述     │
│ [链接 →] │ │ [链接 →] │ │ [链接 →] │
└──────────┘ └──────────┘ └──────────┘
```

### 4.2 三栏实现

```css
.section-grid {
  padding: 80px 24px;
  max-width: 980px;
  margin: 0 auto;
}

.grid-three {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

@media (max-width: 1068px) {
  .grid-three {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 734px) {
  .grid-three {
    grid-template-columns: 1fr;
  }
}

.grid-card {
  border-radius: 20px;
  overflow: hidden;
  background: var(--color-bg-secondary);
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.grid-card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.grid-card-image {
  width: 100%;
  aspect-ratio: 4/3;
  object-fit: cover;
}

.grid-card-content {
  padding: 24px;
}

.grid-card-title {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.33;
}

.grid-card-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-top: 8px;
}

.grid-card-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #0071E3;
  margin-top: 12px;
}
```

---

## 5. 全宽特性展示区

### 5.1 带图标的特性列表

```
┌──────────────────────────────────────────────┐
│                                              │
│    ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐    │
│    │◕ │  │◕ │  │◕ │  │◕ │  │◕ │  │◕ │    │
│    └──┘  └──┘  └──┘  └──┘  └──┘  └──┘    │
│    标题1  标题2  标题3  标题4  标题5  标题6  │
│    副标1  副标2  副标3  副标4  副标5  副标6  │
│                                              │
└──────────────────────────────────────────────┘
```

### 5.2 特性网格实现

```css
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 32px;
  text-align: center;
  padding: 80px 24px;
  max-width: 980px;
  margin: 0 auto;
}

.feature-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
}

.feature-label {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.33;
  color: var(--color-text-primary);
}

.feature-value {
  font-size: 14px;
  font-weight: 400;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

@media (max-width: 734px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    padding: 40px 16px;
  }
}
```

---

## 6. 全宽图文区

### 6.1 左文右图

```
┌──────────────────────────────────────┐
│                                      │
│  ┌──────────────┐  ┌──────────────┐ │
│  │              │  │              │ │
│  │  大标题      │  │              │ │
│  │  副标题      │  │   产品图片   │ │
│  │  描述文字    │  │              │ │
│  │  [了解更多→] │  │              │ │
│  │              │  │              │ │
│  └──────────────┘  └──────────────┘ │
│                                      │
└──────────────────────────────────────┘
```

### 6.2 左文右图实现

```css
.split-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 48px;
  padding: 80px 24px;
  max-width: 980px;
  margin: 0 auto;
}

.split-text-title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.015em;
}

.split-text-desc {
  font-size: 17px;
  font-weight: 400;
  line-height: 1.33;
  color: var(--color-text-secondary);
  margin-top: 16px;
}

.split-image {
  width: 100%;
  border-radius: 20px;
}

/* 右文左图 — 反转 */
.split-reverse {
  direction: rtl;
}

.split-reverse > * {
  direction: ltr;
}

/* 响应式：移动端堆叠 */
@media (max-width: 734px) {
  .split-section {
    grid-template-columns: 1fr;
    gap: 32px;
    padding: 40px 16px;
  }

  .split-reverse {
    direction: ltr;
  }
}
```

---

## 7. 滚动动画

### 7.1 进入动画（Scroll Reveal）

Apple.com 使用 IntersectionObserver 触发滚动进入动画：

```js
/**
 * Apple 风格滚动进入动画
 * 元素从下方淡入，进入视口时触发
 */
function initScrollReveal() {
  const elements = document.querySelectorAll('[data-reveal]');

  // 尊重减少动画偏好
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    elements.forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px',
    }
  );

  elements.forEach(el => observer.observe(el));
}
```

### 7.2 动画 CSS

```css
/* 滚动进入动画基础状态 */
[data-reveal] {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 600ms ease, transform 600ms ease;
}

/* 进入后状态 */
[data-reveal].revealed {
  opacity: 1;
  transform: translateY(0);
}

/* 延迟变体 */
[data-reveal-delay="1"] { transition-delay: 100ms; }
[data-reveal-delay="2"] { transition-delay: 200ms; }
[data-reveal-delay="3"] { transition-delay: 300ms; }

/* 缩放进入 */
[data-reveal="scale"] {
  transform: scale(0.95);
}
[data-reveal="scale"].revealed {
  transform: scale(1);
}

/* 尊重减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

---

## 8. 深色/浅色背景交替

Apple.com 使用深色和浅色背景交替来创建视觉节奏：

```css
/* 交替区块模式 */
.section-light {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.section-alt {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
}

.section-dark {
  background: #000000;
  color: #F5F5F7;
}

.section-dark h2,
.section-dark h3 {
  color: #F5F5F7;
}

.section-dark p {
  color: #A1A1A6;
}

.section-dark a {
  color: #2997FF;
}

.section-dark a:hover {
  color: #547EAE;
}
```

### 典型页面节奏

```
导航栏（毛玻璃）
    ↓
Hero 区（白色背景）
    ↓
双栏特性区（灰色背景卡片）
    ↓
全宽特性展示（白色背景）
    ↓
深色沉浸区（黑色背景 + 产品大图）
    ↓
三栏产品网格（灰色背景）
    ↓
选购引导区（白色背景）
    ↓
页脚（灰色背景）
```

---

## 9. 页面间距系统

### 9.1 区块间距

```css
/* 区块间垂直间距 */
.section {
  padding: 80px 0;
}

.section + .section {
  padding: 80px 0;
}

/* Hero 区更大间距 */
.section-hero {
  padding: 80px 0 0;
}

/* 小区块间距 */
.section-compact {
  padding: 40px 0;
}

/* 响应式间距 */
@media (max-width: 1068px) {
  .section { padding: 60px 0; }
  .section-hero { padding: 60px 0 0; }
}

@media (max-width: 734px) {
  .section { padding: 40px 0; }
  .section-hero { padding: 40px 0 0; }
}
```

### 9.2 元素间距规则

```css
/* 标题到副标题 */
.title-to-subtitle { margin-top: 12px; }

/* 副标题到正文 */
.subtitle-to-body { margin-top: 16px; }

/* 正文到 CTA */
.body-to-cta { margin-top: 20px; }

/* CTA 到图片 */
.cta-to-image { margin-top: 40px; }

/* 图片到下一区块 */
.image-to-section { margin-top: 80px; }
```

---

## 10. 移动端适配

### 10.1 移动端排版缩放

```css
/* 响应式排版 — 使用 clamp() */
.text-hero {
  font-size: clamp(40px, 8vw, 80px);
}

.text-section-title {
  font-size: clamp(28px, 5vw, 48px);
}

.text-card-title {
  font-size: clamp(24px, 4vw, 40px);
}

.text-body {
  font-size: clamp(14px, 2vw, 17px);
}
```

### 10.2 移动端布局调整

```css
/* 移动端隐藏/显示 */
@media (max-width: 734px) {
  /* 隐藏桌面导航，显示汉堡菜单 */
  .nav-desktop { display: none; }
  .nav-mobile { display: block; }

  /* 单列布局 */
  .grid-multi { grid-template-columns: 1fr; }

  /* 缩小间距 */
  .section { padding: 40px 16px; }

  /* 全宽图片 */
  .hero-image { width: calc(100% + 32px); margin-left: -16px; }

  /* 堆叠 CTA */
  .cta-group { flex-direction: column; align-items: center; }
}
```

### 10.3 触摸目标

```css
/* 确保所有可交互元素满足最小触摸目标 */
@media (pointer: coarse) {
  .interactive-element {
    min-height: 44px;
    min-width: 44px;
  }

  /* 增加链接间距 */
  .nav-links a {
    padding: 12px 16px;
  }

  /* 增加按钮内边距 */
  .btn-primary {
    padding: 12px 20px;
  }
}
```

---

## 11. 完整页面模板

### 11.1 产品页 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>产品名称 — Apple (示例)</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- 导航栏 -->
  <header class="navbar" role="banner">
    <div class="navbar-inner">
      <a href="/" aria-label="首页">
        <svg aria-hidden="true"><!-- Logo --></svg>
      </a>
      <nav aria-label="全局导航">
        <ul class="navbar-links">
          <li><a href="#">商店</a></li>
          <li><a href="#">Mac</a></li>
          <li><a href="#">iPad</a></li>
          <li><a href="#">iPhone</a></li>
        </ul>
      </nav>
      <div>
        <button aria-label="搜索"><!-- 搜索 --></button>
        <a href="#" aria-label="购物袋"><!-- 购物袋 --></a>
      </div>
    </div>
  </header>

  <main>
    <!-- Hero 区 -->
    <section class="section-hero" data-reveal>
      <div class="container text-center">
        <h1 class="hero-title">产品名称</h1>
        <p class="hero-subtitle">产品一句话描述。</p>
        <p class="hero-price">RMB XXXX 起</p>
        <div class="hero-cta">
          <a href="#" class="btn-primary">购买</a>
          <a href="#" class="btn-secondary">进一步了解 <span class="arrow"></span></a>
        </div>
        <img class="hero-image" src="product.jpg" alt="产品展示图" />
      </div>
    </section>

    <!-- 双栏特性区 -->
    <section class="section" style="background: var(--color-bg-secondary);">
      <div class="dual-grid">
        <div class="dual-card" data-reveal>
          <h2 class="dual-card-title">特性 A</h2>
          <p class="dual-card-subtitle">特性描述文字。</p>
          <a href="#" class="btn-secondary btn-secondary-sm dual-card-cta">了解更多 <span class="arrow"></span></a>
          <img class="dual-card-image" src="feature-a.jpg" alt="特性 A 展示" />
        </div>
        <div class="dual-card dual-card-dark" data-reveal>
          <h2 class="dual-card-title">特性 B</h2>
          <p class="dual-card-subtitle">特性描述文字。</p>
          <a href="#" class="btn-secondary btn-secondary-sm dual-card-cta">了解更多 <span class="arrow"></span></a>
          <img class="dual-card-image" src="feature-b.jpg" alt="特性 B 展示" />
        </div>
      </div>
    </section>

    <!-- 全宽深色区 -->
    <section class="section section-dark" data-reveal>
      <div class="container text-center">
        <h2 class="hero-title">亮点特性</h2>
        <p class="hero-subtitle">详细描述。</p>
        <img src="highlight.jpg" alt="亮点展示" style="width:100%; margin-top:40px; border-radius:20px;" />
      </div>
    </section>

    <!-- 三栏网格 -->
    <section class="section">
      <div class="grid-three container">
        <article class="grid-card" data-reveal>
          <img class="grid-card-image" src="item1.jpg" alt="" />
          <div class="grid-card-content">
            <h3 class="grid-card-title">产品 1</h3>
            <p class="grid-card-desc">产品描述。</p>
            <a href="#" class="grid-card-link">了解更多 →</a>
          </div>
        </article>
        <!-- 更多卡片... -->
      </div>
    </section>
  </main>

  <!-- 页脚 -->
  <footer class="footer">
    <div class="footer-inner">
      <!-- 页脚内容 -->
    </div>
  </footer>

  <script>
    // 滚动动画初始化
    // Focus 管理初始化
  </script>
</body>
</html>
```
