---
id: prompt-handoff
title: 会话交接 · 换设备续接
type: prompt
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 生成可跨设备续接的交接摘要，并把改进建议写进 inbox 而非直接改核心规则。
tags: [prompt, handoff, trigger]
---
## 触发词

「交接」「换台电脑继续」「写个 handoff」「收尾」

## 模板

```
产出一份交接摘要，包含：
1. 本次目标与结论（不含任何真实姓名、组织、路径、凭据）。
2. 已改动的文件 ID 清单与未提交项。
3. 下次续接必须先读的项目卡片 ID。
4. 待确认的改进建议：逐条写入 inbox/，不要直接改 core/。
5. 提醒：会话后提交，CHANGELOG 留一行。
```

## 输出约束

- 摘要里出现任何具体标识信息时，先替换为 `${...}` 占位或项目 slug。
- 建议卡片必须带 `sensitivity: local`，由人复核后才可能升级。
