# Design Tokens — Apple 设计令牌

> 来源：Apple.com 主 CSS（1MB+ 样式表提取）、HIG 设计资源、Apple Style Guide。
> 所有数值均来自 Apple 实际产品 CSS 源码，非推测值。

---

## 1. 色彩系统

### 1.1 基础色板（Light Mode）

从 Apple.com CSS 提取的完整色值：

```css
:root {
  /* ── 前景/文字 ── */
  --color-text-primary:   #1D1D1F;   /* 主文字 — 近黑，非纯黑 */
  --color-text-secondary: #6E6E73;   /* 次要文字 — 中灰 */
  --color-text-tertiary:  #86868B;   /* 辅助文字/占位符 — 浅灰 */
  --color-text-quaternary:#AEAEB2;   /* 禁用态文字 — 更浅灰 */
  --color-text-inverse:   #FFFFFF;   /* 反色文字 — 用于深色背景 */

  /* ── 背景 ── */
  --color-bg-primary:     #FFFFFF;   /* 主背景 — 纯白 */
  --color-bg-secondary:   #F5F5F7;   /* 区块交替背景 — 微灰蓝（Apple 标志性背景色） */
  --color-bg-tertiary:    #FBFBFD;   /* 悬浮/高亮背景 */
  --color-bg-elevated:    #F0F0F0;   /* 浮层/卡片背景 */
  --color-bg-grouped:     #F2F2F7;   /* 分组列表背景 */

  /* ── 分隔线/边框 ── */
  --color-border:         #D2D2D7;   /* 常规边框 — 输入框、卡片 */
  --color-border-subtle:  #ECECF0;   /* 淡边框 — 轻量分隔线 */
  --color-border-strong:  #C7C7CC;   /* 强边框 — 表格、面板 */

  /* ── 品牌色/交互色 ── */
  --color-link:           #0071E3;   /* 链接蓝 — Apple.com 核心品牌色 */
  --color-link-hover:     #0077ED;   /* 链接悬浮态 */
  --color-link-active:    #006EDB;   /* 链接按下态 */
  --color-link-visited:   #6E6E73;   /* 已访问链接（部分场景） */
  --color-accent-blue:    #2997FF;   /* 强调蓝 — Dark Mode 链接色 */

  /* ── 填充色 ── */
  --color-fill-primary:   #0071E3;   /* 主要填充 — 主按钮 */
  --color-fill-secondary: #E8E8ED;   /* 次要填充 — 次按钮、标签背景 */
  --color-fill-tertiary:  #F5F5F7;   /* 三级填充 — hover 背景 */

  /* ── 状态色（HIG 系统色） ── */
  --color-red:            #FF3B30;   /* 错误、删除、危险 */
  --color-orange:         #FF9500;   /* 警告、提醒 */
  --color-yellow:         #FFCC00;   /* 注意、待处理 */
  --color-green:          #34C759;   /* 成功、确认、安全 */
  --color-teal:           #5AC8FA;   /* 信息、链接（辅助） */
  --color-blue:           #007AFF;   /* 信息、常规交互（iOS 系统蓝） */
  --color-purple:         #AF52DE;   /* 特殊标记、特色功能 */
  --color-pink:           #FF2D55;   /* 强调、社交、健康 */

  /* ── 渐变（Apple.com 实测） ── */
  --gradient-page: linear-gradient(to bottom, #F5F5F7 0%, #D4E6EC 40%, #E5E6DE 75%);
}
```

