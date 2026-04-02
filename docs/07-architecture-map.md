# 07. 架构能力地图

## 1. 顶层能力区

### A. 入口层
对应需求：
- 提供 CLI 入口
- 提供初始化流程
- 提供 SDK 接入方式
- 提供 MCP 入口

### B. Prompt 编排层
对应需求：
- 动态生成系统提示词
- 注入环境信息
- 注入语言与输出风格
- 注入记忆、MCP 说明、会话局部规则

### C. 工具执行层
对应需求：
- 工具发现
- 工具输入校验
- 权限判断
- Hook 拦截
- 执行记录
- 输出回流

### D. Agent 调度层
对应需求：
- 启动子 agent
- 支持 fork / background / remote / teammate 模式
- 管理 agent 生命周期
- 管理 agent 上下文边界

### E. 扩展生态层
对应需求：
- Skills
- Plugins
- MCP
- 命令扩展
- 插件变量替换与配置注入

### F. Memory / Session 层
对应需求：
- 项目记忆
- 用户记忆
- 会话摘要
- transcript
- resume

### G. 任务与后台层
对应需求：
- 本地任务
- 后台 agent 任务
- 远程 agent 任务
- shell 任务
- 进度追踪与通知

### H. 质量保证层
对应需求：
- verification agent
- 构建 / 测试 / lint / 类型检查
- adversarial probe
- FAIL / PASS / PARTIAL 判定

### I. 界面与操作者体验层
对应需求：
- TUI 展示
- 状态栏
- 权限提示
- 任务进度
- 命令系统
- agent / skills / memory / hooks 可视化

## 2. 跨层系统性要求

### 2.1 安全要求跨层存在
- Prompt 层要提醒风险
- Tool 层要校验与限权
- Hook 层要能阻断
- UI 层要能提示用户

### 2.2 上下文管理跨层存在
- Prompt 组装要考虑动态边界
- Session 要考虑压缩与恢复
- Agent 要考虑上下文隔离
- Skills / MCP 要考虑按需注入

### 2.3 产品化要求跨层存在
- 每个子系统不仅要能工作，还要：
  - 可追踪
  - 可恢复
  - 可扩展
  - 可治理

## 3. 反推出来的组织设计

从架构地图可以反推出，这不是一个“以模型为中心”的产品，而是一个“以运行时操作系统为中心”的产品。

模型只是其中一个核心部件，真正的产品能力来自这些部分的组合：

- prompt assembly
- tool execution pipeline
- permission governance
- agent orchestration
- extension surface
- memory/session management
- verification and traceability

## 4. 产品经理视角下的总需求句

> 该产品的架构应被理解为一张能力地图：每一层都不是独立存在的功能点，而是在共同支撑一个目标——让 AI 在真实工程环境中成为一个可控、可扩展、可追踪的执行系统。
