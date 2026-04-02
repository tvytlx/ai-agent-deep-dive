from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class Message:
    role: str
    content: str
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    ok: bool
    content: str
    meta: dict[str, Any] = field(default_factory=dict)


class Tool:
    def __init__(self, name: str, description: str, handler: Callable[[dict[str, Any]], ToolResult]):
        self.name = name
        self.description = description
        self.handler = handler

    def call(self, payload: dict[str, Any]) -> ToolResult:
        return self.handler(payload)


class Agent:
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.tools: dict[str, Tool] = {}
        self.memory: list[str] = []
        self.max_turns: int = 20

    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def add_message(self, role: str, content: str, **meta: Any) -> None:
        self.messages.append(Message(role=role, content=content, meta=meta))

    def remember(self, text: str) -> None:
        self.memory.append(text)

    def can_use_tool(self, tool_name: str) -> bool:
        return tool_name in self.tools

    def load_skills(self, skills_dir: str | Path) -> list[str]:
        skills_path = Path(skills_dir)
        if not skills_path.exists():
            return []

        loaded: list[str] = []
        for path in sorted(skills_path.rglob("SKILL.md")):
            loaded.append(path.parent.name)
        return loaded

    def model_step(self) -> dict[str, Any]:
        return {
            "type": "message",
            "content": "这是一个教学用 Agent 骨架。下一步请在 model_step() 中接入你的模型逻辑。",
        }

    def run(self, user_input: str) -> str:
        self.add_message("user", user_input)

        for turn in range(self.max_turns):
            step = self.model_step()

            if step["type"] == "message":
                content = step["content"]
                self.add_message("assistant", content, turn=turn)
                return content

            if step["type"] == "tool_call":
                tool_name = step["tool"]
                tool_input = step.get("input", {})

                if not self.can_use_tool(tool_name):
                    error = f"Tool not allowed or not found: {tool_name}"
                    self.add_message("tool_result", error, ok=False, tool=tool_name)
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
    text = str(payload.get("text", ""))
    return ToolResult(ok=True, content=f"echo: {text}")
