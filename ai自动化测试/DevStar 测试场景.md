# ## 一、23种测试场景总表

| #   | 场景 ID                            | 场景名称                  | 模块                      | 说明                              |
| --- | -------------------------------- | --------------------- | ----------------------- | ------------------------------- |
| 1   | `platform-access-ready`          | 平台接入准备度               | `platform`              | 判断 DevStar 实例是否可访问,能否开始测试       |
| 2   | `account-session-ready`          | 账号会话准备度               | `platform`              | 判断账号登录态、会话状态是否具备继续测试条件          |
| 3   | `repository-bootstrap-ready`     | 仓库启动能力                | `repository`            | 判断仓库是否具备初始化和继续研发条件              |
| 4   | `repository-collaboration-ready` | 仓库协作准备度               | `repository`            | 判断仓库是否具备协作、评审、流转基础              |
| 5   | `devcontainer-capability-ready`  | 云开发能力准备度              | `devcontainer`          | 判断 DevContainer 能力是否存在          |
| 6   | `ai-integration-ready`           | AI 集成准备度              | `mcp`                   | 判断 AI / MCP / IDE 集成前提是否存在      |
| 7   | `platform-first-impression`      | 平台首屏观感检查              | `platform`              | 检查首页首屏可用性与产品观感                  |
| 8   | `install-entry-ready`            | 安装入口验收                | `install`               | 检查安装入口是否清晰、是否可执行                |
| 9   | `install-first-login-ready`      | 安装后首次登录验收             | `install`               | 检查安装完成后的首次登录链路                  |
| 10  | `repo-git-sync`                  | 仓库 Git 同步链路           | `repository`            | 检查仓库 Git 拉取、同步相关能力              |
| 11  | `issue-create`                   | Issue 创建链路            | `collaboration`         | 检查 Issue 创建流程是否具备条件             |
| 12  | `pr-create`                      | PR 创建链路               | `collaboration`         | 检查 PR 创建入口和前提是否具备               |
| 13  | `pr-merge`                       | PR 合并链路               | `collaboration`         | 检查 PR 合并验证前提是否具备                |
| 14  | `devcontainer-create`            | 开发容器创建链路              | `devcontainer`          | 检查 DevContainer 创建链路            |
| 15  | `devcontainer-open-ide`          | 开发容器 IDE 打开链路         | `devcontainer`          | 检查 DevContainer 页面是否具备 IDE 打开条件 |
| 16  | `mcp-server-call`                | MCP 服务调用准备度           | `mcp`                   | 检查 MCP Server 调用前提是否存在          |
| 17  | `ide-mcp-visible`                | IDE MCP 可见性           | `mcp`                   | 检查 IDE 侧是否能识别 MCP 能力            |
| 18  | `runner-register`                | Runner 注册准备度          | `cicd`                  | 检查 CI/CD Runner 注册前提            |
| 19  | `workflow-run`                   | Workflow 执行准备度        | `cicd`                  | 检查 Workflow 是否具备运行条件            |
| 20  | `workflow-artifact`              | Workflow Artifact 准备度 | `cicd`                  | 检查 Workflow 产物链路是否具备条件          |
| 21  | `devstar-login-flow`             | DevStar 真实登录链路        | `platform`              | 用真实浏览器完成登录,并确认进入用户主页            |
| 22  | `repository-create-flow`         | 仓库真实创建链路              | `repository`            | 用真实浏览器创建新仓库,并确认仓库页成功打开          |
| 23  | `pr-and-vscode-flow`             | PR 提交与 VS Code 打开链路   | `collaboration` / `ide` | 完成代码提交、创建 PR,并用本机 VS Code 打开工作区 |

---

## 二、当前已经存在的20个正式场景

### 1. 安装与平台

| 场景 ID                       | 场景名称      | 说明                         |
| --------------------------- | --------- | -------------------------- |
| `platform-access-ready`     | 平台接入准备度   | 判断当前实例是否已经达到可以继续做产品测试的基本状态 |
| `account-session-ready`     | 账号会话准备度   | 判断账号与会话是否具备进入后续链路的条件       |
| `platform-first-impression` | 平台首屏观感检查  | 从首页入口视角检查页面是否具备继续验证条件      |
| `install-entry-ready`       | 安装入口验收    | 判断安装入口和使用入口是否明确可达          |
| `install-first-login-ready` | 安装后首次登录验收 | 检查安装完成后的第一条登录链路            |

### 2. 仓库与协作

| 场景 ID | 场景名称 | 说明 |
|---|---|---|
| `repository-bootstrap-ready` | 仓库启动能力 | 判断仓库是否具备继续研发和继续测试的基础条件 |
| `repository-collaboration-ready` | 仓库协作准备度 | 判断仓库是否具备协作、评审、流转基础 |
| `repo-git-sync` | 仓库 Git 同步链路 | 检查 Git 基础同步链路是否具备条件 |
| `issue-create` | Issue 创建链路 | 检查 Issue 创建入口和流程条件 |
| `pr-create` | PR 创建链路 | 检查 PR 创建入口、分支对比和流程提示 |
| `pr-merge` | PR 合并链路 | 检查 PR 合并验证前提是否已经具备 |

### 3. 云开发与 IDE

| 场景 ID | 场景名称 | 说明 |
|---|---|---|
| `devcontainer-capability-ready` | 云开发能力准备度 | 判断 DevContainer 是否具备基础能力 |
| `devcontainer-create` | 开发容器创建链路 | 检查是否已经具备创建 DevContainer 的条件 |
| `devcontainer-open-ide` | 开发容器 IDE 打开链路 | 检查是否已经具备打开 IDE 或终端的条件 |

### 4. AI / MCP

| 场景 ID | 场景名称 | 说明 |
|---|---|---|
| `ai-integration-ready` | AI 集成准备度 | 判断 AI / MCP / IDE 集成前提是否存在 |
| `mcp-server-call` | MCP 服务调用准备度 | 检查是否已经具备继续做 MCP Server 调用验证的条件 |
| `ide-mcp-visible` | IDE MCP 可见性 | 判断 IDE 或 AI 客户端是否具备识别 MCP 线索的条件 |

### 5. CI/CD

| 场景 ID | 场景名称 | 说明 |
|---|---|---|
| `runner-register` | Runner 注册准备度 | 检查是否具备继续做 Runner 注册的条件 |
| `workflow-run` | Workflow 执行准备度 | 检查是否具备继续做 Workflow 执行验证的条件 |
| `workflow-artifact` | Workflow Artifact 准备度 | 检查是否具备继续做 Workflow 产物验证的条件 |
