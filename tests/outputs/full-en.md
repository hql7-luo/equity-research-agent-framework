# Northstar Example Corp. (TEST) — Hypothetical Full Research Mode

**Controlled behavioral test only.** Every company fact, market datum, forecast, calculation, rating, and conclusion below is **Hypothetical**, derived solely from the supplied fictional fixture. Nothing is externally verified or a real investment recommendation.

## 1. Executive Summary

- **Hypothetical rating: Buy (general research, Medium confidence).** The USD 10.50 close is below the Hypothetical 20% margin-of-safety price of **USD 11.690256**, while the Base intrinsic value is **USD 14.612820 per share**. This is a model-conditional rating, not a real recommendation.
- **Company quality:** Good but not demonstrably excellent. Recurring revenue, improving margins, cash generation, ROIC, and debt reduction are favorable; customer concentration, lower-price competition, and organizational evidence gaps limit conviction.
- **Valuation:** Hypothetical Bear/Base/Bull values are **USD 7.458422 / 14.612820 / 23.557972**. The market price implies -28.967407% Bear downside, +39.169712% Base upside, and +124.361638% Bull upside. Scenario values are estimates, not price targets.
- **Long-term suitability:** **Monitor / conditional.** Durable switching costs and recurring economics support ownership, but concentration, open-standard disruption, and unproven international execution require evidence.
- **Dates:** Research and valuation date **2026-01-20**; market price at that day's close. Latest period **FY2025 ended 2025-12-31**; fictional filing supplied **2026-01-15**. Forecast horizon is five years, with year-end discounting.

## 2. Structured Financial Data

**Units:** USD millions except per-share data, shares, and percentages. **Source and period:** Hypothetical fixture, FY2023–FY2025. All historical inputs are **Verified Fact (Hypothetical Fixture)** — verified only against this controlled fictional source; calculated rows are derived from those inputs.

| Metric | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 850 | 925 | 1,000 |
| Revenue growth | N/A | 8.823529% | 8.108108% |
| EBIT | 110 | 130 | 150 |
| EBIT margin | 12.941176% | 14.054054% | 15.000000% |
| D&A | 28 | 29 | 30 |
| Operating cash flow | 95 | 110 | 125 |
| Capital expenditure | 40 | 42 | 45 |
| Increase in net working capital | 8 | 9 | 10 |
| Simple FCF proxy (OCF − CapEx) | 55 | 68 | 80 |
| Cash and equivalents | 100 | 110 | 120 |
| Total debt | 210 | 205 | 200 |
| Diluted shares (millions) | 102 | 101 | 100 |
| Stock-based compensation, already expensed | 8 | 9 | 10 |

**FY2025 derived checks:** NOPAT = `150 × (1 − 25%) = 112.5`; ROIC = `112.5 / average invested capital 600 = 18.750000%`; net debt = `200 − 120 = 80`. The simple FCF proxy is not assumed to equal forecast FCFF. SBC is not added back, avoiding double counting.

**Hypothetical operating inputs:** FY2025 recurring revenue is 82% and services 18%; the largest customer is 22% of revenue and the top five are 46%. TAM is USD 5.0 billion with 4% expected long-term growth. These are fictional inputs, not externally validated market facts.

## 3. Valuation & Sensitivity Analysis

**Method:** A five-year FCFF DCF is appropriate for this simplified, profitable operating-company fixture. All cash flows and bridge items are USD millions; diluted shares are 100 million. Year-end discounting is used, with no mid-year convention. All forecast and WACC inputs are **Modeling Assumption (Hypothetical)** supplied by the fixture.

**Operating drivers (Modeling Assumption, Hypothetical):** The fixed FCFF vectors are authoritative and already reflect these rounded drivers — no second forecast is derived from them:

| Driver | Bear | Base | Bull |
|---|---|---|---|
| Revenue growth Y1–Y5 | -5%, 0%, 1%, 2%, 2% | 8%, 7%, 6%, 5%, 5% | 12%, 12%, 10%, 9%, 8% |
| EBIT margin Y1–Y5 | 12.0% → 12.0% | 15.0% → 15.5% | 16.0% → 18.0% |
| Cash tax rate | 25% | 25% | 25% |
| Terminal ROIC | 7.5% | 12.5% | 15.0% |
| Terminal reinvestment = g / ROIC | 20% | 20% | 20% |

