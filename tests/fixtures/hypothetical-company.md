# CONTROLLED HYPOTHETICAL FIXTURE — NOT A REAL COMPANY OR REAL INVESTMENT DATA

**Anti-contamination notice:** This file contains inputs only. It deliberately contains **no** expected valuation results, no target prices, and no margin-of-safety answer. Any model evaluated with this fixture must derive all valuation outputs itself. Expected results live in `tests/oracle.py`, which is never supplied to the model under evaluation.

## Scope

- Company: Northstar Example Corp.
- Ticker/exchange: TEST / Hypothetical Exchange
- Research date: 2026-01-20
- Reporting period: FY2025 ended 2025-12-31; fictional filing supplied 2026-01-15
- Market price: USD 10.50 per share at the 2026-01-20 close
- Currency and units: USD millions except per-share data and percentages
- Evidence labels below use the framework's five categories. **Verified Fact (Hypothetical Fixture)** means verified only against this controlled fictional source, not real-world verified. Forecasts are **Modeling Assumption (Hypothetical)**; absent items are **Unavailable Information**. No external Analyst Estimate is used.
- Execution constraint: use only this fixture; do not browse or add external facts

## Fictional Historical Financials

| Metric | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 850 | 925 | 1,000 |
| EBIT | 110 | 130 | 150 |
| D&A | 28 | 29 | 30 |
| Operating cash flow | 95 | 110 | 125 |
| Capital expenditure | 40 | 42 | 45 |
| Increase in net working capital | 8 | 9 | 10 |
| Cash and equivalents | 100 | 110 | 120 |
| Total debt | 210 | 205 | 200 |
| Diluted shares (millions) | 102 | 101 | 100 |
| Stock-based compensation | 8 | 9 | 10 |

The FY2025 normalized cash tax rate is 25%. SBC is already expensed in EBIT and must not be added back. FY2025 average invested capital is 600. There are no preferred shares, noncontrolling interests, non-operating assets, or additional debt-like claims in this simplified fixture.

## Fictional Business and Industry Evidence

- The company sells recurring industrial workflow software and related services.
- FY2025 recurring revenue is 82% of total revenue; services are 18%.
- The largest customer represents 22% of revenue; the top five represent 46%.
- The fictional industry TAM is USD 5.0 billion with a 4% expected long-term growth rate.
- Two scaled competitors are gaining share in lower-priced segments.
- High switching costs support retention, but a new open-standard product could reduce them.
- Higher interest rates can delay customer purchasing and increase the discount rate.
- The business is moderately cyclical: customer budgets track industrial capex cycles.
- No regulatory or geopolitical crisis is defined in the fixture.

## Fictional Management and Organizational Evidence

- The fictional annual report states a strategy focused on profitable recurring-revenue growth.
- Management has reduced debt from 210 to 200 while continuing product investment.
- The fictional incentive plan uses three-year ROIC and recurring-revenue targets.
- The company reports a centralized product organization and regional sales teams.
- No independently verified employee-sentiment or internal-culture evidence is supplied.
- International expansion is early and execution capability is unproven.

## Forecast Method (Modeling Assumptions, Hypothetical)

Forecast FCFF is **driver-derived**, not an arbitrary fixed vector. For each explicit year:

```text
Revenue_t = Revenue_(t-1) × (1 + growth_t)
EBIT_t = Revenue_t × EBIT margin_t
NOPAT_t = EBIT_t × (1 - 25% cash tax rate)
Reinvestment rate_t = growth_t / ROIC
FCFF_t = NOPAT_t × (1 - Reinvestment rate_t)
```

A negative growth rate implies negative reinvestment (capital release) and therefore FCFF above NOPAT; this is intentional and economically valid for a shrinking business.

Terminal-year economics must connect to Year 5 without discontinuity:

```text
Terminal NOPAT = Year 5 NOPAT × (1 + terminal growth)
Terminal reinvestment rate = terminal growth / terminal ROIC
Terminal FCFF = Terminal NOPAT × (1 - Terminal reinvestment rate)
TV = Terminal FCFF / (WACC - terminal growth), requiring WACC > terminal growth
```

Reinvestment already includes the capex, working-capital, and other investment required to support growth; do not subtract reinvestment a second time and do not add back D&A separately in this simplified model.

## Scenario Drivers

| Driver | Bear | Base | Bull |
|---|---|---|---|
| Revenue growth, Years 1–5 | -5%, 0%, 1%, 2%, 2% | 8%, 7%, 6%, 5%, 5% | 12%, 12%, 10%, 9%, 8% |
| EBIT margin, Years 1–5 | 12.0%, 12.0%, 12.0%, 12.0%, 12.0% | 15.0%, 15.2%, 15.4%, 15.5%, 15.5% | 16.0%, 16.5%, 17.0%, 17.5%, 18.0% |
| ROIC (explicit and terminal) | 7.5% | 12.5% | 15.0% |
| Terminal growth | 1.5% | 2.5% | 3.0% |

Terminal growth rates are below the fixture's 4% long-term industry growth assumption.

## WACC Inputs

Use an 80% equity / 20% debt target structure in every scenario:

| WACC component | Bear | Base | Bull |
|---|---:|---:|---:|
| Cost of equity | 12.0% | 10.0% | 9.0% |
| Pre-tax cost of debt | 9.333333% | 6.666667% | 5.333333% |
| After-tax cost of debt at 25% tax | 7.0% | 5.0% | 4.0% |

Compute WACC as `0.80 × cost of equity + 0.20 × after-tax cost of debt`. Use year-end discounting and a five-year horizon.

## Valuation Bridge and Margin of Safety

- Equity bridge for every scenario: cash 120, debt 200, no other bridge items, 100 million diluted shares.
- The margin-of-safety haircut is **not prescribed**. Determine and justify it from the research: forecast uncertainty, terminal-value dependence, leverage, cyclicality, moat durability, customer concentration, organizational uncertainty, Bear/Base/Bull dispersion, and evidence quality. Cross-check the result against the Bear scenario and quantify downside at the proposed buy price.

## Expected Behavioral Checks

- Full Research Mode must contain all nine sections, seven Agents, the Manager, scenario values derived from the drivers above, a WACC × terminal-growth sensitivity table, a justified margin-of-safety haircut with Bear cross-check, disagreements, 7S limits, and execution-method disclosure.
- Quick Price Mode requested in Simplified Chinese must return exactly two numbered lines whose price equals the stated Base intrinsic value × (1 − stated haircut).
- The report must not claim that this fictional fixture is externally verified or that separate independent models were used.
