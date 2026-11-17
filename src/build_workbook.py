"""Builds ERP-Selection-Scorecard.xlsx from data.py.

Every result in the workbook is a formula. Blue cells are inputs: change a weight,
a score or a price and everything downstream recalculates.

    python src/build_workbook.py            # writes the workbook next to the README
"""
import os
import sys

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

import data as d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "ERP-Selection-Scorecard.xlsx")

FONT = "Arial"
BLUE, GREEN, GREY, ACCENT = "0000FF", "008000", "5F5F5F", "1433FF"
SERIES = ["A3A3A3", "000000", "8C9BFF", ACCENT]  # NetSuite, Business Central, Epicor Kinetic, Plex

f_base = Font(name=FONT, size=10)
f_bold = Font(name=FONT, size=10, bold=True)
f_title = Font(name=FONT, size=16, bold=True)
f_h2 = Font(name=FONT, size=12, bold=True)
f_note = Font(name=FONT, size=9, color=GREY)
f_in = Font(name=FONT, size=10, color=BLUE)
f_link = Font(name=FONT, size=10, color=GREEN)
f_head = Font(name=FONT, size=10, bold=True, color="FFFFFF")
fill_head = PatternFill("solid", start_color="000000")
fill_soft = PatternFill("solid", start_color="F4F4F4")
fill_key = PatternFill("solid", start_color="FFFF00")
thin = Side(style="thin", color="D9D9D9")
line = Side(style="thin", color="000000")
wrap = Alignment(wrap_text=True, vertical="top")
top = Alignment(vertical="top")
center = Alignment(horizontal="center", vertical="top")

NV = len(d.VENDORS)

# Row and column positions that more than one sheet refers to
S_HEAD, S_FIRST = 4, 5
S_LAST = S_FIRST + len(d.CRITERIA) - 1          # 29
S_TOTAL, S_RANK, S_SUMW = S_LAST + 2, S_LAST + 3, S_LAST + 4
S_COST_ROW = S_FIRST + [c[0] for c in d.CRITERIA].index(d.COST_ID)
SC = [L(5 + i) for i in range(NV)]              # score columns E..H on Scores
W_RANGE = f"Scores!$D${S_FIRST}:$D${S_LAST}"
B_RANGE = f"Scores!$B${S_FIRST}:$B${S_LAST}"

C_COLS = [L(2 + i) for i in range(NV)]          # B..E on Cost
C_TOTAL, C_SCORE = 26, 27

R_FIRST = 5
R_LAST = R_FIRST + len(d.CATEGORIES) - 1        # 10
R_ALL = R_LAST + 1                              # 11
RC = [L(3 + i) for i in range(NV)]              # C..F on Results


def put(ws, ref, value, font=f_base, fmt=None, align=top, fill=None, border=None):
    c = ws[ref]
    c.value, c.font, c.alignment = value, font, align
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if border:
        c.border = border
    return c


