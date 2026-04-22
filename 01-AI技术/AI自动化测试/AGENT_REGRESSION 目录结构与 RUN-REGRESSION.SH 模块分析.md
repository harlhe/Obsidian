
## 1. 目录结构（`TESTS/E2E/AGENT_REGRESSION`）

agent_regression/  
├── config/                 # 运行配置（默认读取 config/plaintext.env）  
├── skills/                 # 回归执行时拼接到 Prompt 的技能文档  
│   ├── common/  
│   └── scenarios/  
├── tasks/                  # 回归任务输入（当前唯一任务来源）  
├── templates/              # 任务/结果模板资源  
├── outputs/                # 每次回归运行产物（按 run_id 分目录）  
├── run-regression.sh       # 主执行脚本  
├── README.md               # 使用说明  
└── testcases/              # 历史目录（当前主链路已不依赖）

目录说明：

|目录/文件|作用|备注|
|---|---|---|
|`config/`|存放运行配置，默认读取 `config/plaintext.env`|主要包含 URL、账号、API Key 等环境变量|
|`skills/`|回归执行时拼接到 Prompt 的技能文档|`common/` 放通用规范，`scenarios/` 放场景规则|
|`tasks/`|回归任务输入目录|当前主链路从这里收集 `*.md` 任务|
|`templates/`|任务/结果模板资源|供任务渲染与复用|
|`outputs/`|每次运行的产物目录|按 `run_id` 隔离，便于回溯|
|`run-regression.sh`|回归主执行脚本|负责准备、执行、汇总|
|`README.md`|使用说明文档|提供运行方式和约束说明|
|`testcases/`|历史目录|当前主流程不依赖，仅历史兼容|

### 1.1 运行产物结构（`outputs/<run_id>/`）

outputs/<run_id>/  
├── logs/  
│   └── playwright-install.log  
├── cases/  
│   └── <task_name>/  
│       ├── task.source.md  
│       ├── tasks.md  
│       ├── .claude-global-skills.md  
│       ├── .claude-exec-prompt.md  
│       ├── claude-batch.log  
│       ├── result.md  
│       ├── playwright-cli-commands.md  
│       ├── skill-devstar-smoke.md  
│       └── skill-devstar-smoke-draft.md  
└── summary.md

产物说明：

|路径|作用|产出时机|
|---|---|---|
|`logs/playwright-install.log`|`playwright-cli install --skills` 的安装日志|skills 安装阶段|
|`cases/<task_name>/task.source.md`|原始任务快照|case 初始化|
|`cases/<task_name>/tasks.md`|占位符渲染后的实际任务|case 初始化|
|`cases/<task_name>/.claude-global-skills.md`|本 case 技能集合（含强制 playwright-cli skill）|prompt 构建前|
|`cases/<task_name>/.claude-exec-prompt.md`|最终执行 Prompt 快照|prompt 构建时|
|`cases/<task_name>/claude-batch.log`|Claude 执行日志（stdout/stderr）|agent 执行期间|
|`cases/<task_name>/result.md`|单任务执行结果与状态|agent 执行后|
|`cases/<task_name>/playwright-cli-commands.md`|Playwright CLI 命令时间序记录|agent 按约束输出时|
|`cases/<task_name>/skill-devstar-smoke.md`|通过时的正式 skill 产物|PASS 场景常见|
|`cases/<task_name>/skill-devstar-smoke-draft.md`|未完全通过时的草稿产物|PARTIAL/FAIL 场景可能出现|
|`summary.md`|本次 run 汇总报告（统计+Overall 状态）|全部 case 结束后|

补充：

- `outputs/latest` 是软链接，指向最近一次 `run_id`。
    
- 脚本不会清理历史 `outputs/<old_run_id>/`，历史结果默认保留。
    

### 1.2 task 和 skill 的关系

可以理解为：`task` 负责定义“做什么”，`skill` 负责定义“怎么做”。

|维度|task（`tasks/*.md`）|skill（`skills/**/*.md` + forced skill）|
|---|---|---|
|角色|业务目标与验收项|执行规范与操作 SOP|
|关注点|目标、参数、结果|工具使用方式、流程约束、稳定策略|
|变化频率|随回归场景变化|相对稳定，跨任务复用|
|在 prompt 中的位置|作为 “Task to Execute” 注入|作为 “Global Skills” 注入|

运行时拼接顺序：

1. 先构建 `.claude-global-skills.md`：固定先放 `playwright-cli/SKILL.md`，再拼接 `skills/` 下其它技能文档。
    
2. 再把 `tasks.md` 作为当前 case 的具体目标附在 prompt 后。
    

冲突处理规则：

- 若 task 描述和 skill SOP 冲突，以 skill 为准，并要求在 `result.md` 中记录冲突点。
    
- 这保证了不同 task 在执行动作上保持一致，尤其是“必须通过 `playwright-cli` 执行浏览器操作”。
    

## 2. RUN-REGRESSION.SH 总体职责

一句话：读取配置，串行跑 `tasks/`，按产物判定状态并写 `summary.md`。

主链路：

1. `bootstrap_env`：加载 `config/plaintext.env`，校验 `ANTHROPIC_API_KEY` 和 forced skill 文件。
    
2. 工具准备：缺 `claude`/`playwright-cli` 时用 `npm -g` 安装。
    
3. `install_playwright_skills`：可选安装 skills（支持 `REGRESSION_SKIP_SKILLS_INSTALL=1`）。
    
4. 遍历 `tasks/*.md`：逐个 `run_case` 单次执行（无脚本级 retry）。
    
5. `write_summary`：汇总 PASS/PARTIAL/FAIL 并返回退出码。
    

## 3. 模块速览（精简）

|模块|关键函数|作用|
|---|---|---|
|环境准备|`bootstrap_env`|读取配置并做最小必需校验|
|skills 安装|`install_playwright_skills`|安装 playwright skills（可跳过）|
|case 输入准备|`render_task` / `build_skills_bundle` / `build_prompt`|渲染任务、强制注入 playwright-cli skill、生成执行 prompt|
|case 执行|`invoke_claude` / `run_case`|在 case 目录执行 claude（带总超时）并收集日志|
|状态判定|`evaluate_status`|优先读 `result.md` 的 `Overall-Status`，否则按产物回退判定|
|汇总输出|`write_summary` / `main`|写 `summary.md`，返回最终退出码|

## 4. 状态与退出码

判定逻辑：

- `evaluate_status` 优先使用 `result.md` 中的 `Overall-Status: PASS|PARTIAL|FAIL`。
    
- 缺失该字段时按产物回退：`result+skill => PASS`，`result(+draft) => PARTIAL`，否则 `FAIL`。
    

总体状态：

- `FAIL`：`task_total=0` 或有 `FAIL` case 或 skills 安装失败。
    
- `PARTIAL`：无 FAIL，但存在 `PARTIAL` 或 `SKIPPED`。
    
- `PASS`：其余情况。
    

退出码：

- `PASS` / `PARTIAL` -> `exit 0`
    
- `FAIL` -> `exit 1`
    

## 5. 当前版本关键点

- 默认只使用 `tasks/` 作为任务输入。
    
- 每个 task 只执行一次，不做脚本级重试。
    
- 仍强制注入 `playwright-cli/SKILL.md`，并在 prompt 中约束必须通过 `playwright-cli` 执行。