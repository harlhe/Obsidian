# 基本功能集成测试报告

  

> 维护方式：请优先通过**编辑 issue 描述**或统一 Markdown 文档更新结果，不建议通过追加评论维护最终状态。

  

## 测试维度说明

  

- **开箱即用**：工具安装后无需额外配置即可使用的程度（1-5分）

- **pull/push**：基础 Git 拉取和推送操作

- **MCP pull/push**：通过 MCP 方式执行 Git 拉取和推送

  

## 标记说明

  

### 开箱即用评分

  

- `⭐⭐⭐⭐⭐`：完全开箱即用，零配置

- `⭐⭐⭐⭐`：少量简单配置

- `⭐⭐⭐`：需要中等复杂度配置

- `⭐⭐`：配置复杂

- `⭐`：几乎无法使用或需要大量配置

  

### 功能测试标记

  

- `✅`：测试通过，功能正常，无需额外人工配置

- `⚠️`：部分成功或存在限制，需要手工配置或人工补救

- `❌`：测试失败，功能异常

- `⚪`：待测试

- `🚫`：不适用/不支持

  

> 记录规则：凡是需要手工配置的项，统一记为 `⚠️`，并在备注中写明“需要手工配置什么”。

  

## 一、基本功能集成测试结果

  

| 测试项 | 结果 | 备注 |

|---|---|---|

| 浏览器默认配置安装 | ✅ | Docker 方式安装成功，页面可访问 |

| 首个账号注册登录 | ✅ | 首次初始化完成，可正常进入首页 |

| 从 `templates/base` 创建仓库 | ✅ | 成功创建 `gzy/base` |

| 修改仓库文件触发 CI | ✅ | 提交后成功触发工作流 |

| matrix 多 Dockerfile / OS 标签执行 | ✅ | 多个标签任务成功展开并执行 |

| DevContainer 创建 | ⚠️ | 需要手工配置 `DOCKER_API_VERSION=1.44` 后通过 |

| VSCode 打开 DevContainer | ⚠️ | 需要手工重建 `devstar-remote-base` Docker context 后通过 |

| DevContainer 内 `pull/push` | ⚠️ | 需要手工初始化仓库后通过 |

| DevContainer 内 `MCP pull/push` | ⚠️ | 需要手工配置 MCP Token 和 VSCode MCP server 后通过 |

  

## 二、AI 工具测试结果记录表

  

| 工具名称 | 测试模式 | 开箱即用 | pull/push | MCP pull/push | 备注/问题描述 |

|---|---|---|---|---|---|

