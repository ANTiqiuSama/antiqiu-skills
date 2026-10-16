# Fonts — 中文字体与跨平台回退

> 目标：Apple 设备使用系统字体；其他平台使用可合法分发的开源中文字体，保持接近的观感。

## 1. 授权边界

- SF Pro、PingFang SC 是 Apple 专有字体，只随 Apple 系统授权使用。不要打包、托管或通过 CDN 分发它们，也不要依赖第三方仓库对这些字体声明的许可证。
- 跨平台回退使用 [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) 或 [思源黑体 Source Han Sans](https://github.com/adobe-fonts/source-han-sans)，均为 SIL Open Font License 1.1，可随产品分发。

## 2. Web / PWA / Electron / Tauri

```css
body {
  font-family:
    -apple-system, BlinkMacSystemFont,
    "PingFang SC",          /* Apple 设备系统字体，本地命中，不下载 */
    "SF Pro SC",
    "Noto Sans SC",         /* 开源回退 */
    "Source Han Sans SC",
    "Microsoft YaHei",      /* Windows 系统字体 */
    "Helvetica Neue", Arial, sans-serif;
}
```

需要统一观感时，通过 Google Fonts 或自托管 Noto Sans SC 的 `woff2` 子集加载 400/500/600 三个字重，并设置 `font-display: swap`。中文字体体积大，优先使用按 `unicode-range` 切片的版本，不要把完整 TTF 放进首屏加载链路。

## 3. 客户端

| 平台 | 建议 |
|---|---|
| iOS / macOS | 使用系统字体（`.system` / `PingFang SC`），不打包 |
| Android | 系统默认 Noto Sans CJK；需要固定字形时打包 Noto Sans SC |
| Windows / Linux | 打包 Noto Sans SC 或思源黑体，通过框架注册字体族 |
| React Native / Flutter | 注册 `NotoSansSC` 的 Regular / Medium / SemiBold，iOS 端仍优先系统字体 |

字重映射：正文 400，控件 500，标题 600。

## 4. 注意事项

- 发布前确认所用字体的许可证文件已随产品附带（OFL 要求保留版权与许可声明）。
- 设计稿中出现 SF Pro / PingFang 时，在非 Apple 平台按上表替换，不要在网页中引用 Apple 专有字体文件。
