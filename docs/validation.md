# Validation

## Scope

Validation distinguishes deterministic checks from behavioral artifacts and live-data tests. A static test is not evidence that an LLM produced a correct report, and committed behavioral outputs do not guarantee future model behavior.

## Anti-Contamination Design

Behavioral fixtures contain **inputs only**. Expected valuation results live exclusively in `tests/oracle.py`, which is never supplied to a model under evaluation (enforced by the evaluation prompts). `test_fixture_does_not_leak_expected_answers` asserts that no oracle value appears in the fixture in 2/4/6-decimal renderings and that no margin-of-safety price is precomputed. Behavioral comparisons use tolerance-based numerical matching (0.5% relative for scenario values; 2% for model-chosen haircut arithmetic) instead of string matching, and `NegativeDetectionTests` prove the comparison catches 5% errors.

## What Changed in V1.1 and Why

1. **Terminal-year discontinuity (V1.0 defect).** The V1.0 Base case implied Year 5 NOPAT of ~157.0 from its drivers, but its fixed terminal FCFF implied terminal NOPAT of ~143.5 — an unexplained ~10.9% profitability decline. V1.1 derives FCFF from drivers (`FCFF = NOPAT × (1 − growth/ROIC)`) and connects terminal economics explicitly (`Terminal NOPAT = Y5 NOPAT × (1+g)`, reinvestment `= g/terminal ROIC`). Base intrinsic value changed from 14.612820 to **14.777213**; Bear 7.458422 → **7.098724**; Bull 23.557972 → **26.052694**. This is an economic-consistency correction, not price tuning.
2. **Margin-of-safety discipline.** The universal 20% haircut was replaced by a nine-factor assessment mapped to bands (10–20% / 20–30% / 30–40% / withhold), with mandatory Bear cross-check and explicit separation of safety margin to Base value, Bear downside at the buy price, and non-guaranteed permanent-impairment protection.
3. **Test architecture.** Tests split into static (`test_repository.py`), numerical (`test_financial_math.py` + `tests/oracle.py`), and behavioral artifacts (`test_behavioral_outputs.py`). GitHub Actions runs the deterministic suite with no secrets, paid APIs, or third-party dependencies.

## Executed Checks (2026-10-25, V1.1)

| Check | Method | Result |
|---|---|---|
| Repository structure, frontmatter, seven Agents, Manager, five stages, modes, language rules | `test_repository.py` | **Pass** |
| Fixture contains no oracle answers | `test_fixture_does_not_leak_expected_answers` | **Pass** |
| Skill ↔ standalone Prompt verbatim synchronization | `test_standalone_prompt_contains_complete_skill_body` | **Pass** |
| Relative Markdown links; Mermaid structure (5 stages, A–G, Manager) | `test_repository.py` | **Pass** |
| Mermaid syntax | `mermaid.parse` (mermaid 12.2.0 + jsdom) → flowchart-v2 | **Pass** |
| Skill format | Official `skills-ref validate` (agentskills/agentskills @ main) | **Pass** |
| WACC derivation (80/20 structure), driver-derived FCFF, Bear capital release | `test_financial_math.py` | **Pass** |
| Oracle stability: Bear 7.098724 / Base 14.777213 / Bull 26.052694 | `test_scenario_values_are_stable` | **Pass** |
| Terminal continuity = 0 for all scenarios; V1.0 discontinuity (~10.9%) reproduced and detected; reinvestment double-count rejected | `TerminalConsistencyTests` | **Pass** |
| Edge cases: WACC ≤ g rejected; FCFE discount-rate guard; FCFF/FCFE pairing; bridge sign/double-count errors; SBC double counting; currency/share-class mismatch; invalid haircuts | `EdgeCaseTests` | **Pass** |
| Oracle comparison detects wrong arithmetic | `NegativeDetectionTests` | **Pass** |
| Behavioral artifacts vs oracle (tolerance): full report values, justified haircut arithmetic, Bear cross-check, Quick ZH/EN two-line arithmetic consistency, missing-data refusal | `test_behavioral_outputs.py` | **Pass** |
| Full suite | `python -m unittest discover -s tests -v` | **37 tests, all pass** |

## Behavioral Runs Actually Executed

Four separate agent-context runs on 2026-10-25 used the input-only fixture and no oracle access:

1. **Full Research (English):** independently derived Bear 7.10 / Base 14.78 / Bull 26.05 (within 0.5% of oracle), chose a justified **35% haircut** (High-concern band), buy price USD 9.61, Bear downside 26.09%, rating **Hold** (price 10.50 above the buy threshold).
2. **Quick Price (Simplified Chinese):** exactly two lines; independently derived Base USD 14.78, chose **25% haircut** (Medium band), price USD 11.08 — arithmetic consistent.
3. **Standalone Prompt (English):** identical two-line result without SKILL.md access.
4. **Missing data:** one-sentence refusal listing missing valuation inputs; no fabricated numbers; did not cite the absent market price as a DCF input.

**Observed variance:** the two Quick runs chose 25% while the Full run chose 35%. Both are within the methodology's justified bands and arithmetically consistent; the haircut is a research judgment, and outputs correctly state their own reasoning. This variance is expected behavior, not a test failure.

## Real-Company Smoke Test (Not in CI)

`tests/smoke/sec_smoke.py` fetched official SEC XBRL company facts for Microsoft Corp (CIK 0000789019) on 2026-10-25: FY2026 (2025-07-01 to 2026-06-30) revenue USD 331,839,000,000 and net income USD 133,749,000,000 from 10-K filed 2026-07-29 (accession 0001193125-26-323660). The test validates source retrieval, fiscal-year alignment (June FY ≠ calendar year), and citation integrity (accession numbers). No market price was retrieved, so per the price gate **no rating or target was produced** — by design. Output: `tests/smoke/real-company-smoke.md`. SEC rejected the repository's first User-Agent (noreply.github.com domain); the working UA is documented in the script.

## Not Executed / Limitations

- **Native Kimi Code CLI and Codex CLI loading remain untested** — neither client is installed in this environment. Conformance relies on official documentation plus `skills-ref`.
- Behavioral artifacts are point-in-time LLM outputs; they do not guarantee future model behavior.
- GitHub-rendered Mermaid was not separately verified (parser-level validation only).
- The smoke test's figures reflect the access date and will change as new filings appear.
