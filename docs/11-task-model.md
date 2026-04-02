# 11. 任务模型与后台执行规格

## 1. 目标

任务系统负责把“一个 agent 在做什么”变成可追踪对象，而不是只存在于对话文本里。

## 2. 任务类型

Python 版建议至少支持：

- `main_session_task`
- `local_agent_task`
- `background_agent_task`
- `shell_task`
- `verification_task`
- `remote_task`（可后置）

## 3. 核心任务字段

```python
class TaskRecord:
    task_id: str
    type: str
    session_id: str
    parent_task_id: str | None
    agent_id: str | None
    description: str
    status: str
    created_at: float
    started_at: float | None
    finished_at: float | None
    output_path: str | None
    error: str | None
    result_summary: str | None
    progress: dict | None
```

## 4. 状态机

建议统一状态：
- `pending`
- `running`
- `waiting_permission`
- `backgrounded`
- `completed`
- `failed`
- `cancelled`
- `killed`

## 5. 背景任务需求

background agent 至少要支持：
- 注册
- 更新进度
- 存储输出文件路径
- 完成时通知主线程
- 失败时通知主线程
- 支持 kill / cancel

## 6. 进度跟踪需求

任务进度至少记录：
- 工具调用次数
- token 使用量
- 最近活动
- 最近摘要

## 7. 输出文件需求

后台任务建议将结果落盘到 output file，用于：
- 主线程查看
- resume 后读取
- 审计

## 8. 通知机制需求

任务结束时，系统必须向主线程注入结构化 notification，而不是只静默完成。

## 9. 验收标准

1. 每个子 agent 都能注册为任务
2. 背景任务可查询状态
3. 任务可输出结果文件
4. 任务完成/失败会通知主线程
5. 任务可被停止
