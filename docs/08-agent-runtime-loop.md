# 08. Agent 运行时主循环规格

> 目标：定义 Python 版本实现时最核心的运行时循环。该文档不是源码解释，而是实现规格。

## 1. 设计目标

主循环必须满足以下目标：

1. 能持续推进任务，而不是只做一次回答
2. 能在每轮后根据工具结果重新决策
3. 能在权限阻断、上下文压缩、工具失败时继续可控运行
4. 能触发子 agent、后台任务、验证任务
5. 能生成可追踪的消息流与 transcript

## 2. 主循环的输入

一次主循环至少需要以下输入：

- `messages`: 当前消息序列
- `system_prompt`: 已组装完成的系统提示词
- `tool_registry`: 当前可用工具集合
- `tool_use_context`: 执行上下文（cwd、权限、session、任务状态）
- `memory_context`: 注入后的记忆内容
- `user_context`: 用户态上下文
- `system_context`: 系统态上下文
- `can_use_tool`: 权限判断函数
- `max_turns`: 最大回合数
- `task_budget`: 本轮任务预算（可选）

## 3. 主循环的输出

主循环每轮可能产出：

- 普通 assistant 消息
- tool_use 请求
- tool_result 回写
- progress 消息
- compact / summary 边界消息
- 子任务启动事件
- terminal state（完成 / 失败 / 中断）

## 4. 循环状态

实现时必须维护显式状态，而不是散落在局部变量中。

建议状态字段：

```python
class QueryState:
    messages: list
    turn_count: int
    auto_compact_tracking: dict | None
    pending_tool_summary: object | None
    stop_hook_active: bool
    max_output_recovery_count: int
    has_attempted_reactive_compact: bool
    transition_reason: str | None
```

## 5. 标准单轮流程

每轮执行顺序建议固定为：

1. 预处理当前消息
2. 计算 token / budget 状态
3. 调用模型
4. 解析返回内容
5. 如有工具调用，进入工具执行链
6. 将工具结果追加回消息
7. 如需压缩，执行 compact
8. 决定是否继续下一轮
9. 达到终止条件则返回 terminal state

## 6. 终止条件

至少支持以下终止条件：

- 模型明确结束任务
- 达到 `max_turns`
- 用户中断
- 权限阻断且无可行替代方案
- 发生不可恢复异常
- 任务被后台化或移交

## 7. 工具调用处理要求

如果模型返回一个或多个工具调用：

- 必须按顺序或编排策略执行
- 必须将每个 tool_result 写回消息流
- 如果工具失败，失败信息也必须结构化回写
- 严禁只在 UI 层显示，不回写到模型上下文

## 8. 压缩与恢复点

主循环必须内建以下钩子点：

- 调用模型前检查是否需要压缩
- 工具结果过长时应用 result budget
- prompt 过长时触发 compact / reactive compact
- resume 时从 compact boundary 后恢复有效消息

## 9. 子 agent 与后台任务接入点

主循环必须允许以下事件打断常规路径：

- 启动 foreground subagent
- 启动 background subagent
- 接收 task notification
- 继续 resume 某个已有 agent

## 10. Python 版推荐伪代码

```python
def query_loop(params):
    state = init_state(params)

    while True:
        if should_stop(state, params):
            return terminal_result(state)

        state = maybe_compact(state, params)
        request = build_model_request(state, params)
        response = call_model(request)
        state.messages.append(response.assistant_message)

        if response.tool_calls:
            tool_events = run_tools(response.tool_calls, params)
            state.messages.extend(tool_events)
            state.transition_reason = 'tool_round'
            continue

        if response.should_launch_subagent:
            launch_subagent(response, params)
            state.transition_reason = 'subagent'
            continue

        if response.is_terminal:
            return terminal_result(state)

        state.turn_count += 1
```

## 11. 实现边界

Python 第一版务必保证：
- 单主循环是清晰、可测试的
- 每轮状态可序列化
- 每轮输出可回放
- 每轮失败可定位

不要把主循环写成大量隐式副作用的脚本式逻辑。

## 12. 验收标准

程序员实现完成后，应满足：

1. 可以连续多轮处理任务
2. 工具结果能回流并影响下一轮
3. 超长上下文会压缩而不是直接崩溃
4. 子任务可以插入主流程
5. transcript 可完整记录轮次
