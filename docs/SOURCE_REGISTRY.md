# Source Registry — India Rape Statistics Dataset

Every figure in this dataset must reference an entry in this registry.
Format: SOURCE_ID → full citation + URL + table reference + access date.

---

## PRIMARY SOURCES

### NCRB CII ANNUAL REPORTS (official, Government of India)

| ID | Year | URL | Table refs for rape data |
|----|------|-----|--------------------------|
| NCRB-2022 | 2022 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/1701607577CrimeinIndia2022Book1.pdf | Table 5A.1 (state rape), 5A.3 (victim age), 5A.4 (offender relation), 7A (court disposal) |
| NCRB-2022-CSV | 2022 | https://data.opencity.in/dataset/b2d3ff5c-b109-42ad-afe0-b244c26505cd/resource/a4496020-4d71-4533-9041-d18e3bedb911/download/2176f9d3-19ea-4280-9b82-e643cfb5255d.csv | Crimes against women in metros 2022 — machine-readable |
| NCRB-2021 | 2021 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2021.pdf | Same table structure |
| NCRB-2020 | 2020 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2020.pdf | Same |
| NCRB-2019 | 2019 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2019.pdf | Same |
| NCRB-2018 | 2018 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2018.pdf | Same |
| NCRB-2017 | 2017 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2017.pdf | Same |
| NCRB-2016 | 2016 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2016.pdf | Same |
| NCRB-2015 | 2015 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2015.pdf | Same |
| NCRB-2014 | 2014 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2014.pdf | Same |
| NCRB-2013 | 2013 | https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2013.pdf | Same |
| NCRB-OGD | 2022 | https://www.data.gov.in/catalog/crime-india-2022 | Official open data portal — includes conviction rate, court disposal |

### SECONDARY / ANALYSIS SOURCES

| ID | Description | URL |
|----|-------------|-----|
| CHRI-2024-P1 | CHRI Part 1: National & state rape incidence 2014–2022 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part1-Sep24.pdf |
| CHRI-2024-P2 | CHRI Part 2: Police & court disposal 2014–2022 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part2-Sep24.pdf |
| CHRI-2024-P3 | CHRI Part 3: District-level incidence 2015–2022 | https://www.humanrightsinitiative.org/download/CHRI-NCRBData-RapeStats-Analysis-Part3.pdf |
| OPENCITY-2022 | OpenCity analysis — metro crime against women 2022 | https://opencity.in/crime-in-metros-in-india-in-2022/ |
| WIKI-RAPE-IN | Wikipedia: Rape in India (cross-check only) | https://en.wikipedia.org/wiki/Rape_in_India |

---

## HOW TO VERIFY A FIGURE

1. Find the SOURCE_ID tagged to that cell in the dataset
2. Go to the URL for that source
3. Navigate to the table reference listed above
4. Cross-check the value

## KNOWN ISSUES TO FIX WHEN SCRAPER RUNS

- 2017 national total: NCRB changed methodology mid-year — figure is lower than trend suggests; confirm from Table 5A.1
- Rate/lakh denominators: NCRB uses projected population (2020 National Commission on Population), not Census 2011 for 2017+
- State figures for 2017: several states show anomalous dips — likely reporting lag, not real reduction
- CHRI notes decadal CSV datasets removed from data.gov.in since ~2018 — annual PDFs are now the only primary source

## SCRAPER INSTRUCTIONS (for when network is available)

```python
# Priority download order:
PDFS_TO_FETCH = [
    ("NCRB-2022", "https://www.ncrb.gov.in/uploads/.../CrimeinIndia2022Book1.pdf"),
    ("NCRB-2022-CSV", "https://data.opencity.in/.../2176f9d3...csv"),
    # ... all above
]
# Use pdfplumber to extract Table 5A.1 (rape by state) and Table 7A (court disposal)
# Target pages: Vol 1, Chapter 5 for crimes against women
# Tables are consistently formatted 2013–2022
```
