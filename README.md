# AI Agent Deep Dive

**English** | [简体中文](./README.zh-CN.md)

<a href="https://www.star-history.com/?repos=tvytlx%2Fai-agent-deep-dive&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=tvytlx/ai-agent-deep-dive&type=date&legend=top-left" />
 </picture>
</a>

## Quick Links

PDF reports:
- New: **Hermes Agent Source Code Deep Dive**
- Claude Code: [ai-agent-deep-dive-v2.1.pdf](./ai-agent-deep-dive-v2.1.pdf), including the new Chapter 8: Memory System.
- Claude Code: [ai-agent-deep-dive-v2.pdf](./ai-agent-deep-dive-v2.pdf).

## Educational Agent Code

This repository also includes a **minimal Python agent built for learning**, demonstrating how to structure the core components of an AI agent.

### Where to Find the Code

- Agent core: [`src/agt/agent.py`](./src/agt/agent.py)
- CLI entry point: [`src/agt/cli.py`](./src/agt/cli.py)
- Learning materials: [`docs/`](./docs)

### Project Goals

This minimal agent is designed for educational use, with an emphasis on:

- Keeping the structure clear.
- Avoiding unnecessary engineering complexity.
- Keeping the core code small and easy to explore.
- Focusing on the agent loop, a Fake LLM interface, skill discovery, and the CLI skeleton.

### Running the Minimal Agent

The project uses Poetry to manage dependencies.

#### 1. Install Dependencies

```bash
poetry install
```

#### 2. Run the Agent CLI

```bash
poetry run agt "Hello"
```

#### 3. List Available Skills

```bash
poetry run agt --skills-dir ./skills --list-skills
```

### Current Implementation

The current version is a **minimal educational implementation**. It does not yet connect to a real remote model API.

It includes a replaceable Fake LLM that returns a test response in streamed text chunks for each user input.

This keeps the model integration separate from the agent itself: connecting a real model later only requires replacing the LLM call layer, rather than rewriting the agent.
