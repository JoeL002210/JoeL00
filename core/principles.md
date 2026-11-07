---
id: core-principles
title: 目标、非目标与决策原则
type: rule
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: always
summary: 单一真源、渐进披露、默认拒绝；不做实时协作与 SaaS 依赖，不把仓库变成简历或聊天归档。
tags: [architecture, decisions]
---
## 规则

- PRIN-001 **单一真源**：一条规则只存一处；工具差异只在适配层声明，不复制内容。
- PRIN-002 **渐进式披露**：常驻注入只有一份短简报 + 索引，细节按需读取。
- PRIN-003 **默认不可公开**：新内容默认 `local`，经脱敏复核改标 `public` 才可提交。
- PRIN-004 纯文本 + Git，不依赖任何需要 Client ID / API Key 的知识库服务。

## 目标

- 跨电脑、跨 AI 工具读到同一份规则与上下文。
- 人类可读、可 diff、可 grep、可被任意 LLM 直接解析。

## 非目标

- 不做实时多人协作编辑、不做向量检索服务、不做工具专属内容的第二份副本。

## 反目标

- 把仓库变成简历、聊天记录或日志归档。
- 手改生成物；把 `local/` 内容直接标 `public` 绕过复核。
- 为了让某个工具「读得更全」而放宽隐私边界。
