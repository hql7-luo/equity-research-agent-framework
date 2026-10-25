"""Behavioral artifact tests: field-based validation against the oracle.

Values are extracted from the report's designated Valuation Summary fields
(the labels required by the Skill), not by scanning whole documents for any
matching number. Tests use tolerance-based comparison against tests/oracle.py,
which is never supplied to the model under evaluation.

These tests validate committed artifacts only; they do not rerun an LLM.
"""

import math
import re
import unittest
from pathlib import Path

from oracle import expected_values

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "tests" / "outputs"
TOL = 0.005  # 0.5% relative tolerance for scenario values

FULL = OUTPUTS / "full-en.md"
QUICK_ZH = OUTPUTS / "quick-zh.md"
MISSING = OUTPUTS / "missing-data.md"
STANDALONE = OUTPUTS / "standalone-quick-en.md"

FIELD_PATTERN = r"`?{label}`?\s*[:\uff1a]\s*(?:USD\s*|\$)?([\d,]+(?:\.\d+)?)"


def extract_field(text: str, label: str) -> float:
    """Extract a numeric answer from its designated labeled field."""
    m = re.search(FIELD_PATTERN.format(label=re.escape(label)), text)
    if not m:
        raise AssertionError(f"required field '{label}' not found")
    return float(m.group(1).replace(",", ""))


def extract_haircut(text: str) -> float:
    """Extract the explicitly stated margin-of-safety haircut as a fraction."""
    m = re.search(r"Margin-of-safety haircut:\s*(\d{1,2}(?:\.\d+)?)\s*%", text)
    if not m:  # fall back to the Skill's sentence form
        m = re.search(r"(\d{1,2}(?:\.\d+)?)\s*%\s*(?:margin-of-safety|safety) (?:haircut|discount)", text)
    if not m:
        raise AssertionError("no explicitly stated margin-of-safety haircut")
    return float(m.group(1)) / 100


def parse_full_report(text: str) -> dict:
    return {
        "bear": extract_field(text, "Bear value per share"),
        "base": extract_field(text, "Base value per share"),
        "bull": extract_field(text, "Bull value per share"),
        "haircut": extract_haircut(text),
        "buy_price": extract_field(text, "Margin-of-safety buy price"),
    }


def parse_quick(text: str) -> dict:
    lines = text.splitlines()
    if len(lines) != 2:
        raise AssertionError(f"Quick Price must be exactly 2 lines, got {len(lines)}")
    price_m = re.search(r"(?:USD\s*|\$)\s*([\d,]+(?:\.\d+)?)", lines[0])
    base_m = re.search(r"(?:USD\s*|\$)\s*([\d,]+(?:\.\d+)?)", lines[1])
    if not (price_m and base_m):
        raise AssertionError("Quick Price lines must contain a price and a Base value")
    price = float(price_m.group(1).replace(",", ""))
    base = float(base_m.group(1).replace(",", ""))
    implied = 1 - price / base
    # Line 2 may cite other percentages (TV share, customer concentration).
    # The stated haircut must match the arithmetic implied by price and Base.
    stated = [float(x) / 100 for x in re.findall(r"(\d{1,3}(?:\.\d+)?)\s*%", lines[1])]
    if not any(abs(s - implied) <= 0.01 for s in stated):
        raise AssertionError(f"no stated haircut near implied {implied:.2%}; percents={stated}")
    return {"buy_price": price, "base": base, "haircut": implied}


def valuation_block(text: str) -> str:
    """Return the labeled valuation summary block, or raise if absent."""
    start = text.find("Bear value per share:")
    end = text.find("Margin-of-safety buy price:")
    if start < 0 or end < 0:
        raise AssertionError("valuation summary block incomplete")
    return text[start:end + 60]


def check_valuation_labeling(text: str) -> bool:
    """True only if valuation fields are tagged modeling/derived, not Analyst Estimate."""
    block = valuation_block(text)
    tagged = ("Modeling Assumption" in block or "Derived Valuation" in block)
    mislabeled = "Analyst Estimate" in block
    return tagged and not mislabeled


