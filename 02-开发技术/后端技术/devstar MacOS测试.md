### Feature Description

# 跨平台安装测试测试环境矩阵

|操作系统|架构|发行版/版本|安装结果|功能测试|备注|
|---|---|---|---|---|---|
|Windows|x86_64|ALL|❌|❌|未测通原生安装|
|Windows 11|x86_64|WSL2 Ubuntu|✅|✅|已有验证结论|
|Windows 11|ARM64|WSL2 Ubuntu|⚪|⚪|待测试|
|Linux|x86_64|Ubuntu 22.04 LTS|✅|✅|原生支持|
|Linux|x86_64|Ubuntu 24.04 LTS|✅|✅|最新版本|
|Linux|x86_64|Debian 12|⚪|⚪|待测试|
|Linux|x86_64|CentOS 7|⚪|⚪|待测试|
|Linux|x86_64|RHEL 9|⚪|⚪|待测试|
|Linux|x86_64|Fedora 40|⚪|⚪|待测试|
|Linux|x86_64|Arch Linux|⚪|⚪|滚动更新|
|Linux|x86_64|Alpine 3.19|⚪|⚪|待测试|
|Linux|ARM64|Ubuntu 22.04 (Raspberry Pi)|⚪|⚪|待测试|
|Linux|ARM64|Debian 12 (AWS Graviton)|⚪|⚪|待测试|
|Linux|ARM64|Rocky Linux 9|⚪|⚪|待测试|
|Linux|ARM|ARMv7 (Raspberry Pi 3)|⚪|⚪|32 位 ARM|
|macOS|x86_64|Ventura 13.6|⚪|⚪|Intel Mac，待测试|
|macOS|ARM64|Sonoma 14.5|✅|⚠️|Apple Silicon；Docker 安装、CI、DevContainer、VSCode Copilot 验证通过，但 DevContainer 与 MCP 相关链路需手工配置|
|macOS|ARM64|Sequoia 15.0|⚪|⚪|待测试|
|Docker|x86_64|Alpine 3.19|⚪|⚪|轻量容器|
|Docker|ARM64|Ubuntu 22.04|⚪|⚪|ARM 容器|
|Kubernetes|x86_64|多节点集群|⚪|⚪|生产环境待测试|
|Podman|x86_64|RHEL 9|⚪|⚪|无守护进程|

这些环境可以根据情况删减和添加

### [](https://www.devstar.cn/devstar/devstar/issues/131#%E7%AC%A6%E5%8F%B7%E8%AF%B4%E6%98%8E)符号说明

- ✅: 测试通过
- ❌: 测试失败
- ⚠️: 部分支持/有警告

# [](https://www.devstar.cn/devstar/devstar/issues/131#%E5%9F%BA%E6%9C%AC%E5%8A%9F%E8%83%BD%E9%9B%86%E6%88%90%E6%B5%8B%E8%AF%95)基本功能集成测试

## [](https://www.devstar.cn/devstar/devstar/issues/131#%E6%B5%8B%E8%AF%95%E7%BB%B4%E5%BA%A6%E8%AF%B4%E6%98%8E)测试维度说明

- **开箱即用**: 工具安装后无需额外配置即可使用的程度（1-5分）
- **pull/push**: 基础Git拉取和推送操作
- **MCP pull/push**: 通过MCP方式执行Git拉取和推送

## [](https://www.devstar.cn/devstar/devstar/issues/131#%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C%E8%AE%B0%E5%BD%95%E8%A1%A8)测试结果记录表

