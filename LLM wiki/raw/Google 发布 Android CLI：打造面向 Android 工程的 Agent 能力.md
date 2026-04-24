---
title: "Google 发布 Android CLI：打造面向 Android 工程的 Agent 能力"
source: "https://mp.weixin.qq.com/s/8cSDbKkeZJuQkFCBcMuzIQ"
author:
  - "[[AndroidPub]]"
published:
created: 2026-04-24
description:
tags:
  - "clippings"
---
AndroidPub *2026年4月20日 08:18*

2026 年 4 月，Google 发布了 Android Agent 开发三件套：Android CLI、Android skills 以及 Android Knowledge Base。它的核心诉求很明确：无论开发者在 Android Studio、Gemini CLI，还是第三方 agent（例如 Claude Code、Codex）里发起任务，都应该能以相对一致的方式获得高质量的 Android 工程结果。

这背后对应的是一个现实矛盾：LLM 能写代码，但 Android 开发里大量“有标准答案”的工程动作并不适合让模型用自然语言猜一遍，比如 SDK/组件安装、工程初始化、设备管理与部署、以及一些高度流程化但容易踩坑的任务（edge-to-edge、AGP 升级、R8 keep rules 治理等）。Google 选择的方向不是让每个 agent 都各写一套脚本和提示词，而是把这些能力收敛到一个更可控的分发与调用体系里。

## 为什么是 CLI：把不确定的工程动作变成可调用的接口

在官方介绍里，Android CLI 被定义为“从终端进行 Android 开发的主要接口”，专门为 agent/自动化场景提供轻量、可编程的入口，覆盖环境设置、项目创建、设备管理，并强调易更新。

其一是“接口形态”更适合 agent。对 agent 来说，稳定的命令、结构化输出、明确的参数约束，比依赖 GUI 交互或散落的脚本集合更可控；而 Android 开发生态本身就存在大量命令行工具链，CLI 是天然的整合入口。

其二是“工程动作可标准化”。官方给出的能力清单非常聚焦：用 android sdk install 做 SDK 组件管理，用 android create 从官方模板快速生成工程，用 android emulator 管理虚拟设备、用 android run 部署运行，以及用 android update 保持工具更新。官方也给出了内部实验数据：在项目与环境初始化这类任务上，Android CLI 能显著减少 token 消耗并提升完成速度。官方宣传开发同类 Android Agent 应用 token 使用量降低超过 70%，完成速度提升到 3 倍。

从发布策略看，Android CLI 当前处于 preview 阶段，定位更像“面向 agent 的底座能力”，并且强调与 Android Studio 的衔接：可以先在终端用 agent 快速搭出原型，再回到 Android Studio 做更深入的 UI 调试、profiling 与工程化完善。

## 为什么是 Skills：让 LLM 具备“可重复执行”的专家流程

Google 同步发布 Android skills 仓库 `https://github.com/android/skills` ，动机在官方文中也写得很直白：传统文档偏概念与叙述，适合人类学习，但 LLM 在执行复杂工作流时更需要“可操作、可验证”的技术规范，否则容易出现过时模式、库选择不当或步骤遗漏。

因此 Android skills 选择了偏工程资产的表达形式：每个 skill 是一个目录，核心文件是 `SKILL.md` ，文件头用 YAML 写清楚元数据，例如 `name` 、 `description` 、 `metadata.keywords` ；正文再把前置条件、步骤、必须/禁止规则、检查点与参考资料写成“执行规格”。官方文档也明确说明，技能遵循 Agent Skills 的开放标准（agentskills.io），从而能被“任何支持 skills 的 AI 工具”使用，而不是绑定某一种特定模型或 IDE。

这套 Skill 的第一批内容，正好覆盖了 Android 团队最希望 agent 少踩坑的关键路径：Navigation 3 的安装与迁移、Compose 应用的 edge-to-edge 适配、AGP 9 与 XML-to-Compose 迁移、R8 配置分析等。

## CLI 与 Skills 怎么连在一起：安装、发现、激活

Android CLI 把 Android skills 当作一个可管理的“技能包”。流程可以理解为三步。

第一步是 **发现** ：用 android skills list 查看当前有哪些官方技能可用；如果只记得方向不记得名字，可以用 android skills find <关键词> 做一次匹配检索。

第二步是 **安装** ：用 android skills add 把技能下载安装到本机 agent 的 skills 目录里。可以用 --skill=只装某一个，也可以用 --all 全量安装；如果需要限定安装对象，用 --agent=

指定安装到哪一个 agent。

第三步是 **激活/使用** ：当 agent 执行任务时，如果请求内容与某个 skill 的 description/keywords 命中，它会把该 skill 的 SKILL.md（以及同目录的 references 等资源）加载进上下文，按其中的步骤与约束执行；如果希望显式指定某个技能，也可以在支持 skills 的工具里通过“点名”的方式触发（具体入口取决于所用的 agent/IDE）。

## 为什么还要 Knowledge Base：对抗 LLM 知识不足与漂移

在 Android CLI 与 Skills 之外，Google 还强调了 Android Knowledge Base：通过 android docs 命令从一个专门的数据源里搜索与拉取权威文档片段，作为 agent 的实时上下文。官方给出的解释是，这能让 agent 把回答“接地”到 Android Developer docs、Firebase、Google Developers 与 Kotlin docs 的最新内容上，即使 LLM 的训练截止时间较早，也能在关键决策点参考最新指南。

这也是把 AI 能力工程化的一种典型做法：与其期待模型“天然知道最新最佳实践”，不如提供一个低摩擦的检索入口，让它在执行任务时可以主动对齐权威信息。

## 小结：这次发布的本质是“把 agent 工作流产品化”

Android CLI、Android skills 与 Android Knowledge Base 组合在一起，解决的不是“模型会不会写代码”，而是“工程动作能不能被稳定执行”。CLI 负责把环境、工程创建、设备与部署等核心动作变成确定接口；Skills 负责把关键工作流沉淀成可重复执行的专家流程；Knowledge Base 则负责把最新官方知识以可检索方式注入 agent。

这套体系的一个重要信号是“面向任意 agent”：它既服务 Android Studio 的内置 agent，也面向终端与第三方工具链，希望把高质量 Android 开发的路径从单一 IDE 扩展到更分布式的开发环境。

\-- END --

