# Validation

## Scope

Validation distinguishes executable repository checks from host-specific behavior. A structural test is not evidence that Kimi Code, Codex, or another model produced a correct investment report.

## Controlled Test Data

All financial inputs in `tests/fixtures/` are fictional and explicitly labeled. Expected DCF outputs are mathematical test oracles, not real-world estimates or recommendations.

## Executed Checks (2026-10-24)

| Check | Method | Result |
|---|---|---|
| Repository structure, required files, frontmatter, name/directory match | `tests/test_repository.py` | **Pass** |
| Seven Agents A–G, Manager, five stages preserved | `tests/test_repository.py` | **Pass** |
| Full Research nine-section structure in controlled output | Behavioral fixture run + unit test | **Pass** |
| Quick Price Mode: exactly two lines, English and Simplified Chinese | Behavioral fixture runs + unit test | **Pass** |
| Missing-data fixture: refusal without invented numbers | Behavioral fixture run + unit test | **Pass** |
| Standalone Prompt works without SKILL.md | Separate agent context using only `prompts/equity-research.md` | **Pass** |
| English default; explicit Chinese request produces Chinese | Behavioral fixture runs | **Pass** |
| DCF Bear/Base/Bull reconciliation (7.458422 / 14.612820 / 23.557972) | Independent Python recalculation | **Pass** |
| Margin-of-safety price (14.612820 × 0.8 = 11.690256) | Independent Python recalculation | **Pass** |
| 25-cell WACC × terminal-growth sensitivity table | Cell-by-cell recalculation against report | **Pass** |
| WACC derivation (80% equity + 20% after-tax debt) and terminal reinvestment (g/ROIC = 20%) | Unit test against fixture | **Pass** |
| FCFE has no net-debt bridge; invalid terminal spread rejected | Unit tests | **Pass** |
| Standalone Prompt body identical to SKILL.md body | Unit test | **Pass** |
| Relative Markdown links resolve | Unit test | **Pass** |
| Mermaid architecture diagram syntax | `mermaid.parse` (mermaid 12.2.0, jsdom) — parsed as flowchart-v2; five stages present | **Pass** |
| Agent Skills specification validation | Official `skills-ref validate` (agentskills/agentskills @ main) | **Pass** — "Valid skill" |
| Skill properties readable | Official `skills-ref read-properties` | **Pass** |
| Independent methodology audit | Read-only audit agent; all Critical/High findings fixed and re-verified | **Pass after fixes** |

### Reproduce

```bash
python3 -m unittest discover -s tests -v   # 15 tests
```

## Behavioral Test Method

Four controlled behavioral runs were executed in separate agent contexts using only the fictional fixtures: English Full Research, Chinese Quick Price, missing-data refusal, and standalone-Prompt Quick Price. Outputs live in `tests/outputs/`. These test instruction-following and arithmetic, not live data retrieval. An independent audit pass reviewed the outputs; its findings (evidence-label misuse, missing WACC/driver support, confidence-scale violation, missing Stage 2 in the diagram, weak sensitivity verification) were fixed and covered by new tests.

## Not Executed

- **Native Kimi Code CLI discovery and `/skill:equity-research` invocation:** the CLI is not installed in this environment. Conformance was verified against the official Kimi Code documentation (directory form, required `name`/`description`, `.agents/skills/` project scope, `/skill:` syntax) instead.
- **Native Codex CLI discovery and `$equity-research` invocation:** the CLI is not installed in this environment. Conformance was verified against OpenAI's official Build Skills documentation.
- **Live market-data retrieval:** the Skill does not claim to retrieve data; no live-data test was run or implied.
- **GitHub-rendered Mermaid:** syntax was validated with the official Mermaid parser; rendering on GitHub's frontend was not separately verified.

## Known Limitations

- Simulated perspectives in one model do not create statistical independence.
- Behavioral tests use one capable LLM environment; other models may follow the instructions with different fidelity.
