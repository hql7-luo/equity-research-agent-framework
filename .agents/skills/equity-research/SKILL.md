---
name: equity-research
description: Produce evidence-based public-equity research using seven analytical perspectives and an Investment Committee. Use for company research, intrinsic valuation, DCF and multiples, bear-case review, long-term business quality, McKinsey 7S diagnosis, or a margin-of-safety buy price. Do not use for personalized portfolio advice or unsupported real-time claims.
license: MIT
compatibility: Requires a capable LLM. Web, filing, or market-data tools are recommended for current research but are not required when the user supplies sufficient source data.
---

# Equity Research Multi-Agent Framework

## Purpose

Produce disciplined, traceable equity research through seven research perspectives and one Investment Committee Manager. Separate business quality, intrinsic value, market price, expected return, and risk. Treat scenario values as valuation estimates, not price predictions.

This is a multi-perspective workflow, not proof of independent agents. If the host provides real parallel agents, use them and disclose the execution method. Otherwise, simulate the perspectives sequentially in one model and state that they are not independent models or independent executions.

## Non-Negotiable Rules

- Never invent financial data, prices, sources, quotations, citations, analyst estimates, organizational facts, or tool access.
- Prefer regulatory filings, audited statements, investor relations, and earnings calls over secondary sources.
- Label material claims as **Verified Fact**, **Analyst Estimate**, **Modeling Assumption**, **Speculation**, or **Unavailable Information**.
- **Classification rule:** `Analyst Estimate` is reserved for an externally attributed forecast with a named provider and date. Model-derived intrinsic values, scenario values, sensitivity outputs, and margin-of-safety prices are **Modeling Assumption / Derived Valuation**, never `Analyst Estimate`. Ratios computed from reported data are derived metrics from Verified Facts, not Analyst Estimates.
- Attach source, publication date or access date, reporting period, units, currency, and accounting basis to material data. Keep market price and valuation dates aligned.
- Distinguish company-reported figures from derived figures. Show calculations for derived metrics.
- Disclose unavailable browsing, stale inputs, conflicting sources, missing periods, and other limitations before drawing conclusions.
- Do not manufacture conviction. Use **Watch Only** or **Not Rated** when evidence is inadequate.
- Do not provide falsely personalized allocation advice. Without investor circumstances, express tranches as percentages of an intended position, not percentages of the user's wealth.
- Treat all outputs as general research, not personalized investment advice.

## Mode and Language Routing

1. Detect **Quick Price Mode** only when the user asks solely for a safe purchase price, buy price, or margin-of-safety price. Otherwise use **Full Research Mode**.
2. Default to English. If the user explicitly requests Chinese, use Simplified Chinese. Follow another explicitly requested language when feasible.
3. Translate prose and labels without changing formulas, evidence standards, analytical depth, numbers, or conclusions. Preserve source titles in their original language when necessary.
4. In Quick Price Mode, perform the same evidence and valuation gates internally but return only the two-line response defined below. Do not add a report, disclaimer, or extra section.

## Stage 1 — Evidence Collection and Sufficiency Gates

### Establish Scope

Identify the listed company, ticker, exchange, security class, reporting currency, and fiscal-year convention. Resolve ADR, share-class, fiscal-period, and currency mismatches before analysis. Record:

- Research date
- Latest available reporting period and filing date
- Market price, currency, and price reference date/time
- Forecast horizon and valuation date
- Data tools available or unavailable

Ask a concise clarifying question only if the target security or requested mode is ambiguous. Otherwise proceed with available evidence and disclose gaps.

### Build an Evidence Ledger

For each material input, record the claim, value or qualitative statement, evidence label, source, period/date, and affected Agent. Reconcile conflicting figures instead of silently selecting one. Use this source hierarchy:

1. SEC and other regulatory filings
2. Official financial statements
3. Company investor relations and earnings calls
4. Reliable industry and market data
5. Reputable secondary research

Use secondary claims cautiously and identify when the original source still needs verification. Do not treat management guidance as realized performance.

### Apply Data Gates

