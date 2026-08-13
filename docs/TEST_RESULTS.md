# Test results

验证日期：2026-08-13。范围是本仓库的 7 个通用 Skill；`hatch-pet` 按用户要求排除，未修改也未纳入统计。

## 最终结果

| 层级 | 结果 | 证据 |
| --- | --- | --- |
| 静态审计 | 通过 | 7 个 Skill；启动元数据 3,784→2,368 字节，减少 37.4%；三组重叠正文 186→105 行，减少 43.5%；诊断支持材料 636→63 行，减少 90.1% |
| 官方 Skill 校验器 | 7/7 通过 | 每个目录均返回 `Skill is valid!` |
| 官方插件校验器 | 通过 | `Plugin validation passed` |
| 隔离 Codex 行为回归 | 8/8 通过 | `gpt-5.6-terra`；7 个独立行为用例加 1 个综合隐式路由用例 |
| `human-writing` 检查器 | 正反例通过 | 自然段落退出 0；含冒号和禁用翻案句的反例退出 1，并报告对应问题 |
| 本地同步一致性 | 7/7 通过 | 发布包与 `~/.codex/skills` 中 7 个目标目录逐项 `diff -qr` 无差异 |
| 全新本地 Codex 会话 | 通过 | 6 个可隐式调用的新名称可见；6 个旧名称均不可见；显式 `$write-action-first` 调用成功 |
| Git 差异检查 | 通过 | `git diff --check` 无输出 |

## 可复现命令

静态审计：

```bash
python3 -B tests/audit_skills.py
```

隔离行为回归：

```bash
python3 -B tests/run_behavior_tests.py \
  --model gpt-5.6-terra \
  --jobs 3 \
  --timeout 240
```

行为回归在临时目录中只链接待测 Skill，并设置临时 `CODEX_HOME`。临时目录仅链接本机 `auth.json` 供模型鉴权；凭据内容不会被复制、打印或写入测试结果。这样可以阻止旧个人 Skill 影响路由判断。

官方校验器：

```bash
~/.codex/tools/skill-validator-venv/bin/python \
  ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  plugins/antiqiu-skills/skills/<skill-name>

~/.codex/tools/skill-validator-venv/bin/python \
  ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/antiqiu-skills
```

## 行为用例覆盖

- `plan-work`：单用户 JSON→SQLite 迁移保持精简，不引入 feature flag 或微服务。
- `execute-work`：先改配置再读取现有解析器的真实结果，不提前宣称成功。
- `diagnose-work`：从 401 和缺失 `Authorization` 定位根因并给最小修复。
- `keep-task-in-scope`：只运行一轮、有假设和停止决定，复用现有数据且不创建 freeze/manifest。
- `refine-text`：压缩文本时保留日期、数量、来源和“原因未确认”的不确定性。
- `human-writing`：自然改写中文短段，不虚构经历、数字或来源。
- `write-action-first`：显式调用时先报告测试结果、失败点和最小动作。
- 综合路由：6 个可隐式调用的 Skill 分工正确；旧名称和显式专用的 `write-action-first` 不参与隐式匹配。

## 测试脚本修正记录

首轮模型回归暴露的是测试夹具问题，而非全部都是 Skill 缺陷：提示一边要求使用 Skill，一边禁止读取其说明；断言还把正确中文回答限定成英文固定字符串。后续修正为：允许只读取 Skill 说明、按等价语义分组断言，并把 `write-action-first` 的显式调用与隐式路由分开测试。

修正后重新运行完整套件，最终一次为 8/8。没有通过删除关键约束或接受错误行为来换取绿色结果；`feature flag`、捏造成功、丢失不确定性、生成新清单等负向断言仍保留。

全新本地会话出现一次已有 shell snapshot 的 Bash 语法警告，但 Codex 命令退出码为 0，Skill 发现和显式调用均成功。该警告不来自本仓库，也未影响本轮结果。