Terminal FCFF is after this reinvestment, so terminal growth is not costless. All terminal growth rates stay below the fixture's 4% long-term industry growth assumption.

**WACC derivation (Modeling Assumption, Hypothetical):** An 80% equity / 20% debt target structure applies in every scenario: `WACC = 0.80 × cost of equity + 0.20 × after-tax cost of debt`.

| Component | Bear | Base | Bull |
|---|---:|---:|---:|
| Cost of equity | 12.0% | 10.0% | 9.0% |
| Pre-tax cost of debt | 9.333333% | 6.666667% | 5.333333% |
| After-tax debt cost (25% tax) | 7.0% | 5.0% | 4.0% |
| **Resulting WACC** | **11.0%** | **9.0%** | **8.0%** |

**Formulas:**

- `FCFF = EBIT × (1 − normalized cash tax rate) + D&A − CapEx − increase in net working capital`
- `TV = FCFF_N × (1 + g) / (WACC − g)`, with `WACC > g`
- `EV = Σ[FCFF_t / (1 + WACC)^t] + TV / (1 + WACC)^N`
- `Equity value = EV − debt + cash + non-operating assets − debt-like claims − preferred stock − noncontrolling interest`
- Here, `Equity value = EV − 200 + 120 = EV − 80`; all other bridge items are zero.
- `Intrinsic value per share = common equity value / 100`

**Hypothetical DCF results, recalculated with Python:**

| Scenario | FCFF Years 1–5 | WACC | g | PV explicit FCFF | PV terminal value | EV | Equity = EV − 200 + 120 | Value/share | PV TV / EV | TV / FCFF5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bear | 75, 78, 80, 82, 84 | 11.0% | 1.5% | 293.235279 | 532.606950 | 825.842229 | 745.842229 | **7.458422** | 64.492579% | 10.684211x |
| Base | 92, 97, 102, 107, 112 | 9.0% | 2.5% | 393.403157 | 1,147.878818 | 1,541.281975 | 1,461.281975 | **14.612820** | 74.475588% | 15.769231x |
| Bull | 100, 110, 120, 130, 140 | 8.0% | 3.0% | 472.995260 | 1,962.801940 | 2,435.797200 | 2,355.797200 | **23.557972** | 80.581501% | 20.600000x |

The Base terminal value is `112 × 1.025 / (0.09 − 0.025) = 1,766.153846` before discounting. Terminal value is a high 74.475588% of Base EV, so long-duration assumptions are material. All terminal growth rates are below the fixture's 4% TAM growth assumption, but that does not independently validate them.

**Base-FCFF sensitivity — intrinsic value per share (USD), actually recalculated with Python.** Each cell uses the Base FCFF vector and the same `EV − 200 + 120`, then `/100` bridge. All `WACC > g`; therefore no `N/M` cells apply.

| WACC \ g | 1.5% | 2.0% | 2.5% | 3.0% | 3.5% |
|---|---:|---:|---:|---:|---:|
| 8% | 15.144791 | 16.200219 | 17.447542 | 18.944330 | 20.773738 |
| 9% | 12.985258 | 13.740912 | **14.612820** | 15.630046 | 16.832222 |
| 10% | 11.334889 | 11.897370 | 12.534850 | 13.263397 | 14.104029 |
| 11% | 10.032851 | 10.464301 | 10.946509 | 11.488994 | 12.103809 |
| 12% | 8.979586 | 9.318529 | 9.693150 | 10.109396 | 10.574612 |

**Margin of safety:** `14.612820 × (1 − 20%) = USD 11.690256` per share, using the controlled six-decimal Base result. The 20% haircut addresses terminal-value, forecast, and evidence uncertainty. It exceeds Bear value USD 7.458422 and is **not a guaranteed floor**. The Hypothetical market price is 10.181606% below this buy-price threshold.

**Multiples cross-check:** At USD 10.50, Hypothetical Derived market capitalization is `10.50 × 100 = 1,050`; EV is `1,050 + 200 − 120 = 1,130`; FY2025 P/S is `1,050 / 1,000 = 1.050000x`; EV/EBITDA is `1,130 / (150 + 30) = 6.277778x`. P/E and P/B are unavailable because net income and book equity are not supplied. No peer or historical-multiple comparison is possible without inventing data.

## 4. Seven-Agent Assessments

All seven perspectives were **simulated sequentially in one model**, not run as independent agents or independent models. Each uses the same Hypothetical evidence ledger.

