# Font Packaging — PingFang SC 跨平台字体方案

> 目标：Apple 设备优先使用系统字体，非 Apple 设备使用内置 PingFang SC fallback，让 Web、桌面客户端和移动端界面保持一致的中文观感。

## 1. 字体来源

字体文件来自 [refinec/PingFangSC](https://github.com/refinec/PingFangSC)，上游仓库声明为 MIT License。当前仓库保留 4 个常用字重：

| CSS weight | 字体 | 文件 |
|---|---|---|
| 300 | Light | `assets/fonts/PingFangSC/{woff2,ttf}/PingFangSC-Light.*` |
| 400 | Regular | `assets/fonts/PingFangSC/{woff2,ttf}/PingFangSC-Regular.*` |
| 500 | Medium | `assets/fonts/PingFangSC/{woff2,ttf}/PingFangSC-Medium.*` |
| 600/700 | Semibold | `assets/fonts/PingFangSC/{woff2,ttf}/PingFangSC-Semibold.*` |

## 2. Web / PWA / Electron / Tauri

Web 侧使用 `woff2`。将字体目录复制到站点静态资源目录后，引入：

```html
<link rel="stylesheet" href="/fonts/PingFangSC/pingfang-sc.css">
```

然后使用：

```css
body {
  font-family:
    "PingFang SC",
    "SF Pro SC",
    "Apple PingFang SC Fallback",
    "Noto Sans SC",
    "Helvetica Neue",
    Arial,
    sans-serif;
}
```

不要把内置字体族命名为 `PingFang SC`。使用独立名称 `Apple PingFang SC Fallback` 可以让 Apple 设备先命中系统 `PingFang SC`，非 Apple 设备再加载仓库内置字体。

## 3. React Native

React Native 侧使用 `ttf`。将 `assets/fonts/PingFangSC/ttf/*.ttf` 复制到项目字体目录后，在平台配置中注册字体文件，再在样式中按注册名称使用。

推荐策略：

- iOS：优先使用系统 `PingFang SC`，只有在设计要求完全一致且合规允许时再打包 `ttf`。
- Android：注册 `PingFangSC-Regular.ttf`、`PingFangSC-Medium.ttf`、`PingFangSC-Semibold.ttf`，正文 400，控件 500，标题 600。

## 4. Flutter

Flutter 侧使用 `ttf`，在 `pubspec.yaml` 中注册：

```yaml
flutter:
  fonts:
    - family: PingFangSCFallback
      fonts:
        - asset: assets/fonts/PingFangSC/ttf/PingFangSC-Light.ttf
          weight: 300
        - asset: assets/fonts/PingFangSC/ttf/PingFangSC-Regular.ttf
          weight: 400
        - asset: assets/fonts/PingFangSC/ttf/PingFangSC-Medium.ttf
          weight: 500
        - asset: assets/fonts/PingFangSC/ttf/PingFangSC-Semibold.ttf
          weight: 600
```

在 iOS/macOS 原生页面中优先使用系统字体；Flutter 跨平台页面需要统一观感时再指定 `PingFangSCFallback`。

## 5. 原生客户端

| 平台 | 建议 |
|---|---|
| iOS / macOS | 使用系统 `PingFang SC` / `.system` 字体，不打包字体 |
| Android | 打包 `ttf` 到 `res/font` 或资产目录 |
| Windows / Linux | 打包 `ttf`，通过客户端框架注册字体族 |

## 6. 注意事项

- 字体文件较大，Web 默认只引用 `woff2`，不要把 `ttf` 暴露到 Web 首屏加载链路。
- 仅保留 300/400/500/600 四个常用字重，避免 Thin/Ultralight 增加仓库体积。
- 发布前按团队合规要求确认字体分发授权；上游 license 副本在 `assets/fonts/PingFangSC/LICENSE.refinec-PingFangSC`。

