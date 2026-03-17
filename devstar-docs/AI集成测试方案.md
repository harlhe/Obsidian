# DevStar GUI Agent 自然语言测试方向汇报

  

## 1. 文档信息

  

| 项目 | 内容 |

|---|---|

| 文档名称 | DevStar GUI Agent 自然语言测试方向汇报 |

| 适用范围 | DevStar Web、DevContainer、MCP、跨软件协同测试 |

| 当前版本 | v2.0 |

| 更新时间 | 2026-03-11 |

| 编写人 | Codex |

  

---

  

## 2. 方向调整结论

  

结合最近一轮手工集成测试、最小闭环自动化验证和会议讨论，当前方向正式调整如下：

  

1. 不再把 Playwright 固定脚本作为长期主路线。

2. 新方向以 **GUI Agent / Browser Agent + Skill + 自然语言编排** 为核心。

3. 测试目标从“脚本通过”调整为“自然语言驱动发现问题并保留证据”。

4. 自动化重点从 CI 内固定 E2E 转向 **单机可重复验证的 GUI Agent 测试框架**。

5. AI 不再只是总结器，而是成为场景编排入口；但最终结果仍需有证据支撑。

  

一句话概括：

  

**从“维护 Playwright 脚本”转向“构建可用提示词驱动的 GUI Agent 测试系统”。**

  

---

  

## 3. 为什么要调整方向

  

本轮方向调整的原因很明确：

  

### 3.1 Playwright 方案过于脆弱

  

当前脚本方案存在以下问题：

  

1. UI 结构或文案一改，脚本就容易失效。

2. 页面路径、按钮、表单、DOM 结构都在放大维护成本。

3. 前端变化会持续制造脚本技术债。

4. 复杂链路下，固定脚本很难兼顾灵活性和可维护性。

  

这意味着：

  

**Playwright 适合作为底层能力，但不适合作为长期测试表达层。**

  

### 3.2 纯人工测试效率太低

  

目前手工测试已经能验证很多问题，但存在明显瓶颈：

  

1. 重复操作多。

2. 多软件协同验证成本高。

3. 很难持续复现相同步骤。

4. 结论容易分散在个人操作过程里。

  

### 3.3 纯 AI 自由执行也不够稳

  

会议中已经明确：

  

1. 纯 AI 直接“看页面然后判断通过”不可靠。

2. AI 如果不能感知过程，只看结果，会漏掉很多问题。

3. 测试核心是发现问题，不是让 AI 宣布“通过”。

  

因此，新方向不是“纯 AI 替代测试”，而是：

  

**让 GUI Agent 负责执行，让 Skill 负责稳定动作，让证据系统负责支撑结论。**

  

---

  

## 4. 新方案目标

  

新方案的总体目标是：

  

**通过自然语言描述测试意图，由 GUI Agent 调度 Browser/Desktop Skill 完成实际操作，并输出带证据的测试结论。**

  

具体目标：

  

1. 用自然语言描述测试场景。

2. 用 Agent 驱动浏览器和桌面重复操作。

3. 用 Skill 封装高频稳定动作，降低维护成本。

4. 用统一证据机制记录关键过程、异常和最终结论。

5. 支持跨软件测试，而不局限于单一 Web 页面。

  

---

  

## 5. 新方案核心思想

  

### 5.1 自然语言是入口

  

后续测试不再以“写固定脚本”为主要入口，而是以自然语言描述为入口。

  

例如：

  

1. 验证用户首次进入系统后可以从模板创建仓库。

2. 验证在本地模式下可以完成 pull、修改、push。

3. 验证在 DevContainer 模式下 MCP 可以读取并回写仓库。

  

### 5.2 Skill 是稳定性核心

  

Skill 用来封装容易重复、适合复用的动作单元。

  

例如：

  

1. 登录 DevStar

2. 从模板创建仓库

3. 打开 DevContainer 页面

4. 打开 WebTerminal

5. 在桌面 IDE 中连接 DevContainer

6. 在 MCP 客户端中执行一次标准读写链路

  

Skill 的作用不是替代 Agent，而是约束 Agent：

  

1. 对重复动作给出标准路径。

2. 降低提示词漂移带来的不稳定。

3. 降低因 UI 微调导致的整体失效概率。

  

### 5.3 GUI Agent 负责跨软件协同

  