### Agent A — Macro & Industry
- **Conclusion:** Moderately attractive, structurally growing but rate- and competition-sensitive. **Evidence:** recurring workflow software, USD 5.0 billion TAM, 4% expected growth, and switching costs. **Counterevidence:** two scaled competitors are gaining lower-price share; an open standard could weaken retention; higher rates can delay purchases.
- **Porter/thesis variables:** Rivalry and buyer concentration are material; other force assessments are unavailable. Key variables are rates, open-standard adoption, and competitor share gains. **Confidence:** Medium. **Unresolved:** actual retention, market share, and industry economics.

### Agent B — Financial Quality
- **Conclusion:** Improving quality: revenue reached 1,000, EBIT margin 15%, FCF proxy 80, and ROIC 18.75%; debt fell from 210 to 200. **Counterevidence:** customer concentration, SBC of 10, and limited accounting detail constrain assurance.
- **Assumptions:** FY2025 25% normalized cash tax rate and average invested capital of 600 are accepted only as fixture inputs. **Confidence:** Medium. **Unresolved:** receivables, deferred revenue, accruals, leases, debt maturities, capex capitalization, and future dilution.

### Agent C — Valuation Modeling
- **Conclusion:** DCF produces Bear/Base/Bull values of 7.458422/14.612820/23.557972; Base upside is 39.169712% at USD 10.50. Mathematical reconciliation is high-confidence, but economic forecast confidence is only Medium.
- **Counterevidence:** Base PV terminal value is 74.475588% of EV; sensitivity is substantial. **Assumptions:** fixed FCFF with stated revenue/margin drivers, derived WACC, terminal ROIC/reinvestment, bridge, and shares. **Unresolved:** future issuance/buybacks and whether real-world drivers would match these Hypothetical paths.

### Agent D — Bear Case & Risk Officer
- **Conclusion:** Bear value USD 7.458422 shows that USD 10.50 is not protected against permanent impairment. Customer loss, switching-cost erosion, and adverse discount-rate/FCFF combinations are the strongest challenges.
- **Counterevidence to the bear case:** 82% recurring revenue, improving margins, and debt reduction. **Confidence:** Medium. **Unresolved:** customer durability, open-standard adoption, and whether Bear cash flows capture concentration downside adequately.

### Agent E — Investment Execution
- **Conclusion:** Any entry should be conditional on valuation and thesis evidence, staged only as percentages of an intended position. USD 11.690256 is a valuation discipline threshold, not a floor or personalized allocation instruction.
- **Counterevidence/assumptions:** A price below the threshold does not eliminate Bear downside; investor circumstances and liquidity are unknown. **Confidence:** Medium. **Unresolved:** individual loss capacity, correlation, horizon, and holdings.

### Agent F — Buffett-Style Investment Review
- **Hypothetical ratings:** Economic Moat **Moderate**; Business Model Quality **Good**; Management & Capital Allocation **Adequate**. Switching costs and 82% recurring revenue support durability, but competitors and open standards weaken the moat claim.
- Pricing power/durability: **Moderate**; cash-flow sustainability: **Good but conditional**; long-term compounding: **potentially attractive if ROIC and reinvestment persist**. Ten-year suitability: **conditional**. Five-year market-closure test: **potentially passable on cash generation, but not proven** because debt maturities and financing resilience are unavailable. **Confidence:** Low; long-run reinvestment runway and management behavior remain unresolved.

### Agent G — Organizational Diagnosis (McKinsey 7S)
- **Conclusion:** Strategy and incentives appear aligned with recurring growth and ROIC; centralized products and regional sales are coherent, but international capability is unproven. No internal culture or employee-sentiment claims are inferred as facts.
- **Counterevidence:** thin public-style evidence and no workforce, reporting-line, or operating-system detail. **Confidence:** Low. **Unresolved:** execution consistency, incentives in practice, talent depth, and culture. Ratings are in Section 6.

## 5. Key Disagreements & Bear Case

**Evidence-weighted resolution:** The fixed fixture inputs and Python arithmetic govern valuation reconciliation; observed-in-fixture recurring mix, margins, cash flow, and leverage receive more weight than speculative long-run narratives. Forecast disagreements are not averaged into false consensus. Base remains the central controlled case, Bear remains a credible impairment case, and missing evidence lowers confidence rather than changing numbers.

