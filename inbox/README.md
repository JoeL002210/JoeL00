# inbox

AI 在会话中发现的规则改进、偏好变化、项目状态更新，写到这里，**不直接改 `core/`**。

每张建议卡片沿用 `schema/card.schema.json`，但必须带 `sensitivity: local`。由人 triage 后决定：

- 采纳 → 脱敏后写入 `core/` / `playbook/` / `context/`，改标 `public`，重跑 `build.py`。
- 仅本机有效 → 留在 `local/`。
- 不采纳 → 移入 `archive/` 并注明原因。

处理完清空本目录，只保留本文件。
