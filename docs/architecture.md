# Architecture

## Design Goal

The framework separates evidence collection, analytical judgment, adversarial challenge, and final accountability. It deliberately avoids an orchestration service, model routing, persistent state, and trading functionality. One portable Skill contains the complete decision workflow.

## Five Stages

### 1. Evidence Collection

The workflow identifies the exact security and builds an evidence ledger before valuation. Each material claim carries its source, date, period, units, currency, and evidence label. Data gates prevent missing inputs from becoming fabricated precision.

### 2. Independent Perspectives

The seven roles share facts but not draft conclusions. This limits anchoring and prevents every section from repeating one thesis. Roles may run as real parallel agents when the host supports them; otherwise they are sequential analytical passes in one model.

### 3. Adversarial Review

Agent D challenges the assumptions with the largest valuation impact. Relevant Agents answer with evidence, and Agent C recalculates affected scenarios. A challenge is resolved only by evidence or a disclosed assumption—not by majority agreement.

### 4. Investment Committee

The Manager classifies disagreements as factual, forecast-based, methodological, or risk-related. It weights evidence by source quality, causal relevance, valuation sensitivity, and falsifiability. It does not average ratings or votes.

### 5. Final Decision

Full Research Mode presents nine nonredundant sections. Quick Price Mode hides the analysis but retains the same evidence and valuation gates internally.

## Role Boundaries

| Role | Owns | Does not own |
|---|---|---|
| Agent A — Macro & Industry | Industry structure, macro transmission, TAM constraints, inflection points | Company accounting quality or target price |
| Agent B — Financial Quality | Statements, cash conversion, ROIC, leverage, accounting and dilution | Industry attractiveness or final rating |
| Agent C — Valuation Modeling | Method selection, forecasts, DCF, multiples, scenarios, sensitivity, margin of safety | Business-quality veto or personalized sizing |
| Agent D — Bear Case & Risk | Strongest counter-thesis, triggers, invalidation, permanent impairment | Generic risk lists or bullish promotion |
| Agent E — Investment Execution | Conditional entries, intended-position tranches, reassessment, horizons | Inventing investor circumstances or portfolio weights |
| Agent F — Buffett-Style Review | Moat, economics, capital allocation, compounding, 10-year and five-year tests | Short-term price forecasts |
| Agent G — McKinsey 7S | Publicly supportable organizational alignment and execution diagnosis | Undisclosed internal facts |
| Manager | Conflict resolution, rating, scenario values, central arguments and risks | Vote averaging or manufactured certainty |

## Analytical Independence

A shared evidence ledger creates consistency; separated draft conclusions reduce anchoring. Neither technique creates true independence when one model performs every role. Reports must disclose one of two execution methods:

- **Simulated multi-perspective review:** one model performs all roles sequentially.
- **Host-orchestrated agents:** separately executed agents are used, with their actual independence and limitations described accurately.

The framework never claims separate models, vendors, or executions unless they actually occurred.

## Committee Decision Logic

The rating is conditional on evidence and a dated market price:

- **Buy:** sufficient evidence, acceptable quality/downside, and price at or below a defensible margin-of-safety level.
- **Hold:** intact thesis but insufficient valuation or risk/reward advantage for Buy.
- **Sell:** fundamental impairment or decisively unfavorable valuation/risk.
- **Watch Only:** unresolved price, evidence, or risk prevents a directional rating.
- **Not Rated:** critical evidence or valuation inputs cannot support a responsible judgment.

Business quality, current valuation, and long-term suitability remain separate questions. A high-quality business may receive Watch Only because its price offers no margin of safety.

## Token and Repetition Control

The evidence ledger is the single source of shared facts. Agent sections contain only conclusions, material evidence, counterevidence, assumptions, confidence, and unresolved items. The Manager references prior evidence instead of restating complete sections. Detailed formulas appear in the valuation section, not in every Agent summary.
