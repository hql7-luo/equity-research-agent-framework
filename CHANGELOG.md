# Changelog

All notable changes to this project will be documented in this file. The format follows Keep a Changelog principles, and versions use Semantic Versioning.

## [1.1.1] - 2026-10-25

### Fixed

- **Reinvestment was tied to revenue growth, not profit growth.** V1.1 used `reinvestment rate = revenue growth / ROIC`, but with changing EBIT margins NOPAT grows at a different rate (Base Year 2: revenue +7.00% vs NOPAT +8.43%). Explicit years now use an incremental-investment model: `Reinvestment_t = max(0, NOPAT_t − NOPAT_(t−1)) / incremental ROIC`, `FCFF_t = NOPAT_t − Reinvestment_t`. Declining NOPAT no longer releases capital automatically (reinvestment floors at zero) absent explicit divestment assumptions. Historical reconciliation: FY2025 actual reinvestment of 25 against ΔNOPAT of 15 implies ~60% historical incremental ROIC versus the fixture's deliberately conservative 7.5–15% forecast assumptions.
- **Mode-dependent margin-of-safety haircuts.** Identical inputs previously produced 35% in Full Research and 25% in Quick Price, implying conflicting actions around the USD 10.50 price. The nine-factor assessment now has reproducible anchors (terminal dependence, leverage, customer concentration, scenario dispersion, evidence quality) and a band-selection rule (3+ High → 30–40%, reference 35%; 1–2 → 25%; 0 → 15%). Full, Quick, and standalone runs now all select 35% and a USD 9.54 buy price; divergence requires a documented difference in evidence, not output mode.

### Changed

- Valuations updated for the corrected reinvestment model: Bear 6.591866 (was 7.098724), Base 14.671745 (was 14.777213), Bull 25.027497 (was 26.052694). Base intrinsic value rose slightly because explicit-year reinvestment now follows NOPAT growth at incremental ROIC rather than revenue growth; Bear fell because a shrinking business no longer releases capital by assumption.
- Manager verdict now requires a labeled Valuation Summary block (`Bear/Base/Bull value per share`, `Margin-of-safety haircut`, `Margin-of-safety buy price`), making reported answers machine-checkable.

### Tests

- Behavioral tests now extract values from designated labeled fields instead of scanning the whole document, so a correct number elsewhere cannot mask a wrong valuation field.
- Added parser self-tests: wrong field values detected, values in prose do not satisfy field checks, missing fields rejected.
- Added Full-vs-Quick consistency tests (same Base, same haircut, consistent buy price) and an exact cross-mode haircut check with the standalone Prompt.
- 42 tests pass.

## [1.1.0] - 2026-10-25

### Fixed

- **Test answer leakage:** the behavioral fixture previously published expected DCF results (e.g. Base 14.612820 and buy price 11.690256), so a model could copy answers. Fixtures now contain inputs only; expected values live in `tests/oracle.py`, which is never supplied to the model under evaluation. Behavioral checks now use tolerance-based numerical comparison against independent calculations instead of string matching.
- **Terminal-year discontinuity:** in V1.0 Base, Year 5 operating drivers implied NOPAT of about 157.0 while terminal FCFF implied terminal NOPAT of about 143.5 — an unexplained ~10.9% profitability drop. Forecasts are now driver-derived (`FCFF = NOPAT × (1 − growth/ROIC)`), and terminal economics connect explicitly (`Terminal NOPAT = Y5 NOPAT × (1+g)`, reinvestment `= g/terminal ROIC`). An automated detector flags unexplained discontinuities and terminal reinvestment double counting.
- **Arbitrary 20% margin-of-safety haircut:** replaced with a nine-factor, band-based assessment (10–20% / 20–30% / 30–40% / withhold). Reports must distinguish safety margin to Base value, Bear-scenario downside at the buy price, and conditional permanent-impairment protection.

### Changed

- Controlled Base intrinsic value moved from 14.612820 to 14.777213 and Bull from 23.557972 to 26.052694 because FCFF is now derived from operating drivers rather than fixed vectors; Bear moved from 7.458422 to 7.098724. These are economically motivated corrections, not price-target tuning. The margin-of-safety price is no longer a fixed fixture answer.
- Tests split into static structure (`test_repository.py`), deterministic mathematics (`test_financial_math.py`), and behavioral artifact checks (`test_behavioral_outputs.py`); real-company smoke tests are isolated under `tests/smoke/` and excluded from CI.
- Added edge-case coverage: WACC ≤ g, nonpositive share counts via the oracle, FCFF/FCFE discount-rate mismatch, equity-bridge sign/double-count errors, SBC double counting, currency and share-class mismatches, and negative-detection tests proving the oracle catches wrong arithmetic.

### Added

- GitHub Actions workflow running deterministic unittest checks with no secrets, paid APIs, or third-party dependencies.
- Anti-contamination fixture notice and an automated test asserting no oracle value appears in the behavioral fixture.
- Terminal-normalization and margin-of-safety rules in both SKILL.md and the standalone Prompt (synchronized verbatim).

## [1.0.0] - 2026-10-24

### Added

- One self-contained English `equity-research` Skill with multilingual output routing.
- Seven research perspectives and an Investment Committee Manager.
- Five-stage workflow covering evidence, independent analysis, adversarial review, deliberation, and final output.
- Evidence labels, source hierarchy, dated data requirements, and valuation data gates.
- FCFF/FCFE DCF rules, method selection by business type, sensitivity analysis, relative valuation, and margin-of-safety calculations.
- Full Research and strict two-line Quick Price modes.
- Standalone prompt, architecture and methodology documentation, and report template.
- Standard-library structural and hypothetical DCF tests.

### Improved

- Separated business quality, intrinsic value, current price, expected return, and investment risk.
- Required disagreement resolution by evidence rather than vote averaging.
- Added explicit disclosure of simulated versus genuinely orchestrated agents.
- Prevented personalized position sizing when investor circumstances are unknown.
