# Verification Log

---

## March 2026 — Initial Verification Pass

### Method
- CHRI Part 1 PDF fetched and read directly (full text extraction)
- All 10 national figures compared against CHRI Table 1
- 2022 additionally verified against OGD portal live JSON

### National Totals Result

| Year | Our Figure | CHRI Table 1 | OGD JSON | Status |
|------|-----------|--------------|----------|--------|
| 2013 | 33,707 | 33,707 | — | VERIFIED |
| 2014 | 36,735 | 36,735 | — | VERIFIED |
| 2015 | 34,651 | 34,651 | — | VERIFIED |
| 2016 | 38,947 | 38,947 | — | VERIFIED |
| 2017 | 32,559 | 32,559 | — | VERIFIED |
| 2018 | 33,356 | 33,356 | — | VERIFIED |
| 2019 | 32,033 | 32,033 | — | VERIFIED |
| 2020 | 28,046 | 28,046 | — | VERIFIED |
| 2021 | 31,677 | 31,677 | — | VERIFIED |
| 2022 | 31,516 | 31,516 | 31,516 | VERIFIED (dual) |

Zero discrepancies. All 10 figures confirmed.

### Known Issue: CHRI Text Typo
CHRI narrative text says "highest figure of 38,947 was reported in 2018."
CHRI Table 1 correctly shows 38,947 in the 2016 row.
Our 2016 figure is correct. CHRI's own table contradicts their prose.

---

## What Still Needs Primary Verification

| Data | Current Status | How to Upgrade |
|------|---------------|----------------|
| State-level figures | CHRI cross-verified only | Run `pipeline.py --stage fetch` to pull NCRB PDFs directly |
| Trial backlog (Table 7A) | Sourced from CHRI-2024-P2 | Read NCRB-2022 Table 7A PDF directly |
| 88.7% known offender | Sourced from CHRI summary | Read NCRB-2021 Table 5A.4 directly |

---

## Update Template (copy for each new year)

### [YEAR] Verification — [DATE]

**New row added:** [YEAR] | [FIGURE] | [CONFIDENCE]

**Verified against:**
- [ ] NCRB CII [YEAR] PDF, Table 5A.1
- [ ] OGD portal JSON
- [ ] CHRI update (if available)

**Discrepancies:** None / [describe]

**Notes:**
