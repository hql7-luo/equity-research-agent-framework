# Real-Company Research Smoke Test — Microsoft Corp (MSFT)

**Status: executed manually, excluded from CI.** External data changes over time.

## Source Retrieval

- Source: SEC EDGAR XBRL Company Facts API (official regulatory filing data)
- URL: https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json
- Accessed: 2026-10-25 15:20 UTC
- Entity: Microsoft Corporation (CIK 0000789019)

## Extracted Latest Annual Data

- RevenueFromContractWithCustomerExcludingAssessedTax: 331,839,000,000 USD | period 2025-07-01 to 2026-06-30 | form 10-K filed 2026-07-29 | accession 0001193125-26-323660
- NetIncomeLoss: 133,749,000,000 USD | period 2025-07-01 to 2026-06-30 | form 10-K filed 2026-07-29 | accession 0001193125-26-323660

## Period Alignment Check

Microsoft's fiscal year ends in June; FY labels must NOT be treated as calendar years. The periods above are fiscal-year windows from the filings, not calendar-year data.

## Citation Integrity

Each figure above carries its accession number, form, filing date, and period. Verify against the filing index at https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K

## Missing-Data Handling

No dated market price, WACC inputs, or segment build was retrieved in this smoke test. Per the framework's price gate, no current-attractiveness rating, DCF target, or Buy/Sell recommendation is produced. The test validates retrieval and data discipline only.
