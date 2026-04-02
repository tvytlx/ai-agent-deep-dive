# 10. 上下文管理与压缩规格

## 1. 目标

上下文管理的目标不是“保留一切”，而是让模型在有限预算内持续拿到最关键的信息。

## 2. 必须保留的信息

优先级最高的信息包括：

1. 当前用户任务目标
2. 系统硬规则与安全约束
3. 用户明确偏好
4. 最近关键工具结果
5. 当前活跃子任务状态
6. 记忆摘要
7. 最近 compact 后的摘要

## 3. 可压缩的信息

以下信息应优先被压缩或裁剪：

- 旧的长日志
- 重复解释
- 已完成步骤的冗余细节
- 大量相似 read/search 结果
- 旧的 progress 消息

## 4. 上下文预算机制

Python 版建议同时维护：
- 粗略 token 估计
- 工具结果字符预算
- 每轮输出预算
- 全任务预算（可选）

## 5. 压缩触发条件

建议在以下情况触发：

- 请求前 token 估计超过阈值
- 工具结果总量过大
- 模型返回 prompt too long
- resume 重建会话时

## 6. 压缩策略层级

### 6.1 轻量裁剪
先裁剪：
- 重复 progress
- 冗长工具输出尾部
- 无关附件

### 6.2 摘要压缩
把旧消息浓缩成 summary message。

### 6.3 边界标记
插入 compact boundary，标记压缩点。

## 7. 子任务上下文要求

### fork 子任务
- 继承必要父上下文
- 尽量维持 cache-friendly prefix
- 子任务输出不要原样全部灌回主线程

### verification 子任务
- 需要任务目标、改动文件、实现摘要
- 不需要完整噪声过程

## 8. 工具结果预算

工具结果必须经过 budget 控制。否则：
- 长 grep
- 长 read
- 长 shell 输出
会迅速污染上下文。

## 9. Python 版伪代码

```python
def manage_context(messages, budget):
    messages = drop_ephemeral_progress(messages)
    messages = trim_large_tool_results(messages, budget.tool_result_chars)

    if estimate_tokens(messages) > budget.max_input_tokens:
        summary = summarize_old_messages(messages)
        messages = build_post_compact_messages(summary, messages)

    return messages
```

## 10. 验收标准

1. 长任务不会因上下文无限增长而崩溃
2. resume 后仍可恢复关键事实
3. 子任务不会把噪声大规模回灌主线程
4. 工具长输出会被预算裁剪