class FieldExtractionSelfTests(unittest.TestCase):
    """The parser itself must reject wrong values in designated fields."""

    def _sample(self, base: float) -> str:
        return ("Bear value per share: $7.00\n"
                f"Base value per share: ${base:.2f}\n"
                "Bull value per share: $25.00\n"
                "Margin-of-safety haircut: 35%\n"
                "Margin-of-safety buy price: $9.53\n")

    def test_correct_fields_parse(self):
        parsed = parse_full_report(self._sample(14.67))
        self.assertAlmostEqual(parsed["base"], 14.67)
        self.assertAlmostEqual(parsed["haircut"], 0.35)

    def test_wrong_value_detected(self):
        expected = expected_values()["Base"]["per_share"]
        wrong_report = self._sample(expected * 1.10)  # 10% overstatement
        parsed = parse_full_report(wrong_report)
        self.assertFalse(math.isclose(parsed["base"], expected, rel_tol=TOL))

    def test_value_elsewhere_does_not_satisfy_field(self):
        # Correct number appears in prose, but the designated field is wrong.
        expected = expected_values()["Base"]["per_share"]
        report = self._sample(99.99) + f"\nNote: some other figure is {expected:.2f}."
        parsed = parse_full_report(report)
        self.assertEqual(parsed["base"], 99.99)
        self.assertFalse(math.isclose(parsed["base"], expected, rel_tol=TOL))

    def test_missing_field_rejected(self):
        with self.assertRaises(AssertionError):
            parse_full_report("A report without the labeled valuation block.")

    def test_valuation_labeling_rule_detects_mislabel(self):
        good = self._sample(14.67).replace(
            "Margin-of-safety buy price: $9.53",
            "Margin-of-safety buy price: $9.53 — Derived Valuation")
        self.assertTrue(check_valuation_labeling(good))
        bad = self._sample(14.67).replace(
            "Margin-of-safety buy price: $9.53",
            "Margin-of-safety buy price: $9.53 — Analyst Estimate")
        self.assertFalse(check_valuation_labeling(bad))