def header(ws, row, labels, first_col=1):
    for i, text in enumerate(labels):
        put(ws, f"{L(first_col + i)}{row}", text, f_head, align=Alignment(wrap_text=True, vertical="center"), fill=fill_head)
    ws.row_dimensions[row].height = 30


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def page(ws, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.sheet_view.showGridLines = False


def leader(names, rng):
    return f'=IF(COUNTIF({rng},MAX({rng}))>1,"Tie",INDEX({names},MATCH(MAX({rng}),{rng},0)))'


# ---------------------------------------------------------------------------------------
def sheet_readme(wb):
    ws = wb.active
    ws.title = "Read me"
    page(ws, landscape=False)
    widths(ws, {"A": 30, "B": 92})
    put(ws, "A1", f"Which ERP for {d.COMPANY}", f_title)
    put(ws, "A2", f"Four cloud ERPs scored on 25 criteria. Prepared by {d.AUTHOR}. Vendor facts checked {d.CHECKED}.", f_note)
    put(ws, "A3", f"{d.COMPANY} is a made-up company. The vendors and what is said about them are real, with sources on the last sheet.", f_note)
    r = 5
    put(ws, f"A{r}", "The company", f_h2); r += 1
    for k, v in d.PROFILE:
        put(ws, f"A{r}", k, f_bold); put(ws, f"B{r}", v, align=wrap); r += 1
    r += 1
    put(ws, f"A{r}", "The four systems", f_h2); r += 1
    for v in d.VENDORS:
        put(ws, f"A{r}", v, f_bold); put(ws, f"B{r}", d.VENDOR_FULL[v]); r += 1
    r += 1
    put(ws, f"A{r}", "How to use this workbook", f_h2); r += 1
    guide = [
        ("Scores", "The 25 criteria, their weights and each system's score from 1 to 5, with the reason and the sources for every row."),
        ("Cost", "Five-year cost for 32 office users and 24 floor users. It feeds the cost row on the Scores sheet."),
        ("Results", "Scores rolled up by category, and the overall ranking."),
        ("Sensitivity", "What happens to the ranking when the weights or the cost estimates change."),
        ("Sources", "Where each fact came from."),
    ]
    for k, v in guide:
        put(ws, f"A{r}", k, f_bold); put(ws, f"B{r}", v, align=wrap); r += 1
    r += 1
    put(ws, f"A{r}", "Cell colors", f_h2); r += 1
    put(ws, f"A{r}", "Blue text", f_in); put(ws, f"B{r}", "An input. Change it and everything else recalculates. Weights, scores, prices and scenario weights are all inputs."); r += 1
    put(ws, f"A{r}", "Black text", f_base); put(ws, f"B{r}", "A formula on the same sheet. Leave it alone."); r += 1
    put(ws, f"A{r}", "Green text", f_link); put(ws, f"B{r}", "A formula that pulls from another sheet."); r += 1
    put(ws, f"A{r}", "Yellow fill", f_base, fill=fill_key); put(ws, f"B{r}", "A price I had to assume because the vendor does not publish one. Replace these with real quotes first."); r += 2
    put(ws, f"A{r}", "The scoring scale", f_h2); r += 1
    for n, text in d.SCALE:
        put(ws, f"A{r}", n, f_bold, align=Alignment(horizontal="left", vertical="top")); put(ws, f"B{r}", text); r += 1
    r += 1
    put(ws, f"A{r}", "How sure each row is", f_h2); r += 1
    for k, v in d.BASIS.items():
        put(ws, f"A{r}", k, f_bold); put(ws, f"B{r}", v, align=wrap); r += 1
    r += 1
    put(ws, f"A{r}", "What this is not", f_h2); r += 1
    limits = [
        "I scored from public documentation, consultancy pages and third-party research. I did not sit through vendor demos or get quotes.",
        "Three of the four vendors do not publish prices, so most of the cost sheet is estimate.",
        "Products change. Business Central gained built-in quality inspections in April 2026, for example. Check dates before relying on a score.",
        "This is a portfolio case study, not advice to any real company and not an endorsement of any vendor.",
    ]
    for t in limits:
        put(ws, f"A{r}", t, align=wrap); ws.merge_cells(f"A{r}:B{r}"); ws.row_dimensions[r].height = 28; r += 1


# ---------------------------------------------------------------------------------------
def sheet_scores(wb):
    ws = wb.create_sheet("Scores")
    page(ws)
    widths(ws, {"A": 5, "B": 27, "C": 44, "D": 9, "E": 11, "F": 11, "G": 11, "H": 11, "I": 14, "J": 88, "K": 18})
    put(ws, "A1", "Scores", f_title)
    put(ws, "A2", "1 = not available, 2 = third-party or custom, 3 = basic or separate module, 4 = built in and solid, 5 = built in and a known automotive strength. Weights and scores are inputs.", f_note)
    header(ws, S_HEAD, ["ID", "Category", "Criterion", "Weight"] + d.VENDORS + ["How sure", "Why these scores", "Sources"])
    for i, (cid, cat, name, w, sc, basis, why, src) in enumerate(d.CRITERIA):
        r = S_FIRST + i
        b = Border(bottom=thin)
        put(ws, f"A{r}", cid, f_note, border=b)
        put(ws, f"B{r}", d.CATEGORIES[cat], border=b)
        put(ws, f"C{r}", name, f_bold, align=wrap, border=b)
        put(ws, f"D{r}", w, f_in, "0", center, border=b)
        for j, col in enumerate(SC):
            if cid == d.COST_ID:
                put(ws, f"{col}{r}", f"=Cost!{C_COLS[j]}{C_SCORE}", f_link, "0.0", center, border=b)
            else:
                put(ws, f"{col}{r}", sc[j], f_in, "0.0", center, border=b)
        put(ws, f"I{r}", basis, border=b)
        put(ws, f"J{r}", why, align=wrap, border=b)
        put(ws, f"K{r}", src, f_note, align=wrap, border=b)
        ws.row_dimensions[r].height = 46
    edge = Border(top=line)
    put(ws, f"C{S_TOTAL}", "Weighted score, out of 5", f_bold, border=edge)
    put(ws, f"C{S_RANK}", "Rank", f_bold)
    put(ws, f"C{S_SUMW}", "Weights add up to", f_base)
    put(ws, f"D{S_SUMW}", f"=SUM(D{S_FIRST}:D{S_LAST})", f_base, "0", center)
    for col in ["A", "B", "D"]:
        ws[f"{col}{S_TOTAL}"].border = edge
    for col in SC:
        put(ws, f"{col}{S_TOTAL}", f"=SUMPRODUCT($D${S_FIRST}:$D${S_LAST},{col}{S_FIRST}:{col}{S_LAST})/SUM($D${S_FIRST}:$D${S_LAST})", f_bold, "0.00", center, border=edge)
        put(ws, f"{col}{S_RANK}", f"=RANK({col}{S_TOTAL},${SC[0]}${S_TOTAL}:${SC[-1]}${S_TOTAL})", f_base, "0", center)
    put(ws, f"A{S_SUMW + 2}", "Weights do not have to add up to 100. The formulas divide by whatever they add up to.", f_note)
    ws.conditional_formatting.add(f"{SC[0]}{S_FIRST}:{SC[-1]}{S_LAST}",
                                  ColorScaleRule(start_type="num", start_value=1, start_color="FFFFFF", end_type="num", end_value=5, end_color="B9C4FF"))
    ws.freeze_panes = f"E{S_FIRST}"
    ws.print_title_rows = f"{S_HEAD}:{S_HEAD}"


# ---------------------------------------------------------------------------------------
def sheet_cost(wb):
    ws = wb.create_sheet("Cost")
    page(ws)
    widths(ws, {"A": 50, "B": 17, "C": 17, "D": 17, "E": 17, "F": 70})
    put(ws, "A1", "Five-year cost", f_title)
    put(ws, "A2", "Only Business Central publishes prices. Yellow cells are my assumptions and are the first thing to replace with real quotes.", f_note)

    put(ws, "A3", "Shared inputs", f_h2)
    shared = [
        ("Office users (full access)", "full_users", "0"),
        ("Shop-floor users", "light_users", "0"),
        ("Years", "years", "0"),
        ("Price increase each year", "increase", "0%"),
        ("Contingency on implementation", "contingency", "0%"),
        ("Shop-floor hardware, one time", "hardware", "$#,##0"),
    ]
    for i, (label, key, fmt) in enumerate(shared):
        r = 4 + i
        put(ws, f"A{r}", label)
        assumed = key in ("increase", "contingency", "hardware")
        put(ws, f"B{r}", d.SHARED[key], f_in, fmt, fill=fill_key if assumed else None)
        put(ws, f"C{r}", d.SHARED_NOTES[key], f_note)

    header(ws, 12, ["Per vendor"] + d.VENDORS + ["What the line covers"])
    lines = [
        (13, "Office user, per user per month", "full", "$#,##0", "Full-access seat."),
        (14, "Shop-floor user, per user per month", "light", "$#,##0", "Operators reporting production, scrap and labels."),
        (15, "Platform fee, per month", "platform", "$#,##0", "A flat fee before any users."),
        (16, "Extra modules and add-ons, per year", "modules", "$#,##0", "Whatever it takes to cover MES, quality and scheduling."),
        (17, "EDI service and trading partner fees, per year", "edi", "$#,##0", "Automotive EDI including releases, ASNs and labels."),
        (18, "Implementation services, one time", "impl", "$#,##0", "Consulting, data migration, training."),
    ]
    assumed = {(b[0], b[1]): b[2] == d.MINE for b in d.COST_BASIS}
    names = {"full": "Full user", "light": "Shop-floor user", "platform": "Platform fee", "modules": "Modules and add-ons", "edi": "EDI", "impl": "Implementation"}
    for r, label, key, fmt, note in lines:
        put(ws, f"A{r}", label)
        for j, v in enumerate(d.VENDORS):
            put(ws, f"{C_COLS[j]}{r}", d.COST[v][key], f_in, fmt, fill=fill_key if assumed[(v, names[key])] else None)
        put(ws, f"F{r}", note, f_note)
    put(ws, "A19", "Adjust this vendor's total by (+ or -)")
    for col in C_COLS:
        put(ws, f"{col}19", 0, f_in, "0%")
    put(ws, "F19", "Leave at 0%. Use it to test 'what if this vendor costs 30% more than I think'.", f_note)

    calc = [
        (21, "Subscription in year 1", "=12*({c}13*$B$4+{c}14*$B$5+{c}15)+{c}16+{c}17", "$#,##0", f_base),
        (22, "Subscription over all years", "=IF($B$7=0,{c}21*$B$6,{c}21*((1+$B$7)^$B$6-1)/$B$7)", "$#,##0", f_base),
        (23, "Implementation with contingency", "={c}18*(1+$B$8)", "$#,##0", f_base),
        (24, "Shop-floor hardware", "=$B$9", "$#,##0", f_base),
        (25, "Five-year cost before adjustment", "={c}22+{c}23+{c}24", "$#,##0", f_base),
        (C_TOTAL, "Five-year cost", "={c}25*(1+{c}19)", "$#,##0", f_bold),
        (C_SCORE, "Cost score (5 = cheapest)", f"=5*MIN($B${C_TOTAL}:$E${C_TOTAL})/{{c}}{C_TOTAL}", "0.00", f_bold),
        (28, "Above the cheapest by", f"={{c}}{C_TOTAL}/MIN($B${C_TOTAL}:$E${C_TOTAL})-1", "0%", f_base),
    ]
    for r, label, formula, fmt, font in calc:
        put(ws, f"A{r}", label, font)
        for col in C_COLS:
            put(ws, f"{col}{r}", formula.format(c=col), font, fmt)
    for col in ["A"] + C_COLS:
        ws[f"{col}{C_TOTAL}"].border = Border(top=line)
    put(ws, "F27", "The score that goes to the Scores sheet: 5 x cheapest / this vendor.", f_note)

    r0 = 31
    put(ws, f"A{r0}", "Where each number comes from", f_h2)
    header(ws, r0 + 1, ["Vendor and line", "Basis", "", "", "Source", "Note"])
    ws.merge_cells(f"B{r0 + 1}:D{r0 + 1}")
    for i, (v, item, basis, note, src) in enumerate(d.COST_BASIS):
        r = r0 + 2 + i
        b = Border(bottom=thin)
        put(ws, f"A{r}", f"{v}: {item}", border=b)
        put(ws, f"B{r}", basis, f_bold if basis == d.PUB else f_base, border=b, fill=fill_key if basis == d.MINE else None)
        ws.merge_cells(f"B{r}:D{r}")
        put(ws, f"E{r}", src, f_note, border=b)
        put(ws, f"F{r}", note, align=wrap, border=b)
        ws.row_dimensions[r].height = 28
    ws.freeze_panes = "B13"


# ---------------------------------------------------------------------------------------
def sheet_results(wb):
    ws = wb.create_sheet("Results")
    page(ws)
    widths(ws, {"A": 32, "B": 10, "C": 14, "D": 16, "E": 15, "F": 12, "G": 18})
    put(ws, "A1", "Results", f_title)
    put(ws, "A2", "Each category score is the weighted average of its criteria, out of 5. Everything here is calculated from the Scores sheet.", f_note)
    header(ws, 4, ["Category", "Weight"] + d.VENDORS + ["Comes first"])
    for i, cat in enumerate(d.CATEGORIES):
        r = R_FIRST + i
        b = Border(bottom=thin)
        put(ws, f"A{r}", cat, border=b)
        put(ws, f"B{r}", f"=SUMIF({B_RANGE},$A{r},{W_RANGE})", f_link, "0", center, border=b)
        for j, col in enumerate(RC):
            sc = f"Scores!{SC[j]}${S_FIRST}:{SC[j]}${S_LAST}"
            put(ws, f"{col}{r}", f"=SUMPRODUCT(({B_RANGE}=$A{r})*{W_RANGE}*{sc})/$B{r}", f_link, "0.00", center, border=b)
        put(ws, f"G{r}", leader(f"${RC[0]}$4:${RC[-1]}$4", f"{RC[0]}{r}:{RC[-1]}{r}"), border=b)
    edge = Border(top=line)
    put(ws, f"A{R_ALL}", "Overall, out of 5", f_bold, border=edge)
    put(ws, f"B{R_ALL}", f"=SUM(B{R_FIRST}:B{R_LAST})", f_bold, "0", center, border=edge)
    put(ws, f"A{R_ALL + 1}", "Rank", f_bold)
    for j, col in enumerate(RC):
        put(ws, f"{col}{R_ALL}", f"=Scores!{SC[j]}{S_TOTAL}", Font(name=FONT, size=10, bold=True, color=GREEN), "0.00", center, border=edge)
        put(ws, f"{col}{R_ALL + 1}", f"=RANK({col}{R_ALL},${RC[0]}${R_ALL}:${RC[-1]}${R_ALL})", f_base, "0", center)
    put(ws, f"G{R_ALL}", leader(f"${RC[0]}$4:${RC[-1]}$4", f"{RC[0]}{R_ALL}:{RC[-1]}{R_ALL}"), f_bold, border=edge)
    ws.conditional_formatting.add(f"{RC[0]}{R_FIRST}:{RC[-1]}{R_LAST}",
                                  ColorScaleRule(start_type="num", start_value=1, start_color="FFFFFF", end_type="num", end_value=5, end_color="B9C4FF"))

    ch = BarChart()
    ch.type, ch.grouping = "bar", "clustered"
    ch.title = "Score by category, out of 5"
    ch.add_data(Reference(ws, min_col=3, max_col=6, min_row=4, max_row=R_LAST), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=R_FIRST, max_row=R_LAST))
    ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 5
    ch.y_axis.majorUnit = 1
    ch.x_axis.scaling.orientation = "maxMin"
    ch.height, ch.width = 11, 24
    for s, color in zip(ch.series, SERIES):
        s.graphicalProperties.solidFill = color
        s.graphicalProperties.line.solidFill = color
    finish_chart(ch)
    ws.add_chart(ch, "A15")


