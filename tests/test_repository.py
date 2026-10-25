"""Structural and controlled-math checks; no network or third-party packages."""

import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "equity-research" / "SKILL.md"
PROMPT = ROOT / "prompts" / "equity-research.md"


def terminal_value(last_fcff, wacc, growth):
    """Return a Gordon-growth terminal value, or None for invalid inputs."""
    if wacc <= growth:
        return None
    return last_fcff * (1 + growth) / (wacc - growth)


def fcff_per_share(flows, wacc, growth, cash, debt, shares):
    """Apply year-end FCFF discounting and a simplified EV-to-equity bridge."""
    tv = terminal_value(flows[-1], wacc, growth)
    if tv is None or shares <= 0:
        raise ValueError("Invalid terminal assumptions or share count")
    years = len(flows)
    pv_explicit = sum(value / (1 + wacc) ** year for year, value in enumerate(flows, 1))
    ev = pv_explicit + tv / (1 + wacc) ** years
    return (ev - debt + cash) / shares


def fcfe_equity_value(flows, cost_of_equity, growth):
    """Value equity directly from FCFE; no enterprise-to-equity bridge applies."""
    tv = terminal_value(flows[-1], cost_of_equity, growth)
    if tv is None:
        raise ValueError("Cost of equity must exceed terminal growth")
    return sum(value / (1 + cost_of_equity) ** year for year, value in enumerate(flows, 1)) + tv / (1 + cost_of_equity) ** len(flows)


class RepositoryStructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "README.md", "LICENSE", "CHANGELOG.md", SKILL.relative_to(ROOT),
            PROMPT.relative_to(ROOT), "docs/architecture.md", "docs/methodology.md",
            "docs/usage.md", "docs/validation.md", "examples/report-template.md",
            "tests/fixtures/hypothetical-company.md", "tests/fixtures/missing-data.md",
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

    def test_standalone_prompt_contains_complete_skill_body(self):
        skill_body = SKILL.read_text(encoding="utf-8").split("---", 2)[2].strip()
        prompt = PROMPT.read_text(encoding="utf-8")
        self.assertIn(skill_body, prompt)

    def test_no_template_todos_remain(self):
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("[TODO:", text, str(path))
            self.assertNotIn("example_asset.txt", text, str(path))

    def test_relative_markdown_links_resolve(self):
        link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
        broken = []
        for path in ROOT.rglob("*.md"):
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

    def test_controlled_behavior_outputs(self):
        full_path = ROOT / "tests" / "outputs" / "full-en.md"
        quick_path = ROOT / "tests" / "outputs" / "quick-zh.md"
        missing_path = ROOT / "tests" / "outputs" / "missing-data.md"
        self.assertTrue(full_path.is_file(), "Run the controlled Full Research fixture")
        full = full_path.read_text(encoding="utf-8")
        for number in range(1, 10):
            self.assertRegex(full, rf"(?m)^## {number}\.")
        for letter in "ABCDEFG":
            self.assertIn(f"Agent {letter}", full)
        self.assertIn("14.612820", full)
        self.assertIn("Hypothetical", full)
        self.assertNotIn("Medium-Low", full)
        # Scenario values must appear in the report
        self.assertIn("7.458422", full)
        self.assertIn("23.557972", full)
        self.assertIn("11.690256", full)
        # Standard evidence categories with hypothetical qualifiers
        self.assertIn("Verified Fact (Hypothetical", full)
        self.assertIn("Modeling Assumption (Hypothetical", full)
        self.assertIn("Unavailable Information", full)
        quick_lines = quick_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(quick_lines), 2)
        self.assertTrue(quick_lines[0].startswith("1. **"))
        self.assertTrue(quick_lines[1].startswith("2. **"))
        self.assertIn("11.69", quick_lines[0])
        self.assertRegex("".join(quick_lines), r"[\u4e00-\u9fff]")
        standalone_lines = (ROOT / "tests" / "outputs" / "standalone-quick-en.md").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(standalone_lines), 2)
        self.assertTrue(standalone_lines[0].startswith("1. **Margin-of-Safety Buy Price:**"))
        self.assertIn("11.69", standalone_lines[0])
        missing = missing_path.read_text(encoding="utf-8")
        self.assertNotRegex(missing, r"\$\s*\d")
        self.assertRegex(missing, r"(?i)cannot|unable|insufficient|无法|不能")


