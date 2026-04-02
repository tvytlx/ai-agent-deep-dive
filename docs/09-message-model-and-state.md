# 09. 消息模型与状态规格

## 1. 为什么消息模型必须先定义

这类 Agent 系统的核心不是“函数调用”，而是“结构化消息驱动状态变化”。如果消息模型不稳定，后面的 memory、resume、工具执行、agent 任务都会混乱。

## 2. 顶层消息类型

Python 版本建议至少定义以下消息类型：

- `system`
- `user`
- `assistant`
- `tool_use`
- `tool_result`
- `progress`
- `attachment`
- `summary`
- `compact_boundary`
- `notification`
- `tombstone`（可选，用于删除/隐藏历史消息后的链修复）

## 3. 核心消息字段

所有消息建议共享：

```python
class BaseMessage:
    id: str
    type: str
    created_at: float
    parent_id: str | None
    session_id: str
```

### assistant 消息
```python
class AssistantMessage(BaseMessage):
    content_blocks: list
    usage: dict | None
    stop_reason: str | None
```

### user 消息
```python
class UserMessage(BaseMessage):
    content_blocks: list
    source: str | None
```

### tool_use 消息块
```python
class ToolUseBlock:
    id: str
    name: str
    input: dict
```

### tool_result 消息块
```python
class ToolResultBlock:
    tool_use_id: str
    content: str | list
    is_error: bool = False
```

## 4. 为什么 parent_id 很重要

消息链必须可追踪。这样才能支持：
- transcript 回放
- resume
- 历史修复
- compact boundary 后的有效链重建

## 5. progress 消息的处理原则

高频 progress 消息通常是 UI 态，而不是核心 transcript。实现时建议：

- 可以显示在界面中
- 但默认不参与核心 parent chain
- 不应污染 resume 后的模型上下文

## 6. attachment / notification 的用途

这类消息用于携带结构化系统事件，例如：
- hook 阻断
- task notification
- permission 说明
- MCP 附加上下文

不要把所有系统事件都挤进普通文本消息中。

## 7. 状态对象要求

除消息外，还要有显式状态对象：

```python
class SessionState:
    session_id: str
    cwd: str
    current_task_id: str | None
    memory_summary: str | None
    active_agent_ids: list[str]
    current_permission_mode: str
    token_budget_state: dict | None
```

## 8. compact boundary 的需求

压缩前后必须有清晰边界，方便：
- 知道哪些历史被总结了
- resume 时只加载必要部分
- 保持消息链清晰

## 9. transcript 存储要求

transcript 至少要支持：
- 顺序追加
- 按 session 加载
- 按 agent 侧链加载
- 读取尾部摘要
- 限制超大文件读取风险

## 10. 验收标准

1. 任一轮对话都能序列化为结构化消息
2. tool_use 和 tool_result 可一一对应
3. progress 不污染核心历史链
4. 会话可按消息链恢复
5. 子 agent transcript 能独立存储
