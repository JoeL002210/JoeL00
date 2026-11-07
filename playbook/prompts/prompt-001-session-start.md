---
id: prompt-session-start
title: 会话启动 · 载入共享大脑
type: prompt
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 新会话开头同步远端、自检一致性、按需拉取项目上下文。
tags: [prompt, session, trigger]
---
## 触发词

「开始工作」「接着上次」「新会话」「同步一下大脑」

## 模板

```
1. 在 ${AI_BRAIN} 执行同步远端（会话前 rebase）。
2. 运行自检，确认生成物与内容层一致；不一致先停止并报告，不自行修补。
3. 读简报，按索引判断本次任务需要哪些 on-demand 卡片，只拉需要的。
4. 复述本次任务的目标与验收点，列出由你替我做的默认选择。
5. 若需要原文记忆，确认加密 bundle 已解密到 local 后再读；不把该内容写回仓库。
```

## 输出

一段不超过 10 行的启动摘要 + 本次将用到的卡片 ID 列表。

## 反例

- 一次性把全部卡片塞进上下文 → 违反渐进披露。
