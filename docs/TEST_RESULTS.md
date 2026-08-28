# Test results

验证日期：2026-08-28。范围是本仓库当前的 8 个通用 Skill；`hatch-pet` 按用户要求排除，未修改也未纳入统计。

## 最终结果

| 层级 | 结果 | 证据 |
| --- | --- | --- |
| 静态审计 | 通过 | 8 个 Skill；启动元数据 3,784→2,828 字节，减少 25.3%；三组重叠正文 186→118 行，减少 36.6%；诊断支持材料 636→63 行，减少 90.1% |
| 官方 Skill 校验器 | 本轮变更 2/2 通过 | `refine-text` 与因回归发现而收紧的 `plan-work` 均返回 `Skill is valid!`；其余 6 个 Skill 未修改 |
| 官方插件校验器 | 通过 | `Plugin validation passed`；清单版本为 1.2.0 |
| 隔离 Codex 行为回归 | 10/10 通过 | `gpt-5.6-terra`；原 9 个用例全部通过，新增 1 个中文技术运行手册用例通过 |
| `human-writing` 检查器 | 沿用既有结果 | 该 Skill 本轮未修改；2026-08-13 的自然段落正例退出 0，含禁用项的反例退出 1 |
| 本地安装同步 | 本轮未执行 | 用户要求融合并上传 GitHub；没有覆盖或删除 Antigravity 当前安装的 `ste-cn` |
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

行为回归在临时目录中只链接待测 Skill，并设置临时 `CODEX_HOME`。直接行为用例把被测 `SKILL.md` 明确注入会话；依赖按需材料的用例还会注入用例声明的 reference。综合路由用例只暴露已安装 Skill 的名称和描述，用于独立验证选择边界。临时目录仅链接本机 `auth.json` 供模型鉴权；凭据内容不会被复制、打印或写入测试结果。这样既阻止旧个人 Skill 干扰，也不再把模型默认能力误报成 Skill 行为。

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

- `plan-work`：单用户 JSON→SQLite 转换只使用当前数据所需 schema、一次转换和备份，不引入 schema 版本、feature flag 或微服务。
- `execute-work`：先改配置再读取现有解析器的真实结果，不提前宣称成功。
- `diagnose-work`：从 401 和缺失 `Authorization` 定位根因并给最小修复。
- `keep-task-in-scope`：只运行一轮、有假设和停止决定，复用现有数据且不创建 freeze/manifest。
- `trim-agent-instructions`：保留具体的生产清理安全约束，删除空泛口号和失效路径，并把“仔细验证”改成可执行规则。
- `refine-text`：压缩文本时保留日期、数量、来源和“原因未确认”的不确定性。
- `refine-text` 中文技术模式：把复合运行手册拆成可执行步骤，保留执行者、条件、对象和“没有证据”的限制，不添加效果承诺。
- `human-writing`：自然改写中文短段，不虚构经历、数字或来源。
- `write-action-first`：显式调用时先报告测试结果、失败点和最小动作。
- 综合路由：7 个可隐式调用的 Skill 分工正确；旧名称和显式专用的 `write-action-first` 不参与隐式匹配。

## 测试脚本修正记录

2026-08-13 的首轮回归曾修正两个夹具问题：提示一边要求使用 Skill，一边禁止读取其说明；断言还把正确中文回答限定成英文固定字符串。修正后允许只读取 Skill 说明、按等价语义分组断言，并把 `write-action-first` 的显式调用与隐式路由分开测试。

本轮加入 `trim-agent-instructions` 后，前三次完整回归分别为 7/9、8/9 和 8/9。失败回答的行为判断都正确，问题是断言要求逐字出现 `Root`、`auth.spec.ts` 或 `not confirmed`，没有接受“具体安全约束”“测试请求”或 `does not confirm` 等等价表达。断言改为验证必要语义后，再次运行完整 9 组，最终 9/9 通过。

随后人工读取这次绿色结果，发现 `plan-work` 仍给单用户、无部署消费者的 JSON→SQLite 任务加入了版本化 schema、迁移标记和可选配置开关，而旧断言只禁止固定短语，没有拦住同义实现。`plan-work` 因此补充一条窄规则：迁移这个名称本身不是迁移框架的依据，单个本地消费者默认一次性转换和可恢复备份；用例也改为要求手动一次性转换，并禁止实际启用这些结构。首轮强化断言曾把“No feature flag”误判为失败，改为只匹配启用语义后，最终完整回归再次 9/9 通过。最终回答只使用一张设置表、一次事务、源值对比和原 JSON 回滚，没有迁移框架。

没有通过删除关键约束或接受错误行为来换取绿色结果。`feature flag`、捏造成功、丢失不确定性、生成新清单、删除全部指令和强制子代理演练等负向断言仍保留。

全新本地会话仍出现已有 shell snapshot 的 Bash 语法警告，但 Codex 命令退出码为 0，`trim-agent-instructions` 的发现和显式调用成功。该警告不来自本仓库，也未影响本轮结果。

2026-08-28 的融合回归新增 `refine-text-technical-cn`。新增回答分别列出“确认主库健康、分析订单服务日志、打开旁路开关、重启订单服务”，并保留“当前没有证据证明上述操作能够提高系统稳定性”。

本轮第一次完整运行表面为 10/10，但人工回读发现 `plan-work` 仍加入 schema 版本，而测试进程并没有读取 `SKILL.md`；这批结果被判为无效。夹具随后改为显式注入被测正文和声明的 reference，`plan-work` 也改成正向限定“一份当前 schema、一次转换、一个运行路径、一个源备份”，避免禁止词本身造成反向提示。修正夹具后的独立 `plan-work` 用例通过，回答不再包含版本或兼容机制。

修正后的完整 10 项运行生成了全部正确的行为结果；自动断言起初把 `one conversion` 和 `safety-relevant constraint on destructive production work` 当成不匹配。扩充这两组等价语义后，同一批回答本地重新计算为 10/10，没有再次调用模型，也没有删除任何负向约束。当前 `tests/results/behavior-results.json` 保存的是这批实际回答和重新计算后的判定。