新方向特别强调：

  

1. 不只控制浏览器。

2. 还要能控制桌面软件。

3. 还要能在多个软件之间切换。

  

这正是 GUI Agent 比传统浏览器脚本更有价值的地方。

  

重点不是单个页面点按钮，而是完整链路：

  

1. 浏览器打开 DevStar

2. 创建仓库或 DevContainer

3. 切到 IDE / WebTerminal / MCP 客户端

4. 执行操作

5. 返回系统界面验证结果

  

### 5.4 测试的核心是发现问题

  

会议中明确的一条原则需要保留：

  

**测试的核心不是证明“通过”，而是稳定地发现问题并记录问题。**

  

因此后续体系必须满足：

  

1. 任何需要人工补救的项都要明确标记。

2. 任何异常都要写清楚卡点、症状、临时处理和影响范围。

3. 最终报告必须能说明“哪里不稳定、哪里要人工配置、哪里仍有风险”。

  

---

  

## 6. 新的系统结构

  

建议将后续系统拆成四层：

  

### 6.1 自然语言编排层

  

输入自然语言测试目标。

  

作用：

  

1. 理解用户要测什么。

2. 选择合适场景。

3. 选择执行模式。

4. 决定要调用哪些 Skill。

  

### 6.2 场景层

  

场景层定义“要验证的功能链路”。

  

当前目标场景矩阵：

  

| 测试模式 | 开箱即用 | pull/push | MCP pull/push |

|---|---|---|---|

| 本地模式 | local-out-of-box | local-git-pull-push | local-mcp-pull-push |

| DevContainer 模式 | devcontainer-out-of-box | devcontainer-git-pull-push | devcontainer-mcp-pull-push |

  

说明：

  

1. 场景是业务目标。

2. Skill 是场景的执行单元。

3. Agent 负责在运行时调度 Skill。

  

### 6.3 Skill 层

  

Skill 层负责封装具体稳定动作。

  

建议第一批 Skill 包括：

  

1. DevStar 登录 Skill

2. 模板建仓 Skill

3. 仓库文件修改 Skill

4. DevContainer 打开 Skill

5. WebTerminal 打开 Skill

6. MCP 连接 Skill

7. Git pull/push Skill

8. 结果截图与状态记录 Skill

  

### 6.4 证据与报告层

  

必须保留：

  

1. 操作步骤记录

2. 页面截图或关键状态截图

3. 关键文本/日志摘要

4. 手工配置项说明

5. 最终结论和风险说明

  

这层决定系统是不是“测试系统”，而不只是“Agent 演示”。

  

---

  

## 7. Playwright 在新方案中的位置

  

Playwright 不是完全废弃，而是降级为可选底层能力。

  

具体定位：

  

1. 不再作为主表达层。

2. 不再要求所有测试场景直接写成 Playwright 脚本。

3. 只在需要稳定浏览器动作时，作为某些 Skill 的内部实现。

  

也就是说：

  

**后续维护对象不应该是大量 Playwright 用例，而应该是少量通用 Skill。**

  

这样即使 UI 有变化，影响范围也更可控。

  

---

  

## 8. 当前已有成果如何承接新方向

  

虽然方向调整了，但目前已完成的工作并不浪费。

  

可以保留的内容：

  

1. `basic-function-integration-test-report.md` 中的测试事实和问题清单。

2. 已验证的最小闭环经验。

3. runner Docker API 问题的定位与修复结论。

4. `local-git-pull-push` 已跑通的业务闭环经验。

  

需要调整的内容：

  

1. 不再把现有 Playwright/Node 脚本视为长期最终形态。

2. 把已完成的闭环逻辑抽象为 Skill 或场景知识。

3. 后续重点放在“如何让 Agent 复用这些能力”，而不是继续堆脚本。

  

---

  

## 9. 测试记录规则

  

会议中已经对记录方式达成共识，后续继续保持：

  

1. 测试核心是发现问题，而不是追求“全绿”。

2. 凡是需要手工配置或人工补救的项，统一标记为 `⚠️`。

3. 备注中必须写明：

- 卡点

- 症状

- 手工处理步骤

- 处理后是否可继续验证

4. 最终状态优先维护在统一 Markdown 或 issue 描述中，而不是散落在评论里。

  

---

  

## 10. 技术实施方案

  

