from agt.agent import Agent, Tool, echo_tool


def test_agent_returns_default_message() -> None:
    agent = Agent()
    agent.register_tool(Tool("echo", "Echo input text", echo_tool))

    result = agent.run("hello")

    assert "教学用 Agent 骨架" in result
    assert agent.messages[0].role == "user"
    assert agent.messages[-1].role == "assistant"


def test_load_skills_finds_skill_md(tmp_path) -> None:
    skill_dir = tmp_path / "skills" / "writing"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# writing", encoding="utf-8")

    agent = Agent()
    skills = agent.load_skills(tmp_path / "skills")

    assert skills == ["writing"]
