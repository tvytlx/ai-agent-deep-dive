# 16. Python 实现注意事项

## 1. 实现原则

目标不是逐字复刻原实现，而是用 Python 重建同样的产品能力结构。

## 2. 模块建议

建议 Python 项目按以下模块拆：

- `runtime/`：query loop, orchestration
- `messages/`：message schemas
- `tools/`：tool registry and execution
- `permissions/`：permission engine
- `memory/`：memory loading and retrieval
- `tasks/`：background task model
- `storage/`：transcript and session persistence
- `agents/`：agent definitions
- `extensions/`：skills/plugins/mcp
- `verification/`：verification runner

## 3. 推荐先用的数据模型

优先用：
- `pydantic` / `dataclasses` 定义消息与状态
- `sqlite` 或 JSONL 先做 transcript
- 明确的 service 层代替隐式全局状态

## 4. 不要过早做的事

- 不要先优化 UI
- 不要先做复杂并发
- 不要先支持十几种 agent
- 不要把 memory 做成向量库重系统

## 5. 第一阶段的最佳目标

先做出一个：
- 结构清晰
- transcript 可回放
- message 模型稳定
- verification 能跑
- compact 能工作

的 Python core runtime。

## 6. 推荐里程碑

### Milestone 1
- message model
- query loop
- basic tools
- transcript

### Milestone 2
- permissions
- memory
- resume
- compact

### Milestone 3
- verification agent
- simple skill loading
- background local agent tasks

### Milestone 4
- MCP / plugin minimal support
- worktree isolation
- richer UI
