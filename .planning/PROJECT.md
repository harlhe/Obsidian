# Obsidian 学习笔记重构

## What This Is
这是一个针对个人 Obsidian 知识库的结构化重构项目。目标是把已有 111 篇学习笔记按主题一致性重新归档，建立“总览 + 原文索引 + 可追溯重定向”的知识结构，并补齐稀疏内容以提升复习效率。

## Core Value
同一主题的信息必须可在一个入口下被快速找到、快速复习、快速追溯来源。

## Requirements

### Validated

- ✓ 完成顶层目录结构稳定化（00-06）— existing
- ✓ 完成重分类/融合映射记录机制 — existing

### Active

- [ ] 建立各目录总览并补齐索引
- [ ] 完成非空且字符数 <= 800 笔记的深度补强
- [ ] 完成重分类后旧路径重定向与链接可达性校验

### Out of Scope

- 删除空白笔记 — 当前先保留作为占位，后续再清理
- 引入全新目录体系（改动 00-06）— 保持现有顶层结构稳定

## Context
- 当前仓库：111 篇 Markdown，主题分布不均，存在空白占位与低信息密度笔记。
- 已确认策略：全库分批、主题重构、重复融合、外部资料补充并标注来源。
- 本轮执行强调“先结构后内容”：先完成目录/索引/重定向，再做深度补充。

## Constraints
- **Compatibility**: 保持 00-06 顶层目录不变 — 避免影响既有检索习惯
- **Traceability**: 迁移必须保留旧路径可追踪 — 防止历史链接失效
- **Content Policy**: 空白文件不补内容 — 按既定策略执行

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 使用“主题总览 + 原文索引”作为统一入口 | 降低检索成本，提升复习路径清晰度 | ✓ Good |
| 稀疏阈值使用字符数 <= 800 | 中文语料更稳定，避免词数失真 | ✓ Good |
| 重分类保留旧路径重定向 | 减少断链风险，支持渐进迁移 | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-20 after initialization*
