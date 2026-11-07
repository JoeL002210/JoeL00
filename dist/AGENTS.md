<!-- GENERATED FROM MANIFEST by scripts/build.py — DO NOT EDIT -->
# ai-brain · 共享简报 v1.0.0
本文件为生成物。修改请改 `core/`、`playbook/`、`context/` 后重跑 `scripts/build.py`。
## 常驻规则

### 可为 / 需确认 / 禁止 · `core-boundaries`

## 规则

- BOUND-001 **可自主**：读取仓库与本地文件、生成/更新 `dist/`、运行只读校验与测试、写 `inbox/` 建议卡片。
- BOUND-002 **需确认**：推送到远端、删除文件、安装依赖、调用外部 API、任何外发或消费类操作、把 `local/` 内容升为 `public`、生成加密 bundle。
- BOUND-003 **禁止**：把 secret 写入任何文件；把 WorkBuddy 原文记忆写入内容层；绕过 `audit.py` 或 CI；手改 `dist/`。
- BOUND-004 生成加密 bundle 前必须确认口令来源已就绪（环境变量或本机一次性文件），口令值不进命令行与输出，且原文不落盘到仓库工作区。
- BOUND-005 涉及不可逆操作（推送、清理历史、重建仓库）先说明影响再执行。

### 工作约定 · `core-conventions`

## 规则

- CONV-001 收到任务先检查是否有匹配技能；设计先于编码，测试先于实现。
- CONV-002 声明完成、已修复或测试通过之前，必须运行验证命令并确认输出，用证据支撑断言。
- CONV-003 产品参数、部件位置、尺寸等不臆测，回到原始素材核实；不确定就用标注或示意。
- CONV-004 改文件前先读该文件；优先做小范围定点修改，不擅自重构大文件。
- CONV-005 凭据值不得出现在对话总结、日志、命令输出三处：用一次性文件 + 环境变量传值，落盘前脱敏，完成后用只返回布尔的扫描复核。
- CONV-006 调用带鉴权服务缺少必需凭证且用户已表示放弃时，不再主动重试该路线。
- CONV-007 已知网络结论为「需用户侧先启用接入条件」时，不反复探测端口或重试直连。
- CONV-008 会话前同步远端、会话后提交；冲突时 rebase 后人工裁决，规则类内容不用自动覆盖。

### 角色与协作定位（泛化） · `core-identity`

## 规则

- IDENT-001 角色类型：独立开发者 + 产品对外物料负责人 + 大模型工程实践学习者。不含姓名、组织、职位与任职时间。
- IDENT-002 工作语言：简体中文；技术术语保留英文原文。
- IDENT-003 熟练度：工程工具链与自动化熟练；大模型与 AI Agent 方向从零基础起步，讲解需降低术语门槛、先补前置基础、不预设高算力条件。
- IDENT-004 领域：AI 工具链与技能封装、内容/视觉物料制作、结构化自学资料。
- IDENT-005 提需求时习惯一次给全目标、约束与验收点，属于「已想清楚」类型。
- IDENT-006 所在区域、设备数量、组织与账号信息一律不写进仓库，属 `local/` 层。

## 反例

- 写「姓名 / 公司 / 邮箱 / 所在地 / 履历时间线」→ 违反陌生人测试，退回 `local/`。

### 沟通与交付偏好 · `core-preferences`

## 规则

- PREF-001 用简体中文回答，简明直达，先给结论与要紧信息，不铺陈过程。
- PREF-002 需求已经写清楚时直接推进，一次交付可直接使用的成品，不做多轮澄清。
- PREF-003 由 AI 替用户做的默认选择，必须在交付中显式标注为「AI 的决定」，不写成用户同意过的。
- PREF-004 推荐学习资料时优先给可运行代码 / notebook 与实践顺序；涉及 GPU、权重下载等前置依赖时主动提示。
- PREF-005 讲解降低术语门槛、循序渐进、含实践与阶段检验，不直接要求高算力训练。
- PREF-006 交付时给出产物的完整路径与关键验证数据，不只给脚本或思路。
- PREF-007 路径写完整路径或 `${...}` 占位，不写裸相对路径。

