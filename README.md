# AI Agent Deep Dive

## Star History

<a href="https://www.star-history.com/?repos=tvytlx%2Fai-agent-deep-dive&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&legend=top-left" />
 </picture>
</a>

## Quick Links

PDF 下载 / PDF Report:
- [ai-agent-deep-dive-v2.1.pdf](./ai-agent-deep-dive-v2.1.pdf) 新增第八章：记忆系统
- [ai-agent-deep-dive-v2.pdf](./ai-agent-deep-dive-v2.pdf)

## Notes

- 本仓库仅保留面向学习与评论的分析材料，不提供源码目录。
- 第二版 PDF 已完成。

## Teaching Agent Code

这个仓库现在还包含一个**教学用的最小 Python Agent 项目**，用于演示一个 AI Agent 的核心结构应该怎么组织。

### 核心代码位置

- Agent 核心代码：[`src/agt/agent.py`](./src/agt/agent.py)
- CLI 入口：[`src/agt/cli.py`](./src/agt/cli.py)
- 教学文档：[`docs/`](./docs)

### 这个教学项目的定位

这个最小 Agent 项目是为了教学而设计的，特点是：

- 尽量保持结构清晰
- 尽量减少不必要的工程复杂度
- 所有核心代码集中在一个很小的范围内，方便学习
- 当前重点放在：Agent 主循环、Fake LLM 接口、Skills 发现、CLI 骨架

### 如何运行最小 Agent

本项目使用 Poetry 管理依赖。

#### 1. 安装依赖

```bash
poetry install
```

#### 2. 运行最小 Agent CLI

```bash
poetry run agt "你好"
```

#### 3. 查看 Skills

```bash
poetry run agt --skills-dir ./skills --list-skills
```

### 当前实现说明

当前版本是一个**教学型最小实现**，还没有接入真实远程模型 API。

目前内置的是一个可替换的 Fake LLM：
- 用户输入什么
- 它就会用流式文本块的方式返回一个测试响应

这样做的目的，是为了让后续接入真实模型时，只需要替换 LLM 调用层，而不需要重写整个 Agent 主体。
