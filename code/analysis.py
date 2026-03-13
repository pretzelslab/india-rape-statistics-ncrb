"""
India Rape Statistics — Analysis Script
Produces: 3 publication-quality figures + key findings summary
Sources: NCRB CII 2013–2022 (verified via CHRI Oct 2024)
Run after pipeline.py --stage verify-seed
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings, os
warnings.filterwarnings("ignore")

os.makedirs("outputs", exist_ok=True)

# ── Verified data (update cell-by-cell as you pull from primary PDFs) ─────
years = list(range(2013, 2023))

national_reported = {
    2013: 33707, 2014: 36735, 2015: 34651, 2016: 38947, 2017: 32559,
    2018: 33356, 2019: 32033, 2020: 28046, 2021: 31677, 2022: 31516,
}
# Source: NCRB CII annual reports 2013–2022; cross-verified CHRI Oct 2024 Part 1 Table 1

conviction_rate = {
    2013: 27.1, 2014: 28.4, 2015: 29.8, 2016: 25.5, 2017: 32.2,
    2018: 27.8, 2019: 27.9, 2020: 25.0, 2021: 26.1, 2022: 26.5,
}
# Source: NCRB CII Table 7A; CHRI Part 2 Table 11

trial_pending = {
    2013: 100788, 2014: 113165, 2015: 117451, 2016: 130673, 2017: 117451,
    2018: 136655, 2019: 144682, 2020: 152652, 2021: 161000, 2022: 198285,
}
# Source: CHRI Part 2 — "backlog + new cases before trial courts" (Table 9)

state_2022 = {
    "Rajasthan": 5399, "Madhya Pradesh": 3049, "Uttar Pradesh": 2950,
    "Chhattisgarh": 2202, "West Bengal": 1890, "Odisha": 1873,
    "Maharashtra": 2105, "Haryana": 1499, "Kerala": 1659, "Delhi UT": 1226,
}
# Source: NCRB CII 2022, Table 5A.1

known_offender_pct = {
    2013: 93.9, 2014: 94.2, 2015: 94.5, 2016: 93.8, 2017: 93.0,
    2018: 94.1, 2019: 94.8, 2020: 95.2, 2021: 88.7, 2022: 89.1,
}
# Source: NCRB CII Table 5A.4 (offender relation to victim)

# ── Plot settings ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})
BLUE   = "#1A56DB"
RED    = "#E74C3C"
GREEN  = "#27AE60"
AMBER  = "#F39C12"
GRAY   = "#95A5A6"
DARK   = "#2C3E50"

# ══════════════════════════════════════════════════════════════════════════
# FIGURE 1: National trend — 10 years post-CLA Amendment
# ══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5))

y_vals = [national_reported[yr] for yr in years]
ax.plot(years, y_vals, marker="o", linewidth=2.5, color=BLUE,
        markersize=7, zorder=4, label="Reported cases (FIRs)")
ax.fill_between(years, y_vals, alpha=0.07, color=BLUE)

# COVID shading
ax.axvspan(2019.5, 2020.5, color=AMBER, alpha=0.12, zorder=1)
ax.text(2020, 29500, "COVID\n(underreporting\nlikely)", ha="center",
        fontsize=8, color=AMBER, style="italic")

# Annotate highest and notable points
ax.annotate("38,947\n(2016 peak)", xy=(2016, 38947),
            xytext=(2016.4, 40500), fontsize=8.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))
ax.annotate("~86/day\n(2021)", xy=(2021, 31677),
            xytext=(2021.3, 33800), fontsize=8.5, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))
ax.annotate("28,046\n(COVID dip)", xy=(2020, 28046),
            xytext=(2018.5, 26000), fontsize=8.5, color=AMBER,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xticks(years)
ax.set_xlim(2012.5, 2022.5)
ax.set_ylim(24000, 43000)
ax.set_title("Reported Rape Cases in India, 2013–2022",
             fontsize=14, fontweight="bold", color=DARK, pad=12)
ax.set_ylabel("Registered FIRs", color=DARK)
ax.tick_params(axis="both", colors=DARK)

ax.text(0.01, -0.12,
        "Source: NCRB Crime in India Annual Reports 2013–2022. "
        "Cross-verified: Commonwealth Human Rights Initiative (CHRI) Oct 2024. "
        "Note: reported cases only — underreporting documented.",
        transform=ax.transAxes, fontsize=7.5, color=GRAY,
        ha="left", va="top")
plt.tight_layout()
plt.savefig("outputs/fig1_national_trend.png", dpi=180, bbox_inches="tight")
print("✓ fig1_national_trend.png")


# ══════════════════════════════════════════════════════════════════════════
# FIGURE 2: Justice pipeline — conviction rate vs mounting backlog
# ══════════════════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()

conv_vals = [conviction_rate[yr] for yr in years]
pend_vals = [trial_pending[yr] for yr in years]

bars = ax1.bar(years, conv_vals, color=GREEN, alpha=0.65,
               width=0.6, label="Conviction rate %", zorder=2)
ax2.plot(years, pend_vals, marker="s", color=RED, linewidth=2.5,
         markersize=6, label="Cases pending trial (EOY)", zorder=3)
ax2.fill_between(years, pend_vals, alpha=0.06, color=RED)

# Max trial completion rate reference line
ax1.axhline(13, color=AMBER, linestyle=":", linewidth=1.5, alpha=0.9,
            label="Max trial completion rate ever: 13% (CHRI)")

# Labels on bars
for bar, val in zip(bars, conv_vals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
             f"{val:.0f}%", ha="center", va="bottom", fontsize=7.5, color=DARK)

ax1.set_ylabel("Conviction Rate (%)", color=GREEN, fontsize=10)
ax2.set_ylabel("Cases Pending Trial (cumulative)", color=RED, fontsize=10)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000):.0f}K"))
ax1.set_ylim(0, 50)
ax1.set_xlim(2012.5, 2022.5)
ax1.set_xticks(years)
ax1.set_title("Justice Pipeline: Conviction Rate vs Trial Backlog, 2013–2022",
              fontsize=14, fontweight="bold", color=DARK, pad=12)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc="upper left", fontsize=8.5,
           framealpha=0.9)

ax2.annotate(f"198K\npending\n(2022)", xy=(2022, 198285),
             xytext=(2020.5, 185000), fontsize=8.5, color=RED,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))

ax1.text(0.01, -0.12,
         "Source: NCRB CII Table 7A 2013–2022; "
         "CHRI Part 2 Oct 2024 — trial completion rate never exceeded 13% in any year. "
         "Trial pending = cumulative backlog at year end.",
         transform=ax1.transAxes, fontsize=7.5, color=GRAY, ha="left", va="top")
plt.tight_layout()
plt.savefig("outputs/fig2_justice_pipeline.png", dpi=180, bbox_inches="tight")
print("✓ fig2_justice_pipeline.png")


# ══════════════════════════════════════════════════════════════════════════
# FIGURE 3: State comparison 2022 + known offender context
# ══════════════════════════════════════════════════════════════════════════
fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(11, 8),
                                      gridspec_kw={"height_ratios":[2,1]})

# Top: state bar chart
states_sorted = sorted(state_2022.items(), key=lambda x: x[1], reverse=True)
names  = [s[0] for s in states_sorted]
vals   = [s[1] for s in states_sorted]
colors = [RED if n in ("Rajasthan","Delhi UT") else BLUE for n in names]

bars = ax_top.barh(names[::-1], vals[::-1], color=colors[::-1],
                   alpha=0.8, height=0.65)
for bar, val in zip(bars, vals[::-1]):
    ax_top.text(bar.get_width() + 40, bar.get_y() + bar.get_height()/2,
                f"{val:,}", va="center", fontsize=8.5, color=DARK)

ax_top.set_xlabel("Registered FIRs", color=DARK)
ax_top.set_title("Top 10 States — Reported Rape Cases, 2022",
                 fontsize=13, fontweight="bold", color=DARK)
ax_top.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax_top.set_xlim(0, 6800)

red_patch  = mpatches.Patch(color=RED,  alpha=0.8, label="Notable outlier")
blue_patch = mpatches.Patch(color=BLUE, alpha=0.8, label="Other state")
ax_top.legend(handles=[red_patch, blue_patch], fontsize=8.5, framealpha=0.9)

# Bottom: known offender trend
ko_vals = [known_offender_pct[yr] for yr in years]
ax_bot.plot(years, ko_vals, marker="o", linewidth=2.2, color=AMBER,
            markersize=6, label="Known to victim %")
ax_bot.fill_between(years, ko_vals, 80, alpha=0.08, color=AMBER)
ax_bot.axhline(89, color=GRAY, linestyle="--", linewidth=1, alpha=0.6)
ax_bot.set_ylim(80, 100)
ax_bot.set_xticks(years)
ax_bot.set_ylabel("Known offender %", color=DARK)
ax_bot.set_title("Offender Known to Victim, 2013–2022 (national)",
                 fontsize=11, fontweight="bold", color=DARK)
ax_bot.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax_bot.annotate("~89% of all cases", xy=(2017, 93.0),
                xytext=(2014.5, 97), fontsize=8.5, color=AMBER,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=1))

ax_bot.text(0.01, -0.18,
            "Source: NCRB CII Table 5A.1 (state cases) + Table 5A.4 (offender relation) 2022; "
            "NCRB 2021 for known offender trend. "
            "State figures: seed estimates pending PDF verification.",
            transform=ax_bot.transAxes, fontsize=7.5, color=GRAY, ha="left", va="top")

plt.tight_layout(pad=2.0)
plt.savefig("outputs/fig3_state_and_offender.png", dpi=180, bbox_inches="tight")
print("✓ fig3_state_and_offender.png")


# ══════════════════════════════════════════════════════════════════════════
# KEY FINDINGS SUMMARY
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("KEY FINDINGS — for Fellows application")
print("="*60)
print(f"Total cases 2013–2022:          {sum(national_reported.values()):,}")
print(f"Peak year:                       2016 ({national_reported[2016]:,} cases)")
print(f"Daily average 2021:              {national_reported[2021]/365:.0f} cases")
pend_growth = (trial_pending[2022]-trial_pending[2013])/trial_pending[2013]*100
print(f"Trial backlog growth 2013→2022:  {pend_growth:.0f}% increase")
avg_conv = sum(conviction_rate.values())/len(conviction_rate)
print(f"Avg conviction rate 2013–2022:   {avg_conv:.1f}%")
print(f"Trial completion rate max:       12.38% (2017) — never exceeded 13%")
print(f"Known offender (2021):           {known_offender_pct[2021]}% of cases")
print(f"Cases pending trial (2022):      {trial_pending[2022]:,}")
print()
print("NOTE: All figures from NCRB CII annual reports + CHRI Oct 2024 analysis.")
print("      State-level figures pending primary PDF verification.")
print("      Underreporting not quantified — a core limitation to name in any paper.")
