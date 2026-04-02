from __future__ import annotations

import argparse
from pathlib import Path

from .agent import Agent, Tool, echo_tool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agt", description="Teaching-oriented AI agent CLI")
    parser.add_argument("prompt", nargs="?", default="请开始", help="User prompt")
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Directory containing skill folders with SKILL.md",
    )
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="List discovered skills and exit",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    agent = Agent()
    agent.register_tool(Tool("echo", "Echo input text", echo_tool))

    skills = agent.load_skills(Path(args.skills_dir))
    if args.list_skills:
        for skill in skills:
            print(skill)
        return 0

    if skills:
        agent.remember(f"loaded_skills={','.join(skills)}")

    reply = agent.run(args.prompt)
    print(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
