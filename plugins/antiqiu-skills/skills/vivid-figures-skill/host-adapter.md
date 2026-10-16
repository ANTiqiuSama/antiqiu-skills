# 执行环境与项目配置

`<SKILL>` 是 Skill 安装目录，`<RES>` 是 `<SKILL>/original/resources`，`<WORKSPACE>` 是任务工作区。用当前助手的文件、终端、图像查看及可用的图像生成能力执行工作流。

## 初始化

使用同一个 Python 3.10+ 环境安装 [依赖](requirements.txt)，运行：

```text
python "<RES>/scripts/resolve_runtime.py"
python "<RES>/scripts/bootstrap.py" --workspace "<WORKSPACE>" --profile modeling-competition
```

初始化复制绘图工具及模板，保留用户修改过的文件，并刷新识别到的旧工具副本。生成的 `_utils/`、`skills/shared-scripts/`、`_templates/` 属于任务工作区。后续命令在工作区执行；Bash 片段使用宿主可用的 Bash，Windows 可使用 Git Bash。Bash 请使用 runtime.json 中解析的路径，避免在 Windows 误用 WSL 启动器；`VIVID_BASH` 可显式指定。`VIVID_PYTHON` 可指定同一 Python。

## 配置

- `.vivid/config.json`：项目设置。配色见 [配色选择](color-selection.md)；其他可选字段为 `style`（默认 clean_open）、`style_custom`、`language`（zh/en）、`output_format`（pdf/docx/png 等）、`template`、`title`。保留用户已有字段。读写用 `_utils/vivid_config.py`，支持从子目录查找项目根目录。
- `.vivid/runtime.json`：可执行文件路径及工具复制记录，由初始化生成。
- `.vivid/figure-plan-policy.json`：完整图集的规划校验状态，由规划 CLI 维护。

## 渲染工具

- 数据图：Python；保存源脚本、真实输入及实际输出。
- Draw.io：`python "<RES>/scripts/export_drawio.py" source.drawio --format pdf`；需要桌面版 Draw.io，路径可用 `DRAWIO_PATH` 指定。
- HTML：`python "<RES>/scripts/render_html.py" source.html --format both`；使用本机 Chrome/Chromium 和 Python Playwright，路径可用 `CHROME_PATH` 指定。公式加 `--render-math`，几何检查加 `--geom-check`。
- TikZ：XeLaTeX；PDF 预览使用 PyMuPDF 或 Poppler。
- Mermaid：`python "<RES>/scripts/render_mermaid.py" source.mmd`；需要 Node.js 和 mmdc。
- 科学场景插图：使用宿主提供或用户已配置的图像生成工具；保留工作流的完整构图提示词。缺少工具时说明缺失能力，不将插图改作数据证据。

视觉检查由当前助手实际打开图件完成，执行次数及范围统一见 [检查与修复](original/review-policy.md)。图集来源用用户提供或确认的数据、模型结果及证据文件；只要求绘图时，在图件完成后停止。