@unittest.skipUnless(FULL.is_file(), "behavioral outputs not generated")
class FullResearchOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = FULL.read_text(encoding="utf-8")
        cls.parsed = parse_full_report(cls.text)

    def test_nine_sections_and_all_agents(self):
        for number in range(1, 10):
            self.assertRegex(self.text, rf"(?m)^## {number}\.")
        for letter in "ABCDEFG":
            self.assertIn(f"Agent {letter}", self.text)
        self.assertIn("Manager", self.text)

    def test_designated_scenario_fields_match_oracle(self):
        expected = expected_values()
        for field, name in (("bear", "Bear"), ("base", "Base"), ("bull", "Bull")):
            self.assertTrue(
                math.isclose(self.parsed[field], expected[name]["per_share"], rel_tol=TOL),
                f"{name} field {self.parsed[field]} != oracle {expected[name]['per_share']:.6f}",
            )

    def test_haircut_and_buy_price_fields_are_consistent(self):
        haircut = self.parsed["haircut"]
        self.assertIn(round(haircut * 100), (15, 25, 35),
                      "haircut must be a band reference value (15/25/35) unless deviation is documented")
        implied = self.parsed["base"] * (1 - haircut)
        self.assertTrue(math.isclose(self.parsed["buy_price"], implied, rel_tol=0.02),
                        f"buy price {self.parsed['buy_price']} != base x (1 - {haircut}) = {implied:.4f}")
        bear_downside = expected_values()["Bear"]["per_share"] / self.parsed["buy_price"] - 1
        self.assertLess(bear_downside, 0, "Bear value should be below the buy price in this fixture")

    def test_terminal_economics_and_evidence_labels(self):
        self.assertRegex(self.text, r"(?i)terminal NOPAT")
        self.assertRegex(self.text, r"(?i)incremental ROIC")
        self.assertIn("Verified Fact (Hypothetical", self.text)
        self.assertIn("Modeling Assumption (Hypothetical", self.text)
        self.assertIn("Unavailable Information", self.text)
        self.assertRegex(self.text, r"(?i)simulated|one model|not independent")
        self.assertRegex(self.text, r"(?i)not a guaranteed floor|does not cap losses")

    def test_valuation_fields_not_labeled_analyst_estimate(self):
        self.assertTrue(check_valuation_labeling(self.text),
                        "valuation summary must be labeled Modeling Assumption / Derived Valuation, not Analyst Estimate")
        self.assertNotIn("Analyst Estimate (Hypothetical)", self.text,
                         "model-derived values must not be attributed as Analyst Estimates")

    def test_quick_price_consistency_same_fixture(self):
        """Full and Quick outputs on identical inputs must make the same decision."""
        if not QUICK_ZH.is_file():
            self.skipTest("quick output missing")
        quick = parse_quick(QUICK_ZH.read_text(encoding="utf-8"))
        self.assertTrue(math.isclose(quick["base"], self.parsed["base"], rel_tol=0.01),
                        "Quick and Full must report materially identical Base values")
        self.assertTrue(math.isclose(quick["haircut"], self.parsed["haircut"], abs_tol=0.001),
                        f"mode-dependent haircut: quick {quick['haircut']:.0%} vs full {self.parsed['haircut']:.0%}")
        self.assertTrue(math.isclose(quick["buy_price"], self.parsed["buy_price"], rel_tol=0.01),
                        "buy prices must be materially consistent across modes")
        if STANDALONE.is_file():
            standalone = parse_quick(STANDALONE.read_text(encoding="utf-8"))
            self.assertTrue(math.isclose(standalone["haircut"], self.parsed["haircut"], abs_tol=0.001),
                            "standalone Prompt must reach the same haircut as the Skill")


@unittest.skipUnless(QUICK_ZH.is_file(), "behavioral outputs not generated")
class QuickPriceTests(unittest.TestCase):
    def test_quick_zh_format_and_oracle(self):
        text = QUICK_ZH.read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("1. **"))
        self.assertTrue(lines[1].startswith("2. **"))
        self.assertRegex("".join(lines), r"[\u4e00-\u9fff]")
        parsed = parse_quick(text)
        base = expected_values()["Base"]["per_share"]
        self.assertTrue(math.isclose(parsed["base"], base, rel_tol=0.01))
        self.assertTrue(math.isclose(parsed["buy_price"], parsed["base"] * (1 - parsed["haircut"]), rel_tol=0.02))

    def test_standalone_prompt_quick_en(self):
        if not STANDALONE.is_file():
            self.skipTest("standalone output not generated")
        text = STANDALONE.read_text(encoding="utf-8")
        self.assertTrue(text.splitlines()[0].startswith("1. **Margin-of-Safety Buy Price:**"))
        parsed = parse_quick(text)
        base = expected_values()["Base"]["per_share"]
        self.assertTrue(math.isclose(parsed["base"], base, rel_tol=0.01))
        self.assertTrue(math.isclose(parsed["buy_price"], parsed["base"] * (1 - parsed["haircut"]), rel_tol=0.02))


@unittest.skipUnless(MISSING.is_file(), "behavioral outputs not generated")
class MissingDataTests(unittest.TestCase):
    def test_refusal_is_concise_and_fabrication_free(self):
        text = MISSING.read_text(encoding="utf-8")
        self.assertLessEqual(len([l for l in text.splitlines() if l.strip()]), 3)
        self.assertRegex(text, r"(?i)cannot|unable|insufficient")
        self.assertNotRegex(text, r"(?i)(price|value)[^\n]*\d+\.\d{2}")
        self.assertNotIn("Northstar", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
