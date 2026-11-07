# 私有加密同步通道

用于把本机 **WorkBuddy 与 CodeBuddy 的原文记忆、技能包与配置**跨设备同步上 GitHub，同时不改变公开仓库的零 PII 边界。源范围见 `sources.yaml`，由「更新一下大脑」流程重建。

## 它解决什么

公开层（`core/ context/ playbook/`）只含脱敏蒸馏后的规则与偏好，任何 AI 都能直接读。但原文记忆（身份、联系方式、家庭、印章/发票、签名、简历、使用节奏、含本机路径的技能元信息）也确实需要在新设备上可用。本通道把这些原文打成**一个加密 blob** 后再入库：

- GitHub 上只有一个密文文件，不暴露文件名清单、目录结构与内容。
- 目标设备解密到 `local/workbuddy/`（被 gitignore），AI 在本地可读，写回仓库的永远只是密文。
- 即使仓库公开，也不泄露 PII；口令丢失则密文不可恢复。

## 三种状态

| 状态 | 表现 | 说明 |
|---|---|---|
| 未启用 | `private/workbuddy.bundle.enc` 不存在 | 仓库开箱即用，只有公开层 |
| 已加密同步 | 存在单个 `.enc` 文件 | 由用户在本机显式执行，脚本不会自动生成 |
| 已还原 | `local/workbuddy/` 有解密内容 | 仅本机，永不提交 |

## 口令来源（优先级）

1. `AI_BRAIN_PASSPHRASE` 环境变量 —— 推荐，口令完全不落盘。
2. `local/passphrase.txt` —— 本机一次性文件（被 gitignore），由 `init-passphrase` 生成。

口令值**永不进入**命令行、命令输出、日志、总结与仓库。

## 使用（需确认后执行）

路径一，口令由你掌握：

```powershell
$env:AI_BRAIN_PASSPHRASE = Read-Host -MaskInput
python scripts/sync_private.py encrypt
python scripts/sync_private.py verify
```

路径二，本机一键（值不回显）：

```powershell
python scripts/sync_private.py init-passphrase   # 生成随机口令，只提示保存位置
python scripts/sync_private.py encrypt
python scripts/sync_private.py verify
```

**路径二生成后必做**：把口令从 `local/passphrase.txt` 转移到口令管理器，然后执行 `python scripts/sync_private.py forget` 删除该文件。这是口令唯一一次明文落盘。

新设备（推荐用环境变量，不要复制明文口令文件）：

```powershell
$env:AI_BRAIN_PASSPHRASE = Read-Host -MaskInput
python scripts/sync_private.py decrypt          # 还原到 local/workbuddy/
python scripts/sync_private.py verify
```

`bootstrap` 检测到 bundle 且口令可用时会自动调用 `decrypt`；口令不可用则跳过，不报错。

## 规则

1. 生成 bundle 属于**需确认**操作（见 `core/boundaries.md`），AI 不自动执行。
2. 原文在内存中打包，不落盘到仓库工作区；临时文件一律不用。
3. 口令、解密后的目录、导出清单全部被 `.gitignore` 排除。
4. 密文文件不参与 `audit.py` 扫描（二进制），`doctor.py` 会校验它确为加密产物。
5. 若某个外部服务需要额外凭证才能同步，按 `ADR-0001` 不引入该链路。

## 风险与边界

- 口令是唯一密钥，无恢复机制；请用口令管理器保存，且**不要放进本仓库**。
- 密文一旦推送，历史中始终存在（内容安全，但文件大小与提交时间这类元信息会保留）。
- 更换口令需重新生成并覆盖 bundle，旧密文仍在历史中，因此不要在多处复用口令。
- 聚合效应：`local/workbuddy/` 解密后只在受控设备存在，不要把它复制到公开位置或贴进对话。
