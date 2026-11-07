---
id: core-boundaries
title: 可为 / 需确认 / 禁止
type: rule
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: always
summary: 读取与本地生成可自主；推送、删除、安装、外发与内容升级需确认；敏感数据严禁落盘。
tags: [boundaries, approval]
---
## 规则

- BOUND-001 **可自主**：读取仓库与本地文件、生成/更新 `dist/`、运行只读校验与测试、写 `inbox/` 建议卡片。
- BOUND-002 **需确认**：推送到远端、删除文件、安装依赖、调用外部 API、任何外发或消费类操作、把 `local/` 内容升为 `public`、生成加密 bundle。
- BOUND-003 **禁止**：把 secret 写入任何文件；把 WorkBuddy 原文记忆写入内容层；绕过 `audit.py` 或 CI；手改 `dist/`。
- BOUND-004 生成加密 bundle 前必须确认口令来源已就绪（环境变量或本机一次性文件），口令值不进命令行与输出，且原文不落盘到仓库工作区。
- BOUND-005 涉及不可逆操作（推送、清理历史、重建仓库）先说明影响再执行。
