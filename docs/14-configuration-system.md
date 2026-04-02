# 14. 配置系统规格

## 1. 目标

配置系统负责把产品的默认行为、用户偏好、项目约束和扩展能力统一管理，而不是散落在代码里。

## 2. 配置来源

Python 版建议支持以下来源：

1. 全局用户配置
2. 项目级配置
3. session 级配置
4. plugin / skill frontmatter 配置
5. 环境变量
6. CLI 参数覆盖

## 3. 配置优先级

建议优先级从高到低：

1. runtime override / CLI 参数
2. session 配置
3. 项目配置
4. 用户全局配置
5. 默认配置

## 4. 必须可配置的项目

- 默认模型
- 语言
- 输出风格
- permission mode
- hook 开关与 hook 配置
- MCP server 配置
- plugin 路径
- skill 路径
- token / task budget
- 自动 compact 开关
- transcript 持久化开关

## 5. Agent 级配置需求

每个 agent 定义建议支持：
- agent_type
- when_to_use
- allowed_tools / disallowed_tools
- model
- memory scope
- mcp_servers
- background capability
- isolation mode

## 6. 配置系统验收标准

1. 用户可在不改代码的情况下调整运行行为
2. 项目可定义局部约束
3. session 可临时覆盖配置
4. plugin / skill 可附带配置元信息