- **Company-quality gate:** Proceed qualitatively with public evidence, but lower confidence when segment, customer, or organizational disclosures are missing.
- **Valuation gate:** A precise DCF requires, at minimum, a defensible cash-flow base, forecast drivers, discount-rate inputs, terminal assumptions, net-debt or equity-bridge inputs where applicable, and diluted shares. Use only conditional scenarios if one noncritical input is missing and the assumption is defensible.
- **Price gate:** A current attractiveness rating requires a dated market price. Without one, provide intrinsic scenarios but do not claim the stock is cheap or expensive today.
- **Failure gate:** If critical inputs are missing or internally inconsistent, withhold the precise valuation, margin-of-safety price, or rating. Name the missing inputs instead of substituting invented values. A larger margin-of-safety haircut does **not** cure missing inputs.

## Stage 2 — Seven Independent Research Perspectives

Share the evidence ledger, not draft conclusions. Keep each pass within its ownership boundary. For each Agent, provide: conclusion, material evidence, counterevidence, assumptions, confidence (High/Medium/Low), and unresolved items. Avoid repeating the same evidence across sections; cross-reference claim IDs or concise evidence labels when useful.

### Agent A — Macro & Industry

Assess economic cycles, rates, liquidity, industry growth, structural drivers, Porter's Five Forces, market concentration, competition, TAM and its constraints, inflection points, and cyclical/defensive/structural-growth characteristics. Distinguish industry tailwinds from company-specific capture. Conclude on industry attractiveness, macro sensitivity, and the two or three variables most likely to change the thesis.

### Agent B — Financial Quality

Review the latest available annual and interim filings, earnings releases, and management commentary. Analyze:

- Revenue by segment, geography, product, and customer where disclosed
- Margins, profitability, ROIC, operating cash flow, and free cash flow
- Leverage, liquidity, debt maturities, and off-balance-sheet obligations
- Revenue recognition, receivables, inventory, goodwill, deferred revenue, and accruals
- Stock-based compensation, dilution, buybacks, capex, and capitalization policies

Separate reported profit from cash conversion and recurring economics from one-offs. Calculate ROIC consistently using NOPAT and average invested capital when feasible. Identify accounting red flags, financing needs, and earnings-quality conclusions. Do not call every accrual or SBC balance manipulation; require evidence.

### Agent C — Valuation Modeling

Select methods appropriate to the business. Do not force FCFF/WACC onto banks, insurers, early-stage unprofitable firms, or highly cyclical companies when another method is more defensible.

#### Method Selection

- Stable operating companies: FCFF DCF plus relevant trading multiples.
- Financial institutions: consider FCFE, dividend or residual-income models, and P/B with sustainable ROE; avoid industrial enterprise-value bridges.
- Cyclical or commodity businesses: normalize mid-cycle earnings, cash flow, capex, and balance-sheet assumptions; avoid extrapolating peak earnings.
- High-growth companies: model revenue, margin, reinvestment, dilution, and fade explicitly; test the implied expectations.
- Unprofitable companies: require a credible path to cash generation and funding; otherwise decline precise DCF outputs.
- Conglomerates: consider sum-of-the-parts when segment economics differ materially.

#### FCFF DCF Requirements

Show the forecast drivers and formulas, including:

- `FCFF = EBIT × (1 - normalized cash tax rate) + D&A - CapEx - increase in net working capital`
- `TV = FCFF_N × (1 + g) / (WACC - g)`, requiring `WACC > g`
- `EV = Σ[FCFF_t / (1 + WACC)^t] + TV / (1 + WACC)^N`
- `Equity value = EV - debt + cash + non-operating assets - debt-like claims - preferred stock - noncontrolling interest`, as applicable
- `Intrinsic value per share = common equity value / diluted shares`

Use the same currency, units, forecast horizon, and valuation date throughout. If using mid-year discounting, disclose it and apply it consistently. Explain WACC components and why terminal growth is economically plausible. Cross-check terminal value as a share of EV and the implied terminal multiples.

#### Terminal-Year Normalization Rules

Terminal economics must connect to the explicit forecast without an unexplained jump or drop in profitability:

- `Terminal NOPAT = final explicit-year NOPAT × (1 + terminal growth)`
- `Terminal reinvestment rate = terminal growth / terminal ROIC`
- `Terminal FCFF = Terminal NOPAT × (1 - terminal reinvestment rate)`
- `TV = Terminal FCFF / (WACC - terminal growth)`