### 1.2 Dark Mode 色板

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* ── 文字 ── */
    --color-text-primary:   #F5F5F7;   /* 主文字 — 亮白 */
    --color-text-secondary: #A1A1A6;   /* 次要文字 */
    --color-text-tertiary:  #86868B;   /* 辅助文字（与 Light Mode 相同） */
    --color-text-quaternary:#636366;   /* 禁用态 */
    --color-text-inverse:   #000000;   /* 反色文字 */

    /* ── 背景 — 6 级黑度 ── */
    --color-bg-primary:     #000000;   /* 主背景 — 纯黑（Apple 不使用深灰背景） */
    --color-bg-secondary:   #1D1D1F;   /* 区块背景 */
    --color-bg-tertiary:    #2C2C2E;   /* 悬浮背景 */
    --color-bg-elevated:    #272729;   /* 浮层背景 */
    --color-bg-grouped:     #000000;   /* 分组背景 */

    /* ── 边框 ── */
    --color-border:         #424245;   /* 常规边框 */
    --color-border-subtle:  #333336;   /* 淡边框 */
    --color-border-strong:  #545458;   /* 强边框 */

    /* ── 链接/交互 ── */
    --color-link:           #2997FF;   /* 链接蓝 — Dark Mode 使用更亮的蓝 */
    --color-link-hover:     #547EAE;   /* 链接悬浮 */
    --color-link-active:    #2997FF;   /* 链接按下 */
    --color-accent-blue:    #2997FF;   /* 强调蓝 */

    /* ── 填充 ── */
    --color-fill-primary:   #2997FF;   /* 主按钮填充 */
    --color-fill-secondary: #2C2C2E;   /* 次按钮背景 */
    --color-fill-tertiary:  #1D1D1F;   /* hover 背景 */

    /* ── 状态色（Dark Mode 调亮版） ── */
    --color-red:            #FF453A;
    --color-orange:         #FF9F0A;
    --color-yellow:         #FFD60A;
    --color-green:          #30D158;
    --color-teal:           #64D2FF;
    --color-blue:           #0A84FF;
    --color-purple:         #BF5AF2;
    --color-pink:           #FF375F;
  }
}
```

### 1.3 色彩使用规则

| 规则 | 说明 | 示例 |
|---|---|---|
| 品牌蓝仅用于可交互元素 | `#0071E3` 只出现在链接、按钮、选中态 | 链接文字、主按钮背景、Tab 选中指示器 |
| 状态色仅用于语义 | 严格对应含义，不做装饰 | 红色仅用于错误/删除，绿色仅用于成功 |
| 文字最多 3 级灰度 | primary / secondary / tertiary，不混用自定义灰 | 不使用 `#999` 或 `#666` 等非规范灰色 |
| 深色模式不是简单反色 | 背景 6 级黑（#000 → #545458），前景 3 级白 | 不使用纯白背景 + 黑色文字 |
| 色彩对比度 | 正文 ≥ 4.5:1（WCAG AA），大标题 ≥ 3:1 | 使用对比度检查工具验证 |
| 背景交替 | `#FFFFFF` 与 `#F5F5F7` 交替使用，区分区块 | Hero 白色、特性区灰色、再白色 |
| 渐变极少使用 | 仅用于特殊 Hero 背景 | Apple.com 渐变：`linear-gradient(to bottom, #F5F5F7, #D4E6EC, #E5E6DE)` |

### 1.4 透明度系统

Apple.com CSS 中使用的 opacity 值（完整提取）：

```css
:root {
  --opacity-disabled:   0.32;  /* 禁用态 */
  --opacity-placeholder: 0.36; /* 占位符文字 */
  --opacity-bar-track:  0.42;  /* 进度条轨道 */
  --opacity-ghost:      0.56;  /* 幽灵元素/水印 */
  --opacity-secondary:   0.8;  /* 次要元素（导航链接默认态） */
  --opacity-full:       1.0;   /* 完全不透明 */
}
```

### 1.5 半透明背景值

```css
:root {
  /* Light Mode */
  --bg-glass-nav:      rgba(255, 255, 255, 0.72);  /* 导航栏 */
  --bg-glass-panel:    rgba(255, 255, 255, 0.85);  /* 浮层面板 */
  --bg-glass-toast:    rgba(255, 255, 255, 0.60);  /* Toast 通知 */
  --bg-glass-overlay:  rgba(255, 255, 255, 0.40);  /* 遮罩层 */

  /* Dark Mode */
  --bg-glass-nav-dark:      rgba(29, 29, 31, 0.72);
  --bg-glass-panel-dark:    rgba(29, 29, 31, 0.85);
  --bg-glass-toast-dark:    rgba(29, 29, 31, 0.60);
  --bg-glass-overlay-dark:  rgba(0, 0, 0, 0.50);
}
```

---

## 2. 排版系统

### 2.1 字体族