## 示例

- 「确认后直接落地骨架，并把由我定的默认值列在最后一节」符合 PREF-002 / PREF-003。

## 反例

- 需求已列全却先反问三个澄清问题 → 违反 PREF-002。

### 目标、非目标与决策原则 · `core-principles`

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

### 项目上下文索引 · `context-index`

## 规则

- CTX-001 项目卡片一律 `on-demand`，先读索引再按需拉取，不整批注入。
- CTX-002 项目用 slug 指代，不写组织名、客户名、产品型号、真实路径与报价。
- CTX-003 状态为 `paused` / `archived` 的项目不自动加载，除非本次任务明确涉及。

## 项目索引

| ID | slug | 状态 | 摘要 | last_reviewed |
|---|---|---|---|---|
| PRJ-001 | PROJ-SKILLS | active | 15 个个人技能包的封装与迭代 | 2026-11-07 |
| PRJ-002 | PROJ-LEARN | active | 大模型与 AI Agent 的结构化自学 | 2026-11-07 |
| PRJ-003 | PROJ-MATERIALS | active | 产品对外物料制作，规格以原始素材为准 | 2026-11-07 |
| ADR-001 | decision-0001 | active | 选纯文本 + Git，不依赖外部知识库服务 | 2026-11-07 |

## 按需索引

| ID | 类型 | 摘要 | 路径 |
|---|---|---|---|
| `prompt-session-start` | prompt | 新会话开头同步远端、自检一致性、按需拉取项目上下文。 | `playbook/prompts/prompt-001-session-start.md` |
| `prompt-handoff` | prompt | 生成可跨设备续接的交接摘要，并把改进建议写进 inbox 而非直接改核心规则。 | `playbook/prompts/prompt-002-handoff.md` |
| `prompt-privacy-review` | prompt | 按陌生人测试逐项复核新增内容，扫描器只报布尔结论。 | `playbook/prompts/prompt-003-privacy-review.md` |
| `skill-workbuddy-index` | index | 15 个 wb-* 技能的编号、场景与触发说法；完整原文通过加密 bundle 同步。 | `playbook/skills/workbuddy-index.md` |
| `wf-session` | workflow | 同步 → 自检 → 按需加载 → 收尾写 inbox → 重跑生成 → 提交。 | `playbook/workflows/wf-001-session.md` |
| `wf-onboard-device` | workflow | 克隆 → 装依赖 → bootstrap 安装到用户级 → 可选解密 → doctor 自检。 | `playbook/workflows/wf-002-onboard-device.md` |
| `ADR-001` | context | 不引入需 Client ID / API Key 的外部知识库，避免凭证缺失导致共享链路不可用。 | `context/decisions/ADR-0001.md` |
| `PRJ-002` | context | 零基础起步的结构化自学，偏实践型资料、每日约一小时、含阶段检验。 | `context/projects/proj-learning.md` |
| `PRJ-003` | context | 物料制作以原始素材为唯一权威来源，产品本体保持完整，部件用爆炸图表达。 | `context/projects/proj-materials.md` |
| `PRJ-001` | context | 把一组玩法清单逐条封装为可自然语言触发的用户级技能，迭代时改原技能而非新建。 | `context/projects/proj-skills.md` |
| `context-timeline` | context | 只记阶段与决策，不记具体人物、组织与事件细节。 | `context/timeline.md` |

## 使用约束

- 只按 ID 拉取本次任务需要的卡片，不整批注入（渐进式披露）。
- 一个工具一个适配器，新增工具不动内容层。
- 原文记忆需解密到 `local/` 后才可读；不得写回仓库。
- 本仓库不含 PII；任何真实标识信息都属 `local/`。
