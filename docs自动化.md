# DevStar Actions 工作流图示

  

> 本文档展示 devstar Actions 的 CI/CD 工作流程，用于自动更新用户文档。

  

---

  

## 🌐 整体架构图

  

```mermaid

graph TB

subgraph "devstar 代码仓库"

CODE["📦 devstar 源码"]

CONF["⚙️ 配置文件<br/>app.example.ini"]

DOCS["📝 用户文档<br/>docs/"]

end

subgraph "devstar Actions CI/CD"

TRIGGER["🅰️ 触发器<br/>push/schedule/manual"]

CHECK["🅱️ 变更分析<br/>分析变更文件类型"]

AI["🤖 AI 摘要生成<br/>用户向总结"]

end

subgraph "AI 文档生成"

API["📜 API 文档生成<br/>Go 源码分析 + AI 总结"]

CONFIG["⚙️ 配置文档生成<br/>INI 解析 + AI 优化"]

TRANSLATE["🌐 自动翻译<br/>中译英"]

end

subgraph "部署发布"

BUILD["🔨 VitePress 构建"]

DEPLOY["🚀 部署到 Pages"]

SITE["🌐 docs.devstar.io"]

end

CODE --> TRIGGER

CONF --> TRIGGER

DOCS --> TRIGGER

TRIGGER --> CHECK

CHECK --> AI

AI -->|"Go 文件变更"| API

AI -->|"INI 文件变更"| CONFIG

API --> TRANSLATE

CONFIG --> TRANSLATE

TRANSLATE -->|"中文 + 英文"| DOCS

DOCS --> BUILD

BUILD --> DEPLOY

DEPLOY --> SITE

```

  

---

  

## 📋 触发条件流程图

  

```mermaid

flowchart TD

START([开始]) --> PUSH{push 到 main?}

PUSH -->|Yes| ANALYZE["🔍 分析变更文件<br/>git diff --name-only"]

PUSH -->|No| SCHEDULE{定时触发?}

SCHEDULE -->|Yes| ANALYZE

SCHEDULE -->|No| MANUAL{手动触发?}

MANUAL -->|Yes| ANALYZE

MANUAL -->|No| END([结束])

ANALYZE --> HAS_CHANGES{有变更?}

HAS_CHANGES -->|Yes| AI_SUMMARY["🤖 AI 生成用户友好摘要<br/>过滤敏感信息"]

HAS_CHANGES -->|No| END

AI_SUMMARY --> DETERMINE["📄 判断变更类型<br/>Go / INI / 其他"]

DETERMINE --> GO{GO 文件?}

DETERMINE --> INI{INI 文件?}

GO -->|Yes| RUN_API["📜 执行 API 文档生成 + AI 总结"]

GO -->|No| SKIP_API[⏭️ 跳过]

INI -->|Yes| RUN_CONFIG["⚙️ 执行配置文档生成 + AI 总结"]

INI -->|No| SKIP_CONFIG[⏭️ 跳过]

SKIP_API --> TRANSLATE["🌐 自动翻译为英文"]

SKIP_CONFIG --> TRANSLATE

RUN_API --> TRANSLATE

RUN_CONFIG --> TRANSLATE

TRANSLATE --> COMMIT["📤 提交中英文文档"]

COMMIT -->|"main 分支"| DEPLOY["🚀 部署"]

COMMIT -->|"其他分支"| END

DEPLOY --> SUCCESS["✅ 部署成功"]

DEPLOY -->|"失败"| FAILED["❌ 通知管理员"]

SUCCESS --> END

FAILED --> END

```

  

---

  

## 🔄 AI 文档生成流程图

  

```mermaid

flowchart LR

subgraph "输入"

SRC["📦 源文件<br/>Go / INI"]

end

subgraph "AI 处理"

PARSE["📖 解析源码<br/>提取注释和接口"]

SUMMARIZE["🤖 AI 总结<br/>用户向描述"]

POLISH["✨ AI 优化<br/>专业表达"]

end

subgraph "翻译"

ZH["📄 中文文档<br/>用户友好描述"]

EN["📄 English Docs<br/>专业翻译"]

end

SRC --> PARSE --> SUMMARIZE --> POLISH --> ZH

ZH -.->|"🌐 AI 翻译"| EN

```

  

