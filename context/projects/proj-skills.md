---
id: PRJ-001
title: PROJ-SKILLS · 个人技能包
type: context
scope: project:PROJ-SKILLS
status: active
version: 1
updated: 2026-11-07
review_by: 2027-01-07
sensitivity: public
load: on-demand
summary: 把一组玩法清单逐条封装为可自然语言触发的用户级技能，迭代时改原技能而非新建。
tags: [project, skills]
---
## 规则

- PRJ-101 目标：让一组玩法清单变成可被自然语言触发的技能，而不是仅停留在文档。
- PRJ-102 范围：15 个用户级技能，跨项目可用；索引见 `playbook/skills/workbuddy-index.md`。
- PRJ-103 迭代方式：用后发现问题直接更新对应技能文件，不新建重复技能。
- PRJ-104 分发：单个技能目录可打包分发；打包产物不进本仓库。

## 非目标

- 不做技能市场缓存或未启用插件的同步，那些属于本机缓存，不是「大脑」。

## 关键路径

`${CODEBUDDY_HOME}/skills/${SKILL_NAME}/`、`${WORKSPACE}/00-Shared/`

## 反例

- 把技能包里含本机路径的元信息原样提交 → 违反隐私边界。
