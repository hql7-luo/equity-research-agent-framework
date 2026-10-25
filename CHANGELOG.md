# Changelog

All notable changes to this project will be documented in this file. The format follows Keep a Changelog principles, and versions use Semantic Versioning.

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
