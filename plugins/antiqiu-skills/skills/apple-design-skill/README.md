# Apple Design Language — Frontend Skill

将 Apple 设计语言（Apple.com + HIG + Apple Design Resources）应用到前端开发的 AI Skill。平台无关的 Design Token、Motion Token、Apple 官方文档地图、HIG 组件行为抽取、平台适配、Apple 资源/技术品牌指南、动画模板、组件模式和布局方案，适用于 Web、React Native、Flutter、SwiftUI 等任何前端技术栈。

## 数据来源

本 Skill 的设计 Token 提取自以下**公开资源**，仅供学习与参考：

| 来源 | 说明 |
|---|---|
| [Apple.com 主 CSS](https://www.apple.com) | 从公开样式表中提取的色值、字号、间距等数值 |
| [Human Interface Guidelines (HIG)](https://developer.apple.com/cn/design/) | Apple 官方设计原则和组件规范 |
| [Apple Design Resources](https://developer.apple.com/design/resources/) | 官方 UI Kits、模板、字体、SF Symbols、技术品牌资源 |
| [Apple Style Guide](https://support.apple.com/zh-cn/guide/applestyleguide/welcome/web) | Apple 官方编辑与排版规范 |
| Apple.com 页面结构 | 布局模式、间距规律的逆向分析 |
| Motion 设计标准 | Apple HIG Motion/Loading/Materials、Liquid Glass、Material、Fluent、Carbon、Atlassian、Spectrum、WCAG、MDN |
| [refinec/PingFangSC](https://github.com/refinec/PingFangSC) | PingFang SC fallback 字体文件，MIT License |

> **注意**：Apple、Apple Logo、Human Interface Guidelines 等为 Apple Inc. 的商标或版权内容。本项目仅作为设计学习与参考用途，不隶属于 Apple Inc.，也未获得其endorsement。

## 快速使用

### Claude Code（全局安装）

```bash
# 推荐：按仓库名克隆，保留 Codex/Codex-compatible skill 名称
git clone https://github.com/LukeSONG2000/apple-design-skill.git \
  ~/.claude/commands/apple-design-skill

# 如需兼容旧的 /apple-design 调用，也可以克隆为 legacy 目录名
git clone https://github.com/LukeSONG2000/apple-design-skill.git \
  ~/.claude/commands/apple-design
```

### Codex（全局安装）

```bash
# 克隆到 Codex 全局 skills 目录
git clone https://github.com/LukeSONG2000/apple-design-skill.git \
  ~/.codex/skills/apple-design-skill
```

## 内容结构

```
apple-design-skill/
├── agents/
│   └── openai.yaml              # Codex UI 元数据
├── assets/
│   └── fonts/PingFangSC/        # woff2 + ttf 跨平台中文字体
├── SKILL.md                    # Skill 主文件（Design Token + 组件模式）
├── references/                 # 详细实现参考
│   ├── 00-philosophy.md        # 设计哲学、HIG 六原则
│   ├── 01-tokens.md            # 色彩、排版、间距、断点、圆角、阴影、毛玻璃
│   ├── 02-components.md        # 按钮、导航栏、卡片、表单、模态框、Toast、页脚
│   ├── 03-patterns.md          # Hero 区、双栏、三栏、图文区等页面布局模式
│   ├── 04-accessibility.md     # 色彩对比度、Focus 管理、ARIA、屏幕阅读器
│   ├── 05-tailwind-config.md   # Tailwind CSS 配置、CSS 变量版
│   ├── 06-fonts.md             # PingFang SC 跨平台字体打包方案
│   ├── 07-motion.md            # 独立 Motion Token、动效原则、reduced motion
│   ├── 08-apple-docs-coverage.md # Apple 官方文档覆盖地图
│   ├── 09-motion-templates.md  # Apple 风格动画模板库
│   ├── 10-apple-official-docs-map.md # 爬取后的官方 URL 分类地图
│   ├── 11-hig-foundations-patterns.md # HIG Foundations / Patterns 抽取
│   ├── 12-hig-components-inputs.md # HIG Components / Inputs 抽取
│   └── 13-platform-resources-technologies.md # 平台、资源、技术品牌
```

## 字体资源

仓库内置 `PingFangSC` fallback 字体，用于非 Apple 设备保持统一中文观感；Apple 设备优先使用系统 `PingFang SC`，无需加载内置字体。

| 平台 | 推荐格式 | 目录 |
|---|---|---|
| Web / PWA / Electron / Tauri WebView | `woff2` | `assets/fonts/PingFangSC/woff2` |
| React Native / Flutter / Android / Windows 客户端 | `ttf` | `assets/fonts/PingFangSC/ttf` |
| iOS / macOS 原生 | 系统字体 | 不需要打包 |

Web 可直接引用 `assets/fonts/PingFangSC/pingfang-sc.css`。详细方案见 [references/06-fonts.md](references/06-fonts.md)。

## Motion 规范

前端样式 token 与动画 token 分开维护。色彩、排版、间距、圆角、阴影、毛玻璃见 [references/01-tokens.md](references/01-tokens.md)；动画原则、duration/easing、模式矩阵、reduced motion 方案见 [references/07-motion.md](references/07-motion.md)；Apple 风格动画模板见 [references/09-motion-templates.md](references/09-motion-templates.md)。

## Design Token 速查

### 色彩

| 用途 | 值 | 深色模式 |
|---|---|---|
| 正文 | `#1D1D1F` | `#F5F5F7` |
| 次要文字 | `#6E6E73` | `#A1A1A6` |
| 背景 | `#FFFFFF` | `#000000` |
| 链接/主交互 | `#0071E3` | `#2997FF` |

### 核心设计签名

1. **大留白** — 内容不超过 980px 宽
2. **毛玻璃** — 72% 不透明度 + 180% 饱和度 + 20px 模糊
3. **品牌蓝仅交互** — `#0071E3` 只用于链接和按钮
4. **聚焦环** — 键盘导航时显示，鼠标/触屏时隐藏
5. **渐进式信息** — 大标题 → 副标题 → 正文

## 许可证

MIT License — 本项目仅供学习参考，Apple 相关设计资产版权归 Apple Inc. 所有。
