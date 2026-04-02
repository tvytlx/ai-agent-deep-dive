# 产品需求文档反推总览

> 目标：基于现有源码结构，反推出这套 AI 编程产品的核心需求与产品设计，而不是复述实现细节。

## 文档原则

- 只写需求、目标、交互、约束、边界条件
- 不直接泄露原始源码实现
- 如需描述机制，只用自然语言或 Python 风格伪代码
- 文档站在产品经理 / 系统设计者视角，回答“为什么需要这个能力”

## 文档结构

1. `00-product-overview.md`
   - 产品定位
   - 核心用户
   - 核心问题
   - 顶层系统能力

2. `01-system-prompt-and-orchestration.md`
   - 系统提示词层的需求
   - 为什么要做动态拼装
   - 为什么要做角色化 agent orchestration

3. `02-tools-permissions-and-execution.md`
   - 工具系统需求
   - 权限系统需求
   - Hook / 执行链路 / 安全要求

4. `03-skills-plugins-mcp.md`
   - Skills 需求
   - Plugins 需求
   - MCP 集成需求

5. `04-memory-and-session.md`
   - 记忆系统需求
   - Session 管理需求
   - 压缩、归档、恢复、摘要需求

6. `05-commands-ui-and-operator-experience.md`
   - 命令系统需求
   - TUI / 状态栏 / 任务可视化需求
   - 操作者体验

7. `06-verification-and-quality.md`
   - 验证 agent 需求
   - 质量保证需求
   - 失败报告与可追溯性需求

8. `07-architecture-map.md`
   - 按模块汇总产品能力地图
   - 用于快速定位需求归属

9. `08-agent-runtime-loop.md`
   - 主循环规格
   - 多轮执行与终止条件

10. `09-message-model-and-state.md`
   - 消息模型
   - 会话与状态对象

11. `10-context-management.md`
   - 上下文预算
   - 压缩与恢复

12. `11-task-model.md`
   - 任务模型
   - 后台执行与通知

13. `12-workspace-and-isolation.md`
   - 工作区隔离策略
   - 角色与写权限边界

14. `13-failure-recovery.md`
   - 失败处理
   - 恢复机制

15. `14-configuration-system.md`
   - 配置来源与优先级
   - Agent / Session 配置项

16. `15-mvp-scope.md`
   - Python MVP 范围
   - 哪些先做，哪些后置

17. `16-python-implementation-notes.md`
   - Python 版实现建议
   - 模块划分与里程碑

## 阅读建议

如果你想快速理解这套产品：

1. 先看 `00-product-overview.md`
2. 再看 `04-memory-and-session.md`
3. 再看 `02-tools-permissions-and-execution.md`
4. 最后看 `03-skills-plugins-mcp.md` 和 `06-verification-and-quality.md`
