

  

## 1. 文档信息

  

| 项目 | 内容 |

|---|---|

| 文档名称 | DevStar AI E2E 调研与落地汇报 |

| 适用范围 | DevStar Web、CI/CD、DevContainer、MCP 相关功能验证 |

| 当前版本 | v1.2 |

| 更新时间 | 2026-03-11 |


  

---

  

## 2. 结论

  

本次调研与 POC 的核心结论如下：

  

1. 不建议采用纯 Playwright 固定脚本作为长期主方案。

2. 不建议采用纯 AI 浏览器代理作为正式回归主方案。

3. 推荐采用 **AI 编排 + 稳定执行器 + API/日志断言 + 自动证据归档** 的混合方案。

4. 当前正确路线不是“AI 像人一样手动测试”，而是“AI 驱动测试意图，执行器完成确定性验证”。

5. 当前 `qa/ai-e2e` 已经具备稳定执行器雏形，并已跑通两个真实场景。

  

---

  

## 3. 当前问题

  

现有 E2E 体系的主要问题：

  

1. 强依赖页面文案、选择器和固定流程，UI 调整后容易失效。

2. 长链路场景多，失败后缺少结构化证据，排障成本高。

3. 浏览器脚本承担了过多职责，执行、断言、归因混在一起。

4. 环境波动较大，尤其是 runner、Docker、DevContainer、MCP 等链路。

5. 现有方案难以直接演进到“自然语言驱动验证”。

  

---

  

## 4. 方案

  

**自然语言定义目标 + 场景层编排 + 稳定执行器执行 + API/日志断言 + 结构化报告**

  

设计原则：

  

1. 自然语言负责定义测试目标，不负责最终判定。

2. 执行动作优先走稳定接口，不依赖 AI 临场自由发挥。

3. 最终结果由规则断言，不由模型主观判断。

4. 每次执行必须保留 artifacts，支持复盘和审计。

  

---

  

## 5. 当前落地结构

  

当前 `qa/ai-e2e` 拟定三层结构：

  

### 5.1 能力层

  

负责提供基础执行能力：

  

1. `ui.mjs`：登录、建仓等最小 UI 动作

2. `api.mjs`：DevStar API 封装

3. `report.mjs`：结构化报告输出

4. `utils.mjs`：轮询、状态判断、日志处理等通用工具

5. `config.mjs`：环境变量和路径配置

  

### 5.2 场景层

  

负责组合能力层，形成可复用测试场景：

  

1. `minimal-ci`

2. `local-git-pull-push`

3. 后续待扩展的 `out-of-box`、`mcp-pull-push`、`devcontainer-*`

  

### 5.3 自然语言编排层

  

当前尚未正式实现，后续目标是：

  

1. 用自然语言选择场景

2. 用自然语言填充参数

3. 用自然语言组合断言目标

4. 最终映射到稳定场景执行器，而不是直接驱动底层动作

  

---

  

## 6. 当前已验证结果

  

### 6.1 最小 CI 闭环已跑通

  

已验证链路：

  

1. 登录

2. 模板建仓

3. API 写入 workflow 和 Dockerfile

4. 修改 README 触发 CI

5. 轮询 workflow run 和 jobs

6. matrix job 全部成功

  

说明：

  

1. `UI 最小入口 + API 稳定执行 + 状态断言` 路线可行。

2. 该场景已经从一次性脚本演进为稳定执行器场景。

  

### 6.2 Runner Docker API 缺陷已定位并验证修复方向

  

已确认的问题：

  

1. runner 容器内 Docker client API 版本过旧。

2. 导致 workflow job 在镜像检查阶段失败。

  

已验证的修复方式：

  

1. 在创建 runner 容器时注入 `DOCKER_API_VERSION`。

2. 在创建 runner 容器时注入 `DOCKER_HOST`。

  

结果：

  

1. 相同实例、相同链路下，修复前 job 全量失败。

2. 注入兼容环境变量后，相同 matrix job 全量成功。

  

### 6.3 本地 pull/push 场景已跑通

  

已验证链路：

  

1. 登录

2. 模板建仓

3. 本地 clone 两个工作区

4. 修改 README

5. commit

6. push

7. 第二工作区 pull

8. 对比远端和本地结果一致

  

说明：

  

1. `local-git-pull-push` 已经是一个真实可运行场景，而不是规划项。

2. 这证明场景层扩展路线成立。

  

---

  

## 7. 场景矩阵

  

后续目标场景矩阵如下：

  

| 测试模式 | 开箱即用 | pull/push | MCP pull/push |

|---|---|---|---|

| 本地模式 | local-out-of-box | local-git-pull-push | local-mcp-pull-push |

| DevContainer 模式 | devcontainer-out-of-box | devcontainer-git-pull-push | devcontainer-mcp-pull-push |

  

说明：

  

1. 本地模式和 DevContainer 模式要分开验证。

2. pull/push 与 MCP pull/push 属于不同能力链路。

3. 后续自然语言系统应以这些稳定场景 ID 为目标，而不是直接操作底层脚本。

  

---

  

## 8. 当前优先级

  

建议优先级如下：

  

| 优先级 | 场景 ID | 当前状态 |

|---|---|---|

| P0 | minimal-ci | 已完成并验证 |

| P0 | local-git-pull-push | 已完成并验证 |

| P0 | local-out-of-box | 待补齐 |

| P0 | devcontainer-out-of-box | 待实现 |

| P1 | devcontainer-git-pull-push | 待实现 |

| P1 | local-mcp-pull-push | 待实现 |

| P1 | devcontainer-mcp-pull-push | 待实现 |

  

---

  

## 9. 为什么不是纯 AI 浏览器测试

  

原因很明确：

  

1. 纯 AI 浏览器测试可复现性不足。

2. 最终判定容易主观化。

3. 长链路问题更适合 API、日志和状态断言。

4. 当前阶段更需要稳定性和可审计性，而不是浏览器自由导航能力。

  

因此，AI 在当前方案中的正确位置是：

  

1. 生成场景草案。

2. 选择场景和参数。

3. 总结失败原因。

4. 辅助维护执行器。

  

而不是：

  

1. 直接代替最终断言。

2. 直接代替整个浏览器执行层。

  

---

  

## 10. 下一步计划

  

下一阶段建议按以下顺序推进：

  

1. 完善 `local-out-of-box` 场景。

2. 实现 `devcontainer-out-of-box` 场景。

3. 在场景层之上补自然语言到场景计划的映射层。

4. 再扩 `local-mcp-pull-push` 和 `devcontainer-mcp-pull-push`。

  

阶段目标不是继续堆脚本，而是完成以下升级：

  

1. 从“单次脚本”升级为“场景化执行器”。

2. 从“命令驱动”升级为“自然语言选择场景”。

3. 从“人工分析失败”升级为“自动取证 + 自动归因 + AI 总结”。

  

---

  

## 11. 结论


1. 方向：不是纯 AI 测试，而是 AI 驱动的稳定验证系统。

2. 执行器已经跑通，不再是纯调研阶段。

3. 当前已验证两个真实场景：`minimal-ci` 和 `local-git-pull-push`。

4. runner 环境缺陷已被定位，并验证了产品修复方向。

5. 下一阶段重点是补齐场景矩阵，并接入自然语言编排层。