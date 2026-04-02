# 13. 失败处理与恢复规格

## 1. 目标

Agent 系统不能把失败当成异常边缘情况。失败是常态，系统必须有明确恢复策略。

## 2. 失败类型

建议至少区分：

- `tool_input_error`
- `permission_denied`
- `hook_blocked`
- `shell_runtime_error`
- `model_api_error`
- `prompt_too_long`
- `mcp_connect_error`
- `task_killed`
- `resume_load_error`
- `session_storage_error`

## 3. 各类失败处理原则

### tool_input_error
- 直接回写错误给模型
- 不执行真实工具

### permission_denied
- 不重复原样调用
- 引导模型调整方案

### hook_blocked
- 将阻断原因结构化返回
- 允许模型或用户后续处理

### prompt_too_long
- 触发 compact / reactive compact
- 必要时重建消息序列后重试

### model_api_error
- 保留错误记录
- 可尝试有限恢复

## 4. resume 恢复需求

系统必须支持：
- 读取 transcript
- 找到 compact boundary 后有效历史
- 恢复 session_id 与 project dir
- 恢复活跃任务或至少恢复摘要

## 5. 子任务失败需求

子任务失败后不能静默消失，必须：
- 写入任务状态
- 通知主线程
- 保留错误摘要

## 6. 恢复策略级别

### 轻恢复
- 调整输入
- 重新请求权限
- 简短重试

### 中恢复
- 压缩上下文后重试
- 重建子任务上下文

### 重恢复
- resume 会话
- 用户介入
- 终止并保留证据

## 7. 验收标准

1. 常见失败都有明确处理路径
2. 子任务失败不会丢失
3. prompt too long 可进入压缩恢复
4. 会话中断后可恢复
