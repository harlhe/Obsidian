---
title: Agent Skills
aliases: [AI 技能标准, 技能标准, agent-skills]
type: concept
created: 2026-04-24
updated: 2026-04-24
tags: [agent, skills, standard, automation]
sources: [google-releases-android-cli]
---

# Agent Skills

一种用于定义和标准化 AI agent 技能的开放标准，旨在让 AI 工具能够以可重复、可验证的方式执行复杂工作流。标准网站：agentskills.io

## 核心思想

传统文档偏重概念与叙述，适合人类学习，但 LLM 在执行复杂工作流时更需要"可操作、可验证"的技术规范。Agent Skills 标准提供了一种结构化的方式来定义这些规范。

## 技术规范格式

一个 Agent Skill 通常包含以下部分：

- **元数据**: 使用 YAML 格式定义名称、描述、关键词等
- **前置条件**: 执行前需要满足的环境、依赖和配置
- **执行步骤**: 详细的操作步骤和命令
- **规则约束**: 必须遵守的操作和禁止的操作
- **检查点**: 用于验证执行结果的检查项和预期输出
- **参考资料**: 相关文档、链接和资源

## 核心文件

每个 skill 的核心文件是 `SKILL.md`，采用标准化的格式编写，确保：
- **可操作性**: 提供明确的步骤和命令
- **可验证性**: 包含检查点和预期结果
- **可维护性**: 结构清晰，易于更新

## 标准优势

1. **跨平台兼容**: 不绑定特定模型或 IDE，可被任何支持该标准的 AI 工具使用
2. **减少错误**: 避免使用过时模式、选择不当的库或遗漏关键步骤
3. **提升质量**: 将最佳实践沉淀为可重复执行的流程
4. **易于分享**: 技能可以打包、分发和复用

## 应用实例

[[android-skills]] 是 Agent Skills 标准的一个具体实现，提供了 Android 开发领域的标准化技能包。

## 设计理念

Agent Skills 体现了 AI 能力工程化的思路：将领域专家的知识和经验转化为可被 AI 理解和执行的结构化规范，而不是依赖 AI 通过自然语言猜测或学习。

## Related

- [[google-releases-android-cli]] — 来源素材
- [[android-skills]] — 该标准在 Android 领域的实现
- [[android-agent]] — 使用技能标准的 AI 代理概念
