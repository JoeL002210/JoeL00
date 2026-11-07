---
id: prompt-privacy-review
title: 提交前 · 脱敏复核
type: prompt
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 按陌生人测试逐项复核新增内容，扫描器只报布尔结论。
tags: [prompt, privacy, trigger]
---
## 触发词

「提交前检查」「脱敏复核」「查一下有没有敏感信息」

## 模板

```
1. 列出本次新增/修改的内容层文件（ID 与路径），不打印文件内容。
2. 逐项核对 PRIVACY.md 的脱敏检查清单，特别检查聚合效应：把全部 public 文件当成一个整体评估。
3. 检查元数据：提交者邮箱、仓库名、图片 EXIF、日志与对话原文。
4. 运行扫描器，只接受布尔结论，不回显命中文本。
5. 输出结论：CLEAN 或 需人工复核的文件数。有命中即停止提交。
```

## 反例

- 把扫描命中的原文贴进对话或日志 → 造成二次泄露。