```css
:root {
  /* ── 英文/通用 ── */
  --font-system:
    "SF Pro Text",        /* 正文（≤20px） — 仅 Apple 域名可合法使用 */
    "SF Pro Display",     /* 标题（>20px） — 仅 Apple 域名可合法使用 */
    "SF Pro Icons",       /* 图标字体 */
    "Helvetica Neue",     /* 主回退 — 广泛可用 */
    "Helvetica",
    "Arial",
    sans-serif;

  /* ── 中文简体 ── */
  --font-cn:
    "PingFang SC",        /* Apple 设备系统字体 */
    "SF Pro SC",          /* Apple 中文字体 */
    "SF Pro Text",
    "SF Pro Icons",
    "Apple PingFang SC Fallback", /* 非 Apple 设备内置 fallback */
    "Noto Sans SC",       /* 跨平台中文回退（Google） */
    "Helvetica Neue",
    "Helvetica",
    "Arial",
    sans-serif;

  /* ── 中文繁体 ── */
  --font-tc:
    "SF Pro TC",
    "SF Pro Text",
    "PingFang TC",
    "Noto Sans TC",
    sans-serif;

  /* ── 日文 ── */
  --font-jp:
    "SF Pro JP",
    "SF Pro Text",
    "Hiragino Sans",
    "Noto Sans JP",
    sans-serif;

  /* ── 韩文 ── */
  --font-kr:
    "SF Pro KR",
    "SF Pro Text",
    "Apple SD Gothic Neo",
    "Noto Sans KR",
    sans-serif;

  /* ── 等宽/代码 ── */
  --font-mono:
    "SF Mono",
    "Menlo",              /* macOS 默认 */
    "Consolas",           /* Windows 默认 */
    "Source Code Pro",
    monospace;

  /* ── 系统字体栈（跨平台通用回退，非 Apple 专用） ── */
  --font-system-universal:
    -apple-system,        /* macOS/iOS 系统字体 */
    BlinkMacSystemFont,   /* macOS Chrome */
    "Segoe UI",           /* Windows */
    Roboto,               /* Android */
    "Helvetica Neue",
    "Noto Sans",          /* 跨平台 */
    Arial,
    sans-serif;
}
```

> **跨平台提示**：SF Pro 是 Apple 专有字体，Web 上仅 Apple 域名可合法加载。中文优先使用 Apple 设备系统 `PingFang SC`；非 Apple 设备需要统一中文观感时，可按 [06-fonts.md](06-fonts.md) 引入内置 `Apple PingFang SC Fallback`。

### 2.2 字号阶梯

从 Apple.com CSS 完整提取的字号值（按使用频率排序）：

```css
:root {
  /* ── Display / Hero 标题 ── */
  --text-9xl:  96px;    /* Hero 大标题（iPhone Pro Max "Titanium"） */
  --text-8xl:  80px;    /* 一级标题（产品名称） */
  --text-7xl:  64px;    /* 二级标题（产品特性标题） */
  --text-6xl:  56px;    /* 三级标题 */
  --text-5xl:  53px;    /* 区块标题（Apple.com 实测值，非标准 48px） */
  --text-4xl:  48px;    /* 卡片大标题 */
  --text-3xl:  40px;    /* 卡片标题 */
  --text-2xl:  32px;    /* 小节标题 */
  --text-xl:   28px;    /* 段落标题 / 副标题 */
  --text-lg:   24px;    /* 强调文字 / 大链接 */

  /* ── 正文 ── */
  --text-base: 17px;    /* 基础正文（Apple.com 基准：font-size: 106.25%） */
  --text-md:   21px;    /* 大正文 / 引言 */
  --text-sm:   14px;    /* 辅助文字 / 按钮 */
  --text-xs:   12px;    /* 注脚 / 标签 / 导航链接 */

  /* ── Apple.com CSS 中的其他字号 ── */
  --text-15:   15px;    /* 某些卡片描述 */
  --text-18:   18px;    /* 某些副标题 */
  --text-19:   19px;    /* 某些强调文字 */
  --text-20:   20px;    /* 某些小标题 */
}
```

**响应式字号变化**（Apple.com 实测）：

