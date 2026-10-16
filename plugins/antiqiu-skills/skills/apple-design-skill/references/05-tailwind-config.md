# Tailwind CSS 配置参考

> 将 Apple 设计语言的 Design Tokens 映射为 Tailwind CSS 配置，实现开箱即用的 Apple 风格开发。

---

## 1. tailwind.config.js 完整配置

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,ts,jsx,tsx}'],

  theme: {
    /* ── 颜色映射（apple 命名空间） ── */
    colors: {
      apple: {
        // 前景/文字
        text: {
          DEFAULT:     '#1D1D1F',  // 主文字
          secondary:   '#6E6E73',  // 次要文字
          tertiary:    '#86868B',  // 辅助文字
        },

        // 背景
        bg: {
          DEFAULT:     '#FFFFFF',  // 主背景
          secondary:   '#F5F5F7',  // 区块背景
          tertiary:    '#FBFBFD',  // 悬浮背景
          elevated:    '#F0F0F0',  // 浮层/卡片背景
        },

        // 分隔线/边框
        border: {
          DEFAULT:     '#D2D2D7',  // 常规边框
          subtle:      '#ECECF0',  // 淡边框
        },

        // 品牌色/交互色
        link: {
          DEFAULT:     '#0071E3',  // 链接蓝
          hover:       '#0077ED',  // 链接悬浮
          active:      '#006EDB',  // 链接激活
        },
        accent: {
          blue:        '#2997FF',  // 蓝色强调
        },

        // 深色模式专用
        dark: {
          bg:          '#000000',  // 深色主背景
          elevated:    '#1D1D1F',  // 深色浮层
          surface:     '#272729',  // 深色表面
          text:        '#F5F5F7',  // 深色主文字
          'text-secondary': '#A1A1A6', // 深色次要文字
          link:        '#2997FF',  // 深色链接蓝
        },

        // 状态色（HIG 系统色）
        red:          '#FF3B30',
        orange:       '#FF9500',
        yellow:       '#FFCC00',
        green:        '#34C759',
        teal:         '#5AC8FA',
        purple:       '#AF52DE',
        pink:         '#FF2D55',
      },
    },

    /* ── 字体族 ── */
    fontFamily: {
      system: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"SF Pro Text"',
        '"Helvetica Neue"',
        'Helvetica',
        'Arial',
        'sans-serif',
      ],
      cn: [
        '"PingFang SC"',
        '"SF Pro SC"',
        '"Apple PingFang SC Fallback"',
        '"Noto Sans SC"',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
      ],
      mono: [
        '"SF Mono"',
        'Menlo',
        'Consolas',
        'monospace',
      ],
    },

    /* ── 字号阶梯 ── */
    fontSize: {
      'xs':    ['12px', { lineHeight: '1.47' }],   // 注脚/标签
      'sm':    ['14px', { lineHeight: '1.33' }],   // 辅助文字
      'base':  ['17px', { lineHeight: '1.33' }],   // 基础正文
      'md':    ['21px', { lineHeight: '1.33' }],   // 大正文/引言
      'lg':    ['24px', { lineHeight: '1.21' }],   // 强调文字
      'xl':    ['28px', { lineHeight: '1.21' }],   // 段落标题
      '2xl':   ['32px', { lineHeight: '1.1' }],    // 小节标题
      '3xl':   ['40px', { lineHeight: '1.1' }],    // 卡片标题
      '4xl':   ['48px', { lineHeight: '1.05' }],   // 卡片大标题
      '5xl':   ['56px', { lineHeight: '1.05' }],   // 三级标题
      '6xl':   ['64px', { lineHeight: '1.05' }],   // 二级标题
      '7xl':   ['80px', { lineHeight: '1.0' }],    // 一级标题
      '8xl':   ['96px', { lineHeight: '1.0' }],    // Hero 大标题
    },

    /* ── 断点（Apple 4 级断点） ── */
    screens: {
      xs:   '320px',   // 小手机
      sm:   '735px',   // 手机/小平板
      md:   '1068px',  // 平板/小桌面
      lg:   '1441px',  // 大桌面
    },

    /* ── 圆角 ── */
    borderRadius: {
      sm:   '8px',     // 按钮、小卡片
      md:   '12px',    // 卡片、模态框
      lg:   '20px',    // 大面板
      xl:   '28px',    // 全宽卡片
      pill: '980px',   // 全圆角/药丸形按钮
      full: '50%',     // 头像、图标
    },

    /* ── 扩展（不覆盖 Tailwind 默认值） ── */
    extend: {
      /* backdrop blur — 毛玻璃效果 */
      backdropBlur: {
        glass:  '20px',   // 导航栏
        panel:  '40px',   // 浮层
        toast:  '2px',    // 通知/Toast
      },
      backdropSaturate: {
        apple: '180%',    // Apple 标志性饱和度增强
      },

      /* motion utilities: detailed standards live in references/07-motion.md */
      transitionDuration: {
        immediate: '50ms',
        instant:   '100ms',
        fast:      '150ms',
        standard:  '200ms',
        content:   '300ms',
        modal:     '350ms',
        large:     '500ms',
        hero:      '600ms',
        loop:      '1500ms',
      },

      /* motion easing */
      transitionTimingFunction: {
        'apple-linear':     'linear',
        'apple-standard':   'cubic-bezier(0.25, 0.1, 0.25, 1)',
        'apple-emphasized': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'apple-enter':      'cubic-bezier(0, 0, 0.2, 1)',
        'apple-exit':       'cubic-bezier(0.4, 0, 1, 1)',
        'apple-productive': 'cubic-bezier(0.2, 0, 0.38, 0.9)',
        'apple-expressive': 'cubic-bezier(0.4, 0.14, 0.3, 1)',
        'apple-spring':     'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
      },

      /* letter spacing */
      letterSpacing: {
        tighter: '-0.022em',  // Display 大标题
        tight:   '-0.015em',  // 标题
        wide:    '0.011em',   // 大写/标签
      },

      /* box shadow */
      boxShadow: {
        card:     '0 2px 8px rgba(0, 0, 0, 0.08)',
        elevated: '0 4px 16px rgba(0, 0, 0, 0.12)',
        modal:    '0 8px 32px rgba(0, 0, 0, 0.16)',
        nav:      '0 1px 0 rgba(0, 0, 0, 0.08)',
      },

      /* spacing — Apple 间距阶梯 */
      spacing: {
        4.5: '4px',     // xs
        18:  '18px',    // sm+md 之间
      },

      /* max width */
      maxWidth: {
        content: '980px',     // 桌面内容最大宽度
        'content-sm': '692px', // 平板内容最大宽度
      },

      /* height */
      height: {
        nav: '44px',    // 导航栏高度
        'nav-mobile': '48px', // 移动导航栏高度
      },

      /* aspect ratio */
      aspectRatio: {
        apple: '16 / 10',  // Apple 产品图常用比例
      },
    },
  },

  plugins: [],
};
```

---

## 2. CSS 变量版本（:root 定义）

以下为完整的 CSS 变量定义，与 Tailwind 配置对应，可在非 Tailwind 项目中直接使用：

```css
:root {
  /* ══════════════════════════════════════
   *  Apple Design Tokens — CSS 变量版
   * ══════════════════════════════════════ */

  /* ── 色彩 ── */
  --apple-text:             #1D1D1F;
  --apple-text-secondary:   #6E6E73;
  --apple-text-tertiary:    #86868B;

  --apple-bg:               #FFFFFF;
  --apple-bg-secondary:     #F5F5F7;
  --apple-bg-tertiary:      #FBFBFD;
  --apple-bg-elevated:      #F0F0F0;

  --apple-border:           #D2D2D7;
  --apple-border-subtle:    #ECECF0;

  --apple-link:             #0071E3;
  --apple-link-hover:       #0077ED;
  --apple-link-active:      #006EDB;
  --apple-accent-blue:      #2997FF;

  --apple-red:              #FF3B30;
  --apple-orange:           #FF9500;
  --apple-yellow:           #FFCC00;
  --apple-green:            #34C759;
  --apple-teal:             #5AC8FA;
  --apple-purple:           #AF52DE;
  --apple-pink:             #FF2D55;

  /* ── 排版 ── */
  --apple-font-system:      -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --apple-font-cn:          "PingFang SC", "SF Pro SC", "Apple PingFang SC Fallback", "Noto Sans SC", "Helvetica Neue", Arial, sans-serif;
  --apple-font-mono:        "SF Mono", Menlo, Consolas, monospace;

  --apple-text-xs:          12px;
  --apple-text-sm:          14px;
  --apple-text-base:        17px;
  --apple-text-md:          21px;
  --apple-text-lg:          24px;
  --apple-text-xl:          28px;
  --apple-text-2xl:         32px;
  --apple-text-3xl:         40px;
  --apple-text-4xl:         48px;
  --apple-text-5xl:         56px;
  --apple-text-6xl:         64px;
  --apple-text-7xl:         80px;
  --apple-text-8xl:         96px;

  --apple-font-light:       300;
  --apple-font-regular:     400;
  --apple-font-medium:      500;
  --apple-font-semibold:    600;
  --apple-font-bold:        700;

  --apple-leading-none:     1.0;
  --apple-leading-tight:    1.05;
  --apple-leading-snug:     1.1;
  --apple-leading-normal:   1.21;
  --apple-leading-relaxed:  1.33;
  --apple-leading-loose:    1.47;
  --apple-leading-cn-body:  1.8;

  --apple-tracking-tighter: -0.022em;
  --apple-tracking-tight:   -0.015em;
  --apple-tracking-normal:  0em;
  --apple-tracking-wide:    0.011em;

  /* ── 间距 ── */
  --apple-space-xs:         4px;
  --apple-space-sm:         8px;
  --apple-space-md:         12px;
  --apple-space-lg:         20px;
  --apple-space-xl:         24px;
  --apple-space-2xl:        32px;
  --apple-space-3xl:        40px;
  --apple-space-4xl:        48px;
  --apple-space-5xl:        64px;
  --apple-space-6xl:        80px;
  --apple-space-7xl:        96px;

  /* ── 断点（CSS 无法直接使用，仅作记录） ── */
  /* xs: 320px | sm: 735px | md: 1068px | lg: 1441px */

  /* ── 圆角 ── */
  --apple-radius-sm:        8px;
  --apple-radius-md:        12px;
  --apple-radius-lg:        20px;
  --apple-radius-xl:        28px;
  --apple-radius-pill:      980px;
  --apple-radius-full:      50%;

  /* ── 阴影 ── */
  --apple-shadow-card:      0 2px 8px rgba(0, 0, 0, 0.08);
  --apple-shadow-elevated:  0 4px 16px rgba(0, 0, 0, 0.12);
  --apple-shadow-modal:     0 8px 32px rgba(0, 0, 0, 0.16);
  --apple-shadow-nav:       0 1px 0 rgba(0, 0, 0, 0.08);

  /* ── 毛玻璃 ── */
  --apple-blur-glass:       20px;
  --apple-blur-panel:       40px;
  --apple-blur-toast:       2px;
  --apple-saturate-glass:   180%;

  /* ── Motion tokens ── */
  /* 完整动画规范见 references/07-motion.md；此处仅提供 CSS 变量入口 */
  --apple-motion-duration-immediate: 50ms;
  --apple-motion-duration-instant:   100ms;
  --apple-motion-duration-fast:      150ms;
  --apple-motion-duration-standard:  200ms;
  --apple-motion-duration-content:   300ms;
  --apple-motion-duration-modal:     350ms;
  --apple-motion-duration-large:     500ms;
  --apple-motion-duration-hero:      600ms;
  --apple-motion-duration-loop:      1500ms;

  --apple-motion-ease-linear:        linear;
  --apple-motion-ease-standard:      cubic-bezier(0.25, 0.1, 0.25, 1);
  --apple-motion-ease-emphasized:    cubic-bezier(0.4, 0, 0.2, 1);
  --apple-motion-ease-enter:         cubic-bezier(0, 0, 0.2, 1);
  --apple-motion-ease-exit:          cubic-bezier(0.4, 0, 1, 1);
  --apple-motion-ease-productive:    cubic-bezier(0.2, 0, 0.38, 0.9);
  --apple-motion-ease-expressive:    cubic-bezier(0.4, 0.14, 0.3, 1);
  --apple-motion-ease-spring:        cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* ── 布局 ── */
  --apple-max-content:      980px;
  --apple-max-content-sm:   692px;
  --apple-nav-height:       44px;
  --apple-nav-height-mobile: 48px;
}

