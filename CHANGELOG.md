# Changelog

## Unreleased — 2026-11-25

- 修复 `private/sources.yaml` 排除规则：剔除 `.git/`、node_modules 与媒体二进制，避免 bundle 膨胀至数百 MB；本次 bundle 收敛到 33.77 MB / 4882 个源文件。

## 1.0.0 — 2026-11-07

- 建立仓库骨架：三层内容模型、卡片 schema、7 个工具适配器、生成/自检/扫描脚本与 CI 护栏。
- 完成 WorkBuddy 技能与记忆的脱敏蒸馏，加入 `core/`、`playbook/`、`context/`。
- 新增 `private/` 加密 bundle 通道，用于跨设备同步 WorkBuddy 原文记忆（默认不启用、不生成）。