```css
/* 桌面端 */
.hero-title { font-size: 80px; }
.section-title { font-size: 48px; }

/* 平板（735-1068px） */
@media (max-width: 1068px) {
  .hero-title { font-size: 64px; }
  .section-title { font-size: 40px; }
}

/* 手机（≤734px） */
@media (max-width: 734px) {
  .hero-title { font-size: 40px; }
  .section-title { font-size: 28px; }
}

/* 超小屏（≤320px） */
@media (max-width: 320px) {
  .hero-title { font-size: 32px; }
  .section-title { font-size: 24px; }
}
```

### 2.3 字重

```css
:root {
  --font-thin:       100;  /* 极少使用 — 超大 Display 标题 */
  --font-light:      300;  /* 大标题 — Apple.com Hero 标题标准字重 */
  --font-regular:    400;  /* 正文 — 绝大多数文字 */
  --font-medium:     500;  /* 按钮文字 — 某些强调文字 */
  --font-semibold:   600;  /* 小标题 — 区块标题、导航选中态 */
  --font-bold:       700;  /* 强调 — 极少使用，Apple 风格不推荐粗体 */
  --font-heavy:      800;  /* 极少使用 */
  --font-black:      900;  /* 不使用 */
}
```

> **Apple 排版特征**：Apple.com 几乎从不使用 bold（700+）。大标题通过超大字号 + 轻（300）或常规（400）字重 + 极紧字距来营造高级感。

### 2.4 行高

```css
:root {
  --leading-none:     1.0;    /* 超大标题 — 96px/80px 标题 */
  --leading-tight:    1.05;   /* Display 标题 — 64px/56px */
  --leading-snug:     1.1;    /* 大标题 — 48px/40px */
  --leading-normal:   1.21;   /* 中标题 — 32px/28px */
  --leading-relaxed:  1.33;   /* 英文正文 — 17px~24px */
  --leading-loose:    1.47;   /* 小字/辅助文字 — 12px~14px */
  --leading-cn-body:  1.8;    /* 中文正文 — Apple.com 中文页面实测值 */
  --leading-cn-title: 1.4;    /* 中文标题 */
}
```

> **中英差异**：中文因字形较密、笔画较多，需要更大的行高。Apple.com 中文页面正文行高约 1.8（英文为 1.33），标题行高约 1.4（英文为 1.1）。

### 2.5 字间距

```css
:root {
  --tracking-tighter:  -0.022em;  /* Display 大标题（96px/80px） */
  --tracking-tight:    -0.015em;  /* 标题（48px~64px） */
  --tracking-normal:   0em;       /* 正文（17px~24px） */
  --tracking-wide:     0.011em;   /* 大写标签/导航（12px~14px） */
}
```

> **设计洞察**：大字号使用负字间距是 Apple 排版的关键签名。这让大标题看起来更紧凑、更有力量感。小字号使用正字间距则提高可读性。

### 2.6 排版组合速查

```css
/* ── Hero 大标题 ── */
.hero-title {
  font-family: var(--font-system);
  font-size: 80px;
  font-weight: 300;
  line-height: 1.05;
  letter-spacing: -0.022em;
  color: var(--color-text-primary);
}

/* ── 区块标题 ── */
.section-title {
  font-size: 48px;
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.015em;
  color: var(--color-text-primary);
}

/* ── 卡片标题 ── */
.card-title {
  font-size: 32px;
  font-weight: 600;
  line-height: 1.21;
  letter-spacing: -0.015em;
  color: var(--color-text-primary);
}

/* ── 英文正文 ── */
.body-text-en {
  font-size: 17px;
  font-weight: 400;
  line-height: 1.33;
  letter-spacing: 0;
  color: var(--color-text-primary);
}

/* ── 中文正文 ── */
.body-text-cn {
  font-family: var(--font-cn);
  font-size: 17px;
  font-weight: 400;
  line-height: 1.8;
  letter-spacing: 0;
  color: var(--color-text-primary);
}

/* ── 导航链接 ── */
.nav-link {
  font-size: 12px;
  font-weight: 400;
  line-height: 1;
  letter-spacing: 0.011em;
  color: var(--color-text-primary);
  opacity: 0.8;
}

/* ── 次要按钮 ── */
.cta-secondary {
  font-size: 21px;
  font-weight: 400;
  line-height: 1;
  letter-spacing: 0;
  color: var(--color-link);
}

/* ── 注脚 ── */
.footnote {
  font-size: 12px;
  font-weight: 400;
  line-height: 1.47;
  letter-spacing: 0;
  color: var(--color-text-tertiary);
}
```