|工具名称|测试模式|开箱即用|pull/push|MCP pull/push|备注/问题描述|
|---|---|---|---|---|---|
|Claude Code(CLI)|本地模式|⚪|⚪|⚪|未测|
|Claude Code(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|OpenCode(CLI)|本地模式|⚪|⚪|⚪|未测|
|OpenCode(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|OpenClaw(CLI)|本地模式|⚪|⚪|⚪|未测|
|OpenClaw(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|GEMINI(CLI)|本地模式|⚪|⚪|⚪|未测|
|GEMINI(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|iFlow(CLI)|本地模式|⚪|⚪|⚪|未测|
|iFlow(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|QWEN(CLI)|本地模式|⚪|⚪|⚪|未测|
|QWEN(CLI)|DevContainer 模式|⚪|⚪|⚪|未测|
|VSCode Copilot|本地模式|⭐⭐⭐⭐|✅|⚠️|MCP 需手工配置 Access Token|
|VSCode Copilot|DevContainer 模式|⭐⭐⭐|⚠️|⚠️|`pull/push`需手工初始化仓库；MCP 需手工配置 Token、`stdio bridge` 和 MCP server|
|Windsurf|本地模式|⚪|⚪|⚪|未测|
|Windsurf|DevContainer 模式|⚪|⚪|⚪|未测|
|Trae|本地模式|⚪|⚪|⚪|未测|
|Trae|DevContainer 模式|⚪|⚪|⚪|未测|
|Trae CN|本地模式|⚪|⚪|⚪|未测|
|Trae CN|DevContainer 模式|⚪|⚪|⚪|未测|
|Cursor|本地模式|⚪|⚪|⚪|未测|
|Cursor|DevContainer 模式|⚪|⚪|⚪|未测|

这些AI工具可以根据情况删减和添加

## [](https://www.devstar.cn/devstar/devstar/issues/131#%E6%A0%87%E8%AE%B0%E8%AF%B4%E6%98%8E)标记说明

- **开箱即用评分**:
    
    - ⭐⭐⭐⭐⭐: 完全开箱即用，零配置
    - ⭐⭐⭐⭐: 少量简单配置
    - ⭐⭐⭐: 需要中等复杂度配置
    - ⭐⭐: 配置复杂
    - ⭐: 几乎无法使用或需要大量配置
- **功能测试标记**:
    
    - ✅: 测试通过，功能正常
    - ❌: 测试失败，功能异常
    - ⚠️: 部分成功或存在限制
    - ⚪: 待测试
    - 🚫: 不适用/不支持

## [](https://www.devstar.cn/devstar/devstar/issues/131#macos-%E6%B5%8B%E8%AF%95%E9%85%8D%E7%BD%AE%E4%B8%8E%E9%97%AE%E9%A2%98%E8%AE%B0%E5%BD%95)macOS 测试配置与问题记录

### [](https://www.devstar.cn/devstar/devstar/issues/131#1-macos-%E6%B5%8B%E8%AF%95%E7%9B%B8%E5%85%B3%E9%85%8D%E7%BD%AE)1. macOS 测试相关配置

|配置项|配置值/处理方式|说明|
|---|---|---|
|DevStar 访问地址|`http://127.0.0.1:8080`|本地 Docker 部署地址|
|Docker API 兼容配置|`DOCKER_API_VERSION=1.44`|用于修复 DevContainer 创建失败|
|DevContainer 仓库初始化|在容器内手工 clone 仓库|用于修复 `/workspace/base` 为空的问题|
|VSCode Docker context|`docker context create devstar-remote-base --docker "host=ssh://base"`|用于修复 VSCode 重连 DevContainer|
|MCP 认证|在 DevStar 中创建 Access Token|用于 VSCode Copilot MCP 调用|
|VSCode MCP 接入|使用 `stdio bridge` + 用户级 `mcp.json`|避免 OAuth 自动注册流程失败|
|VSCode DevStar 地址|从 `http://localhost:3000` 改为 `http://127.0.0.1:8080`|避免扩展继续连接旧实例|

### [](https://www.devstar.cn/devstar/devstar/issues/131#2-macos-%E6%B5%8B%E8%AF%95%E4%B8%AD%E9%81%87%E5%88%B0%E7%9A%84%E9%97%AE%E9%A2%98)2. macOS 测试中遇到的问题

|问题|现象|影响|处理结果|
|---|---|---|---|
|Docker API 版本不兼容|`client version 1.43 is too old. Minimum supported API version is 1.44`|DevContainer 无法创建|通过补充 `DOCKER_API_VERSION=1.44`恢复|
|DevContainer 仓库未自动初始化|`/workspace/base` 为空，`git status` 报 `not a git repository`|容器内无法直接进行 `pull/push`|手动 clone 后通过|
|VSCode 临时 Docker Context 丢失|`context "devstar-remote-base" not found`|从 VSCode 恢复窗口重新进入容器失败|重建临时 Docker context 后恢复|
|MCP 错误进入 OAuth 流程|`Dynamic Client Registration not supported`|Copilot 无法直接连 DevStar MCP|改为 `stdio bridge + token` 方式后恢复|
|MCP bridge 与 Node 22 兼容性问题|MCP server 启动失败|无法完成 MCP 测试|调整 bridge 启动方式后恢复|
|VSCode 仍指向旧实例地址|配置里仍为 `http://localhost:3000`|易导致扩展与 MCP 访问旧实例|已改为当前实例地址 `http://127.0.0.1:8080`|

### [](https://www.devstar.cn/devstar/devstar/issues/131#3-%E7%B3%BB%E7%BB%9F%E4%BF%A1%E6%81%AF)3. 系统信息

|项目|信息|
|---|---|
|测试日期|2026-03-10|
|测试平台|macOS Apple Silicon|
|DevStar 访问地址|`http://127.0.0.1:8080`|
|DevStar 部署方式|Docker|
|DevStar 版本|`1.0+2104-g49085a9900`|
|测试仓库|`gzy/base`|
|仓库来源|`templates/base`|
|VSCode 使用场景|本地模式、DevContainer 模式|
|Docker Engine|`29.2.1`|
|Docker API|`1.53`|
|Docker 最低兼容 API|`1.44`|
|Node.js|`v22.19.0`|
|Runner 关键标签|`Dockerfiles`, `ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`|

## [](https://www.devstar.cn/devstar/devstar/issues/131#4-%E7%BB%93%E8%AE%BA)4. 结论

1. 当前 `macOS ARM64` 环境下，DevStar 安装、初始化、模板建仓、CI matrix、DevContainer、VSCode Copilot 本地模式、VSCode Copilot DevContainer 模式均已完成验证。
2. 其中本地模式基础使用稳定；DevContainer 与 MCP 相关链路可以验证通过，但依赖手工配置与人工补救，因此按 `⚠️` 记录更准确。
3. 当前主要问题集中在 DevContainer 初始化链路、临时 Docker context 管理、MCP 接入方式与旧配置残留。