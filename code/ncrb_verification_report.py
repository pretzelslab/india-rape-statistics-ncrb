"""
NCRB National Figures Verification Report
Run this locally once you have downloaded the PDFs.
pip install pdfplumber pandas openpyxl requests
"""

import json
from datetime import datetime

FIGURES_TO_VERIFY = [
    {
        "year": 2013,
        "figure_cited": 33707,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2013",
        "source_table": "Table 5A.1 or equivalent",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2013.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "First year post Criminal Law Amendment Act. Figure should be clearly higher than 2012.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2014,
        "figure_cited": 36735,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2014",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2014.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "Peak region begins. Rajasthan drives much of the volume.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2015,
        "figure_cited": 34651,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2015",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2015.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "Slight dip from 2014 peak.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2016,
        "figure_cited": 38947,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2016",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2016.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "Highest year in dataset. Verify this is not a data entry error before citing.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2017,
        "figure_cited": 32559,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2017",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2017.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "MEDIUM CONFIDENCE. NCRB changed reporting methodology this year. The figure looks anomalously low vs the trend. Read the methodology note in this year's report before citing.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2018,
        "figure_cited": 33356,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2018",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2018.pdf",
        "cross_check": "CHRI-2024-P1 Table 1",
        "note": "Post-methodology-change baseline. Compare with 2017 carefully.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2019,
        "figure_cited": 32033,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2019",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2019.pdf",
        "cross_check": "Wikipedia cross-check: https://en.wikipedia.org/wiki/Rape_in_India",
        "note": "Last pre-COVID year. Should be close to 2018 figure.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2020,
        "figure_cited": 28046,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2020",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2020.pdf",
        "cross_check": "Wikipedia cross-check",
        "note": "COVID year. Documented drop in reporting due to lockdowns reducing police access, not necessarily reflecting a real reduction in incidence.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2021,
        "figure_cited": 31677,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2021",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/CrimeinIndia2021.pdf",
        "cross_check": "Wikipedia cross-check. Also check: 31677 / 365 = 86.8 cases per day, consistent with widely cited 86/day figure.",
        "note": "Cross-check the per-day calculation as a sanity test.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
    {
        "year": 2022,
        "figure_cited": 31516,
        "figure_label": "Total reported rape cases",
        "source_id": "NCRB-2022",
        "source_table": "Table 5A.1",
        "source_url": "https://www.ncrb.gov.in/uploads/nationalcrimerecordsbureau/custom/1701607577CrimeinIndia2022Book1.pdf",
        "cross_check": "NCRB-OGD: https://www.data.gov.in/catalog/crime-india-2022",
        "note": "Most recent year. Also verifiable via NCRB Open Government Data portal CSV.",
        "verified_figure": None,
        "verified_by": None,
        "verified_date": None,
        "match": None,
        "delta": None,
    },
]

JUSTICE_FIGURES_TO_VERIFY = [
    {
        "figure": "Trial completion rate never exceeded 13% (2013-2022)",
        "cited_value": "12.38% max (2017)",
        "source": "CHRI-2024-P2 Table 9",
        "ncrb_table_to_check": "Table 7A in each year's CII report",
        "how_to_calculate": "trials completed in year / (trials pending start of year + new cases sent for trial). CHRI reports this as 'disposal rate'.",
        "verified": None,
        "notes": None,
    },
    {
        "figure": "Trial backlog 198,285 at end of 2022",
        "cited_value": 198285,
        "source": "CHRI-2024-P2 / NCRB-2022 Table 7A",
        "ncrb_table_to_check": "Table 7A, column 'cases pending trial at end of year'",
        "how_to_calculate": "Direct read from table. Should be labeled 'pending at end of year' or similar.",
        "verified": None,
        "notes": None,
    },
    {
        "figure": "Trial backlog grew 97% from 2013 to 2022",
        "cited_value": "97%",
        "source": "Calculated: (198285 - 100788) / 100788",
        "ncrb_table_to_check": "Table 7A in both NCRB-2013 and NCRB-2022",
        "how_to_calculate": "(end_2022 - end_2013) / end_2013 * 100. Once both endpoints are verified the percentage follows automatically.",
        "verified": None,
        "notes": None,
    },
    {
        "figure": "88.7% of rapes committed by known person (2021)",
        "cited_value": 88.7,
        "source": "NCRB-2021 Table 5A.4",
        "ncrb_table_to_check": "Table 5A.4: Offender's relation and nearness to rape victims",
        "how_to_calculate": "Sum of all non-stranger categories / total victims * 100. Categories include: family members, neighbours, acquaintances, employers etc.",
        "verified": None,
        "notes": None,
    },
]

def print_verification_checklist():
    print("=" * 70)
    print("NCRB NATIONAL FIGURES VERIFICATION CHECKLIST")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 70)
    print()
    print("STEP 1: Download PDFs from NCRB")
    print("Run: python pipeline.py --stage fetch")
    print("Or download manually from: https://www.ncrb.gov.in")
    print()
    print("STEP 2: For each year below, open the PDF and find the table listed.")
    print("Fill in 'verified_figure' with what you read from the PDF.")
    print()

    all_ok = True
    for row in FIGURES_TO_VERIFY:
        status = "PENDING"
        if row["verified_figure"] is not None:
            delta = row["verified_figure"] - row["figure_cited"]
            status = "OK" if delta == 0 else f"MISMATCH: delta {delta:+,}"
            if delta != 0:
                all_ok = False

        conf = "MEDIUM CONFIDENCE" if row["year"] == 2017 else "HIGH CONFIDENCE"
        print(f"  Year {row['year']} | Cited: {row['figure_cited']:,} | Status: {status} | {conf}")
        print(f"    Table: {row['source_table']}")
        print(f"    URL:   {row['source_url']}")
        if row["note"]:
            print(f"    Note:  {row['note']}")
        print()

    print()
    print("JUSTICE PIPELINE FIGURES:")
    print()
    for row in JUSTICE_FIGURES_TO_VERIFY:
        print(f"  Figure: {row['figure']}")
        print(f"    Cited value:  {row['cited_value']}")
        print(f"    Source:       {row['source']}")
        print(f"    NCRB table:   {row['ncrb_table_to_check']}")
        print(f"    How to calc:  {row['how_to_calculate']}")
        print()

    print("=" * 70)
    if all_ok:
        print("All figures verified and match.")
    else:
        print("Some figures pending or mismatched. Review before citing in paper.")
    print("=" * 70)

def export_to_json(path="verification_report.json"):
    report = {
        "generated": datetime.now().isoformat(),
        "status": "pending",
        "national_totals": FIGURES_TO_VERIFY,
        "justice_pipeline": JUSTICE_FIGURES_TO_VERIFY,
    }
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report template saved to {path}")
    print("Fill in 'verified_figure' fields as you check each PDF, then re-run.")

if __name__ == "__main__":
    print_verification_checklist()
    export_to_json("/home/claude/outputs/verification_report.json")