按“主流、容易跑通、能尽快出结果”这三个标准，建议采用下面这条技术路线：

  

**Browser Agent 为主，Skill 为核心，Playwright 作为浏览器执行底座，Git/API 作为结果断言底座，桌面 GUI 控制放到第二阶段。**

  

这条路线不是最炫的，但最适合当前 DevStar 现状：

  

1. 当前仓库已经有 Node.js、Playwright、Makefile、现成场景代码，可以直接复用。

2. 浏览器链路是当前最成熟、最容易稳定复现的一层。

3. Git、API、日志断言已经验证有效，比纯视觉判断可靠很多。

4. 真正重的桌面 GUI 自动化在 macOS 上会碰到权限、焦点切换、OCR、分辨率适配等问题，不适合第一步就作为主链路。

  

### 10.1 技术选型

  

建议首期统一使用以下技术栈：

  

| 层级 | 选型 | 作用 |

|---|---|---|

| 编排层 | Node.js | 复用现有仓库技术栈，降低接入成本 |

| Agent 入口 | LLM + 结构化 Prompt | 把自然语言目标转成场景计划 |

| Browser 执行层 | Playwright | 稳定执行浏览器动作 |

| Skill 层 | 本地 JS 模块 + 清单定义 | 封装可复用动作 |

| 断言层 | DevStar API + Git CLI + 日志抓取 | 判断是否成功、沉淀证据 |

| 报告层 | Markdown + JSON + 截图 | 输出过程和结论 |

  

首期不建议直接上重型 Agent 框架，原因很简单：

  

1. 先把自然语言到 Skill 调用这条链路跑通，比先引入复杂框架更重要。

2. 现阶段真正的难点不在多 Agent 编排，而在场景稳定性和证据闭环。

3. 一个轻量的“计划器 + Skill 执行器 + 报告器”更容易控制。

  

### 10.2 系统模块拆分

  

建议在 `qa/ai-e2e` 下继续演进为以下结构：

  

1. `agent/`

- 负责接收自然语言输入

- 生成结构化执行计划

2. `skills/`

- 每个 Skill 一个独立模块

- 对外暴露统一输入输出

3. `scenarios/`

- 定义业务目标和 Skill 编排顺序

4. `assertions/`

- 负责 API 校验、Git 校验、日志校验

5. `artifacts/`

- 保存截图、步骤记录、JSON 结果、Markdown 报告

  

建议的数据流如下：

  

1. 用户输入自然语言目标。

2. Agent 将目标转成结构化 Scenario Plan。

3. Scenario Plan 调用一个或多个 Skill。

4. Skill 执行动作并返回结构化结果。

5. 断言层收集 API/Git/日志证据。

6. 报告层汇总为最终结论。

  

### 10.3 首期 Skill 设计

  

首批 Skill 不宜太多，建议只做 6 个：

  

1. `login-devstar`

2. `create-repo-from-template`

3. `clone-edit-commit-push`

4. `open-devcontainer`

5. `run-mcp-read-write`

6. `capture-evidence`

  

每个 Skill 统一遵循一个接口：

  

```ts

type SkillInput = {

runId: string;

scenarioId: string;

params: Record<string, unknown>;

};

  

type SkillResult = {

ok: boolean;

summary: string;

outputs?: Record<string, unknown>;

evidence?: {

screenshots?: string[];

logs?: string[];

apiChecks?: string[];

gitChecks?: string[];

};

};

```

  

这样做的价值是：

  

1. Agent 不直接操作细节，只负责选择 Skill。

2. Skill 可以被场景复用。

3. 失败时可以精确知道是哪一个 Skill 失效。

  

### 10.4 自然语言编排的最小实现

  

首期不要追求“AI 自主思考很多步”，建议直接做成受控编排。

  

推荐流程：

  

1. 输入一句自然语言目标。

2. 让模型只输出结构化 JSON。

3. JSON 中只允许：

- 选择场景

- 选择 Skill

- 填充参数

4. 本地执行器校验 JSON 合法后再执行。

  

示例：

  

```json

{

"scenarioId": "local-git-pull-push",

"mode": "local",

"skills": [

{"name": "login-devstar", "params": {}},

{"name": "create-repo-from-template", "params": {"template": "base"}},

{"name": "clone-edit-commit-push", "params": {"file": "README.md"}},

{"name": "capture-evidence", "params": {"finalCheck": true}}

]

}

```

  

