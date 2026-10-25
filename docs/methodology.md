# Research Methodology

## 1. Evidence Standard

### Source Hierarchy

1. SEC and other regulatory filings
2. Official financial statements
3. Company investor relations and earnings calls
4. Reliable industry and market data
5. Reputable secondary research

Higher-quality sources take precedence when figures conflict, but differences in accounting basis, period, currency, or definition must be reconciled before calling one source wrong. Secondary quotations and estimates should be checked against the original when material.

### Claim Labels

- **Verified Fact:** directly supported by an identified source and period.
- **Analyst Estimate:** an external forecast attributed to its provider and date.
- **Modeling Assumption:** an input chosen for this analysis and disclosed as such.- **Speculation:** an unverified possibility; never a factual foundation.
- **Unavailable Information:** a material item not found or not disclosed.

**Classification discipline:** `Analyst Estimate` applies only to an externally attributed forecast with a named provider and date. Model-derived intrinsic values, scenario values, sensitivity outputs, and margin-of-safety prices are `Modeling Assumption / Derived Valuation`, never Analyst Estimates. Ratios computed from filings are derived metrics from Verified Facts.

Every material time series needs units, currency, reporting period, and accounting basis. Every market comparison needs a price reference date. A report date is not a substitute for a price date.

## 2. Research Questions

A complete study answers three different questions:

1. Is the business economically attractive and durable?
2. What is the security worth under defensible scenarios?
3. Does the current price provide adequate expected return and downside protection?

It also identifies what the market appears to expect, which assumptions create an expectations gap, and which observable evidence would invalidate the thesis.

## 3. Financial Quality

Analyze growth by segment and driver, margins, returns on invested capital, accruals, cash conversion, reinvestment, leverage, and dilution. Use consistent definitions:

- `NOPAT = EBIT × (1 - normalized cash tax rate)`
- `ROIC = NOPAT / average invested capital`
- `FCFF = NOPAT + D&A - CapEx - increase in net working capital`

Do not confuse operating cash flow with free cash flow, enterprise free cash flow with equity free cash flow, or buybacks with per-share value creation. Evaluate buybacks against intrinsic value and dilution. Treat SBC as an economic cost and reconcile any cash-flow adjustment with share dilution.

## 4. Valuation

### Method Selection

| Business type | Preferred starting point | Main caution |
|---|---|---|
| Stable operating company | FCFF DCF and suitable multiples | Terminal assumptions and reinvestment consistency |
| Bank or insurer | FCFE, dividend/residual income, P/B and sustainable ROE | Industrial WACC/EV bridges are usually unsuitable |
| Cyclical or commodity company | Normalized mid-cycle cash flow and balance sheet | Peak earnings are not a perpetual base |
| High-growth company | Driver-based DCF with margin/reinvestment fade and multiples | Dilution and expectations embedded in price |
| Unprofitable company | Unit economics, funding path, conditional scenarios | Decline precise value without a credible cash-flow path |
| Conglomerate | Sum-of-the-parts plus consolidated cross-check | Segment allocations and holding-company discounts |

### FCFF Model

For an explicit `N`-year forecast:

```text
FCFF = EBIT × (1 - normalized cash tax rate) + D&A - CapEx - increase in NWC
TV = FCFF_N × (1 + g) / (WACC - g)
EV = Σ[FCFF_t / (1 + WACC)^t] + TV / (1 + WACC)^N
Equity value = EV - debt + cash + non-operating assets
               - debt-like claims - preferred stock - noncontrolling interest
Intrinsic value per share = common equity value / diluted shares
```

`WACC` must exceed `g`. Explain the cash-flow base, tax rate, reinvestment, cost of capital, terminal growth, and forecast horizon. If mid-year discounting is used, apply it consistently. Review terminal value as a share of EV and inspect implied terminal multiples.

### Reinvestment, ROIC, and Terminal-Year Normalization

Distinguish four quantities: revenue growth, NOPAT growth, average ROIC, and incremental ROIC. Margins change over time, so revenue growth is not profit growth.

For explicit forecast years, prefer an incremental-investment model:

```text
Reinvestment_t = (NOPAT_t - NOPAT_(t-1)) / incremental ROIC
FCFF_t = NOPAT_t - Reinvestment_t
```

A sales-to-capital variant is acceptable when disclosed. Do not let declining NOPAT automatically release invested capital; without divestment evidence, floor reinvestment at zero. Reconcile forecast reinvestment with historical capex, depreciation, working-capital change, and cash conversion where feasible, and explain material gaps.

The terminal year is a steady state where revenue growth equals NOPAT growth, so the stable-state reinvestment rate `terminal growth / terminal ROIC` applies there and only there:

```text
Terminal NOPAT = final explicit-year NOPAT × (1 + terminal growth)
Terminal reinvestment rate = terminal growth / terminal ROIC
Terminal FCFF = Terminal NOPAT × (1 - terminal reinvestment rate)
```

