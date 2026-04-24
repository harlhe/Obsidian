---
title: Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力
aliases: [Android CLI 发布, Android Agent 三件套]
type: source
created: 2026-04-24
updated: 2026-04-24
tags: [android, cli, agent, google]
raw_file: raw/Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力.md
---

# Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力

## 来源信息

- **原始文件**: [raw/Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力.md](../../raw/Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力.md)
- **类型**: 技术文章
- **日期**: 2026-04-20
- **作者**: [[androidpub]]

## 核心内容

2026 年 4 月，Google 发布了 Android Agent 开发三件套：[[android-cli]]、[[android-skills]] 以及 [[android-knowledge-base]]。这套工具旨在为 AI 代理提供标准化、可重复的 Android 工程能力，无论开发者在 Android Studio、Gemini CLI，还是第三方 agent（如 Claude Code、Codex）中发起任务，都能以相对一致的方式获得高质量的 Android 工程结果。

这一举措解决了 Android 开发中的一个现实矛盾：LLM 能够编写代码，但 Android 开发中大量"有标准答案"的工程动作（如 SDK/组件安装、工程初始化、设备管理与部署、edge-to-edge 适配、AGP 升级、R8 keep rules 治理等）并不适合让模型用自然语言猜测。Google 的策略是将这些能力收敛到一个更可控的分发与调用体系中。

## 核心组件

### Android CLI
定义为"从终端进行 Android 开发的主要接口"，专门为 agent/自动化场景提供轻量、可编程的入口。覆盖环境设置、项目创建、设备管理，并强调易更新。官方数据显示，在项目与环境初始化类任务上，Android CLI 能显著降低 token 消耗（超过 70%）并提升完成速度（提升到 3 倍）。

### Android Skills
发布于 `https://github.com/android/skills`，提供可操作、可验证的技术规范，帮助 LLM 执行复杂工作流。每个 skill 是一个目录，核心文件是 `SKILL.md`，包含元数据、前置条件、步骤、规则、检查点与参考资料。遵循 [[agent-skills]] 开放标准（agentskills.io）。首批内容覆盖 Navigation 3 安装与迁移、Compose 应用 edge-to-edge 适配、AGP 9 与 XML-to-Compose 迁移、R8 配置分析等关键路径。

### Android Knowledge Base
通过 `android docs` 命令提供权威文档片段的实时检索，让 agent 能够参考 Android Developer docs、Firebase、Google Developers 与 Kotlin docs 的最新内容，对抗 LLM 知识不足与漂移问题。

## 关键要点

- **标准化工程动作**：CLI 将环境设置、项目创建、设备管理、部署等核心动作变成确定接口
- **可重复专家流程**：Skills 将关键工作流沉淀成可重复执行的专家流程，避免 LLM 使用过时模式或遗漏步骤
- **实时权威知识**：Knowledge Base 提供最新官方知识的检索入口，确保 agent 对齐最佳实践
- **跨平台兼容**：面向任意 agent，既服务 Android Studio 内置 agent，也面向终端与第三方工具链
- **性能提升**：官方实验数据显示 token 使用量降低超过 70%，完成速度提升到 3 倍

## 引用与数据

- Token 使用量降低：超过 70%
- 完成速度提升：提升到 3 倍
- Skills 仓库：https://github.com/android/skills
- Agent Skills 标准：agentskills.io

## Related

- [[android-cli]] — 终端 Android 开发接口
- [[android-skills]] — 可重复执行的专家流程
- [[android-knowledge-base]] — 实时权威文档检索
- [[agent-skills]] — 开放技能标准
- [[android-agent]] — AI 驱动的 Android 开发概念
- [[androidpub]] — 文章发布的媒体平台