| Disagreement | Positions and underlying assumptions | Evidence and resolution | Residual uncertainty |
|---|---|---|---|
| Growth and industry capture | A/C: Base growth is usable for the test; D: lower-price share gains and customer concentration could justify Bear FCFF. F: TAM alone does not prove capture. | Recurring mix supports Base qualitatively, but no retention or segment evidence settles the forecast; retain separate scenarios. | Customer retention, share, and FCFF conversion. |
| Moat, margins, and reinvestment | F: switching costs support a Moderate moat; D: an open standard could impair pricing and margins; B: current margin/ROIC trends are favorable. | Historical Hypothetical improvement is weighted above unproven durability; no moat upgrade. | Whether margins and ROIC survive competitive pressure. |
| WACC and terminal growth | C: fixed Base 9%/2.5% is mathematically valid; D: high TV contribution and rate sensitivity weaken precision. | Use the mandated Base assumptions and disclose the full recalculated sensitivity rather than choosing a more favorable rate. | WACC components and economically durable terminal growth. |

**Strongest Hypothetical bear risks and falsification:**

| Risk and transmission | Leading indicator | Severity / likelihood | Thesis-invalidating condition and evidence that would disprove the bear view |
|---|---|---|---|
| Largest-customer or top-five loss reduces revenue, utilization, and FCFF. | Customer concentration, recurring mix, revenue and FCFF versus scenario paths. | High / likelihood unavailable; Medium confidence. | Sustained customer loss plus FCFF below Base invalidates the ownership thesis; stable recurring revenue and Base-or-better FCFF despite concentration would weaken it. |
| Scaled rivals and an open standard reduce switching costs, pricing, and margins. | EBIT margin, recurring mix, product adoption, and cash conversion. | High / elevated competitive pressure; likelihood not quantified. | Persistent margin erosion and Bear-or-worse cash flow indicate impairment; durable margins and retention would disprove it. |
| Higher rates delay purchases and raise discount rates; terminal assumptions amplify the effect. | Purchasing delays, realized FCFF, WACC and terminal assumptions. | High valuation sensitivity / likelihood unavailable. | Bear FCFF with 11% WACC and 1.5% g yields USD 7.458422; sustained cash generation and less adverse assumptions would weaken this case. |

Price volatility alone is temporary and is not thesis deterioration. Sustained customer economics, cash-flow, or moat impairment can be permanent. No regulatory or geopolitical crisis is defined, so none is invented.

## 6. McKinsey 7S Diagnosis

All organizational statements are **Hypothetical Input** or explicitly identified inference; none is independently verified.

| Dimension | Hypothetical evidence and assessment | Evidence limit |
|---|---|---|
| Strategy | Profitable recurring-revenue growth aligns with the business mix and ROIC/recurring-revenue incentives. | No detailed strategic milestones or outcomes. |
| Structure | Centralized product organization and regional sales teams plausibly support product focus and local selling. | Reporting lines and decision effectiveness are undisclosed. |
| Systems | Three-year ROIC and recurring-revenue targets support long-term measurement. | Operating systems and actual incentive outcomes are unavailable. |
| Shared Values | Profitability and recurring growth are stated priorities; cultural alignment is only an inference. | No independent culture or employee-sentiment evidence. |
| Style | Debt reduction alongside product investment is consistent with disciplined allocation. | Management behavior and decision style cannot be inferred reliably. |
| Staff | No rating on talent depth or morale is possible. | Workforce, retention, and capability data are absent. |
| Skills | Continued product investment supports an inference of product capability; international execution is unproven. | No skills inventory or expansion track record. |

- **7S Alignment: Medium.** Strategy, incentives, and stated structure are directionally aligned.
- **Execution Support: Moderate.** Debt reduction and investment are favorable, but international readiness and systems evidence are weak.
- **Long-Term Ownership Support: Monitor.** Organizational evidence is insufficient for Yes.
- **Overall confidence: Low.** The dominant limitation is thin organizational evidence, not a verified organizational defect.

## 7. Investment Execution Strategy

This is a **Hypothetical, non-personalized framework**, not an instruction or allocation based on the reader's wealth. Tranches refer only to an **intended position**.

- **Conditional staged entry:** 40% only while price is at or below USD 11.690256 and the Base thesis remains intact; 30% after evidence supports recurring-revenue durability and Base FCFF tracking; 30% after concentration/open-standard risks and debt/liquidity review are satisfactorily addressed. Do not add merely because price falls.
- **Sizing principles:** Reduce intended size for forecast/terminal uncertainty, customer concentration, weak liquidity, portfolio correlation, or limited loss capacity. No exact capital amount is appropriate without investor context.

