---
title: Android Skills
aliases: [Android 技能包, android-skills]
type: entity
created: 2026-04-24
updated: 2026-04-24
tags: [android, skills, automation, google]
sources: [google-releases-android-cli]
---

# Android Skills

Google 于 2026 年 4 月发布的 Android 技能包仓库，提供可操作、可验证的技术规范，帮助 LLM 执行复杂的 Android 工作流。仓库地址：https://github.com/android/skills

## 核心动机

传统 Android 文档偏重概念与叙述，适合人类学习，但 LLM 在执行复杂工作流时更需要"可操作、可验证"的技术规范。否则容易出现：
- 使用过时的开发模式
- 选择不当的库
- 遗漏关键步骤

## 技术规范

每个 Android Skill 是一个目录，核心文件是 `SKILL.md`，包含：

- **元数据**: 使用 YAML 格式定义，包括 `name`、`description`、`metadata.keywords`
- **前置条件**: 执行前需要满足的环境和依赖
- **执行步骤**: 详细的操作步骤
- **规则约束**: 必须遵守和禁止的操作
- **检查点**: 用于验证执行结果的检查项
- **参考资料**: 相关文档和链接

## 标准兼容

Android Skills 遵循 [[agent-skills]] 开放标准（agentskills.io），这意味着：
- 可被"任何支持 skills 的 AI 工具"使用
- 不绑定特定模型或 IDE
- 跨平台兼容性

## 首批技能覆盖

第一批 Android Skills 覆盖了 Android 团队最希望 agent 少踩坑的关键路径：

- **Navigation 3**: 安装与迁移
- **Compose 应用**: Edge-to-edge 适配
- **AGP 9**: Android Gradle Plugin 升级
- **XML-to-Compose**: 迁移工作流
- **R8 配置**: 代码混淆和精简配置分析

## 与 Android CLI 的集成

Android CLI 将 Android Skills 当作可管理的"技能包"：

1. **发现**: `android skills list` — 查看可用技能；`android skills find <关键词>` — 关键词检索
2. **安装**: `android skills add [--skill=] [--all] [--agent=]` — 下载并安装技能
3. **激活**: 当 agent 执行任务时，如果请求内容与某个 skill 的 description/keywords 匹配，会自动加载该 skill 的 SKILL.md 并按规范执行

## Related

- [[google-releases-android-cli]] — 来源素材
- [[android-cli]] — 技能包的管理和调用工具
- [[agent-skills]] — 遵循的开放标准
- [[android-agent]] — 使用技能包的 AI 代理
- [[androidpub]] — 报道此技能包发布的媒体平台