/* ── Dark Mode ── */
@media (prefers-color-scheme: dark) {
  :root {
    --apple-text:             #F5F5F7;
    --apple-text-secondary:   #A1A1A6;
    --apple-text-tertiary:    #86868B;

    --apple-bg:               #000000;
    --apple-bg-secondary:     #1D1D1F;
    --apple-bg-tertiary:      #161617;
    --apple-bg-elevated:      #272729;

    --apple-border:           #424245;
    --apple-border-subtle:    #333336;

    --apple-link:             #2997FF;
    --apple-link-hover:       #547EAE;
  }
}

/* ── 增强对比度 ── */
@media (prefers-contrast: more) {
  :root {
    --apple-text:             #000000;
    --apple-text-secondary:   #424245;
    --apple-text-tertiary:    #515154;
    --apple-border:           #86868B;
  }
}
```

---

## 3. Tailwind 使用示例

```html
<!-- Hero 区 -->
<section class="text-center py-20 md:py-24 lg:py-40">
  <h1 class="font-system text-4xl md:text-7xl lg:text-8xl font-light tracking-tighter leading-none">
    iPhone 16 Pro
  </h1>
  <p class="font-system text-md md:text-lg mt-4 text-apple-text-secondary">
    你好，Apple Intelligence。
  </p>
  <div class="mt-6 flex justify-center gap-4">
    <a href="#" class="inline-block px-4 py-2 text-sm text-white bg-apple-link rounded-pill hover:bg-apple-link-hover transition-instant">
      立即购买
    </a>
    <a href="#" class="inline-flex items-center gap-1 text-lg text-apple-link hover:underline">
      进一步了解 <span aria-hidden="true">→</span>
    </a>
  </div>
