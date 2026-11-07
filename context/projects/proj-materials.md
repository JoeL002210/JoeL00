---
id: PRJ-003
title: PROJ-MATERIALS · 产品对外物料
type: context
scope: project:PROJ-MATERIALS
status: active
version: 1
updated: 2026-11-07
review_by: 2027-01-07
sensitivity: public
load: on-demand
summary: 物料制作以原始素材为唯一权威来源，产品本体保持完整，部件用爆炸图表达。
tags: [project, media, source-of-truth]
---
## 规则

- PRJ-301 产品图、部件名与尺寸的**唯一权威来源是原始素材文件**；不臆测参数，不编造规格。
- PRJ-302 涉及结构拆解 / 部件特写时，先回到素材图定位真实部件；不确定就用标注或示意。
- PRJ-303 演示中产品本体保持完整，部件用独立爆炸图抽出并标注，**不对产品图做几何切分**。
- PRJ-304 素材缺失的过程实拍不得伪装成实拍，用示意图表达并说明。
- PRJ-305 连载类成片必须复用已锁定的角色图、场景图与音色参数，不逐集重新随机生成；改设定须同步更新基准文件并标注版本。
- PRJ-306 组织名、客户名、产品型号、真实尺寸、报价与素材绝对路径属 `local/`，不进仓库。

## 关键路径

`${ASSET_ROOT}/`（具体值由 `local/overrides.yaml` 提供）

## 反例

- 凭想象把机身下半段当作某个可拆卸部件 → 曾导致整段成片返工。
