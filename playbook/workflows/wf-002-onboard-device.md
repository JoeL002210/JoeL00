---
id: wf-onboard-device
title: 新设备 / 新工具接入
type: workflow
scope: global
status: active
version: 1
updated: 2026-11-07
review_by: 2027-02-07
sensitivity: public
load: on-demand
summary: 克隆 → 装依赖 → bootstrap 安装到用户级 → 可选解密 → doctor 自检。
tags: [workflow, onboarding]
---
## 规则

- WF-201 每台设备只克隆一份到约定位置，不复制内容；所有工具指向同一份生成物。
- WF-202 优先配置工具的**用户级全局指令**，一次配置全项目生效；项目级入口只放该项目特有补充。
- WF-203 `bootstrap` 负责安装入口、合并 `local/overrides.yaml`、按需解密 bundle。
- WF-204 机器差异（路径、接入条件、工具版本）只写 `local/`，永不提交。
- WF-205 接入后必须 `doctor.py` 输出 `OK`，否则不算接入完成。
- WF-206 新增 AI 工具 = 加 `adapters/<tool>.yaml` + 重跑 `build.py`，内容层不动。

## 反例

- 在两台机器上各自维护一份规则副本 → 必然漂移，违反单一真源。