| Claude Code(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Claude Code(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| OpenCode(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| OpenCode(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| OpenClaw(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| OpenClaw(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| GEMINI(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| GEMINI(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| iFlow(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| iFlow(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| QWEN(CLI) | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| QWEN(CLI) | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| VSCode Copilot | 本地模式 | ⭐⭐⭐⭐ | ✅ | ⚠️ | MCP 需手工配置 Access Token |

| VSCode Copilot | DevContainer 模式 | ⭐⭐⭐ | ⚠️ | ⚠️ | `pull/push` 需手工初始化仓库；MCP 需手工配置 Token、`stdio bridge` 和 MCP server |

| Windsurf | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Windsurf | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Trae | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Trae | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Trae CN | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Trae CN | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Cursor | 本地模式 | ⚪ | ⚪ | ⚪ | 未测 |

| Cursor | DevContainer 模式 | ⚪ | ⚪ | ⚪ | 未测 |

  

> 这些 AI 工具可以根据情况删减和添加。

  

## 三、环境矩阵测试结果

  

> 目前重点是 x86_64 和 ARM64 环境下的 Linux 主流发行版和苹果的 macOS。

  

| 操作系统 | 架构 | 发行版/版本 | 安装结果 | 功能测试 | 备注 |

|---|---|---|---|---|---|

| Windows | x86_64 | ALL | ❌ | ❌ | 未测通原生安装 |

| Windows 11 | x86_64 | WSL2 Ubuntu | ✅ | ✅ | 已有验证结论 |

| Windows 11 | ARM64 | WSL2 Ubuntu | ⚪ | ⚪ | 待测试 |

| Linux | x86_64 | Ubuntu 22.04 LTS | ✅ | ✅ | 原生支持 |

| Linux | x86_64 | Ubuntu 24.04 LTS | ✅ | ✅ | 最新版本 |

| Linux | x86_64 | Debian 12 | ⚪ | ⚪ | 待测试 |

| Linux | x86_64 | CentOS 7 | ⚪ | ⚪ | 待测试 |

| Linux | x86_64 | RHEL 9 | ⚪ | ⚪ | 待测试 |

| Linux | x86_64 | Fedora 40 | ⚪ | ⚪ | 待测试 |

| Linux | x86_64 | Arch Linux | ⚪ | ⚪ | 滚动更新 |

| Linux | x86_64 | Alpine 3.19 | ⚪ | ⚪ | 待测试 |

| Linux | ARM64 | Ubuntu 22.04 (Raspberry Pi) | ⚪ | ⚪ | 待测试 |

| Linux | ARM64 | Debian 12 (AWS Graviton) | ⚪ | ⚪ | 待测试 |

| Linux | ARM64 | Rocky Linux 9 | ⚪ | ⚪ | 待测试 |

| Linux | ARM | ARMv7 (Raspberry Pi 3) | ⚪ | ⚪ | 32 位 ARM |

| macOS | x86_64 | Ventura 13.6 | ⚪ | ⚪ | Intel Mac，待测试 |

| macOS | ARM64 | Sonoma 14.5 / 实际本机版本 | ⚠️ | ⚠️ | Apple Silicon；Docker 安装、CI、DevContainer、VSCode Copilot 验证通过，但 DevContainer 与 MCP 相关链路需手工配置 |

| macOS | ARM64 | Sequoia 15.0 | ⚪ | ⚪ | 待测试 |

| Docker | x86_64 | Alpine 3.19 | ⚪ | ⚪ | 轻量容器 |

| Docker | ARM64 | Ubuntu 22.04 | ⚪ | ⚪ | ARM 容器 |

| Kubernetes | x86_64 | 多节点集群 | ⚪ | ⚪ | 生产环境待测试 |

| Podman | x86_64 | RHEL 9 | ⚪ | ⚪ | 无守护进程 |

  

> 这些环境可以根据情况删减和添加。

  

## 四、macOS 测试配置与问题记录

  

### 1. macOS 测试相关配置

  

| 配置项 | 配置值/处理方式 | 说明 |

|---|---|---|

| DevStar 访问地址 | `http://127.0.0.1:8080` | 本地 Docker 部署地址 |

| Docker API 兼容配置 | `DOCKER_API_VERSION=1.44` | 用于修复 DevContainer 创建失败 |

| DevContainer 仓库初始化 | 在容器内手工 clone 仓库 | 用于修复 `/workspace/base` 为空的问题 |

| VSCode Docker context | `docker context create devstar-remote-base --docker "host=ssh://base"` | 用于修复 VSCode 重连 DevContainer |

| MCP 认证 | 在 DevStar 中创建 Access Token | 用于 VSCode Copilot MCP 调用 |

| VSCode MCP 接入 | 使用 `stdio bridge` + 用户级 `mcp.json` | 避免 OAuth 自动注册流程失败 |

| VSCode DevStar 地址 | 从 `http://localhost:3000` 改为 `http://127.0.0.1:8080` | 避免扩展继续连接旧实例 |

  

### 2. macOS 测试中遇到的问题

  

| 问题 | 现象 | 影响 | 处理结果 |

|---|---|---|---|

| Docker API 版本不兼容 | `client version 1.43 is too old. Minimum supported API version is 1.44` | DevContainer 无法创建 | 通过补充 `DOCKER_API_VERSION=1.44` 恢复 |

| DevContainer 仓库未自动初始化 | `/workspace/base` 为空，`git status` 报 `not a git repository` | 容器内无法直接进行 `pull/push` | 手动 clone 后通过 |

| VSCode 临时 Docker Context 丢失 | `context "devstar-remote-base" not found` | 从 VSCode 恢复窗口重新进入容器失败 | 重建临时 Docker context 后恢复 |

| MCP 错误进入 OAuth 流程 | `Dynamic Client Registration not supported` | Copilot 无法直接连 DevStar MCP | 改为 `stdio bridge + token` 方式后恢复 |

| MCP bridge 与 Node 22 兼容性问题 | MCP server 启动失败 | 无法完成 MCP 测试 | 调整 bridge 启动方式后恢复 |

| VSCode 仍指向旧实例地址 | 配置里仍为 `http://localhost:3000` | 易导致扩展与 MCP 访问旧实例 | 已改为当前实例地址 `http://127.0.0.1:8080` |

  

## 五、系统信息

  

| 项目 | 信息 |

|---|---|

| 测试日期 | 2026-03-10 |

| 测试平台 | macOS Apple Silicon |

| DevStar 访问地址 | `http://127.0.0.1:8080` |

| DevStar 部署方式 | Docker |

| DevStar 版本 | `1.0+2104-g49085a9900` |

| 测试仓库 | `gzy/base` |

| 仓库来源 | `templates/base` |

| VSCode 使用场景 | 本地模式、DevContainer 模式 |

| Docker Engine | `29.2.1` |

| Docker API | `1.53` |

| Docker 最低兼容 API | `1.44` |

| Node.js | `v22.19.0` |

| Runner 关键标签 | `Dockerfiles`, `ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04` |

  

## 六、结论

  

1. 当前 `macOS ARM64` 环境下，DevStar 安装、初始化、模板建仓、CI matrix、DevContainer、VSCode Copilot 本地模式、VSCode Copilot DevContainer 模式均已完成验证。

2. 其中本地模式基础使用稳定；DevContainer 与 MCP 相关链路可以验证通过，但依赖手工配置与人工补救，因此按 `⚠️` 记录更准确。

3. 当前主要问题集中在 DevContainer 初始化链路、临时 Docker context 管理、MCP 接入方式与旧配置残留。