---
id: prompt-update-brain
title: 更新一下大脑 · 全量同步
type: prompt
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 同步远端、收集两侧变化、重建加密 bundle、重生成入口、全套验证后推送到 ai-brain。
tags: [prompt, sync, trigger, workbuddy, codebuddy]
---
## 触发词

「更新一下大脑」「同步一下大脑」「刷新大脑」「同步一下 WorkBuddy」「同步一下 CodeBuddy」

## 模板

```
1. 在 ${AI_BRAIN} 切到 ai-brain 分支，会话前同步远端（rebase）。
2. 收集两侧变化，范围以 private/sources.yaml 为准：
   - WorkBuddy：镜像记忆、wb-* 技能包、技能索引、共享清单。
   - CodeBuddy：项目记忆、用户级与项目级技能包、工作区根指令、共享文档。
3. 重新生成加密 bundle（需确认操作；口令只从环境变量或本机一次性文件读取，不回显）。
4. 新出现的行为规则/偏好先写 inbox/，由人确认并脱敏后才进公开层；不自动把原文升为 public。
5. 重跑 scripts/build.py，让 dist/ 与内容层一致。
6. 依次运行：单元测试、audit.py、build.py --check、doctor.py、bundle verify。
   任一不通过即停止，不提交、不推送。
7. 提交（内容层 + dist/ + bundle 一起），推送到 ai-brain；main 保持不动。
8. 回报改动文件数、bundle 源文件数与分组计数、验证结论；不回显任何记忆原文或口令。
```

## 约束

- 每次更新都是**全量快照**，不做增量、不自动定时执行。
- 日志、插件与市场缓存、业务产出物（视频、PPT、表格、原型、邮件、消息汇总、笔记）不纳入，也不临时扩大源清单。
- 口令不可用则跳过第 3 步并明确告知，不得用明文替代物。
- 仓库默认分支是 main；未切到 ai-brain 就更新，等于把内容写错地方。

## 反例

- 只更新公开层却忘了重建 bundle → 云端两侧不一致。
- 把新记忆直接写进 core/ 再提交 → 绕过脱敏复核，违反隐私边界。
