from pathlib import Path
from subprocess import run
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_cli_lists_skills(tmp_path) -> None:
    skill_dir = tmp_path / "skills" / "analysis"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# analysis", encoding="utf-8")

    result = run(
        [
            sys.executable,
            "-m",
            "agt.cli",
            "--skills-dir",
            str(tmp_path / "skills"),
            "--list-skills",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "analysis" in result.stdout