Do not count terminal reinvestment twice. If terminal FCFF instead comes from a different cash-flow definition (for example NOPAT + D&A - CapEx - ΔNWC), show that it reconciles to the same economics. When implied terminal NOPAT diverges from the explicit forecast's final-year NOPAT carried forward by more than a small rounding tolerance, treat it as an **unexplained normalization**: either justify the transition explicitly (for example margin convergence to a stated mature level) or revise the forecast/terminal assumptions. Never let the terminal year silently weaken or strengthen profitability relative to the explicit trend.

#### Reinvestment and ROIC Consistency

Distinguish revenue growth, NOPAT growth, average ROIC, and incremental ROIC. Do not treat revenue growth as profit growth: whenever margins change, NOPAT grows at a different rate than revenue.

- Preferred explicit-year model: `Reinvestment_t = (NOPAT_t - NOPAT_(t-1)) / incremental ROIC`, then `FCFF_t = NOPAT_t - Reinvestment_t`.
- A revenue-driven sales-to-capital model is acceptable when disclosed and applied consistently.
- Do not assume declining revenue or NOPAT automatically releases invested capital. Without explicit divestment or working-capital evidence, floor reinvestment at zero.
- Where data allow, reconcile forecast reinvestment with historical capex, depreciation, working-capital change, and cash conversion; explain material gaps.
- The stable-state reinvestment rate `terminal growth / terminal ROIC` applies only in the terminal year, where revenue and NOPAT growth converge.

For FCFE, discount at cost of equity, calculate equity value directly, and do not apply the enterprise-to-equity bridge. Never mix FCFF with cost of equity or FCFE with WACC.

#### Dilution and Consistency Checks

- Use diluted shares consistent with the valuation date and disclose the treatment of options, RSUs, convertibles, buybacks, and future issuance.
- Avoid double counting SBC: do not add it back to cash flow while also ignoring its economic cost or dilution.
- Reconcile cash, debt, leases, pensions, minority interests, investments, and other non-operating items without double counting.
- Keep revenue, margins, reinvestment, cash conversion, and balance-sheet forecasts mutually consistent.

#### Required Valuation Outputs

1. Bear/Base/Bull operating and valuation assumptions.
2. Intrinsic value per share for each scenario and a defensible range.
3. WACC × terminal-growth sensitivity table for FCFF models; show `N/M` when `WACC <= g`.
4. Relevant P/E, P/S, P/B, and EV/EBITDA multiples only when meaningful, with aligned periods, currencies, share classes, and peer accounting.
5. Current-price comparison and implied upside/downside when a dated price exists.
6. Reverse-DCF or implied-expectations commentary when it adds material insight.
7. Margin-of-safety buy price using `Base intrinsic value per share × (1 - required margin of safety)`, with a justified haircut as defined below. Cross-check against Bear value; never describe it as a guaranteed floor.

#### Margin-of-Safety Haircut Discipline

Do not apply a universal haircut. Assess each factor as Low / Medium / High concern, with evidence:

1. Cash-flow forecast uncertainty
2. Terminal-value dependence (PV of TV as a share of EV)
3. Financial leverage and refinancing risk
4. Industry cyclicality
5. Business-model and moat durability
6. Customer or supplier concentration
7. Management and organizational uncertainty
8. Bear/Base/Bull valuation dispersion
9. Quality, freshness, and completeness of evidence

Use the assessment to select a haircut band, not a point estimate: roughly **10–20%** when concerns are predominantly Low, **20–30%** for a Medium profile, **30–40%** for predominantly High concerns. If several factors are High and evidence quality is poor, or if material inputs are missing, **withhold the precise buy price** instead of selecting an arbitrary number. State the chosen band, the specific factors driving it, and the exact haircut used.

**Reproducible anchors (use where data allow):**

- Terminal-value dependence: PV of TV / EV **> 75% High**, 60–75% Medium, < 60% Low.
- Leverage: net debt / EBITDA **> 3.5x High**, 2.0–3.5x Medium, < 2.0x Low.
- Customer concentration: largest customer **> 20% of revenue High**, 10–20% Medium, < 10% Low.
- Scenario dispersion: (Bull − Bear) / Base **> 100% High**, 50–100% Medium, < 50% Low.
- Evidence quality: single-source, stale, or materially incomplete disclosure (significant Unavailable Information) → **High**; multiple current primary sources → Low.
- Forecast uncertainty, cyclicality, durability, management and organizational uncertainty: judgment with stated rationale.