---

## 3. 间距系统

### 3.1 间距阶梯

```css
:root {
  --space-0:    0px;
  --space-xxs:  2px;     /* 图标内部微调 */
  --space-xs:   4px;     /* 图标与文字间距 */
  --space-sm:   8px;     /* 紧凑元素间距、按钮内间距 */
  --space-md:   12px;    /* 表单元素间距、卡片网格间距 */
  --space-lg:   16px;    /* 移动端页面边距（≈4.5% @375px） */
  --space-xl:   20px;    /* 段落间距 */
  --space-2xl:  24px;    /* 列间距、桌面端页面内边距 */
  --space-3xl:  32px;    /* 区块内间距 */
  --space-4xl:  40px;    /* 区块间距（最小值） */
  --space-5xl:  48px;    /* 大区块间距 */
  --space-6xl:  64px;    /* 段落大间距 */
  --space-7xl:  80px;    /* Hero 间距 */
  --space-8xl:  96px;    /* 首屏上下留白 */
  --space-9xl:  120px;   /* 超大间距（特殊场景） */
}
```

### 3.2 Apple.com 实测间距值

从 CSS 中提取的 padding-top 值，反映实际使用的垂直间距：

```css
:root {
  /* 元素级间距 */
  --pt-icon-text: 3px;       /* 图标与文字 */
  --pt-badge: 7px;           /* 标签/徽章 */
  --pt-button: 10px;         /* 按钮内边距 */
  --pt-input: 11px;          /* 输入框内边距 */
  --pt-list-item: 15px;      /* 列表项 */
  --pt-card-sm: 17px;        /* 小卡片 */
  --pt-section-inner: 21px;  /* 区块内元素间距 */
  --pt-section: 30px;        /* 区块内边距 */
  --pt-hero-text: 37px;      /* Hero 文字区 */
  --pt-hero-image: 42px;     /* Hero 图片区 */
  --pt-card-lg: 53px;        /* 大卡片 */
  --pt-hero-top: 61px;       /* Hero 顶部 */
}
```

### 3.3 响应式间距

```css
/* 桌面端（≥1069px） */
.section { padding: 80px 0; }
.container { max-width: 980px; padding: 0 24px; }

/* 平板（735-1068px） */
@media (max-width: 1068px) {
  .section { padding: 60px 0; }
  .container { max-width: 692px; }
}

/* 手机（≤734px） */
@media (max-width: 734px) {
  .section { padding: 40px 0; }
  .container { padding: 0 4.5%; } /* ≈16px @375px */
}
```

---

## 4. 响应式断点

### 4.1 Apple.com 四级断点系统

```css
:root {
  --bp-xsmall:  320px;   /* 小手机（iPhone SE 1st gen） */
  --bp-small:   735px;   /* 手机/小平板（iPhone 14 Pro Max: 430px） */
  --bp-medium:  1068px;  /* 平板/小桌面（iPad Pro 12.9": 1024px） */
  --bp-large:   1441px;  /* 大桌面 */
}
```

**命名惯例与范围**：

| 名称 | 范围 | 典型设备 |
|---|---|---|
| xlarge | ≥ 1441px | 超宽屏显示器、iMac 27" |
| large | 1069–1440px | 标准桌面、MacBook Pro 16" |
| medium | 735–1068px | 平板、iPad、小笔记本 |
| small | ≤ 734px | 手机（iPhone 全系列） |
| xsmall | ≤ 320px | 小屏手机（iPhone SE 1st） |

### 4.2 断点使用

