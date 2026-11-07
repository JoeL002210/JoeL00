---
id: wf-session
title: 会话前后标准流程
type: workflow
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 同步 → 自检 → 按需加载 → 收尾写 inbox → 重跑生成 → 提交。
tags: [workflow, session]
---
## 规则

- WF-101 会话前：同步远端（rebase），运行 `doctor.py`；不一致先停并报告。
- WF-102 任务前：读简报，按索引只拉本次需要的 `on-demand` 卡片。
- WF-103 收尾：改进建议写 `inbox/`，标 `sensitivity: local`，不直接改 `core/`。
- WF-104 任何卡片改动后重跑 `build.py`，`dist/` 与内容层一并提交。
- WF-105 提交前跑 `audit.py`，只接受布尔结论；有命中即停。
- WF-106 `CHANGELOG.md` 留一行，格式为 `type(scope): 简述`。

## 示例

```
改 core/preferences.md → build.py → audit.py → doctor.py → 提交（含 dist/）
```
