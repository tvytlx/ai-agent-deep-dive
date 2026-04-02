# 03. Skills、Plugins 与 MCP 需求文档

## 1. 为什么产品不能只靠内置能力

如果产品所有能力都硬编码在主程序里，会遇到几个问题：
- 难以扩展
- 难以适配不同团队
- 难以承载领域知识
- 难以形成生态

因此，这套产品必须支持可扩展能力面。

## 2. Skills 的需求本质

Skill 不是普通帮助文档，而是一种可复用的工作流能力包。

### 2.1 Skill 需要承载什么
- 某类任务的使用规则
- 某类任务的上下文说明
- 某类任务的执行 SOP
- 该任务适用的工具边界

### 2.2 为什么 Skill 必须是 first-class primitive
因为产品需要让模型在遇到特定任务时，优先加载相应能力，而不是每次都重新即兴发挥。

## 3. Skill 的产品需求

1. 系统要能列出当前可用技能
2. 模型要能在合适时调用技能
3. skill 内容要能注入会话
4. skill 要能带 frontmatter 元信息
5. skill 可以约束 allowed-tools
6. skill 需要避免重复加载

## 4. Plugin 的需求本质

Plugin 的角色不是给程序员加脚本，而是为模型注入新的行为表面。

### Plugin 至少要支持
- 新命令
- 新技能目录
- frontmatter 配置
- 运行时变量替换
- 工具约束
- 用户可调用与否的声明
- effort / model 等提示

## 5. 为什么要有 MCP

MCP 的需求本质是：
- 用统一协议接入外部工具
- 让产品获得更多外部能力
- 让工具与说明一起进入运行时

### MCP 需要满足
1. 接入外部 server
2. 拉取工具定义
3. 注入使用说明
4. 在 agent 级别支持额外 server
5. 在生命周期结束时清理资源

## 6. 为什么模型需要“知道扩展能力存在”

很多系统扩展做不起来，不是因为没有插件，而是模型根本不知道：
- 有哪些技能
- 什么时候该用
- 扩展工具怎么使用

因此产品必须把这些扩展能力转化成模型可感知的提示信息。

## 7. Plugin / Skill / MCP 三者关系

### Skill
解决“某类任务应该怎么做”

### Plugin
解决“系统可以新增什么能力面”

### MCP
解决“系统如何连接外部工具与外部能力”

三者叠加后，产品才能具备生态能力。

## 8. 伪代码表达

```python
class ExtensionRuntime:
    def load_skills(self, cwd):
        return discover_skill_packages(cwd)

    def load_plugins(self):
        return discover_plugins()

    def connect_mcp_servers(self, configs):
        return [connect(server) for server in configs]

    def expose_capabilities_to_model(self, skills, plugins, mcp_servers):
        return build_runtime_capability_listing(skills, plugins, mcp_servers)
```

## 9. 产品经理视角下的总需求句

> 产品必须提供一套可扩展运行时：Skill 负责封装工作流知识，Plugin 负责扩展命令与能力表面，MCP 负责接入外部工具与说明，三者共同让系统具备持续生长的能力。