def finish_chart(ch):
    ch.roundedCorners = False
    ch.legend.overlay = False
    ch.legend.position = "b"
    if ch.title is not None:
        ch.title.overlay = False
    ch.x_axis.delete = False
    ch.y_axis.delete = False


# ---------------------------------------------------------------------------------------
def sheet_sensitivity(wb):
    ws = wb.create_sheet("Sensitivity")
    page(ws)
    widths(ws, {"A": 34, "B": 15, "C": 16, "D": 16, "E": 15, "F": 16, "G": 3, "H": 15, "I": 16, "J": 15, "K": 13, "L": 13})
    put(ws, "A1", "Sensitivity", f_title)
    put(ws, "A2", "A weighted score is only as good as its weights. These three tables show when the answer changes.", f_note)
    cats = f"Results!$A${R_FIRST}:$A${R_LAST}"
    catw = f"Results!$B${R_FIRST}:$B${R_LAST}"

    # 1. scenarios
    put(ws, "A4", "1. Different people, different weights", f_h2)
    header(ws, 5, ["Category", "My weights"] + [s[0] for s in d.SCENARIOS])
    put(ws, "B6", "Baseline", f_note)
    for j, s in enumerate(d.SCENARIOS):
        put(ws, f"{L(3 + j)}6", s[1], f_note, align=wrap)
    ws.row_dimensions[6].height = 26
    for i, cat in enumerate(d.CATEGORIES):
        r = 7 + i
        put(ws, f"A{r}", cat)
        put(ws, f"B{r}", f"=Results!B{R_FIRST + i}", f_link, "0", center)
        for j, s in enumerate(d.SCENARIOS):
            put(ws, f"{L(3 + j)}{r}", s[2][i], f_in, "0", center)
    put(ws, "A13", "Total", f_note)
    ncol = 2 + len(d.SCENARIOS)
    for c in range(2, ncol + 1):
        put(ws, f"{L(c)}13", f"=SUM({L(c)}7:{L(c)}12)", f_note, "0", center)
    put(ws, "A15", "Score with these weights", f_bold)
    for i, v in enumerate(d.VENDORS):
        r = 16 + i
        put(ws, f"A{r}", v)
        for c in range(2, ncol + 1):
            col = L(c)
            put(ws, f"{col}{r}", f"=SUMPRODUCT({col}$7:{col}$12,Results!${RC[i]}${R_FIRST}:${RC[i]}${R_LAST})/{col}$13", f_link, "0.00", center)
    put(ws, "A20", "Comes first", f_bold, border=Border(top=line))
    put(ws, "A21", "Lead over second place")
    for c in range(2, ncol + 1):
        col = L(c)
        put(ws, f"{col}20", leader("$A$16:$A$19", f"{col}16:{col}19"), f_bold, align=center, border=Border(top=line))
        put(ws, f"{col}21", f"=LARGE({col}16:{col}19,1)-LARGE({col}16:{col}19,2)", f_base, "0.00", center)

    # 2. one category sweep
    put(ws, "A24", "2. Change the weight of one category", f_h2)
    put(ws, "A25", "Category to change (pick from the list)")
    put(ws, "B25", d.CATEGORIES[0], f_in)
    ws.merge_cells("B25:D25")
    dv = DataValidation(type="list", formula1=f"={cats}", allow_blank=False)
    ws.add_data_validation(dv); dv.add("B25")
    put(ws, "A26", "Its share of the weight today")
    put(ws, "B26", f"=INDEX({catw},MATCH($B$25,{cats},0))/SUM({catw})", f_link, "0%")
    header(ws, 28, ["Share of weight on that category"] + d.VENDORS + ["Comes first"])
    put(ws, "A29", "Score on that category alone", f_note)
    put(ws, "A30", "Score on everything else", f_note)
    for i in range(NV):
        col = L(2 + i)
        put(ws, f"{col}29", f"=INDEX(Results!{RC[i]}${R_FIRST}:{RC[i]}${R_LAST},MATCH($B$25,{cats},0))", f_link, "0.00", center)
        put(ws, f"{col}30", f"=(Results!{RC[i]}${R_ALL}-$B$26*{col}29)/(1-$B$26)", f_link, "0.00", center)
    put(ws, "F30", leader("$B$28:$E$28", "B30:E30"), f_note)
    steps = [k / 20 for k in range(21)]
    for k, share in enumerate(steps):
        r = 31 + k
        put(ws, f"A{r}", share, f_in, "0%", Alignment(horizontal="left", vertical="top"))
        for i in range(NV):
            col = L(2 + i)
            put(ws, f"{col}{r}", f"=$A{r}*{col}$29+(1-$A{r})*{col}$30", f_base, "0.00", center)
        put(ws, f"F{r}", leader("$B$28:$E$28", f"B{r}:E{r}"))
    last = 31 + len(steps) - 1   # 51
    put(ws, f"A{last + 1}", "The other five categories keep their proportions to each other as the chosen one grows or shrinks.", f_note)

    ch = LineChart()
    ch.title = "Overall score as the chosen category's weight changes"
    ch.add_data(Reference(ws, min_col=2, max_col=5, min_row=31, max_row=last), titles_from_data=False)
    for s, name, color in zip(ch.series, d.VENDORS, SERIES):
        from openpyxl.chart.series import SeriesLabel
        s.tx = SeriesLabel(v=name)
        s.graphicalProperties.line.solidFill = color
        s.graphicalProperties.line.width = 22000
        s.smooth = False
    ch.set_categories(Reference(ws, min_col=1, min_row=31, max_row=last))
    ch.y_axis.scaling.min, ch.y_axis.scaling.max = 2, 5
    ch.y_axis.title = "Score out of 5"
    ch.x_axis.title = "Share of total weight"
    ch.x_axis.number_format = "0%"
    ch.x_axis.tickLblSkip = 4
    ch.height, ch.width = 11, 17
    finish_chart(ch)
    ch.y_axis.title.overlay = False
    ch.x_axis.title.overlay = False
    ws.add_chart(ch, "H24")

    # 3. cost what-if
    c0 = 55
    put(ws, f"A{c0}", "3. What if one vendor costs more than I estimated", f_h2)
    put(ws, f"A{c0 + 1}", "Vendor to change (pick from the list)")
    put(ws, f"B{c0 + 1}", "Plex", f_in)
    ws.merge_cells(f"B{c0 + 1}:C{c0 + 1}")
    dv2 = DataValidation(type="list", formula1='"' + ",".join(d.VENDORS) + '"', allow_blank=False)
    ws.add_data_validation(dv2); dv2.add(f"B{c0 + 1}")
    put(ws, f"A{c0 + 2}", "Weight on five-year cost")
    put(ws, f"B{c0 + 2}", f"=Scores!D{S_COST_ROW}/Scores!D{S_SUMW}", f_link, "0%")
    h = c0 + 4
    header(ws, h, ["That vendor's cost against my estimate"] + d.VENDORS + ["Comes first"])
    header(ws, h, d.VENDORS + ["Cheapest"], first_col=8)
    put(ws, f"H{h - 1}", "Five-year cost in each case", f_note)
    adj = [-0.3, -0.2, -0.1, 0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    for k, a in enumerate(adj):
        r = h + 1 + k
        put(ws, f"A{r}", a, f_in, '+0%;-0%;"as estimated"', Alignment(horizontal="left", vertical="top"))
        for i in range(NV):
            hc = L(8 + i)
            put(ws, f"{hc}{r}", f"=Cost!{C_COLS[i]}${C_TOTAL}*IF({hc}${h}=$B${c0 + 1},1+$A{r},1)", f_link, "$#,##0")
        put(ws, f"L{r}", f"=MIN(H{r}:K{r})", f_base, "$#,##0")
        for i in range(NV):
            col, hc = L(2 + i), L(8 + i)
            put(ws, f"{col}{r}", f"=Results!{RC[i]}${R_ALL}+$B${c0 + 2}*(5*$L{r}/{hc}{r}-Cost!{C_COLS[i]}${C_SCORE})", f_link, "0.00", center)
        put(ws, f"F{r}", leader(f"$B${h}:$E${h}", f"B{r}:E{r}"))
    end = h + len(adj) + 2
    put(ws, f"A{end}", "Cost is scored as 5 x cheapest / this vendor. With cost at a small share of the weight, a price gap alone cannot overturn a large gap elsewhere.", f_note)
    put(ws, f"A{end + 1}", "That is a limit of weighted scoring, so treat a large price gap as its own decision and not as something the scorecard has settled.", f_note)


# ---------------------------------------------------------------------------------------
def sheet_sources(wb):
    ws = wb.create_sheet("Sources")
    page(ws)
    widths(ws, {"A": 6, "B": 24, "C": 52, "D": 22, "E": 80, "F": 70})
    put(ws, "A1", "Sources", f_title)
    put(ws, "A2", f"All checked {d.CHECKED}. Consultancy and reseller pages sell the product they describe, so I leaned on them for what a product lacks more than for what it does well.", f_note)
    header(ws, 4, ["ID", "Publisher", "Title", "Kind", "What I took from it", "Link"])
    for i, (sid, pub, title, kind, used, url) in enumerate(d.SOURCES):
        r = 5 + i
        b = Border(bottom=thin)
        put(ws, f"A{r}", sid, f_bold, border=b)
        put(ws, f"B{r}", pub, border=b, align=wrap)
        put(ws, f"C{r}", title, border=b, align=wrap)
        put(ws, f"D{r}", kind, border=b)
        put(ws, f"E{r}", used, border=b, align=wrap)
        c = put(ws, f"F{r}", url, Font(name=FONT, size=9, color=BLUE, underline="single"), border=b, align=wrap)
        c.hyperlink = url
        ws.row_dimensions[r].height = 40
    ws.freeze_panes = "A5"


def build(path=OUT):
    wb = Workbook()
    sheet_readme(wb)
    sheet_scores(wb)
    sheet_cost(wb)
    sheet_results(wb)
    sheet_sensitivity(wb)
    sheet_sources(wb)
    wb.properties.creator = d.AUTHOR
    wb.properties.title = f"ERP selection scorecard, {d.COMPANY}"
    wb.save(path)
    return path


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else OUT))
