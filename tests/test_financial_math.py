"""Deterministic numerical tests: DCF oracle, terminal consistency, edge cases.

These tests validate mathematics and methodology rules only. They do not
prove LLM runtime behavior; behavioral artifact checks live in
test_behavioral_outputs.py.
"""

import math
import unittest

from oracle import (
    SCENARIOS, dcf_per_share, detect_terminal_discontinuity, expected_values,
    fcfe_equity_value, forecast, check_currency_consistency,
    check_equity_bridge, check_fcff_fcfe_consistency, check_sbc_treatment,
    mos_buy_price, terminal_continuity_error,
)


class DriverModelTests(unittest.TestCase):
    def test_all_scenario_waccs_reconcile(self):
        # 80% equity + 20% after-tax debt at 25% tax
        self.assertAlmostEqual(SCENARIOS["Bear"].wacc, 0.11, places=6)
        self.assertAlmostEqual(SCENARIOS["Base"].wacc, 0.09, places=6)
        self.assertAlmostEqual(SCENARIOS["Bull"].wacc, 0.08, places=6)

    def test_explicit_fcff_is_driver_derived(self):
        # Base Y1: revenue 1080, EBIT 15.0%, NOPAT 121.5, reinvestment 8%/12.5%=64%
        f = forecast(SCENARIOS["Base"])
        self.assertAlmostEqual(f["nopat"][0], 121.5, places=6)
        self.assertAlmostEqual(f["fcff"][0], 121.5 * 0.36, places=6)

    def test_negative_growth_releases_capital(self):
        # Bear Y1: shrinking business has FCFF above NOPAT (negative reinvestment)
        f = forecast(SCENARIOS["Bear"])
        self.assertGreater(f["fcff"][0], f["nopat"][0])

    def test_scenario_values_are_stable(self):
        # Regression guard: driver-based values must not drift silently.
        expected = expected_values()
        self.assertAlmostEqual(expected["Bear"]["per_share"], 7.098724, places=4)
        self.assertAlmostEqual(expected["Base"]["per_share"], 14.777213, places=4)
        self.assertAlmostEqual(expected["Bull"]["per_share"], 26.052694, places=4)

    def test_bear_less_than_base_less_than_bull(self):
        e = expected_values()
        self.assertLess(e["Bear"]["per_share"], e["Base"]["per_share"])
        self.assertLess(e["Base"]["per_share"], e["Bull"]["per_share"])


class TerminalConsistencyTests(unittest.TestCase):
    def test_fixture_scenarios_have_zero_discontinuity(self):
        for s in SCENARIOS.values():
            self.assertAlmostEqual(terminal_continuity_error(s), 0.0, places=12)

    def test_reproduces_v1_0_discontinuity(self):
        # V1.0 Base: Y5 NOPAT ~157.0, terminal FCFF 112*1.025=114.8 at
        # reinvestment 20% implied terminal NOPAT 143.5 — an unexplained
        # ~10.9% profitability drop. The detector must flag it.
        y5_nopat = 1350.4949 * 0.155 * 0.75  # V1.0 Base Y5 drivers
        old_terminal_fcff = 112 * 1.025
        self.assertTrue(
            detect_terminal_discontinuity(y5_nopat, 0.025, old_terminal_fcff, 0.125)
        )
        # Magnitude of the V1.0 error, documented for the changelog
        implied = old_terminal_fcff / 0.8
        expected = y5_nopat * 1.025
        self.assertGreater(abs(implied - expected) / expected, 0.10)

    def test_accepts_consistent_terminal(self):
        f = forecast(SCENARIOS["Base"])
        self.assertFalse(
            detect_terminal_discontinuity(
                f["nopat"][-1], 0.025, f["terminal_fcff"], 0.125
            )
        )

    def test_terminal_reinvestment_not_double_counted(self):
        # terminal FCFF = NOPAT*(1+g)*(1-r); applying (1-r) again must fail continuity
        f = forecast(SCENARIOS["Base"])
        double_counted = f["terminal_fcff"] * (1 - 0.025 / 0.125)
        self.assertTrue(
            detect_terminal_discontinuity(f["nopat"][-1], 0.025, double_counted, 0.125)
        )


class EdgeCaseTests(unittest.TestCase):
    def test_wacc_leq_growth_rejected(self):
        bad = SCENARIOS["Base"]
        from oracle import Scenario
        invalid = Scenario("X", bad.growth, bad.margins, bad.roic, 0.10, 0.10, 0.06666667)
        with self.assertRaises(ValueError):
            dcf_per_share(invalid)

    def test_fcfe_rejects_growth_above_discount_rate(self):
        with self.assertRaises(ValueError):
            fcfe_equity_value([10, 11], 0.08, 0.09)

    def test_fcff_fcfe_pairing(self):
        self.assertTrue(check_fcff_fcfe_consistency("FCFF", "WACC"))
        self.assertTrue(check_fcff_fcfe_consistency("FCFE", "cost_of_equity"))
        self.assertFalse(check_fcff_fcfe_consistency("FCFF", "cost_of_equity"))
        self.assertFalse(check_fcff_fcfe_consistency("FCFE", "WACC"))

    def test_equity_bridge_errors_detected(self):
        self.assertEqual(check_equity_bridge({"debt": -200, "cash": 120}), [])
        self.assertTrue(check_equity_bridge({"debt": 200}))          # sign error
        self.assertTrue(check_equity_bridge({"cash": -120}))         # sign error
        self.assertTrue(check_equity_bridge({"debt": -200, "Debt": -200}))  # double count

    def test_sbc_double_counting_detected(self):
        self.assertFalse(check_sbc_treatment(sbc_added_back=True, dilution_ignored=True))
        self.assertTrue(check_sbc_treatment(sbc_added_back=False, dilution_ignored=False))
        self.assertTrue(check_sbc_treatment(sbc_added_back=True, dilution_ignored=False))

    def test_currency_and_share_class_mismatch(self):
        self.assertEqual(check_currency_consistency("USD", "USD", "A", "A"), [])
        self.assertTrue(check_currency_consistency("USD", "CNY", "A", "A"))
        self.assertTrue(check_currency_consistency("USD", "USD", "A", "ADR"))

    def test_mos_arithmetic(self):
        self.assertAlmostEqual(mos_buy_price(14.777213, 0.30), 10.344049, places=5)
        with self.assertRaises(ValueError):
            mos_buy_price(100, 0)
        with self.assertRaises(ValueError):
            mos_buy_price(100, 1.2)


class NegativeDetectionTests(unittest.TestCase):
    """The oracle comparison itself must catch wrong arithmetic."""

    def test_wrong_value_fails_tolerance_check(self):
        correct = expected_values()["Base"]["per_share"]
        wrong = correct * 1.05  # 5% overstatement
        self.assertFalse(math.isclose(correct, wrong, rel_tol=0.005))

    def test_transposed_digits_detected(self):
        correct = expected_values()["Base"]["per_share"]
        wrong = 14.77 + 0.5
        self.assertGreater(abs(correct - wrong), 0.01)


if __name__ == "__main__":
    unittest.main(verbosity=2)
