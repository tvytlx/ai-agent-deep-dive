# 06. 验证与质量保证需求文档

## 1. 为什么“做完”不等于“完成”

在 AI 编程产品里，最大的风险之一是：模型会把“代码改了”误当成“任务完成了”。

因此，这个产品必须把“验证”设计成一个独立能力，而不是可有可无的附属步骤。

## 2. 验证系统的产品目标

1. 独立检查实现是否真的可用
2. 防止只读代码就宣称完成
3. 防止 happy path 偏见
4. 让验证结果带证据而不是口头判断

## 3. 验证 Agent 的需求

### 3.1 独立角色
验证角色需要与实施角色分离，避免实现者偏见。

### 3.2 默认心智模型
验证角色的工作不是“帮实现找理由通过”，而是主动尝试发现问题。

### 3.3 必须禁止的行为
验证角色不能：
- 修改项目文件
- 安装依赖
- 用写操作掩盖问题

### 3.4 必须支持的检查类型
- build
- test suite
- lint / type-check
- 接口调用验证
- UI 自动化验证
- CLI 输入输出验证
- migration 验证
- adversarial probe

## 4. 输出格式需求

验证结果必须满足：
- 有检查项标题
- 有实际执行命令
- 有真实输出
- 有 PASS / FAIL / PARTIAL 结果
- 最后有统一 verdict

## 5. 为什么需要 adversarial probe

只验证 happy path 会导致大量问题漏检。因此系统要要求验证阶段主动尝试：
- 边界输入
- 并发场景
- 空输入 / 非法输入
- 重复请求
- 不存在资源引用

## 6. 为什么验证必须可追溯

如果验证没有命令和输出，用户无法判断：
- 到底测没测
- 测了什么
- 失败在哪

因此，质量系统必须要求“证据化验证”。

## 7. 质量保证不只是测试

这套产品的质量保证包括：
- 提示词中对诚实汇报的要求
- 验证角色的独立存在
- 执行链的日志与 transcript
- 失败可追踪
- 结果可复盘

## 8. 伪代码表达

```python
class VerificationRunner:
    def verify(self, task, changed_files, context):
        checks = build_verification_plan(task, changed_files)
        results = []
        for check in checks:
            cmd = check.command
            output = run(cmd)
            results.append(evaluate(output, check.expectation))
        return summarize_verdict(results)
```

## 9. 产品经理视角下的总需求句

> 产品必须把验证设计成独立、对抗性、证据化的质量系统：它不依赖实施者自我声明，而是通过命令、输出与统一 verdict 来证明任务是否真正完成。
