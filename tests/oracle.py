"""Independent valuation oracle for the controlled fixtures.

This module is the test oracle. It is NEVER supplied to a model under
behavioral evaluation: behavioral agents receive only the fixture file
(inputs) and the Skill/Prompt (instructions). Values here are computed
independently from the driver inputs so that a model's report can be
compared by tolerance instead of matching leaked answer strings.

No network access, no third-party packages.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

TAX = 0.25
CASH = 120.0
DEBT = 200.0
SHARES = 100.0  # millions
FY2025_REVENUE = 1000.0


@dataclass(frozen=True)
class Scenario:
    name: str
    growth: tuple[float, ...]      # revenue growth, years 1-5
    margins: tuple[float, ...]     # EBIT margin, years 1-5
    roic: float                    # explicit and terminal ROIC
    terminal_growth: float
    cost_of_equity: float
    pretax_debt_cost: float
    equity_weight: float = 0.80

    @property
    def wacc(self) -> float:
        after_tax_debt = self.pretax_debt_cost * (1 - TAX)
        return self.equity_weight * self.cost_of_equity + (1 - self.equity_weight) * after_tax_debt


SCENARIOS = {
    "Bear": Scenario("Bear", (-0.05, 0.0, 0.01, 0.02, 0.02), (0.12,) * 5, 0.075, 0.015, 0.12, 0.09333333),
    "Base": Scenario("Base", (0.08, 0.07, 0.06, 0.05, 0.05), (0.150, 0.152, 0.154, 0.155, 0.155), 0.125, 0.025, 0.10, 0.06666667),
    "Bull": Scenario("Bull", (0.12, 0.12, 0.10, 0.09, 0.08), (0.16, 0.165, 0.17, 0.175, 0.18), 0.15, 0.03, 0.09, 0.05333333),
}


def forecast(s: Scenario) -> dict:
    """Derive the explicit FCFF path and terminal-year economics from drivers."""
    revenue, nopat_path, fcff_path = FY2025_REVENUE, [], []
    for g, margin in zip(s.growth, s.margins):
        revenue *= 1 + g
        nopat = revenue * margin * (1 - TAX)
        reinvestment = g / s.roic
        nopat_path.append(nopat)
        fcff_path.append(nopat * (1 - reinvestment))
    terminal_nopat = nopat_path[-1] * (1 + s.terminal_growth)
    terminal_reinvestment = s.terminal_growth / s.roic
    terminal_fcff = terminal_nopat * (1 - terminal_reinvestment)
    return {
        "nopat": nopat_path,
        "fcff": fcff_path,
        "terminal_nopat": terminal_nopat,
        "terminal_reinvestment": terminal_reinvestment,
        "terminal_fcff": terminal_fcff,
    }


def dcf_per_share(s: Scenario) -> dict:
    """Full driver-based DCF with simplified EV-to-equity bridge."""
    if s.wacc <= s.terminal_growth:
        raise ValueError(f"{s.name}: WACC {s.wacc:.4f} must exceed terminal growth {s.terminal_growth}")
    if SHARES <= 0:
        raise ValueError("Diluted share count must be positive")
    f = forecast(s)
    wacc = s.wacc
    pv_explicit = sum(v / (1 + wacc) ** t for t, v in enumerate(f["fcff"], 1))
    tv = f["terminal_fcff"] / (wacc - s.terminal_growth)
    pv_tv = tv / (1 + wacc) ** 5
    ev = pv_explicit + pv_tv
    equity = ev - DEBT + CASH
    return {
        "scenario": s.name,
        "wacc": wacc,
        "pv_explicit": pv_explicit,
        "pv_tv": pv_tv,
        "ev": ev,
        "equity": equity,
        "per_share": equity / SHARES,
        "tv_share_of_ev": pv_tv / ev,
    }


def expected_values() -> dict[str, dict]:
    return {name: dcf_per_share(s) for name, s in SCENARIOS.items()}


def terminal_continuity_error(s: Scenario) -> float:
    """Relative divergence between Y5 NOPAT carried forward and implied terminal NOPAT.

    In a consistent model this is exactly 0: terminal NOPAT is defined as
    Y5 NOPAT x (1 + g). A model that silently normalizes profitability up or
    down produces a nonzero error. Tests assert on this function directly and
    on reports derived from the fixture.
    """
    f = forecast(s)
    implied = f["nopat"][-1] * (1 + s.terminal_growth)
    return (f["terminal_nopat"] - implied) / implied


def detect_terminal_discontinuity(y5_nopat: float, terminal_growth: float,
                                  terminal_fcff: float, terminal_roic: float,
                                  tolerance: float = 0.01) -> bool:
    """Return True when terminal economics break from the explicit forecast.

    Given terminal FCFF and reinvestment r = g/ROIC, the implied terminal
    NOPAT is FCFF / (1 - r). If that diverges from Y5 NOPAT x (1 + g) by more
    than `tolerance` (relative), the transition is an unexplained
    normalization and must be justified in the research.
    """
    r = terminal_growth / terminal_roic
    implied_terminal_nopat = terminal_fcff / (1 - r)
    expected_terminal_nopat = y5_nopat * (1 + terminal_growth)
    return abs(implied_terminal_nopat - expected_terminal_nopat) / expected_terminal_nopat > tolerance


def mos_buy_price(base_value: float, haircut: float) -> float:
    """Margin-of-safety buy price: Base intrinsic value x (1 - haircut)."""
    if not 0 < haircut < 1:
        raise ValueError("Haircut must be between 0 and 1")
    return base_value * (1 - haircut)


def fcfe_equity_value(flows, cost_of_equity, growth):
    """FCFE values equity directly; no net-debt bridge applies."""
    if cost_of_equity <= growth:
        raise ValueError("Cost of equity must exceed terminal growth")
    tv = flows[-1] * (1 + growth) / (cost_of_equity - growth)
    return sum(v / (1 + cost_of_equity) ** t for t, v in enumerate(flows, 1)) + tv / (1 + cost_of_equity) ** len(flows)


def check_fcff_fcfe_consistency(cash_flow_type: str, discount_rate_type: str) -> bool:
    """FCFF pairs with WACC; FCFE pairs with cost of equity. Anything else is an error."""
    valid = {("FCFF", "WACC"), ("FCFE", "cost_of_equity")}
    return (cash_flow_type, discount_rate_type) in valid


def check_equity_bridge(components: dict) -> list[str]:
    """Detect common enterprise-to-equity bridge errors.

    components: mapping of item name -> signed value as applied in the bridge
    (e.g. {"debt": -200, "cash": +120}). Flags double counting and sign errors.
    """
    errors = []
    seen = set()
    for item, value in components.items():
        canonical = item.lower().replace(" ", "_")
        if canonical in seen:
            errors.append(f"double counted: {item}")
        seen.add(canonical)
        if canonical.startswith(("debt", "minority", "preferred", "pension", "lease")) and value > 0:
            errors.append(f"sign error: {item} must reduce equity value")
        if canonical.startswith(("cash", "non_operating_asset", "investment")) and value < 0:
            errors.append(f"sign error: {item} must increase equity value")
    return errors


def check_sbc_treatment(sbc_added_back: bool, dilution_ignored: bool) -> bool:
    """SBC double count: adding SBC back to cash flow while ignoring dilution."""
    return not (sbc_added_back and dilution_ignored)


def check_currency_consistency(financials_ccy: str, price_ccy: str, share_class: str, price_share_class: str) -> list[str]:
    errors = []
    if financials_ccy != price_ccy:
        errors.append(f"currency mismatch: financials {financials_ccy} vs price {price_ccy}")
    if share_class != price_share_class:
        errors.append(f"share-class mismatch: {share_class} vs {price_share_class}")
    return errors


if __name__ == "__main__":
    for name, result in expected_values().items():
        print(f"{name}: WACC={result['wacc']:.4f} per_share={result['per_share']:.6f} "
              f"TV%={result['tv_share_of_ev']:.4f}")
