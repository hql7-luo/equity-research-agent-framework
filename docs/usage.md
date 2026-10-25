# Installation and Usage

## Requirements

The Skill itself requires only a compatible LLM host that can read `SKILL.md`. Current equity research additionally requires browsing, filing access, market-data tools, or user-supplied source documents. No API key, Python package, or external service is embedded in this repository.

## Kimi Code

### Project Scope

1. Clone the repository.
2. Start Kimi Code from the repository root.
3. Kimi Code scans `.agents/skills/` at project scope.
4. Invoke the Skill by name.

```bash
git clone https://github.com/hql7-luo/equity-research-agent-framework.git
cd equity-research-agent-framework
```

```text
/skill:equity-research Analyze <company or ticker>.
```

Additional text after the invocation is passed to the Skill. Start a new session if the Skill is not visible.

### User Scope

Install manually by copying the complete Skill directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/equity-research ~/.agents/skills/
```

The resulting path must be:

```text
~/.agents/skills/equity-research/SKILL.md
```

Kimi Code also supports `$KIMI_CODE_HOME/skills/` (default `~/.kimi-code/skills/`). The shared `~/.agents/skills/` location is preferable when using both Kimi Code and Codex.

## OpenAI Codex

Codex scans `.agents/skills/` from repository locations and `$HOME/.agents/skills/` for user Skills. Use the cloned repository directly or copy the folder as shown above.

Explicit invocation:

```text
$equity-research Analyze <company or ticker>.
```

Or run `/skills` and select the Skill. Codex normally detects new Skills automatically; restart it if necessary. Do not use Kimi's `/skill:` syntax in Codex.

## Other Agent Skills Hosts

Copy `.agents/skills/equity-research/` into the host's documented Skill directory. Confirm that the host supports directory-form `SKILL.md`, YAML `name` and `description`, and Markdown instructions. This repository uses only standard fields plus the documented `license` and `compatibility` fields.

## Standalone Prompt

Use [`prompts/equity-research.md`](../prompts/equity-research.md) when Skill installation is unavailable:

1. Open the file and copy all of it.
2. Paste it into a capable LLM.
3. Append the company, ticker, mode, language, and any source documents.
4. Keep the entire prompt together; deleting the evidence gates changes the methodology.

Example:

```text
Use Full Research Mode. Analyze <company or ticker> in English. Use only the attached filings and this dated market price: <price, currency, date>. Disclose every unavailable input.
```

## Full Research Requests

A useful request identifies the security and evidence constraints:

```text
/skill:equity-research Produce Full Research on <company, ticker, exchange>. Use the latest available regulatory filings and a dated market price. Respond in English. If current data cannot be verified, say so and withhold any precise valuation or rating that depends on it.
```

For Chinese output:

```text
/skill:equity-research 使用最新可核实的监管文件和有日期的市场价格，对 <公司与代码> 输出简体中文完整研报。数据不足时不要编造估值。
```

## Quick Price Requests

```text
/skill:equity-research What is a defensible margin-of-safety buy price for <company or ticker>?
```

```text
/skill:equity-research <公司与代码> 的安全边际买入价是多少？请用简体中文回答。
```

Quick Price Mode returns exactly two numbered lines when a price is defensible. Otherwise, it briefly identifies the missing critical inputs.

## Offline and Supplied-Data Research

The framework works with attached filings, spreadsheets, transcripts, and dated prices. Label user-provided hypothetical data explicitly and never present it as real-world verified evidence. Without a dated market price, the Skill can estimate scenario values but cannot responsibly say that the stock is attractive today.

## Official Documentation

- Kimi Code: https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
- OpenAI Codex: https://learn.chatgpt.com/codex/build-skills
- Agent Skills specification: https://agentskills.io/specification
