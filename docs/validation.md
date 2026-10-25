# Validation

## Scope

Validation separates static checks, deterministic mathematics, behavioral artifacts, and live-data smoke tests. Static tests do not prove runtime LLM behavior; committed artifacts do not guarantee future outputs.

## Anti-Contamination Design

Behavioral fixtures contain **inputs only**. Expected values live in `tests/oracle.py`, never supplied to a model under evaluation. `test_fixture_does_not_leak_expected_answers` asserts no oracle value appears in the fixture. Behavioral tests read answers from the report's **designated labeled fields** (`Bear/Base/Bull value per share`, `Margin-of-safety haircut`, `Margin-of-safety buy price`), not by scanning the document for any matching number, and use tolerance-based comparison.

## V1.1.1 Corrections

1. **Reinvestment/ROIC mismatch.** V1.1 applied `revenue growth / ROIC` while margins changed; Base Year 2 revenue grew 7.00% but NOPAT grew 8.43%. Explicit years now use `Reinvestment_t = (NOPAT_t − NOPAT_(t−1)) / incremental ROIC`, `FCFF_t = NOPAT_t − Reinvestment_t`, with reinvestment floored at zero (no automatic capital release). FY2025 historical reinvestment of 25 against ΔNOPAT of 15 implies ~60% incremental ROIC, versus 7.5–15% forecast assumptions — deliberately conservative and disclosed in the report. Terminal economics remain `Terminal NOPAT = Y5 NOPAT × (1+g)` with `g / terminal ROIC` reinvestment, applied once.
2. **Mode inconsistency.** Full Research previously chose a 35% haircut while Quick Price chose 25% on identical inputs. The nine-factor framework now has reproducible anchors (TV dependence >75%, net debt/EBITDA >3.5x, largest customer >20%, scenario dispersion >100%, single-source/incomplete evidence) and a band rule (3+ High → 35% reference; 1–2 → 25%; 0 → 15%).
3. **Field-level behavioral validation.** Answers are parsed from labeled valuation fields; negative self-tests prove wrong field values fail and correct numbers in prose cannot satisfy a wrong field.

## Updated Valuations

| Scenario | V1.1 | V1.1.1 | Reason |
|---|---:|---:|---|
| Bear | 7.098724 | **6.591866** | Declining NOPAT no longer releases capital by assumption |
| Base | 14.777213 | **14.671745** | Reinvestment follows NOPAT growth at incremental ROIC |
| Bull | 26.052694 | **25.027497** | Same correction, margin expansion |

## Executed Checks (2026-10-25, V1.1.1)

| Check | Result |
|---|---|
| 42 deterministic unittest cases (static + numerical + behavioral artifacts) | **Pass** |
| Official `skills-ref validate` | **Pass** |
| Mermaid parse (flowchart-v2) | **Pass** |
| Fixture anti-leakage (no oracle values, no precomputed price) | **Pass** |
| Terminal continuity zero for all scenarios; V1.0 discontinuity reproduced/detected; double-count rejected | **Pass** |
| Reinvestment: NOPAT-growth vs revenue-growth divergence; negative-growth capital-release prevention; historical reconciliation | **Pass** |
| Field-parser negative tests (wrong value, value elsewhere, missing field) | **Pass** |
| Full vs Quick vs standalone: same Base, identical 35% haircut, buy price USD 9.54 | **Pass** |
| Missing-data refusal: concise, no fabricated numbers | **Pass** |

## Behavioral Runs Actually Executed

Fresh runs on 2026-10-25 used the input-only fixture and no oracle access:

- **Full Research (English):** derived Bear $6.59 / Base $14.67 / Bull $25.03; 4 High factors → 35% haircut → buy price $9.54; market $10.50 above threshold → **Watch Only**; Bear downside at buy price −30.9%, no guarantee.
- **Quick Price (Simplified Chinese):** two lines; same Base $14.67, same 35% band and $9.54 price.
- **Standalone Prompt (English):** two lines; same Base, 35%, $9.54, without SKILL.md access.
- **Missing data:** one-sentence refusal; no fabricated values.

Cross-mode result: identical intrinsic values, identical haircut, identical buy price. (An earlier V1.1.1 Quick run initially selected 25% before the anchor rule was added; after the rule, it selected 35%. The anchor rule is what removed the mode-dependent judgment drift.)

## Real-Company Smoke Test (Not in CI)

`tests/smoke/sec_smoke.py` fetched SEC XBRL facts for Microsoft (CIK 0000789019) on 2026-10-25: FY2026 (2025-07-01 to 2026-06-30) revenue USD 331,839,000,000; net income USD 133,749,000,000; 10-K filed 2026-07-29, accession 0001193125-26-323660. No market price retrieved → no rating, per the price gate. Excluded from CI because external data changes.

## Not Executed / Limitations

- **Native Kimi Code and Codex CLI loading:** clients not installed; conformance rests on official documentation and `skills-ref`.
- Behavioral artifacts are point-in-time outputs and do not guarantee future model behavior.
- GitHub-rendered Mermaid not separately verified (parser-level only).
- SEC smoke-test figures change with new filings.
- The 25% vs 35% episode shows that without explicit anchors, models can rate qualitative factors differently; the anchor rule mitigates but does not eliminate judgment variance outside the anchored factors.
