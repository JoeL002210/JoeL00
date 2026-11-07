# 写入协议

## 唯一真源

只改 `core/`、`playbook/`、`context/` 里的卡片。**禁止手改 `dist/` 与任何入口文件**，生成物头部有 `GENERATED` 标记；手改视为破坏一致性。

## 卡片格式

UTF-8 / LF 的 Markdown + YAML frontmatter。必填字段与枚举见 `schema/card.schema.json`。

```yaml
---
id: P-003
title: 需求明确时直接给成品
type: preference          # preference | rule | prompt | context | workflow | index
scope: global             # global | project:<slug> | tool:<name>
status: active            # active | deprecated | archived
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public       # public 才允许进仓库
load: always              # always | on-demand | never
summary: 需求写清楚时一次交付成品，不多轮追问。
tags: [communication, delivery]
---
## 规则
- P-003 需求已明确时直接推进，一次交付可用成品。

## 示例
...
## 反例
...
## 变更记录
- v1 2026-11-07 建立。
```

- 每条规则一行、祈使句、带稳定 ID；引用只认 ID 不认路径。
- 固定小节标题 `## 规则 / ## 示例 / ## 反例 / ## 变更记录`，供 `build.py` 稳定切片。
- `summary` ≤ 150 字，用于索引与 `index.jsonl`。
- 单卡片 ≤ 200 行；`always` 卡片总量受 `MANIFEST.yaml` 预算约束。

## 流程

1. 一条主题一次提交：`type(scope): 简述`。
2. 更新卡片时同步 `version`、`updated`、`## 变更记录`，并在 `CHANGELOG.md` 留一行。
3. 改完执行 `python scripts/build.py`，把 `dist/` 一并提交。
4. AI 在会话中提出的改进写 `inbox/`，由人 triage 后合并，**不直接改 `core/`**。
5. `review_by` 到期标 `stale`；月度复审，季度把无引用的 `stale` 卡片移入 `archive/`，只归档不删除。

## 发版

`content_version` 与 tag 同步。破坏性 schema 变更升主版本，并同步升级全部 `adapters/`。旧字段先标 `deprecated`，下个主版本再移除。新增 AI 工具 = 加一个 `adapters/<tool>.yaml` + 重跑 `build.py`，内容层一个字不动。

## 冲突

规则类内容**不用 last-write-wins 自动覆盖**。多设备冲突时 rebase 后按 `updated` 与人工裁决。会话前 `git pull --rebase`，会话后提交。
