
## 1. 目标与结论


1. 取消Playwright 

2. 浏览器底层统一收口采用 `agent-browser --native`。

3.  `自然语言 -> scenario -> skill -> action` 。

4. 一键入口已经收口到 [`qa-all.sh`](/Users/gaozhiyang/dev-docs/devstar/qa-all.sh)，默认会一次性跑通所有测试场景。

 [`meeting01.md`](/Users/gaozhiyang/dev-docs/devstar/docs/meeting01.md) ：先做单机可跑通的 AI 驱动方案，不维护脆弱的页面脚本。

  
## 2. 方案概览

整体链路如下：

  

1. 自然语言输入目标

2. planner 选择 scenario 或动态 skill

3. scenario 组织业务顺序

4. skill 组织单个业务动作

5. action 调用底层执行能力

6. `agent-browser` / Git / Docker / MCP / VS Code CLI 执行真实动作

7. API / Git / MCP / CLI 负责确定性校验

8. evidence / report 输出截图、日志和结论

## 4. Skill 说明


- `goal`：用户想完成什么

- `scenario`：为了完成目标，需要按什么顺序跑

- `skill`：每一步具体做什么

- `action`：每一步调用什么底层能力

- `executor`：真正执行命令的底层实现

  

当前分层关系是：

  

**`goal -> planner -> scenario -> skill -> action -> executor`**

  

在代码里的对应位置：

  

- `scenario`：[`scenario-catalog.ts`](/Users/gaozhiyang/dev-docs/devstar/qa/devstar-agent-runtime/src/scenarios/scenario-catalog.ts)

- `skill registry`：[`registry.ts`](/Users/gaozhiyang/dev-docs/devstar/qa/devstar-agent-runtime/src/skills/registry.ts)

- 浏览器 action：[`agent-browser.ts`](/Users/gaozhiyang/dev-docs/devstar/qa/devstar-agent-runtime/src/actions/browser/agent-browser.ts)

| **维度**                | **page-agent**                | **agent-browser**              |
| --------------------- | ----------------------------- | ------------------------------ |
| **面向对象**              | 页面任务目标                        | 浏览器原子动作                        |
| **所在层级**              | planner / scenario / skill 上层 | engine / action 底层             |
| **典型输入**              | 自然语言目标、页面上下文、已有 plan          | URL、selector/ref、截图路径、命令参数     |
| **典型输出**              | 任务步骤、下一步决策、任务结果               | URL、snapshot、screenshot、动作执行结果 |
| **更适合做什么**            | 组织页面任务                        | 执行浏览器动作                        |
| **是否适合作为交互入口**        | 是                             | 否                              |
| **是否适合作为底层执行基础**      | 否                             | 是                              |
| **在 DevStar QA 中的角色** | 未来可作为上层 agent 形态              | 当前实际使用的浏览器底座                   |
## 5. 结果


目前已经把 QA 能力收口成一个统一总目录：

1. 顶层一键测试入口：[`qa-all.sh`](/Users/gaozhiyang/dev-docs/devstar/qa-all.sh)
`](/Users/gaozhiyang/dev-docs/devstar/devstar-qa-scripts/bin/devstar-qa)

2. Web 控制台入口：`./devstar-qa-suite/scripts/bin/devstar-qa-console`

  

其中顶层一键入口现在默认包含 IDE 场景，并且终端只输出简洁结果，例如：


```text

doctor PASS

PASS login-probe

PASS create-repo

PASS vscode-mcp-tool-call

qa PASS

```

  

### 5.3 当前支持场景

  
已验证可实现结果：
1 核心业务场景：

  

1. 登录页探测

2. 模板建仓

3. 本地 Git pull/push

4. DevContainer 启动

5. DevContainer 内 Git pull/push

6. MCP pull/push

2 IDE 集成场景：

  

1. VS Code MCP 配置识别

2. VS Code Copilot 真实 MCP tool call

  

### 5.4 已验证结果
核心 6 场景完整通过的批次：

[`summary.md`](/Users/gaozhiyang/dev-docs/devstar/qa/devstar-agent-runtime/artifacts/scenario-sweep-20260316T170215/summary.md)

结果：

doctor PASS

PASS login-probe

PASS create-repo

PASS local-git

PASS devcontainer-oob

PASS devcontainer-git

PASS mcp-sync

PASS vscode-mcp-tool-call

qa PASS


## 附录：安装、打包与使用步骤（README）

  

### A.1 打包范围

  

如果目标机器已经安装好了 DevStar，当前最稳的做法不是只拷一个 `suite` 目录，而是至少一起带上下面 4 个目录，并保持相对路径不变：

  

1. [`devstar-qa-suite`](/Users/gaozhiyang/dev-docs/devstar/devstar-qa-suite)

2. [`devstar-qa-scripts`](/Users/gaozhiyang/dev-docs/devstar/devstar-qa-scripts)

3. [`qa`](/Users/gaozhiyang/dev-docs/devstar/qa)

4. [`docs`](/Users/gaozhiyang/dev-docs/devstar/docs)

  

### A.2 目标机器依赖

  

目标机器至少需要：

  

1. Node.js 22+

2. pnpm

3. git

4. curl

5. jq

  

如果要跑 DevContainer 场景，还需要：

  

1. Docker

  

如果是 Linux，`agent-browser` 还需要浏览器运行依赖。

  

### A.3 安装步骤

  

在目标机器进入仓库根目录后，按顺序执行：

  

```bash

pnpm --dir qa/agent-browser install

pnpm --dir qa/devstar-agent-runtime install

pnpm --dir devstar-qa-scripts install

  

pnpm --dir qa/agent-browser run build

pnpm --dir qa/devstar-agent-runtime run build

```

  

然后安装 `agent-browser` 的本地浏览器依赖：

  

macOS 或依赖已齐全的环境：

  

```bash

node qa/agent-browser/bin/agent-browser.js install

```

  

Linux 推荐：

  

```bash

node qa/agent-browser/bin/agent-browser.js install --with-deps

```

  

### A.4 运行配置

  

最简单的方式是直接配置环境变量：

  

```bash

export DEVSTAR_BASE_URL=http://127.0.0.1:8080

export DEVSTAR_USERNAME=your-login

export DEVSTAR_PASSWORD=your-password

export DEVSTAR_OWNER=your-owner

export DEVSTAR_TOKEN=your-token

```

  

### A.5 一键运行

  

最推荐的入口：

  

```bash

./qa-all.sh

```

  

它会默认把 VS Code Copilot MCP tool-call 场景一起带上，并且终端只输出简洁的 PASS/FAIL 列表。

  

如果只想先检查环境：

  

```bash

./devstar-qa-suite/verify-devstar.sh --doctor

```

  

如果只跑冒烟：

  

```bash

./qa-all.sh --smoke

```

  

如果只跑一个场景：

  

```bash

./devstar-qa-suite/verify-devstar.sh --scenario "从模板创建仓库并确认结果"

./devstar-qa-suite/verify-devstar.sh --scenario "通过 VSCode Copilot 真实调用 MCP get_my_user_info 工具"

```

  

### A.6 控制台入口

  

本地 Web 控制台入口：

  

```bash

./devstar-qa-suite/scripts/bin/devstar-qa-console

```

  

然后打开：

  

`http://127.0.0.1:4318`