这样可以避免两个常见问题：

  

1. 模型随意发挥，导致执行失控。

2. 提示词一变化，整体流程不稳定。

  

### 10.5 浏览器执行层怎么做

  

浏览器侧继续使用 Playwright，但职责要收缩：

  

1. 只做“页面打开、点击、输入、等待、截图”这类稳定动作。

2. 不让 Playwright 直接承担业务判断。

3. 页面结果判断尽量下沉到 API、Git、日志三类断言。

  

这意味着后续 Playwright 代码应该像 Skill Driver，而不是 E2E 用例集合。

  

例如：

  

1. `login-devstar` Skill 内部调用 Playwright 完成登录。

2. `create-repo-from-template` Skill 内部调用 Playwright 完成建仓。

3. 最终仓库是否创建成功，不靠页面 toast 判断，而靠 API 查仓库是否存在。

  

### 10.6 为什么桌面 GUI 控制放第二阶段

  

桌面 Agent 当然要做，但不建议作为第一阶段主路线。

  

原因：

  

1. macOS 桌面控制需要额外权限授权。

2. IDE、Terminal、浏览器之间切换时，焦点和窗口状态会引入随机性。

3. 纯视觉识别相比 DOM/API 断言更容易漂移。

4. 首期如果直接做桌面主链路，成本高且不利于快速形成可复用样板。

  

因此建议：

  

1. 第一阶段先做 Browser Agent + Git/API 断言。

2. 第二阶段再把 VSCode、Terminal、MCP Client 纳入桌面 Skill。

  

### 10.7 首期要跑通的两条链路

  

从实施角度，只建议先做两条：

  

1. `local-git-pull-push`

2. `devcontainer-out-of-box`

  

原因：

  

1. 第一条最贴近当前已经跑通的事实，可以最快转成 Agent 化能力。

2. 第二条可以验证 DevContainer、Browser Agent、证据记录三者联动。

  

不建议首期就做：

  

1. 全量 MCP 场景

2. 桌面 IDE 深度控制

3. 多 Agent 协同调度

  

这些都应该在第一条链路稳定后再上。

  

### 10.8 推荐落地顺序

  

建议按 4 周拆：

  

#### 第 1 周：搭最小 Agent 骨架

  

目标：

  

1. 支持输入一句自然语言。

2. 输出结构化 Scenario Plan。

3. 能调用 2 个 Skill。

4. 能生成一份 Markdown 报告。

  

#### 第 2 周：抽稳定 Skill

  

目标：

  

1. 把现有登录、建仓、pull/push 拆成独立 Skill。

2. 统一 Skill 入参和回参。

3. 统一截图和日志采集方式。

  

#### 第 3 周：接入断言和失败归因

  

目标：

  

1. 接 DevStar API 校验。

2. 接 Git CLI 校验。

3. 失败时输出“动作失败 / 环境失败 / 产品缺陷 / 手工补救”分类。

  

#### 第 4 周：补 DevContainer 代表链路

  

目标：

  

1. 跑通 `devcontainer-out-of-box`。

2. 明确哪些步骤仍需 `⚠️`。

3. 形成第一版可汇报 Demo。

  

---

  

## 11. 下一步计划

  

建议后续按以下顺序推进：

  

1. 先把 `local-git-pull-push` 改造成自然语言触发的 Skill 链路。

2. 再把 `devcontainer-out-of-box` 做成第二条代表性场景。

3. 等这两条稳定后，再考虑桌面 GUI Skill 和 MCP 场景。

4. 在此之前，不建议继续扩写大量独立 Playwright 用例。

  

---

  

## 12. 汇报口径建议

  

如果对内汇报，建议统一使用以下口径：

  

1. 当前方向已从 Playwright 脚本维护，转向 GUI Agent + Skill + 自然语言测试。

2. 核心原因是 Playwright 对 UI 变化过于脆弱，维护成本高。

3. 新方向更适合多软件协同测试，也更契合 DevContainer、MCP、IDE 联动场景。

4. 现有手工测试和最小闭环验证结果，已经为新方向提供了场景基础和问题清单。

5. 下一步重点不是补更多固定脚本，而是先搭 Agent 框架和 Skill 体系。