</section>

<!-- 导航栏 -->
<header class="sticky top-0 z-[9999] h-nav bg-white/72 backdrop-blur-glass backdrop-saturate-apple border-b border-black/8">
  <nav class="max-w-content mx-auto flex items-center justify-between h-full px-4.5">
    <a href="/" aria-label="Apple 首页">
      <svg class="w-5 h-5" aria-hidden="true"><!-- Apple Logo --></svg>
    </a>
    <ul class="hidden sm:flex items-center gap-8">
      <li><a class="text-xs opacity-80 hover:opacity-100 transition-instant">商店</a></li>
      <li><a class="text-xs opacity-80 hover:opacity-100 transition-instant">Mac</a></li>
      <li><a class="text-xs opacity-80 hover:opacity-100 transition-instant">iPad</a></li>
      <li><a class="text-xs opacity-80 hover:opacity-100 transition-instant">iPhone</a></li>
    </ul>
  </nav>
</header>

<!-- 产品卡片 -->
<article class="bg-apple-bg-secondary rounded-lg overflow-hidden hover:scale-[1.02] hover:shadow-elevated transition-fast">
  <img src="product.jpg" alt="产品图片" class="w-full" />
  <div class="p-6">
    <h3 class="text-xl font-semibold tracking-tight">产品名称</h3>
    <p class="text-sm text-apple-text-secondary mt-2">产品描述文字</p>
    <a href="#" class="inline-flex items-center gap-1 text-apple-link mt-4 text-sm">
      进一步了解 <span aria-hidden="true">→</span>
    </a>
  </div>
