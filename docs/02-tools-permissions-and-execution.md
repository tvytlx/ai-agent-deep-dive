# 02. 工具、权限与执行链需求文档

## 1. 为什么工具系统是产品核心

如果模型不能操作环境，它只是建议生成器。这个产品的目标是帮助用户推进真实工程任务，因此必须具备正式的工具系统。

## 2. 工具系统需求

### 2.1 基础工具能力
产品至少需要以下工具类别：
- 读文件
- 改文件
- 写文件
- 搜索文件
- 搜索内容
- shell / 命令执行
- todo / 任务管理
- 用户追问
- 启动子 agent
- 调用外部 MCP 工具

### 2.2 工具使用规范
系统必须对模型明确规定工具使用优先级，避免：
- 用 shell 替代专用文件工具
- 误删或误改文件
- 低效重复操作

## 3. 权限系统需求

### 3.1 用户控制边界
用户必须能控制哪些工具自动允许，哪些要询问，哪些禁止。

### 3.2 权限决策来源
权限决策至少可能来自：
- 当前模式
- 用户规则
- 项目规则
- Hook 决策
- 特殊工具安全策略

### 3.3 被拒后的行为要求
如果某次工具调用被拒绝，系统不能机械重试，而应：
- 理解拒绝信号
- 调整方案
- 必要时向用户澄清

## 4. 执行链路需求

工具执行不能是“模型决定 -> 直接运行”。产品需要一条正式执行链：

1. 找到工具
2. 校验输入结构
3. 做额外 validateInput
4. 执行 PreToolUse hooks
5. 做权限决策
6. 真正执行工具
7. 记录 telemetry
8. 执行 PostToolUse hooks
9. 格式化结果回流给模型

## 5. 为什么需要 Hook

Hook 的需求本质是：
- 让组织规则进入运行时
- 让系统可以插入额外检查
- 让工具调用具备动态治理能力

### Hook 至少要支持的行为
- 返回消息
- 阻断执行
- 修改输入
- 提供 allow / ask / deny 建议
- 注入额外上下文

## 6. 为什么输入校验是必需的

模型本身会生成错误参数，因此产品必须在执行层拦住：
- schema 不合法
- 参数越界
- 缺字段
- 类型错误

## 7. shell 类工具的特殊需求

shell 工具的风险高于读写文件类工具，因此需要：
- 更严格的权限策略
- 可能的前置分类器检查
- 更强的审计能力

## 8. 工具执行结果的产品要求

工具执行结果不仅要“返回成功/失败”，还要满足：
- 可读
- 可追踪
- 能被后续 Hook 处理
- 能成为 transcript 的一部分

## 9. 伪代码表达

```python
def execute_tool(tool_name, raw_input, context):
    tool = find_tool(tool_name)
    validated = schema_validate(tool, raw_input)
    validated = run_custom_validation(tool, validated)

    hook_result = run_pre_hooks(tool, validated, context)
    decision = resolve_permission(hook_result, context)
    if decision == 'deny':
        return denied_result()

    final_input = maybe_update_input(validated, hook_result)
    output = tool.call(final_input)
    run_post_hooks(tool, final_input, output, context)
    return output
```

## 10. 产品经理视角下的总需求句

> 工具系统必须从“可调用”升级到“可治理”：既要让模型拥有执行能力，也要在执行前后经过校验、权限、Hook、审计与结果回流，确保整个过程安全、稳定、可追踪。
