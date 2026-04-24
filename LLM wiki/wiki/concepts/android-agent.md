---
title: Android Agent
aliases: [Android AI 代理, Android 智能助手, android-agent]
type: concept
created: 2026-04-24
updated: 2026-04-24
tags: [android, agent, ai, automation]
sources: [google-releases-android-cli]
---

# Android Agent

指能够理解和执行 Android 开发任务的 AI 代理，通过自然语言交互或自动化方式完成 Android 应用开发、调试、部署等工作。

## 核心挑战

虽然 LLM 能够编写代码，但 Android 开发中存在大量"有标准答案"的工程动作，这些动作不适合让模型用自然语言猜测：

- SDK 和组件的安装
- 项目工程初始化
- 设备管理与部署
- 高度流程化但容易踩坑的任务（如 edge-to-edge 适配、AGP 升级、R8 keep rules 治理）

## 解决方案

Google 提供的解决方案是通过 [[android-cli]]、[[android-skills]] 和 [[android-knowledge-base]] 三件套，将这些工程动作标准化：

1. **CLI 层**: 将环境设置、项目创建、设备管理、部署等核心动作变成确定接口
2. **Skills 层**: 将关键工作流沉淀成可重复执行的专家流程
3. **Knowledge Base 层**: 把最新官方知识以可检索方式注入 agent

## 跨平台兼容

Android Agent 概念的一个重要特征是"面向任意 agent"：

- 既可以在 Android Studio 的内置 agent 中使用
- 也可以在终端工具（如 Gemini CLI）中使用
- 还可以在第三方 agent（如 Claude Code、Codex）中使用

目标是在不同环境中都能以相对一致的方式获得高质量的 Android 工程结果。

## 工作流程

典型的 Android Agent 工作流程：

1. 用户通过自然语言描述任务
2. Agent 分析任务需求，匹配相关的 [[android-skills]]
3. 调用 [[android-cli]] 执行具体的工程动作
4. 必要时通过 [[android-knowledge-base]] 检索最新官方文档
5. 完成任务并返回结果

## 价值

- **一致性**: 在不同环境中获得一致的工程质量
- **效率**: 显著降低 token 消耗，提升任务完成速度
- **可靠性**: 基于标准化流程和权威文档，减少错误
- **可扩展**: 可以跨平台、跨工具使用

## Related

- [[google-releases-android-cli]] — 来源素材
- [[android-cli]] — Android Agent 的核心工具
- [[android-skills]] — Android Agent 的技能包
- [[android-knowledge-base]] — Android Agent 的知识来源
- [[agent-skills]] — Android Agent 遵循的技能标准