```css
/* Mobile-first 写法（Apple 不使用这种方式，但更通用） */
/* Apple.com 使用 Desktop-first：从大到小覆盖 */

/* 大桌面（≥1441px） */
@media (min-width: 1441px) {
  .container { max-width: 980px; }
}

/* 标准桌面（1069-1440px） */
@media (max-width: 1440px) and (min-width: 1069px) {
  .container { max-width: 980px; }
}

/* 平板（735-1068px） */
@media (max-width: 1068px) {
  .container { max-width: 692px; }
}

/* 手机（≤734px） */
@media (max-width: 734px) {
  .container { width: 100%; padding: 0 4.5%; }
}
```

### 4.3 栅格系统

```
桌面（≥1069px）:   最大宽度 980px，居中，12 列，列间距 24px
平板（735-1068px）: 最大宽度 692px，居中，自适应
手机（≤734px）:    全宽，两侧 padding 4.5%（≈16px @375px）
```

**980px 的由来**：Apple.com 的最大内容宽度为 980px（不含页面两侧留白）。这是从早期 Apple.com 设计中延续下来的值，在 1440px 及更宽的屏幕上，980px 内容区域两侧各有约 230px 留白，营造出优雅的聚焦感。

---

## 5. 圆角

### 5.1 圆角阶梯

```css
:root {
  --radius-xs:    4px;    /* 极小元素（标签、芯片） */
  --radius-sm:    8px;    /* 按钮、小卡片、输入框 */
  --radius-md:    12px;   /* 卡片、模态框、下拉菜单 */
  --radius-lg:    20px;   /* 大面板、内容卡片 */
  --radius-xl:    28px;   /* 全宽卡片、底部弹窗 */
  --radius-pill:  980px;  /* 全圆角/药丸形（按钮、标签、徽章） */
  --radius-full:  50%;    /* 头像、图标、圆形按钮 */
}
```

### 5.2 Apple.com CSS 中提取的圆角值

```css
/* 实际使用的 border-radius 值 */
.radius-5  { border-radius: 5px; }   /* 某些输入框 */
.radius-8  { border-radius: 8px; }   /* 小卡片 */
.radius-10 { border-radius: 10px; }  /* 中等卡片 */
.radius-12 { border-radius: 12px; }  /* 大卡片 */
.radius-980 { border-radius: 980px; } /* 药丸形按钮（Apple 标志性圆角值） */
.radius-50 { border-radius: 50%; }    /* 圆形 */
```

> **设计洞察**：`980px` 是 Apple.com 按钮的标志性圆角值。实际效果等同于 `9999px`（因为元素高度远小于 980px），但 Apple 选择使用 980px 这个精确值。这是从 Apple.com CSS 源码中直接提取的。

---

## 6. 阴影与深度

### 6.1 阴影阶梯

```css
:root {
  /* ── 卡片/浮层 ── */
  --shadow-sm:      0 1px 2px rgba(0, 0, 0, 0.04);    /* 微阴影 */
  --shadow-card:    0 2px 8px rgba(0, 0, 0, 0.08);     /* 卡片默认 */
  --shadow-elevated: 0 4px 16px rgba(0, 0, 0, 0.12);   /* 悬浮态/浮层 */
  --shadow-modal:   0 8px 32px rgba(0, 0, 0, 0.16);    /* 模态框 */
  --shadow-drawer:  0 12px 48px rgba(0, 0, 0, 0.20);   /* 侧边抽屉 */

  /* ── 导航栏 ── */
  --shadow-nav:     0 1px 0 rgba(0, 0, 0, 0.08);       /* 底部细线 */
  --shadow-nav-scroll: 0 2px 8px rgba(0, 0, 0, 0.08);  /* 滚动时增强 */

  /* ── Dark Mode 阴影（更深） ── */
  --shadow-card-dark:    0 2px 8px rgba(0, 0, 0, 0.32);
  --shadow-elevated-dark: 0 4px 16px rgba(0, 0, 0, 0.40);
  --shadow-modal-dark:   0 8px 32px rgba(0, 0, 0, 0.50);
}
```

### 6.2 深度层级

| 层级 | 元素 | 阴影 | Z-index |
|---|---|---|---|
| 0 | 页面背景 | 无 | 0 |
| 1 | 内容区域 | 无 | 1 |
| 2 | 卡片、列表项 | `--shadow-card` | 10 |
| 3 | 粘性头部 | `--shadow-nav` | 100 |
| 4 | 下拉菜单 | `--shadow-elevated` | 1000 |
| 5 | 模态框遮罩 | `--shadow-modal` | 3000 |
| 6 | Toast/通知 | `--shadow-elevated` | 4000 |

