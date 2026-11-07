# ai-brain

跨电脑、跨 AI 工具共享同一份「大脑」。纯文本 + Git，无服务端、无 API Key 依赖。

## 30 秒理解

- `core/`、`playbook/`、`context/` 是**唯一真源**，只有这里能改。
- `dist/` 是生成物，提交进仓库但**禁止手改**（头部有 `GENERATED` 标记）。
- 各 AI 工具读 `dist/` 的入口文件，由 `bootstrap` 安装到工具的**用户级**配置位置，一次配置全项目生效。
- 公开层只含脱敏后的规则与偏好；WorkBuddy 原文记忆与技能包通过 `private/` 的加密 bundle 跨设备同步，见 `private/README.md`。

## 分支约定

**所有内容与更新都在 `ai-brain` 分支**，`main` 保持仓库原有内容不动。

- 克隆后第一件事：`git checkout ai-brain`（仓库默认分支是 `main`，不切就看不到这套内容）。
- 上游已指向 `origin/ai-brain`，日常直接 `git pull --rebase` 与 `git push`，不要加分支参数。
- 不向 `main` 推送、不向 `main` 发合并请求、不把 `main` 合进 `ai-brain`。

## 新设备接入

1. `git clone <repo-url> ~/ai-brain`（Windows：`%USERPROFILE%\ai-brain`）
2. `git checkout ai-brain`
3. `python -m pip install -r requirements.txt`
4. `pwsh scripts/bootstrap.ps1`（Linux/macOS：`bash scripts/bootstrap.sh`）先看 dry-run 计划，确认后再加 `-Install` / `--install` 真正写入各工具配置；已存在的目标文件会先备份到 `local/backups/`。
5. `python scripts/doctor.py` → 期望输出 `OK`

## 日常

说一句「**更新一下大脑**」即执行全量同步：同步远端 → 收集 WorkBuddy / CodeBuddy 两侧变化 → 重建加密 bundle → 重生成入口 → 全套验证 → 提交并推送到 `ai-brain`。完整步骤见 `playbook/prompts/prompt-004-update-brain.md`，这套流程写在仓库里，换设备、换 AI 都读得到。

会话中 AI 的改进建议写进 `inbox/`，不直接改 `core/`；改了任何卡片后必须重跑 `python scripts/build.py` 并在 `CHANGELOG.md` 留一行。

详见 `CONTRIBUTING.md`（写入协议）、`PRIVACY.md`（边界）、`SECURITY.md`（误提交处理）。