---

  

## 🌐 自动翻译流程图

  

```mermaid

flowchart TD

NEW_DOC["📄 新生成的文档<br/>docs/zh/*.md"]

NEW_DOC -->|"检测新文件"| CHECK{"已有英文版?}

CHECK -->|No| TRANSLATE["🌐 调用 AI 翻译"]

CHECK -->|Yes| SKIP[⏭️ 跳过]

TRANSLATE --> SELECT["🤖 选择 AI 模型<br/>GPT-4 / GLM-4"]

SELECT --> PROMPT["📝 构建翻译 Prompt<br/>保持术语一致性"]

PROMPT --> EXECUTE["⚡ 执行翻译"]

EXECUTE --> OUTPUT["📄 生成英文文档<br/>docs/en/*.md"]

OUTPUT -->|"格式优化"| FORMAT["📋 格式化<br/>Markdown 格式"]

FORMAT --> DONE[✅ 完成]

SKIP --> DONE

```

  

---

  

## 🤖 AI Prompt 示例

  

### 1️⃣ 用户友好摘要生成

  

```markdown

请用简洁的中文，总结以下代码变更的用户影响。

  

变更的文件:

- cmd/web/main.go

- modules/auth/login.go

  

变更详情（摘录）:

... (diff 内容)

  

请用 1-2 句话总结这次更新对用户的影响，使用友好的语气。

例如: "新增了 XXX 功能，优化了 XXX 体验" 或 "修复了 XXX 问题，提升了稳定性"

不要提及具体的代码实现细节。

```

  

**AI 输出示例:**

> "✅ 新增了第三方 OAuth 登录支持，现在用户可以使用 GitHub、Google 账号快速登录。"

> "✅ 优化了 CI/CD Pipeline 的构建速度，平均节省 30% 构建时间。"

  

---

  

### 2️⃣ 文档翻译 (中译英)

  

```markdown

请将以下中文技术文档翻译为英文。

  

要求：

1. 保持 Markdown 格式

2. 保持代码块不变

3. 技术术语首次出现时在括号中给出中文解释

4. 语气正式、专业

5. 标题使用 Title Case

  

原文：

# 用户认证

用户认证是系统的核心功能...

```

  

**AI 输出示例:**

```markdown

# User Authentication

  

User authentication is the core functionality of the system. The platform supports multiple authentication methods:

  

- **Username/Password**: Traditional username and password authentication

- **OAuth 2.0**: Third-party OAuth 2.0 authentication (支持 GitHub, Google, etc.)

- **LDAP**: Enterprise LDAP/AD integration (企业级轻量目录访问协议)

```

  

---

  

## 📁 文档路径映射图

  

```mermaid

graph LR

subgraph "源文件 (devstar)"

A["cmd/**/*.go"]

B["models/**/*.go"]

C["conf/*.ini"]

end

subgraph "AI 文档生成"

P1["📝 解析源码"]

P2["🤖 AI 用户向总结"]

P3["🌐 自动翻译"]

end

subgraph "输出文档 (docs)"

D1["📄 zh/reference/source/*.md<br/>用户友好的 API 文档"]

D2["📄 en/reference/source/*.md<br/>English API Docs"]

D3["📄 zh/reference/config/*.md<br/>配置说明文档"]

D4["📄 en/reference/config/*.md<br/>English Config Docs"]

end

A --> P1

B --> P1

C --> P1

P1 --> P2

P2 --> D1

P2 --> D3

D1 -.-> P3

D3 -.-> P3

P3 --> D2

P3 --> D4

```

  

---

  

## 🚀 部署流程图

  

