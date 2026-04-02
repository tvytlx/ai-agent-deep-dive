# 15. Python 版本 MVP 范围

## 1. 目标

避免 Python 版本一开始就无限扩张。MVP 只做能跑通核心闭环的最小系统。

## 2. MVP 必须包含

### 2.1 主循环
- 多轮 query loop
- tool call -> tool result -> next turn

### 2.2 基础工具
- read file
- write file
- edit file
- grep/search
- bash

### 2.3 基础权限系统
- allow / ask / deny
- 被拒后不原样重试

### 2.4 基础 transcript / session
- 消息持久化
- resume 会话

### 2.5 基础 memory
- 用户 / 项目记忆注入
- 简单记忆文件结构

### 2.6 基础 agent orchestration
- main agent
- 至少一个 verification agent
- 可选一个 explore / plan agent

### 2.7 基础 compact
- 超长消息时压缩历史
- 工具结果 budget 裁剪

## 3. MVP 可以后置的能力

- 完整 TUI
- remote execution
- 多人 teammate / swarm
- 高级 telemetry
- 高级 tracing
- 复杂 MCP delta 更新
- 高级 proactive / coordinator 模式
- 完整插件生态

## 4. 推荐实现顺序

1. 消息模型
2. 主循环
3. 工具执行链
4. transcript / resume
5. memory
6. verification agent
7. skills / plugin / MCP 里的最小一项

## 5. 成功标准

MVP 成功不等于“功能很多”，而是下面闭环能跑通：

> 用户给任务 -> 系统多轮推进 -> 调用工具 -> 保留上下文 -> 必要时压缩 -> 完成后给结果 -> 可恢复会话 -> 可做基本验证

## 6. 不建议在 MVP 阶段做的错误方向

- 先做复杂 UI
- 先做很多 agent 类型
- 先做大而全插件系统
- 没有 transcript / resume 就上 background task
- 没有权限系统就直接开放 bash