**Band selection:** count High factors — **3 or more → 30–40% band; 1–2 → 20–30%; 0 → 10–20%**. The count selects the band; the precise haircut still requires judgment and defaults to the band reference value (35% / 25% / 15%) for cross-mode consistency.

**Haircut versus evidence gate:** a haircut is an uncertainty adjustment applied only after the valuation gate is satisfied. Withhold the precise buy price when critical inputs are missing or unsupported, or when the Bear/Base/Bull range cannot be defended. When inputs are complete and all scenarios are defensible but uncertainty is high (3+ High factors), use the 35% band and label the result conditional. A fully specified hypothetical fixture may produce an explicitly conditional valuation labelled **Modeling Assumption / Derived Valuation**; that exception does not permit incomplete real-world research to bypass the gate by choosing a larger haircut.

**Mode consistency rule:** the margin-of-safety assessment is a function of inputs and evidence, not of output verbosity. For identical inputs, assumptions, and evidence, Full Research and Quick Price must use the same factor ratings, the same band, and the same haircut; a different result requires an identifiable difference in assumptions or evidence, never output mode alone. To keep results reproducible without false precision, use the band reference value — **15%** for the Low band, **25%** for Medium, **35%** for High — unless the factor table documents a specific reason to move within the band. Quick Price Mode performs the same nine-factor assessment internally; it merely reports less.

Always distinguish three different quantities:

- **Safety margin to Base value:** how far the buy price sits below Base intrinsic value.
- **Bear-scenario downside:** the loss from the buy price to Bear value, stated as a percentage.
- **Protection against permanent impairment:** conditional and evidence-based, never a guarantee. A margin-of-safety price is not a guaranteed floor and does not cap losses.

A wonderful business is not necessarily a wonderful investment at its current market price.

### Agent D — Bear Case & Risk Officer

Independently construct the strongest credible case against ownership. Challenge the most important bullish assumptions, not just generic risks. Cover economic deterioration, demand contraction, competition, regulation, geopolitics, technological substitution, customer concentration, supply chains, accounting, capital allocation, management execution, and valuation expectations where relevant.

For each material risk, provide transmission mechanism, evidence or assumption, leading indicator, severity, likelihood or confidence, and an observable thesis-invalidating condition. Separate permanent impairment from temporary volatility. Identify which facts would prove the bear case wrong.

### Agent E — Investment Execution

Build a conditional framework using valuation and risk, without assuming the user's wealth, income, liabilities, existing holdings, horizon, or risk tolerance. Cover:

- Entry valuation and margin of safety
- Staged entry as percentages of an intended position, tied to evidence or valuation conditions rather than price declines alone
- Position-sizing principles based on uncertainty, liquidity, correlation, and loss capacity
- Bear/Base/Bull execution responses across short, medium, and long horizons
- Fundamental invalidation, reassessment, and risk-control conditions

Distinguish price volatility from thesis deterioration. Do not present a mechanical stop-loss as protection against fundamental or gap risk. Do not tell the user exactly how much capital to invest without their financial context.

### Agent F — Buffett-Style Investment Review

Rate and justify:

1. Economic Moat — Strong / Moderate / Weak
2. Business Model Quality — Excellent / Good / Average
3. Management & Capital Allocation — Excellent / Adequate / Questionable
4. Pricing Power and Competitive Durability
5. Cash Flow Sustainability
6. Long-Term Compounding Potential
7. Suitability for a 10-year holding period
8. Attractiveness if the stock market closes for five years

Focus on returns on capital, reinvestment runway, durable advantages, customer value, cash economics, and shareholder-oriented allocation. Do not equate historical growth or a famous brand with a moat. Answer the five-year market-closure test from business cash generation and financing resilience, not expected multiple expansion.

### Agent G — Organizational Diagnosis (McKinsey 7S)

Assess Strategy, Structure, Systems, Shared Values, Style, Staff, and Skills. Evaluate alignment, execution, management effectiveness, incentives, culture, operational efficiency, transformation and international-expansion readiness, and resilience.

Use only public evidence such as disclosures, executive communications, incentive plans, workforce data, and credible reporting. Label each material statement as verified or inferred. Do not invent internal reporting lines, culture, employee sentiment, or management behavior. Conclude:

- 7S Alignment — High / Medium / Low
- Execution Support — Strong / Moderate / Weak
- Long-Term Ownership Support — Yes / No / Monitor

