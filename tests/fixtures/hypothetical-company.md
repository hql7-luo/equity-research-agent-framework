# CONTROLLED HYPOTHETICAL FIXTURE — NOT A REAL COMPANY OR REAL INVESTMENT DATA

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
- No regulatory or geopolitical crisis is defined in the fixture.

## Fictional Management and Organizational Evidence

- The fictional annual report states a strategy focused on profitable recurring-revenue growth.
- Management has reduced debt from 210 to 200 while continuing product investment.
- The fictional incentive plan uses three-year ROIC and recurring-revenue targets.
- The company reports a centralized product organization and regional sales teams.
- No independently verified employee-sentiment or internal-culture evidence is supplied.
- International expansion is early and execution capability is unproven.

## Modeling Assumptions for Controlled DCF Tests

All forecast cash flows are FCFF in USD millions. Use year-end discounting and a five-year horizon.

| Scenario | FCFF Years 1–5 | WACC | Terminal growth |
|---|---|---:|---:|
| Bear | 75, 78, 80, 82, 84 | 11.0% | 1.5% |
| Base | 92, 97, 102, 107, 112 | 9.0% | 2.5% |
| Bull | 100, 110, 120, 130, 140 | 8.0% | 3.0% |

The fixed FCFF vectors are authoritative for the controlled arithmetic and already reflect the following operating and reinvestment assumptions; do not derive a second, different FCFF forecast from rounded drivers:

| Operating driver | Bear | Base | Bull |
|---|---|---|---|
| Revenue growth, Years 1–5 | -5%, 0%, 1%, 2%, 2% | 8%, 7%, 6%, 5%, 5% | 12%, 12%, 10%, 9%, 8% |
| EBIT margin, Years 1–5 | 12.0%, 11.5%, 11.5%, 12.0%, 12.0% | 15.0%, 15.2%, 15.5%, 15.5%, 15.5% | 16.0%, 16.5%, 17.0%, 17.5%, 18.0% |
| Normalized cash tax rate | 25% | 25% | 25% |
| Terminal ROIC | 7.5% | 12.5% | 15.0% |
| Terminal reinvestment rate = g / ROIC | 20% | 20% | 20% |

WACC uses an 80% equity / 20% debt target structure in every scenario. The scenario inputs are:

| WACC component | Bear | Base | Bull |
|---|---:|---:|---:|
| Cost of equity | 12.0% | 10.0% | 9.0% |
| Pre-tax cost of debt | 9.333333% | 6.666667% | 5.333333% |
| After-tax cost of debt at 25% tax | 7.0% | 5.0% | 4.0% |
| Result: 80% × cost of equity + 20% × after-tax debt cost | 11.0% | 9.0% | 8.0% |

The terminal growth rates remain below the fixture's 4% long-term industry growth assumption. Terminal FCFF is after the reinvestment rates above, so growth is not treated as costless.

For every scenario, use cash 120, debt 200, no other bridge items, and 100 million diluted shares. Use a 20% margin-of-safety haircut on Base intrinsic value for the controlled Quick Price test. These assumptions are intentionally fixed so that results can be independently recalculated.

Expected mathematical results, rounded to six decimals:

- Bear value per share: 7.458422
- Base value per share: 14.612820
- Bull value per share: 23.557972
- Base margin-of-safety buy price at 20%: 11.690256

These expected values are test oracles, not real-world estimates or recommendations.

## Expected Behavioral Checks

- Full Research Mode must contain all nine sections, seven Agents, the Manager, scenario values, sensitivity, disagreements, 7S limits, and execution-method disclosure.
- Quick Price Mode requested in Simplified Chinese must return exactly two numbered lines and use the controlled Base result.
- The report must not claim that this fictional fixture is externally verified or that separate independent models were used.
