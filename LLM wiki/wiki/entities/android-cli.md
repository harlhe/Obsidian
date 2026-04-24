---
title: Android CLI
aliases: [Android 命令行工具, android-cli]
type: entity
created: 2026-04-24
updated: 2026-04-24
tags: [android, cli, tool, google]
sources: [google-releases-android-cli]
---

# Android CLI

Google 于 2026 年 4 月发布的 Android 命令行工具，定义为"从终端进行 Android 开发的主要接口"，专门为 AI agent 和自动化场景设计。

## 核心定位

Android CLI 旨在解决 LLM 在 Android 开发中执行"有标准答案"的工程动作时的不确定性问题。通过提供稳定的命令、结构化输出和明确的参数约束，让 AI agent 能够以可预测的方式完成 Android 工程任务。

## 主要能力

- **SDK 组件管理**: `android sdk install` — 管理和安装 SDK 组件
- **项目创建**: `android create` — 从官方模板快速生成工程
- **设备管理**: `android emulator` — 管理虚拟设备
- **部署运行**: `android run` — 部署和运行应用
- **工具更新**: `android update` — 保持工具最新版本
- **技能管理**: `android skills list/find/add` — 发现、安装和管理 Android Skills

## 技术特点

- **轻量可编程**: 专为 agent/自动化场景优化的接口设计
- **稳定输出**: 提供结构化输出和明确的参数约束
- **易于更新**: 简化的更新机制确保工具保持最新
- **与 IDE 衔接**: 可与 Android Studio 配合使用，agent 在终端快速搭建原型后，可在 IDE 中进行深度调试和工程化完善

## 性能数据

根据 Google 内部实验数据：
- **Token 消耗降低**: 在项目与环境初始化任务上，token 使用量降低超过 70%
- **完成速度提升**: 任务完成速度提升到 3 倍

## 应用场景

- AI agent 驱动的 Android 开发
- 自动化 CI/CD 流水线
- 快速原型搭建
- 批量设备管理和部署

## Related

- [[google-releases-android-cli]] — 来源素材
- [[android-skills]] — 与 CLI 配合使用的技能包
- [[android-knowledge-base]] — 实时文档检索
- [[android-agent]] — 使用此工具的 AI 代理概念
- [[androidpub]] — 报道此工具发布的媒体平台
