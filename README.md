# India Rape Statistics: NCRB Dataset (2013–2022)

Empirical dataset on rape case incidence, justice outcomes, and victim profile in India.
Built from primary NCRB (National Crime Records Bureau) annual Crime in India (CII) 
reports for 2013–2022. Every figure is tagged to its source table and cross-verified 
against the Commonwealth Human Rights Initiative (CHRI) independent analysis 
published in October 2024.

The dataset covers the full justice pipeline from First Information Report (FIR) 
through police chargesheet through trial to verdict, state-level incidence across 
17 states, victim profile breakdowns by age and offender relationship, and a 
19-city metro time series. It was built to support AI safety research on 
demographic invariance in model safety responses — specifically, whether AI systems 
give equivalent quality safety advice across the populations most affected by 
gender-based violence in India.

**Research context:** The data establishes the structural conditions within which 
any AI-based safety intervention must operate. The trial completion rate in rape 
cases never exceeded 13% in any year from 2013 to 2022. The pending trial backlog 
grew 97%, reaching 198,285 cases by end of 2022. And 88.7% of reported rapes in 
2021 were committed by someone known to the victim — a figure that directly shapes 
the threat model underpinning the companion bias evaluation framework.

---

## Key Verified Findings

| Finding | Value | Source |
|---------|-------|--------|
| Trial completion rate (max, 2013–2022) | 12.38% (2017) | CHRI-2024-P2, Table 9 |
| Trial backlog at end of 2022 | 198,285 cases | NCRB-2022, Table 7A |
| Trial backlog growth 2013–2022 | +97% | Calculated from Table 7A |
| Rapes by a known person (2021) | 88.7% | NCRB-2021, Table 5A.4 |
| Peak year in dataset | 38,947 cases (2016) | NCRB-2016, Table 5A.1 |
| Daily average (2021) | ~86.8 cases/day | 31,677 / 365 |

---

## National Totals — All 10 Years Verified

Confirmed against CHRI Part 1 Table 1 (PDF read directly).
2022 additionally confirmed against OGD portal live JSON (data.gov.in).

| Year | Cases | Confidence | Notes |
|------|-------|------------|-------|
| 2013 | 33,707 | HIGH | First year post Criminal Law Amendment Act |
| 2014 | 36,735 | HIGH | |
| 2015 | 34,651 | HIGH | |
| 2016 | 38,947 | HIGH | Peak year in dataset |
| 2017 | 32,559 | MEDIUM | NCRB methodology change year |
| 2018 | 33,356 | HIGH | |
| 2019 | 32,033 | HIGH | Last pre-COVID year |
| 2020 | 28,046 | HIGH | COVID lockdowns reduced police access |
| 2021 | 31,677 | HIGH | |
| 2022 | 31,516 | HIGH | Dual-verified: CHRI + OGD JSON |

**Note on 2017:** NCRB changed reporting methodology that year. The drop from 2016 is partly a counting artefact.

**CHRI text typo (documented):** CHRI narrative says "highest figure of 38,947 was reported in 2018." Their own Table 1 shows 38,947 in the 2016 row. Our figure is correct.

---

## Repo Structure

```
india-rape-statistics-ncrb/
│
├── README.md
├── VERIFICATION_LOG.md
├── .gitignore
│
├── data/
│   ├── national_totals.csv                      <- live source for Lovable UI
│   ├── justice_pipeline.csv                     <- 6 key justice metrics
│   ├── state_totals_2022.csv                    <- top 17 states, 2022
│   └── India_Rape_Stats_Verified_Pipeline.xlsx  <- full 4-sheet verified dataset
│
├── code/
│   ├── pipeline.py                              <- fetch + extract from NCRB PDFs
│   ├── analysis.py                              <- produces the 3 figures
│   └── ncrb_verification_report.py             <- verification checklist runner
│
├── figures/
│   ├── fig1_national_trend.png
│   ├── fig2_justice_pipeline.png               <- recommended for application
│   └── fig3_state_and_offender.png
│
├── verification/
│   └── verification_report.json
│
└── docs/
    ├── SOURCE_REGISTRY.md
    └── Structural_Interventions_Framework.docx
```

---

## Scalable Update Process

NCRB publishes each year's data in December. To update:

```bash
# 1. Fetch new PDFs
python code/pipeline.py --stage fetch

# 2. Manually verify new year figure against NCRB PDF and OGD

# 3. Add new row to data/national_totals.csv

# 4. Push — Lovable UI updates automatically on next page load
git add data/
git commit -m "Add XXXX figures: XX,XXX cases verified"
git push
```

No UI code changes required. The viz page reads from the raw GitHub CSV URL.

---

## Running Locally

```bash
pip install pandas openpyxl matplotlib pdfplumber requests

python code/pipeline.py --stage fetch    # fetch and verify
python code/analysis.py                  # reproduce figures
python code/ncrb_verification_report.py  # print verification checklist
```

---

## Primary Sources

| ID | Source | URL |
|----|--------|-----|
| NCRB CII 2013–2022 | Crime in India annual volumes | https://www.ncrb.gov.in |
| NCRB-OGD | OGD Portal: Crime in India 2022 | https://www.data.gov.in/catalog/crime-india-2022 |
| CHRI-2024-P1 | Rape Stats Analysis Part 1 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part1-Sep24.pdf |
| CHRI-2024-P2 | Rape Stats Analysis Part 2 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part2-Sep24.pdf |
| CHRI-2024-P3 | Rape Stats Analysis Part 3 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part3.pdf |

Full table-level references: see `docs/SOURCE_REGISTRY.md`

---

## Citation

```
pretzelslab(2026). India Rape Statistics: NCRB Dataset 2013–2022.
GitHub. https://github.com/YOUR-USERNAME/india-rape-statistics-ncrb

Primary source: National Crime Records Bureau, Crime in India annual reports.
Cross-verification: Commonwealth Human Rights Initiative, October 2024.
```
---

## Related Research

This dataset provides the domain grounding for a companion bias evaluation framework 
testing demographic invariance in AI safety responses across GBV contexts.

**[ai-bias-evaluation-framework](https://github.com/pretzelslab/ai-bias-evaluation-framework)**

The known-perpetrator statistic (88.7% of reported rapes committed by someone known 
to the victim) directly motivates the prompt design in that framework — three of the 
four base prompts involve a known perpetrator, reflecting the actual distribution of 
reported violence in India rather than the stranger-danger framing that dominates 
Western safety AI research.

---

*National totals: verified. State figures: CHRI-cross-verified only, pending primary PDF pass.*
*Last updated: March 2026*