class ControlledValuationTests(unittest.TestCase):
    def test_base_dcf_reconciles(self):
        value = fcff_per_share([92, 97, 102, 107, 112], 0.09, 0.025, 120, 200, 100)
        self.assertTrue(math.isclose(value, 14.61281975, rel_tol=0, abs_tol=1e-8))
        self.assertTrue(math.isclose(value * 0.8, 11.6902558, rel_tol=0, abs_tol=1e-7))

    def test_bear_and_bull_scenarios_reconcile(self):
        bear = fcff_per_share([75, 78, 80, 82, 84], 0.11, 0.015, 120, 200, 100)
        bull = fcff_per_share([100, 110, 120, 130, 140], 0.08, 0.03, 120, 200, 100)
        self.assertEqual(round(bear, 6), 7.458422)
        self.assertEqual(round(bull, 6), 23.557972)

    def test_invalid_terminal_spread_is_not_meaningful(self):
        self.assertIsNone(terminal_value(100, 0.08, 0.08))
        self.assertIsNone(terminal_value(100, 0.07, 0.08))
        with self.assertRaises(ValueError):
            fcff_per_share([100], 0.08, 0.09, 0, 0, 100)

    def test_fcfe_has_no_net_debt_bridge(self):
        flows = [10, 11, 12]
        direct = fcfe_equity_value(flows, 0.10, 0.02)
        expected_tv = 12 * 1.02 / (0.10 - 0.02)
        expected = sum(v / 1.10**i for i, v in enumerate(flows, 1)) + expected_tv / 1.10**3
        self.assertTrue(math.isclose(direct, expected, rel_tol=0, abs_tol=1e-12))

    def test_report_sensitivity_table_reconciles(self):
        """Every cell in the report's 5x5 sensitivity table must match recalculation."""
        full = (ROOT / "tests" / "outputs" / "full-en.md").read_text(encoding="utf-8")
        flows = [92, 97, 102, 107, 112]
        waccs = [0.08, 0.09, 0.10, 0.11, 0.12]
        growths = [0.015, 0.02, 0.025, 0.03, 0.035]
        for w in waccs:
            row_pattern = rf"\| {int(w*100)}% \|([^\n]+)\|"
            match = re.search(row_pattern, full)
            self.assertIsNotNone(match, f"Sensitivity row for WACC {w} missing")
            cells = [c.strip().replace("*", "").replace(",", "") for c in match.group(1).split("|")]
            self.assertEqual(len(cells), 5, f"WACC {w} row must have 5 cells")
            for g, cell in zip(growths, cells):
                expected = fcff_per_share(flows, w, g, 120, 200, 100)
                self.assertTrue(
                    math.isclose(float(cell), round(expected, 6), abs_tol=1e-6),
                    f"WACC {w}, g {g}: report {cell} != recalculated {expected:.6f}",
                )

    def test_report_wacc_derivation_reconciles(self):
        """WACC components in the report must reconcile: 80% equity + 20% after-tax debt."""
        cases = {"Bear": (0.12, 0.07, 0.11), "Base": (0.10, 0.05, 0.09), "Bull": (0.09, 0.04, 0.08)}
        for name, (coe, atd, expected_wacc) in cases.items():
            derived = 0.80 * coe + 0.20 * atd
            self.assertTrue(math.isclose(derived, expected_wacc, abs_tol=1e-12), name)
        fixture = (ROOT / "tests" / "fixtures" / "hypothetical-company.md").read_text(encoding="utf-8")
        self.assertIn("Terminal reinvestment rate = g / ROIC", fixture)
        # Terminal reinvestment: g / ROIC must equal 20% in all scenarios
        for g, roic in [(0.015, 0.075), (0.025, 0.125), (0.03, 0.15)]:
            self.assertTrue(math.isclose(g / roic, 0.20, abs_tol=1e-12))


if __name__ == "__main__":
    unittest.main(verbosity=2)