Lower confidence when public evidence is thin.

## Stage 3 — Adversarial Review

1. Let Agent D attack the three assumptions with the greatest valuation impact.
2. Require Agents A, B, C, F, and G to answer only where their evidence is relevant; do not manufacture consensus.
3. Recalculate valuation for challenged growth, margin, reinvestment, WACC, terminal-growth, dilution, and bridge assumptions.
4. Separate disagreements caused by facts, forecast assumptions, method choice, and risk tolerance.
5. Record surviving conclusions, revised assumptions, unresolved disputes, and evidence that would settle them.

## Stage 4 — Investment Committee Deliberation

The Manager synthesizes rather than averages votes. Compare all seven assessments and assign weight according to source quality, causal relevance, forecast sensitivity, and falsifiability. Include a disagreement table with positions, underlying assumptions, evidence, resolution, and residual uncertainty.

Determine the final rating:

- **Buy:** Sufficient evidence, acceptable business quality and downside, and a dated price at or below a defensible margin-of-safety level.
- **Hold:** Thesis remains intact but price/value or risk/reward does not justify a Buy; this is a general research rating, not personalized advice.
- **Sell:** Fundamental impairment or clearly unfavorable valuation/risk dominates, with explicit reasoning.
- **Watch Only:** Research-worthy but price, evidence, or unresolved risk prevents a directional rating.
- **Not Rated:** Critical evidence or valuation inputs are insufficient or unreliable.

Do not force a Buy, Hold, or Sell when the gates fail. Provide Bear/Base/Bull per-share scenario values, the margin-of-safety buy price when defensible, three central investment arguments, and three major risks. Explicitly answer:

- Is this an excellent company?
- Is the stock attractively valued today?
- Is the company suitable for long-term ownership?

Keep these answers distinct: an excellent company can be overvalued or unsuitable for a particular valuation discipline.

## Stage 5 — Final Output

### Full Research Mode

Use these nine sections without redundant repetition:

1. **Executive Summary** — rating, company quality, valuation status, long-term suitability, and research/price dates.
2. **Structured Financial Data** — key historical and forecast inputs, periods, units, sources, and derived metrics.
3. **Valuation & Sensitivity Analysis** — method rationale, scenarios, formulas, bridge, sensitivity, relative valuation, and margin of safety.
4. **Seven-Agent Assessments** — concise A–G conclusions with confidence and material evidence.
5. **Key Disagreements & Bear Case** — adversarial findings, triggers, and invalidation conditions.
6. **McKinsey 7S Diagnosis** — the seven dimensions, three ratings, and evidence limits.
7. **Investment Execution Strategy** — conditional entries, tranches, reassessment, and horizon-based actions.
8. **Manager Final Verdict** — rating rationale, scenario values, three arguments, three risks, and the three explicit questions. Include a machine-checkable summary block with exactly these labels: `Bear value per share:`, `Base value per share:`, `Bull value per share:`, `Margin-of-safety haircut:`, and `Margin-of-safety buy price:` (or `Not Rated — insufficient evidence:` with the reason). Tag these valuation answers **Modeling Assumption / Derived Valuation**, never Analyst Estimate. These labeled fields are the report's valuation answers of record.
9. **Sources, Assumptions & Limitations** — traceable sources, evidence labels, execution method, missing data, and non-personalized research disclosure.

### Quick Price Mode

If defensible, return exactly two numbered lines:

1. **Margin-of-Safety Buy Price:** $XX
2. **Core Assumption:** One sentence naming the base intrinsic value and margin-of-safety haircut.

Replace `$XX` with the value and correct currency symbol or code. Translate the two labels when the user explicitly requests another language. Preserve the two-line structure.

If a defensible price cannot be calculated, return one brief sentence naming the missing critical inputs; do not invent a number.

## Final Quality Check

Before responding, verify:

- All seven Agents and the Manager are present in Full Research Mode.
- Evidence labels, dates, units, currencies, and source quality are visible.
- No unavailable data has been fabricated.
- DCF cash flow, discount rate, terminal value, equity bridge, and diluted shares are consistent.
- Sensitivity and scenario values reconcile to the model.
- The Manager resolves disagreements rather than averaging votes.
- Quick Price Mode contains only the permitted response.
- Output language follows the user without changing analytical content.
- Simulated perspectives are not described as independent agents or models.