```mermaid

flowchart LR

subgraph "构建阶段"

INPUT["📝 docs/ 目录<br/>包含中英文文档"]

NODE["⚡ npm install<br/>安装依赖"]

BUILD["🔨 npm run build<br/>VitePress 构建"]

ARTIFACT["📦 .vitepress/dist<br/>静态文件"]

end

subgraph "部署阶段"

UPLOAD["📤 上传 Artifact<br/>actions/upload-pages-artifact"]

DEPLOY["🚀 部署 Pages<br/>actions/deploy-pages"]

SITE["🌐 https://docs.devstar.io"]

end

INPUT --> NODE --> BUILD --> ARTIFACT --> UPLOAD --> DEPLOY --> SITE

```

  

---

  

## 📋 工作流任务依赖图

  

```mermaid

graph TD

START([开始]) --> ANALYZE

ANALYZE["📊 Analyze Changes<br/>分析变更文件"] --> AI_SUMMARY["🤖 AI 生成摘要<br/>用户向描述"]

AI_SUMMARY --> HAS_GO{GO 文件变更?}

AI_SUMMARY --> HAS_INI{INI 文件变更?}

HAS_GO -->|Yes| API_DOCS["📜 Generate API Docs<br/>AI 总结 + 翻译"]

HAS_GO -->|No| SKIP_API[⏭️]

HAS_INI -->|Yes| CONFIG_DOCS["⚙️ Generate Config Docs<br/>AI 总结 + 翻译"]

HAS_INI -->|No| SKIP_CONFIG[⏭️]

API_DOCS --> TRANSLATE["🌐 Auto-Translate<br/>中译英"]

CONFIG_DOCS --> TRANSLATE

SKIP_API --> TRANSLATE

SKIP_CONFIG --> TRANSLATE

TRANSLATE -->|"更新 docs/"| COMMIT_API["📤 提交中文文档"]

TRANSLATE -->|"更新 docs/"| COMMIT_CONFIG["📤 提交英文文档"]

COMMIT_API --> SIDEBAR["📑 Update Sidebar<br/>自动更新侧边栏"]

COMMIT_CONFIG --> SIDEBAR

SIDEBAR -->|"main 分支"| DEPLOY["🚀 Deploy Docs<br/>部署文档"]

DEPLOY --> SUCCESS["✅ 部署成功<br/>docs.devstar.io"]

DEPLOY -->|"失败"| FAILED["❌ 通知管理员"]

SUCCESS --> NOTIFY["🔔 发送通知"]

NOTIFY --> END([结束])

FAILED --> END

```

  

---

  

## 🔧 配置项说明

  

### 环境变量

  

| 变量名 | 说明 | 必填 |

|-------|------|------|

| `OPENAI_API_KEY` | OpenAI API Key | 可选 |

| `ZHIPU_API_KEY` | 智谱 AI API Key | 可选 |

| `AI_PROVIDER` | AI 提供商 (`openai` / `zhipu`) | 可选 |

| `AI_MODEL` | AI 模型 (`gpt-4` / `glm-4`) | 可选 |

  

### Secrets 配置

  

| Secret | 说明 |

|--------|------|

| `OPENAI_API_KEY` | OpenAI API Key |

| `ZHIPU_API_KEY` | 智谱 AI API Key |

| `SMTP_SERVER` | SMTP 服务器（邮件通知） |

  

---

  

## 📊 过滤规则

  

### AI 摘要生成时过滤敏感文件

  

```python

sensitive_patterns = [

'test', # 测试文件

'fixtures', # 测试数据

'migrations' # 数据库迁移

]

  

user_docs = [f for f in files if not any(p in f.lower() for p in sensitive_patterns)]

```

  

### 只处理用户相关文档

  

| 文件类型 | 处理方式 |

|---------|---------|

| `cmd/**/*.go` | ✅ 生成 API 文档 |

| `models/**/*.go` | ✅ 生成数据模型文档 |

| `conf/*.ini` | ✅ 生成配置文档 |

| `tests/**/*.go` | ❌ 跳过 |

| `fixtures/**` | ❌ 跳过 |

  

---

  

*最后更新: 2026-02-04*