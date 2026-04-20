
## 1. 定义

  

本文档定义 DevStar 自动化测评的新主线。

  

这条主线不是 Playwright 脚本工程，也不是纯模型自由发挥点击页面，而是：

  

**用 AI 自然语言理解目标并生成计划，用 `agent-browser --native` 和 skill 执行操作，用 API/Git/CLI 做确定性校验，用 evidence/report 产出问题发现结果。**

  

## 2. 核心结论

  

1. Playwright 业务执行器不再进入主线。

2. 浏览器执行入口只允许 `agent-browser --native`。

3. 项目是 AI 自然语言驱动的项目，但不是纯 Prompt 裸奔执行。

4. 执行层可以由 `agent-browser` 原子动作和基于这些动作封装的 skill 共同组成。

5. 最终成功与否不依赖页面文案，而依赖 API、Git、CLI 等确定性校验。

6. 测试目标是发现问题和沉淀证据，不是追求“自动化通过率”。

  

## 3. 明确排除项

  

以下内容不再作为当前主线：

  

1. 不再新增任何 Playwright 业务执行器。

2. 不再保留任何“Playwright 作为 DevStar runtime 底层执行器”的方案表述。

3. 不再把 selector 脚本当成长期维护资产。

4. 不再做“纯大模型直接点页面但没有 skill、没有校验、没有证据”的方案。

5. 不再继续暴露旧 `ai-e2e` POC 目录、文件名和入口命名。

  

说明：

  

`agent-browser` 仓库内部是否还保留其他实现细节，不属于 DevStar 主线对外设计的一部分。对 DevStar runtime 来说，浏览器能力被严格定义为 `agent-browser --native`。

  

## 4. 设计原则

  

### 4.1 AI-first, but not AI-only

  

AI 负责：

  

1. 理解自然语言目标。

2. 选择 skill 或 action。

3. 生成执行计划。

4. 在失败时给出重试或回退建议。

  

Runtime 负责：

  

1. 受控执行。

2. 证据采集。

3. 确定性校验。

4. 失败分类。

5. 报告产出。

  

### 4.2 Native execution only

  

当前实现只围绕 `agent-browser --native` 设计浏览器能力边界：

  

1. 浏览器动作统一走 native browser adapter。

2. 不在 DevStar runtime 中实现任何 Playwright 页面对象模型或包装层。

3. 不允许出现第二套浏览器执行器与 native runtime 并行维护。

  

### 4.3 Skill-first

  

系统长期维护的对象不是“页面脚本”，而是“能力单元”。

  

skill 的要求：

  

1. 面向目标，而不是面向单次点击。

2. 有输入输出契约。

3. 能被多个场景复用。

4. 失败时可分类、可恢复、可回放。

  

### 4.4 Observation-first

  

执行前先观察，执行后再观察。

  

系统必须持续保留：

  

1. 当前 URL

2. 页面标题或等价页面标识

3. snapshot

4. screenshot

5. 关键断言结果

6. 失败分类

  

### 4.5 Hybrid verification

  

UI 负责进入场景，API 和 Git/CLI 负责确定性验证。

  

例如：

  

1. 登录成功由页面状态和用户态共同确认。

2. 仓库创建成功优先用 API 二次确认。

3. pull/push 是否成功优先用 Git 和 API 确认。

4. workflow 是否成功优先用 API 查询 run 状态。

  

### 4.6 Finding issues first

  

测试报告首先服务于发现问题，而不是证明“跑通了”。

  

因此报告必须能说明：

  

1. 执行到了哪一步。

2. 哪一步失败。

3. 为什么失败。

4. 失败时页面和系统状态是什么。

5. 是否需要人工介入。

  

## 5. 运行时分层

  

建议运行时拆为八层。

  

### 5.1 Planner layer

  

职责：接收自然语言目标，生成受控执行计划。

  

Planner 输出不是随意文本，而是明确步骤：

  

1. 选择已有 skill。

2. 必要时选择允许暴露的 action。

3. 指定断言与证据要求。

4. 指定失败回退策略。

  

### 5.2 Engine layer

  

职责：提供底层执行引擎。

  

当前包含：

  

1. `agent-browser --native`

2. DevStar API client

3. Git CLI adapter

4. 本地文件和临时目录能力

  

### 5.3 Action layer

  

职责：对底层引擎做稳定、最小、可测试的动作封装。

  

示例：

  

1. `open-url`

2. `snapshot-page`

3. `get-current-url`

4. `take-screenshot`

5. `get-repo-by-api`

6. `clone-repo`

  

Action 不是 skill。Action 是 skill 的基础积木。

  

### 5.4 Skill layer

  

职责：封装面向目标的可复用能力。

  

示例：

  

1. `login-devstar`

2. `create-repo-from-template`

3. `assert-login-success`

4. `assert-repo-created`

5. `open-devcontainer-and-wait-ready`

  

### 5.5 Scenario layer

  

职责：把多个 skill 组合成业务闭环。

  

它有两种来源：

  

1. 固定模板 scenario

2. Planner 根据自然语言目标动态拼装的 scenario

  

第一批目标场景：

  

1. `native-login-page-probe`

2. `native-login-create-repo`

3. `local-git-pull-push`

4. `devcontainer-out-of-box`

  

### 5.6 Verification layer

  

职责：执行确定性断言。

  

包括：

  

1. API 校验

2. Git 校验

3. CLI 校验

4. 页面状态校验

  

