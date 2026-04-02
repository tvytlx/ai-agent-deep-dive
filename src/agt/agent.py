"""
教学版 Agent 核心文件。

本文件的目标不是追求最复杂、最完整的工程实现，而是：

1. 用尽量清晰的 Python 代码，演示一个 Agent 的核心结构
2. 保持代码易读、易改、易扩展，方便教学与逐步演进
3. 为后续接入真实 LLM、工具系统、Skills、记忆系统提供稳定骨架
4. 在写法上尽量遵循清晰封装、低耦合、易测试的最佳实践

教学约定：
- 所有文档与注释优先使用中文
- 类、函数、重要属性都尽量提供清晰文档
- 优先追求“容易理解”，再追求“功能丰富”
- 允许用最小可用实现来表达结构，但要保留明确扩展点
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator, Protocol


@dataclass
class Message:
    """
    表示 Agent 运行时中的一条消息。

    这是一种教学用的最小消息模型。真实产品中，消息通常会更复杂，
    可能还会包含：消息 ID、父子关系、时间戳、工具块、token 使用信息等。

    属性：
        role:
            消息角色。
            常见值包括：
            - "user"：用户消息
            - "assistant"：模型回复
            - "tool_result"：工具执行结果

        content:
            消息正文内容。
            这里为了教学简化为纯文本。

        meta:
            附加元数据。
            用于保存额外的结构化信息，例如 turn 编号、chunks、工具名等。
    """

    role: str
    content: str
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """
    表示工具执行后的结果。

    属性：
        ok:
            表示工具执行是否成功。

        content:
            工具返回给 Agent 的文本内容。
            在真实系统中，这里也可以扩展为结构化内容。

        meta:
            工具执行附带的元数据。
            例如执行耗时、文件路径、命中条数等。
    """

    ok: bool
    content: str
    meta: dict[str, Any] = field(default_factory=dict)


class Tool:
    """
    表示一个可注册到 Agent 中的工具。

    设计思路：
    - 工具本身只关心自己的名字、说明和处理函数
    - Agent 只依赖统一的 Tool 接口，而不关心具体工具细节
    - 这样可以降低 Agent 与具体工具实现之间的耦合

    参数：
        name:
            工具名称，必须唯一。

        description:
            工具用途说明。
            主要用于教学展示、调试和未来做工具提示词时使用。

        handler:
            工具执行函数。
            输入为字典，输出为 ToolResult。
    """

    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable[[dict[str, Any]], ToolResult],
    ):
        """
        初始化一个工具对象。

        参数：
            name:
                工具名称。

            description:
                工具用途描述。

            handler:
                真正执行工具逻辑的函数。
        """
        self.name = name
        self.description = description
        self.handler = handler

    def call(self, payload: dict[str, Any]) -> ToolResult:
        """
        执行工具。

        参数：
            payload:
                传给工具的输入参数。

        返回：
            ToolResult：工具执行结果。
        """
        return self.handler(payload)


class LLMClient(Protocol):
    """
    LLM 客户端协议。

    这是一个非常重要的教学设计点：

    我们不让 Agent 直接依赖某一个具体模型 SDK，
    而是先定义一个统一接口。这样以后无论接：

    - OpenAI
    - Anthropic
    - LiteLLM
    - 本地模型
    - 假模型（Fake LLM）

    都可以复用同一个 Agent 主体。

    方法：
        stream_text:
            输入当前消息列表，返回一个文本分块迭代器。
    """

    def stream_text(self, messages: list[Message]) -> Iterator[str]:
        """
        基于当前消息列表，流式返回文本分块。

        参数：
            messages:
                当前上下文消息列表。

        返回：
            一个字符串迭代器，每次 yield 一段文本。
        """
        ...


class FakeLLMClient:
    """
    教学用假模型客户端。

    这个类的核心价值是：
    - 不依赖任何远程 API
    - 方便本地测试
    - 能模拟“流式输出”的基本行为
    - 未来可以被真实 LLM 客户端直接替换

    当前行为非常简单：
    - 读取最后一条用户消息
    - 拼成一段固定风格的回复
    - 再把回复切成多个 chunk 流式返回
    """

    def stream_text(self, messages: list[Message]) -> Iterator[str]:
        """
        根据消息列表流式生成文本。

        参数：
            messages:
                当前消息列表。

        返回：
            文本块迭代器。
        """
        last_user_message = next(
            (m.content for m in reversed(messages) if m.role == "user"),
            "",
        )
        response = f"[fake-llm] 你刚才说的是：{last_user_message}"
        for chunk in self._chunk_text(response, size=8):
            yield chunk

    @staticmethod
    def _chunk_text(text: str, size: int = 8) -> Iterator[str]:
        """
        将一段文本切成多个小块，用于模拟流式返回。

        参数：
            text:
                要切分的完整文本。

            size:
                每个文本块的最大长度。

        返回：
            文本块迭代器。
        """
        for i in range(0, len(text), size):
            yield text[i : i + size]


class Agent:
    """
    教学版 Agent 主类。

    这是当前项目中最核心的对象。它负责：
    - 保存消息
    - 管理工具
    - 管理简单记忆
    - 调用 LLM
    - 运行最小主循环

    当前版本是教学最小骨架，因此刻意保持简单。
    未来可以在这个类上继续演化：
    - 权限系统
    - system prompt
    - tool calling 协议
    - verification agent
    - transcript 持久化
    - context management

    参数：
        llm:
            可注入的 LLM 客户端。
            如果不传，则默认使用 FakeLLMClient。

    属性：
        messages:
            当前 Agent 的消息历史。

        tools:
            已注册工具表，key 为工具名，value 为 Tool 实例。

        memory:
            教学版最小记忆列表。
            当前只做演示用途。

        max_turns:
            最大回合数，避免无限循环。

        llm:
            当前绑定的 LLM 客户端实现。
    """

    def __init__(self, llm: LLMClient | None = None) -> None:
        """
        初始化 Agent。

        参数：
            llm:
                可选的 LLM 客户端。
                不传时使用默认的 FakeLLMClient。
        """
        self.messages: list[Message] = []
        self.tools: dict[str, Tool] = {}
        self.memory: list[str] = []
        self.max_turns: int = 20
        self.llm: LLMClient = llm or FakeLLMClient()

    def register_tool(self, tool: Tool) -> None:
        """
        注册一个工具到 Agent 中。

        参数：
            tool:
                要注册的工具对象。
        """
        self.tools[tool.name] = tool

    def add_message(self, role: str, content: str, **meta: Any) -> None:
        """
        向消息历史中追加一条消息。

        参数：
            role:
                消息角色。

            content:
                消息文本内容。

            **meta:
                任意附加元数据。
        """
        self.messages.append(Message(role=role, content=content, meta=meta))

    def remember(self, text: str) -> None:
        """
        向简化记忆列表中加入一条记忆。

        参数：
            text:
                要保存的记忆文本。
        """
        self.memory.append(text)

    def can_use_tool(self, tool_name: str) -> bool:
        """
        判断某个工具当前是否可用。

        当前教学版逻辑非常简单：
        - 只判断该工具是否已注册

        未来可以扩展为：
        - 权限判断
        - allow / ask / deny
        - agent 角色限制

        参数：
            tool_name:
                工具名称。

        返回：
            bool：是否可用。
        """
        return tool_name in self.tools

    def load_skills(self, skills_dir: str | Path) -> list[str]:
        """
        从目录中发现可用 Skills。

        当前教学版规则：
        - 递归查找 `SKILL.md`
        - skill 名称使用其父目录名

        参数：
            skills_dir:
                Skills 根目录路径。

        返回：
            已发现的 skill 名称列表。
        """
        skills_path = Path(skills_dir)
        if not skills_path.exists():
            return []

        loaded: list[str] = []
        for path in sorted(skills_path.rglob("SKILL.md")):
            loaded.append(path.parent.name)
        return loaded

    def call_llm_stream(self) -> Iterator[str]:
        """
        调用当前绑定的 LLM 客户端，并返回流式文本块。

        这是一个关键的抽象层。
        以后接真实模型时，优先改的是 LLMClient 的实现，
        而不是 Agent 主循环本身。

        返回：
            文本块迭代器。
        """
        return self.llm.stream_text(self.messages)

    def model_step(self) -> dict[str, Any]:
        """
        执行一次模型步骤。

        当前教学版逻辑：
        - 调用 LLM 流式接口
        - 收集所有 chunk
        - 组装为一条 message 类型结果

        在未来版本中，这里可以继续扩展为：
        - message
        - tool_call
        - subagent_call
        - verification_request

        返回：
            一个描述“本轮模型决定”的字典。
        """
        chunks = list(self.call_llm_stream())
        return {
            "type": "message",
            "content": "".join(chunks),
            "chunks": chunks,
        }

    def run(self, user_input: str) -> str:
        """
        运行 Agent 的最小主循环。

        当前版本流程：
        1. 记录用户输入
        2. 调用 model_step()
        3. 如果返回 message，则结束
        4. 如果未来返回 tool_call，则执行工具并继续循环
        5. 超过最大轮次则停止

        参数：
            user_input:
                用户输入文本。

        返回：
            Agent 最终返回给用户的文本。
        """
        self.add_message("user", user_input)

        for turn in range(self.max_turns):
            step = self.model_step()

            if step["type"] == "message":
                content = step["content"]
                self.add_message(
                    "assistant",
                    content,
                    turn=turn,
                    chunks=step.get("chunks", []),
                )
                return content

            if step["type"] == "tool_call":
                tool_name = step["tool"]
                tool_input = step.get("input", {})

                if not self.can_use_tool(tool_name):
                    error = f"Tool not allowed or not found: {tool_name}"
                    self.add_message(
                        "tool_result",
                        error,
                        ok=False,
                        tool=tool_name,
                    )
                    continue

                result = self.tools[tool_name].call(tool_input)
                self.add_message(
                    "tool_result",
                    result.content,
                    ok=result.ok,
                    tool=tool_name,
                    tool_input=tool_input,
                    tool_meta=result.meta,
                )
                continue

            raise ValueError(f"Unknown step type: {step['type']}")

        final_text = "Agent stopped because it reached max_turns."
        self.add_message("assistant", final_text)
        return final_text


def echo_tool(payload: dict[str, Any]) -> ToolResult:
    """
    一个最简单的教学示例工具。

    作用：
        把输入文本原样回显回来。

    参数：
        payload:
            工具输入字典。
            约定使用 `text` 字段。

    返回：
        ToolResult：工具执行结果。
    """
    text = str(payload.get("text", ""))
    return ToolResult(ok=True, content=f"echo: {text}")
