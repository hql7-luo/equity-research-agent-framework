"""Real-company research smoke test (NOT part of CI).

Fetches official SEC XBRL company facts for Microsoft Corp (CIK 0000789019)
and checks source retrieval, fiscal-period alignment, and citation integrity.
No API key, no paid data, standard library only. Results change over time;
this test is run manually and its dated output is committed for review.
"""

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CIK = "0000789019"
COMPANY = "Microsoft Corp"
URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"
USER_AGENT = "Equity Research Framework Test admin@example.com"
OUT_DIR = Path(__file__).resolve().parent


def latest_annual(facts, tag):
    """Return the most recent FY 10-K value for a US-GAAP tag, or None."""
    node = facts["facts"].get("us-gaap", {}).get(tag)
    if not node:
        return None
    for unit, entries in node["units"].items():
        annual = [e for e in entries if e.get("form") == "10-K" and e.get("fp") == "FY"
                  and e.get("frame") or (e.get("form") == "10-K" and e.get("fp") == "FY" and e.get("start"))]
        annual = [e for e in annual if e.get("start") and (datetime.fromisoformat(e["end"]) - datetime.fromisoformat(e["start"])).days > 300]
        if not annual:
            continue
        latest = max(annual, key=lambda e: (e["end"], e["filed"]))
        return {
            "tag": tag, "unit": unit, "value": latest["val"], "fy_start": latest["start"],
            "fy_end": latest["end"], "form": latest["form"], "filed": latest["filed"],
            "accession": latest["accn"],
        }
    return None


def main():
    request = urllib.request.Request(URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        facts = json.load(response)

    accessed = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    revenue = latest_annual(facts, "RevenueFromContractWithCustomerExcludingAssessedTax")
    net_income = latest_annual(facts, "NetIncomeLoss")

    lines = [
        "# Real-Company Research Smoke Test — Microsoft Corp (MSFT)",
        "",
        "**Status: executed manually, excluded from CI.** External data changes over time.",
        "",
        "## Source Retrieval",
        "",
        f"- Source: SEC EDGAR XBRL Company Facts API (official regulatory filing data)",
        f"- URL: {URL}",
        f"- Accessed: {accessed}",
        f"- Entity: {facts.get('entityName')} (CIK {CIK})",
        "",
        "## Extracted Latest Annual Data",
        "",
    ]
    for item in (revenue, net_income):
        if item is None:
            lines.append("- Unavailable Information: required tag not found; no value substituted.")
        else:
            lines.append(
                f"- {item['tag']}: {item['value']:,} {item['unit']} | period {item['fy_start']} to {item['fy_end']} "
                f"| form {item['form']} filed {item['filed']} | accession {item['accession']}"
            )
    lines += [
        "",
        "## Period Alignment Check",
        "",
        "Microsoft's fiscal year ends in June; FY labels must NOT be treated as calendar years. "
        "The periods above are fiscal-year windows from the filings, not calendar-year data.",
        "",
        "## Citation Integrity",
        "",
        "Each figure above carries its accession number, form, filing date, and period. "
        "Verify against the filing index at https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K",
        "",
        "## Missing-Data Handling",
        "",
        "No dated market price, WACC inputs, or segment build was retrieved in this smoke test. "
        "Per the framework's price gate, no current-attractiveness rating, DCF target, or Buy/Sell "
        "recommendation is produced. The test validates retrieval and data discipline only.",
        "",
    ]
    (OUT_DIR / "real-company-smoke.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:24]))


if __name__ == "__main__":
    main()
