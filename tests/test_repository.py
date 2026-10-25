"""Static structural tests: files, frontmatter, architecture, links, sync.

These tests never prove runtime LLM behavior; behavioral artifact checks are
in test_behavioral_outputs.py and real-data smoke tests are excluded from CI.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "equity-research" / "SKILL.md"
PROMPT = ROOT / "prompts" / "equity-research.md"


class RepositoryStructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "README.md", "LICENSE", "CHANGELOG.md", SKILL.relative_to(ROOT),
            PROMPT.relative_to(ROOT), "docs/architecture.md", "docs/methodology.md",
            "docs/usage.md", "docs/validation.md", "examples/report-template.md",
            "tests/fixtures/hypothetical-company.md", "tests/fixtures/missing-data.md",
            "tests/oracle.py", ".github/workflows/tests.yml",
        ]
        missing = [str(path) for path in required if not (ROOT / path).is_file()]
        self.assertEqual(missing, [])

    def test_skill_frontmatter_and_name(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: equity-research$")
        self.assertRegex(frontmatter, r"(?m)^description: \S.+$")
        self.assertEqual(SKILL.parent.name, "equity-research")
        self.assertLessEqual(len("equity-research"), 64)

    def test_all_agents_manager_and_stages_are_preserved(self):
        text = SKILL.read_text(encoding="utf-8")
        for letter in "ABCDEFG":
            self.assertIn(f"### Agent {letter} —", text)
        for stage in range(1, 6):
            self.assertIn(f"## Stage {stage} —", text)
        self.assertIn("Investment Committee", text)
        self.assertIn("rather than averages votes", text)
        self.assertIn("McKinsey 7S", text)
        self.assertIn("Buffett-Style", text)

    def test_modes_language_and_missing_data_rules(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Full Research Mode", text)
        self.assertIn("Quick Price Mode", text)
        self.assertIn("Default to English", text)
        self.assertIn("Simplified Chinese", text)
        self.assertIn("do not invent a number", text)
        self.assertIn("Watch Only", text)
        self.assertIn("Not Rated", text)

    def test_terminal_normalization_rule_present(self):
        for path in (SKILL, PROMPT):
            text = path.read_text(encoding="utf-8")
            self.assertIn("Terminal NOPAT", text, path.name)
            self.assertIn("terminal growth / terminal ROIC", text, path.name)
            self.assertIn("unexplained", text.lower(), path.name)

    def test_margin_of_safety_factor_framework_present(self):
        for path in (SKILL, PROMPT):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            self.assertIn("terminal-value dependence", lowered, path.name)
            self.assertIn("customer concentration", lowered, path.name)
            self.assertIn("withhold", lowered, path.name)
            self.assertIn("not a guaranteed floor", lowered, path.name)

    def test_evidence_labeling_and_gate_rules_present(self):
        for path in (SKILL, PROMPT):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            self.assertIn("reserved for an externally attributed forecast", lowered, path.name)
            self.assertIn("derived valuation", lowered, path.name)
            self.assertIn("never `analyst estimate`", lowered, path.name)
            self.assertIn("cure missing inputs", lowered, path.name)
            self.assertIn("haircut versus evidence gate", lowered, path.name)
            self.assertIn("incomplete real-world research", lowered, path.name)
            self.assertIn("fully specified hypothetical fixture", lowered, path.name)

    def test_standalone_prompt_contains_complete_skill_body(self):
        skill_body = SKILL.read_text(encoding="utf-8").split("---", 2)[2].strip()
        prompt = PROMPT.read_text(encoding="utf-8")
        self.assertIn(skill_body, prompt)

    def test_no_template_todos_remain(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("[TODO:", text, str(path))

    def test_fixture_does_not_leak_expected_answers(self):
        """The behavioral fixture must not contain any oracle valuation result."""
        import sys
        sys.path.insert(0, str(ROOT / "tests"))
        from oracle import expected_values

        fixture = (ROOT / "tests" / "fixtures" / "hypothetical-company.md").read_text(encoding="utf-8")
        self.assertNotIn("Expected mathematical results", fixture)
        for result in expected_values().values():
            value = result["per_share"]
            for rendering in (f"{value:.6f}", f"{value:.4f}", f"{value:.2f}"):
                self.assertNotIn(rendering, fixture, f"fixture leaks expected value {rendering}")
        self.assertNotRegex(fixture, r"(?i)margin.of.safety (buy )?price[^\n]*\d+\.\d{2,}")

    def test_relative_markdown_links_resolve(self):
        link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
        broken = []
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for target in link_pattern.findall(path.read_text(encoding="utf-8")):
                target = target.split()[0].strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                local = target.split("#", 1)[0]
                if local and not (path.parent / local).resolve().exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(broken, [])

    def test_mermaid_architecture_is_complete(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme.count("```mermaid"), 1)
        diagram = readme.split("```mermaid", 1)[1].split("```", 1)[0]
        self.assertIn("flowchart TD", diagram)
        for stage in range(1, 6):
            self.assertIn(f"Stage {stage}", diagram)
        for letter in "ABCDEFG":
            self.assertRegex(diagram, rf"\b{letter}\[")
        self.assertIn("Investment Committee Manager", diagram)


if __name__ == "__main__":
    unittest.main(verbosity=2)