| Scenario | Short horizon | Medium horizon | Long horizon |
|---|---|---|---|
| Bear | Do not treat a lower price alone as an opportunity; reassess cash flow and impairment. | Pause further tranches if customer, margin, or FCFF deterioration persists. | Exit/reassess if moat or cash economics are permanently impaired. |
| Base | Initial tranche is model-conditional at or below the margin-of-safety threshold. | Add only on evidence and valuation, not price momentum. | Retain only while ROIC, recurring economics, and balance-sheet resilience persist. |
| Bull | Avoid extrapolating upside or chasing above assessed value. | Reassess expectations and concentration rather than assuming further multiple expansion. | Review whether reinvestment and moat durability still support compounding. |

Reassess on missed scenario FCFF, sustained margin compression, loss of major-customer economics, adverse switching-cost evidence, or financing stress. Mechanical stop-losses do not protect against gap risk or fundamental impairment.

## 8. Manager Final Verdict

**Manager — Investment Committee:** **Hypothetical Buy, Medium confidence**, because the dated USD 10.50 price is below the defensible controlled margin-of-safety threshold and the valuation gate has all required simplified inputs. This is not an average of agent votes: verified-within-fixture arithmetic and financial trends receive greatest weight, while unresolved forecast and organizational claims reduce confidence. The Bear case prevents a high-conviction conclusion.

- **Scenario values:** Bear **USD 7.458422**; Base **USD 14.612820**; Bull **USD 23.557972**.
- **20% margin-of-safety price:** **USD 11.690256**. It is not a guaranteed floor and exceeds Bear value.

**Three central Hypothetical investment arguments:**
1. Recurring revenue is 82%, supported by switching costs, which can aid cash-flow durability.
2. EBIT margin improved to 15%, FY2025 ROIC was 18.75%, and debt declined while product investment continued.
3. USD 10.50 is below both Base value and the 20% margin-of-safety threshold, providing model-conditional upside.

**Three major Hypothetical risks:**
1. Customer concentration: the largest customer is 22% and the top five are 46% of revenue.
2. Scaled competitors and a possible open standard could erode retention, pricing, and margins.
3. DCF dependence on terminal value and fixed WACC/growth assumptions creates substantial valuation sensitivity.

**Three explicit Manager questions:**
1. **Is this an excellent company?** **Not yet demonstrated.** It has good Hypothetical financial and recurring-revenue indicators, but moat durability, concentration, and organizational evidence prevent an unqualified excellent rating.
2. **Is the stock attractively valued today?** **Yes, only within this Hypothetical model.** The 2026-01-20 price of USD 10.50 is below USD 11.690256 and Base value, although Bear downside remains material.
3. **Is the company suitable for long-term ownership?** **Conditionally; Monitor.** Long-term ownership depends on recurring economics, ROIC, customer durability, and financing resilience—not on multiple expansion.

## 9. Sources, Assumptions & Limitations

- **Sole source:** `tests/fixtures/hypothetical-company.md`, a controlled fictional fixture. No external source, real filing, quotation, citation, or market data was used. Browsing was not performed.
- **Evidence convention:** This report uses the framework's five categories with hypothetical qualifiers: **Verified Fact (Hypothetical Fixture)** for data verified only against the fictional fixture; **Modeling Assumption (Hypothetical)** for fixed test forecasts; **Unavailable Information** for gaps. No Analyst Estimate or Speculation is used. None of these means real-world verification.
- **Execution method:** Agent A–G perspectives were simulated sequentially in **one model**. They were not independent models or independent executions. The Manager synthesized evidence and disagreements rather than averaging votes.
- **Calculation verification:** Python independently recalculated all three DCF scenarios, EV-to-equity bridges, price comparisons, multiples, and every sensitivity cell. Results matched the fixture's six-decimal Bear/Base/Bull and margin-of-safety test oracles.
- **Missing or limited evidence (Unavailable Information):** no external verification; no detailed segment/geography/product disclosures; no retention or customer-contract data; no debt-maturity, lease, pension, accounting-quality, net-income, book-equity, peer, future-dilution, workforce, culture, or international-execution evidence.
- **Research boundary:** This is general, non-personalized controlled research. It does not consider any investor's finances, holdings, horizon, liquidity needs, or risk tolerance and is not personalized investment advice.