---

## 7. 毛玻璃 / 材质

### 7.1 三层毛玻璃系统

```css
/* ── 标准毛玻璃 — 导航栏 ── */
.glass-nav {
  background: rgba(255, 255, 255, 0.72);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  backdrop-filter: saturate(180%) blur(20px);
}

/* ── 深度毛玻璃 — 浮层面板 ── */
.glass-panel {
  background: rgba(255, 255, 255, 0.85);
  -webkit-backdrop-filter: blur(40px);
  backdrop-filter: blur(40px);
}

/* ── 轻度毛玻璃 — Toast/通知 ── */
.glass-toast {
  background: rgba(255, 255, 255, 0.60);
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
}

/* ── Dark Mode ── */
@media (prefers-color-scheme: dark) {
  .glass-nav   { background: rgba(29, 29, 31, 0.72); }
  .glass-panel { background: rgba(29, 29, 31, 0.85); }
  .glass-toast { background: rgba(29, 29, 31, 0.60); }
}
```

### 7.2 降级方案

```css
/* 不支持 backdrop-filter 的浏览器降级为实色背景 */
@supports not (backdrop-filter: blur(20px)) {
  .glass-nav   { background: rgba(255, 255, 255, 0.95); }
  .glass-panel { background: rgba(255, 255, 255, 0.98); }
}
```

> **兼容性**：`backdrop-filter` 现代浏览器支持良好（Chrome 76+, Firefox 103+, Safari 9+）。全局使用率超过 95%。务必提供实色背景降级方案。

---

## 8. Motion Token 分离

本文件只维护前端视觉样式 token，包括色彩、排版、间距、断点、圆角、阴影、毛玻璃。动画属于独立 motion system，不在此处混写。

- Duration、easing、property、pattern matrix: 见 [07-motion.md](07-motion.md)
- Tailwind motion utilities: 见 [07-motion.md](07-motion.md#6-tailwind-extension)
- Reduced motion contract: 见 [07-motion.md](07-motion.md#7-reduced-motion-contract)

---

## 9. 图标系统

### 9.1 Apple SF Symbols 规格

| 规格 | 说明 |
|---|---|
| 标准图标 | 44×44pt（iOS 可点击区域最小值） |
| 小图标 | 20×20pt（工具栏、导航栏） |
| 标签图标 | 25×25pt（Tab Bar） |
| 线条粗细 | Regular / Medium / Semibold / Bold 四种粗细 |
| 渲染模式 | Monochrome / Hierarchical / Palette / Multicolor |

### 9.2 Web 替代方案

SF Symbols 是 Apple 专有资源，Web 端使用以下替代方案：

| 图标库 | 风格 | 推荐度 | 说明 |
|---|---|---|---|
| Lucide | 线性、简洁 | ★★★★★ | 最接近 SF Symbols 的开源图标库 |
| Heroicons | 线性、圆润 | ★★★★ | Tailwind 官方推荐 |
| Phosphor Icons | 多粗细 | ★★★★ | 支持多种粗细变体 |
| Tabler Icons | 线性、一致 | ★★★★ | 4000+ 图标 |
| Material Icons | 填充/线性 | ★★★ | Google 风格，与 Apple 差异较大 |

---

## 10. 触摸目标

### 10.1 HIG 最小触摸目标

| 元素 | 最小尺寸 | 推荐尺寸 |
|---|---|---|
| 可点击区域 | 44×44pt | 48×48pt |
| 按钮高度 | 34pt | 44pt |
| 列表项高度 | 44pt | 48pt |
| Tab Bar 图标 | 44×44pt | — |
| 导航栏按钮 | 44×44pt | — |

### 10.2 Web 适配

```css
/* 确保触摸目标足够大 */
.touch-target {
  min-height: 44px;
  min-width: 44px;
}

/* 如果视觉尺寸小于 44px，使用伪元素扩大可点击区域 */
.small-icon-button {
  position: relative;
  width: 24px;
  height: 24px;
}
.small-icon-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
}
```
