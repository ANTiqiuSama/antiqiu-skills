# PingFangSC Font Assets

字体来源：[refinec/PingFangSC](https://github.com/refinec/PingFangSC)。

本目录保留 Apple Design Skill 使用频率最高的 4 个字重：

| 字重 | 文件 | 用途 |
|---|---|---|
| 300 | `PingFangSC-Light` | 大标题、轻量展示文字 |
| 400 | `PingFangSC-Regular` | 正文 |
| 500 | `PingFangSC-Medium` | 控件、导航、强调正文 |
| 600/700 | `PingFangSC-Semibold` | 小标题、标签、强调 |

## 格式选择

| 平台 | 推荐格式 | 说明 |
|---|---|---|
| Web / PWA / Electron / Tauri WebView | `woff2` | 体积较小，浏览器支持好 |
| React Native / Flutter / Android / Windows 客户端 | `ttf` | 原生字体注册兼容性更稳定 |
| iOS / macOS 原生 | 系统 `PingFang SC` | Apple 设备优先使用系统字体，不需要打包字体 |

Web 项目可直接引用 `pingfang-sc.css`。该 CSS 使用独立字体族名 `Apple PingFang SC Fallback`，字体栈会先尝试系统 `PingFang SC`，Apple 设备可直接走系统字体；非 Apple 设备在没有系统苹方时才使用内置 fallback。

## License

上游仓库声明为 MIT License，许可证副本保存在 `LICENSE.refinec-PingFangSC`。产品发布前仍应按团队合规要求确认字体分发授权。