</article>

<!-- 毛玻璃面板 -->
<div class="bg-white/85 backdrop-blur-panel rounded-lg shadow-modal p-8">
  <h2 class="text-2xl font-semibold tracking-tight">面板标题</h2>
  <p class="text-base text-apple-text-secondary mt-4">面板内容</p>
</div>
```

---

## 4. 与主规范文件的对应关系

| Tailwind 配置项 | 对应主规范章节 | 主规范文件 |
|---|---|---|
| `colors.apple.*` | 2.1 色彩系统 | `apple-design-language.md` |
| `fontFamily.*` | 2.2 排版系统 — 字体族 | `apple-design-language.md` |
| `fontSize.*` | 2.2 排版系统 — 字号阶梯 | `apple-design-language.md` |
| `screens.*` | 2.3 间距与布局 — 断点 | `apple-design-language.md` |
| `borderRadius.*` | 2.4 圆角 | `apple-design-language.md` |
| `boxShadow.*` | 2.5 阴影与深度 | `apple-design-language.md` |
| `backdropBlur.*` | 2.6 毛玻璃/材质 | `apple-design-language.md` |
| `transitionDuration.*` | 07 Motion System | `references/07-motion.md` |
| `transitionTimingFunction.*` | 07 Motion System | `references/07-motion.md` |
| `letterSpacing.*` | 2.2 排版系统 — 字间距 | `apple-design-language.md` |
