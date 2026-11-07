---
id: context-index
title: 项目上下文索引
type: index
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-01-07
sensitivity: public
load: always
summary: 按需拉取的项目卡片清单；只列 ID、状态与摘要，不复制正文。
tags: [index, context]
---
## 规则

- CTX-001 项目卡片一律 `on-demand`，先读索引再按需拉取，不整批注入。
- CTX-002 项目用 slug 指代，不写组织名、客户名、产品型号、真实路径与报价。
- CTX-003 状态为 `paused` / `archived` 的项目不自动加载，除非本次任务明确涉及。

## 项目索引

| ID | slug | 状态 | 摘要 | last_reviewed |
|---|---|---|---|---|
| PRJ-001 | PROJ-SKILLS | active | 15 个个人技能包的封装与迭代 | 2026-11-07 |
| PRJ-002 | PROJ-LEARN | active | 大模型与 AI Agent 的结构化自学 | 2026-11-07 |
| PRJ-003 | PROJ-MATERIALS | active | 产品对外物料制作，规格以原始素材为准 | 2026-11-07 |
| ADR-001 | decision-0001 | active | 选纯文本 + Git，不依赖外部知识库服务 | 2026-11-07 |
