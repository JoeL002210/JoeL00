# ai-brain

跨电脑、跨 AI 工具共享同一份「大脑」。纯文本 + Git，无服务端、无 API Key 依赖。

## 30 秒理解

- `core/`、`playbook/`、`context/` 是**唯一真源**，只有这里能改。
- `dist/` 是生成物，提交进仓库但**禁止手改**（头部有 `GENERATED` 标记）。
- 各 AI 工具读 `dist/` 的入口文件，由 `bootstrap` 安装到工具的**用户级**配置位置，一次配置全项目生效。
- 公开层只含脱敏后的规则与偏好；WorkBuddy 原文记忆与技能包通过 `private/` 的加密 bundle 跨设备同步，见 `private/README.md`。

## 新设备接入

1. `git clone <repo-url> ~/ai-brain`（Windows：`%USERPROFILE%\ai-brain`）
2. `python -m pip install -r requirements.txt`
3. `pwsh scripts/bootstrap.ps1`（Linux/macOS：`bash scripts/bootstrap.sh`）先看 dry-run 计划，确认后再加 `-Install` / `--install` 真正写入各工具配置；已存在的目标文件会先备份到 `local/backups/`。
4. `python scripts/doctor.py` → 期望输出 `OK`

## 日常

会话前 `git pull --rebase`；会话中 AI 的改进建议写进 `inbox/`，不直接改 `core/`；会话后提交并在 `CHANGELOG.md` 留一行。改了任何卡片后必须重跑 `python scripts/build.py`。

详见 `CONTRIBUTING.md`（写入协议）、`PRIVACY.md`（边界）、`SECURITY.md`（误提交处理）。