### 5.7 Evidence layer

  

职责：记录步骤、观察结果、截图、断言、错误、人工干预。

  

### 5.8 Report layer

  

职责：产出结构化 JSON 和可读 Markdown 报告，用于 CLI、人工复盘、后续前端展示。

  

## 6. Planner 与 skill 契约

  

skill 不能只是一个 TS 文件，还要有声明信息，便于 planner、CLI 扩展和 IDE 插件发现可用能力。

  

建议 skill spec 至少包含：

  

```ts

type SkillSpec = {

name: string;

description: string;

category: 'observe' | 'interact' | 'assert' | 'recover' | 'environment' | 'evidence';

inputs: Record<string, string>;

outputs: Record<string, string>;

preconditions: string[];

successCriteria: string[];

fallbackSkills?: string[];

};

```

  

每个 skill 应同时具备：

  

1. spec

2. handler

3. 输入输出契约

4. 成功标准

5. 失败回退关系

  

Planner 的默认选择顺序应为：

  

1. 优先使用已有 skill

2. skill 不足时，使用受控 action 补齐

3. 不允许直接生成不可审计的自由操作流

  

## 7. Skill 分类

  

为适配 CLI 扩展，skill 必须可发现、可选择、可组合。建议分为六类。

  

### 7.1 Observe skills

  

1. `observe-current-page`

2. `observe-interactive-elements`

3. `observe-console-errors`

4. `observe-network-failures`

  

### 7.2 Interaction skills

  

1. `login-devstar`

2. `create-repo-from-template`

3. `open-actions-page`

4. `open-devcontainer-page`

  

### 7.3 Assertion skills

  

1. `assert-login-success`

2. `assert-repo-created`

3. `assert-workflow-succeeded`

4. `assert-devcontainer-ready`

  

### 7.4 Recovery skills

  

1. `refresh-and-reobserve`

2. `dismiss-blocking-ui`

3. `recover-from-redirect`

4. `fallback-to-api-verification`

  

### 7.5 Environment skills

  

1. `prepare-auth-state`

2. `create-temp-workspace`

3. `clone-repository`

4. `cleanup-test-assets`

  

### 7.6 Evidence skills

  

1. `capture-evidence`

2. `classify-failure`

3. `write-run-summary`

  

## 8. P0 范围

  

P0 只做一个真实闭环，不铺太开。

  

### 8.1 P0 目标

  

通过“自然语言目标 -> planner -> native browser skill 执行 -> API 校验”的链路，稳定跑通：

  

1. 打开登录页

2. 登录 DevStar

3. 从模板创建仓库

4. 用 API 确认仓库存在

5. 输出完整证据和报告

  

### 8.2 P0 action / skill 列表

  

1. `open-login-page`

2. `login-devstar`

3. `assert-login-success`

4. `open-new-repo-page`

5. `create-repo-from-template`

6. `assert-repo-exists-via-api`

7. `capture-evidence`

  

### 8.3 P0 成功标准

  

1. 浏览器动作只通过 `agent-browser --native` 完成。

2. 自然语言目标能被 planner 映射到受控 plan。

3. 最终仓库校验不依赖页面文案，使用 API 二次确认。

4. 每一步有 screenshot 或 snapshot 证据。

5. 报告可明确指出失败步骤和失败分类。

6. 主线文档、目录和入口中不再出现 Playwright 执行器方案和旧 `ai-e2e` 命名。

  

说明：

  

P0 可以先用“自然语言目标到 scenario 模板的轻量映射”作为 planner bootstrap，但这只是过渡实现，不是最终架构终点。

  

## 9. QA 目录结构

  

当前 `qa` 目录结构如下：

  

```text

qa/

README.md

agent-browser/ # 浏览器能力引擎，外部底座

devstar-agent-runtime/ # 当前主线：AI + native skill runtime

devstar-matrix-runner/ # 从零安装矩阵编排层，负责安装后交接给 runtime

```

  

其中：

  

1. `agent-browser/` 只承担 engine 角色。

2. `devstar-agent-runtime/` 存放当前主线 runtime。

3. `devstar-matrix-runner/` 负责不同系统/环境矩阵的安装调度与 install-to-runtime handoff。

  

`devstar-agent-runtime/src/` 后续内部继续收敛为：

  

```text

src/

actions/

browser/

api/

git/

skills/

observe/

interact/

assert/

recover/

environment/

evidence/

scenarios/

planner/

runtime/

reporting/

lib/

cli.ts

app.ts

types.ts

```

  

## 10. 迁移原则

  

重构 `qa` 目录时遵循以下原则：

  

1. 不保留与当前主线无关的旧执行器目录。

2. 不暴露任何历史 POC 入口和旧 `ai-e2e` 命名。

3. 让主路径命名直接体现 AI agent runtime 主线。

4. README、方案文档和入口命名统一收敛到 `AgentPlan` 与 `devstar-agent-runtime`。

  

## 11. 下一步实施顺序

  

1. 完成 `AgentPlan` 文档重命名和引用更新。

2. 清理旧 `ai-e2e` 文档、目录和入口别名。

3. 将当前 runtime 内部继续收敛为 `planner + actions + skills + scenarios + reporting`。

4. 为现有 skill 补齐 `spec`、失败回退和证据约束。

5. 实现 P0 planner bootstrap。

6. 跑通 `native-login-create-repo`。

7. 再扩展 `local-git-pull-push` 与 `devcontainer-out-of-box`。