Never subtract this reinvestment twice. If implied terminal NOPAT diverges materially from the final explicit-year NOPAT carried forward, the model contains an unexplained normalization: either justify the transition (for example a stated mature-margin convergence) or revise the assumptions. Silent terminal-year profitability declines or improvements are modeling errors, not conservatism.

### FCFE Model

FCFE belongs to equity holders and is discounted at the cost of equity. It produces equity value directly. Do not subtract net debt again and do not use WACC. Define borrowing and cash-flow treatment consistently.

### Multiples

Use P/E, P/S, P/B, and EV/EBITDA only when economically meaningful. Align equity metrics with equity value and enterprise metrics with enterprise value. Align fiscal periods, currencies, share classes, growth, profitability, and accounting policies. A lower multiple is not automatically better value.

### Scenario and Sensitivity Design

Bear/Base/Bull cases must change underlying operating drivers, not just terminal multiples. A WACC × terminal-growth table accompanies FCFF models; invalid cells where `WACC <= g` are `N/M`. Reverse DCF can reveal the growth, margins, or returns implied by the current price.

### Margin of Safety

```text
Margin-of-safety buy price = Base intrinsic value per share × (1 - required margin of safety)
```

The haircut is a research judgment, not a universal constant. Assess nine factors as Low / Medium / High concern with evidence:

1. Cash-flow forecast uncertainty
2. Terminal-value dependence (PV of TV as a share of EV)
3. Financial leverage and refinancing risk
4. Industry cyclicality
5. Business-model and moat durability
6. Customer or supplier concentration
7. Management and organizational uncertainty
8. Bear/Base/Bull valuation dispersion
9. Quality, freshness, and completeness of evidence

Select a band rather than a false-precision formula: roughly 10–20% for predominantly Low concerns, 20–30% for Medium, 30–40% for High. When several factors are High and evidence is poor, or material inputs are missing, withhold the precise buy price.

Anchors keep the band reproducible: terminal dependence >75% of EV is High (60–75% Medium); net debt/EBITDA >3.5x High (2.0–3.5x Medium); largest customer >20% of revenue High (10–20% Medium); scenario dispersion (Bull−Bear)/Base >100% High (50–100% Medium); single-source, stale, or materially incomplete evidence is High. Count High factors: 3+ → 30–40% band; 1–2 → 20–30%; 0 → 10–20%. Use the band reference value (35/25/15%) unless a specific within-band reason is documented.

**Mode consistency:** the assessment depends on inputs and evidence, not on output length. Identical inputs must yield identical factor ratings, band, and haircut in Full Research and Quick Price. Use the band reference value (15% / 25% / 35%) unless the factor table documents a specific reason to move within the band. Any divergence between modes requires an identifiable difference in assumptions or evidence.

**Haircut versus evidence gate:** a haircut is an uncertainty adjustment, not a substitute for missing evidence. Withhold the precise buy price when critical inputs are missing or unsupported, or when the Bear/Base/Bull range cannot be defended. Use the 35% band when inputs are complete and scenarios are defensible but uncertainty is high. A fully specified hypothetical fixture may produce an explicitly conditional valuation labelled Modeling Assumption / Derived Valuation; incomplete real-world research cannot bypass the gate by choosing a larger haircut.

Report three distinct quantities and never merge them:

- **Safety margin to Base value:** discount of the buy price to Base intrinsic value.
- **Bear-scenario downside:** percentage loss from the buy price to Bear value.
- **Protection against permanent impairment:** conditional on the thesis, never guaranteed. The buy price is a decision threshold, not a floor and not a maximum-loss cap.

## 5. Bear Case and Invalidation

Each material risk needs a transmission path: event → operating effect → financial effect → valuation effect. Add observable triggers and thesis-invalidating conditions. Separate:

- temporary price volatility;
- reversible operational weakness;
- permanent earnings-power impairment;
- financing or solvency threats;
- thesis failure caused by incorrect assumptions.

The bear case must attack the strongest bullish evidence and state what would disprove the bear view as well.

## 6. Execution Without False Personalization

Without investor-specific information, describe tranches as percentages of an **intended position**, not total assets. Tie additions to valuation or evidence conditions. Position size depends on uncertainty, downside, liquidity, correlation, and loss capacity; no universal percentage is appropriate.

A price decline alone is not thesis invalidation, and a mechanical stop-loss does not eliminate gap or fundamental risk. Reassess when predefined operating, financial, governance, or valuation conditions change.

## 7. Long-Term Ownership and 7S

The Buffett-style review tests moat durability, pricing power, cash generation, reinvestment runway, and capital allocation. The ten-year test asks whether economics can compound; the five-year market-closure test removes reliance on multiple expansion.

McKinsey 7S uses Strategy, Structure, Systems, Shared Values, Style, Staff, and Skills to evaluate execution. Public sources are incomplete, so verified evidence and inference must be separated and confidence reduced when visibility is weak.

## 8. Decision Discipline

The final rating must be consistent with the evidence gates and dated price. Do not average Agent ratings. Resolve disagreements using source quality, causal relevance, valuation sensitivity, and falsifiability. Choose Watch Only or Not Rated instead of manufacturing certainty.
