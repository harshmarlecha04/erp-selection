"""Checks that the workbook's formulas and model.py give the same numbers.

The workbook is calculated by a spreadsheet engine and model.py by Python, so
agreement between them is a real check and not the same code run twice.

    pytest src/test_model.py
"""
import os

import pytest
from openpyxl import load_workbook

import build_workbook as b
import data as d
import model as m

BOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ERP-Selection-Scorecard.xlsx")
V = d.VENDORS
ERRORS = {"#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!"}


@pytest.fixture(scope="module")
def wb():
    book = load_workbook(BOOK, data_only=True)
    assert book["Scores"][f"E{b.S_TOTAL}"].value is not None, "Workbook has no calculated values. Open and save it in Excel or LibreOffice first."
    return book


def near(a, b_, tol=1e-6):
    return abs(a - b_) < tol


def test_25_criteria_and_weights_sum_to_100():
    assert len(d.CRITERIA) == 25
    assert sum(c[3] for c in d.CRITERIA) == 100
    assert len({c[0] for c in d.CRITERIA}) == 25


def test_scores_are_whole_numbers_from_1_to_5():
    for c in d.CRITERIA:
        if c[0] != d.COST_ID:
            assert all(s in (1, 2, 3, 4, 5) for s in c[4]), c[0]


def test_every_source_reference_exists():
    ids = {s[0] for s in d.SOURCES}
    for c in d.CRITERIA:
        assert set(c[7].split()) <= ids, c[0]
    for c in d.COST_BASIS:
        assert set(c[4].split()) <= ids, c[:2]


def test_every_cost_input_has_a_basis():
    have = {(c[0], c[1]) for c in d.COST_BASIS}
    assert len(have) == len(V) * 6


def test_five_year_cost_matches(wb):
    ws, want = wb["Cost"], m.costs()
    for i, v in enumerate(V):
        assert near(ws[f"{b.C_COLS[i]}{b.C_TOTAL}"].value, want[v]["total"], 0.01), v
        assert near(ws[f"{b.C_COLS[i]}21"].value, want[v]["year1"], 0.01), v
        assert near(ws[f"{b.C_COLS[i]}{b.C_SCORE}"].value, m.cost_scores()[v]), v


def test_overall_scores_match(wb):
    ws, want = wb["Scores"], m.overall()
    for i, v in enumerate(V):
        assert near(ws[f"{b.SC[i]}{b.S_TOTAL}"].value, want[v]), v
    assert ws[f"D{b.S_SUMW}"].value == 100


def test_ranking_matches(wb):
    ws = wb["Scores"]
    order = [v for v, _ in m.ranked(m.overall())]
    for i, v in enumerate(V):
        assert ws[f"{b.SC[i]}{b.S_RANK}"].value == order.index(v) + 1


def test_category_scores_match(wb):
    ws, want = wb["Results"], m.by_category()
    for k in range(len(d.CATEGORIES)):
        r = b.R_FIRST + k
        assert ws[f"A{r}"].value == d.CATEGORIES[k]
        assert ws[f"B{r}"].value == want[k][0]
        for i, v in enumerate(V):
            assert near(ws[f"{b.RC[i]}{r}"].value, want[k][1][v]), (d.CATEGORIES[k], v)
        assert ws[f"G{r}"].value == m.leader(want[k][1])
    assert ws[f"G{b.R_ALL}"].value == m.leader(m.overall())


def test_scenarios_match(wb):
    ws = wb["Sensitivity"]
    assert ws["B20"].value == m.leader(m.overall())
    for j, (name, note, weights) in enumerate(d.SCENARIOS):
        col = b.L(3 + j)
        want = m.with_weights(weights)
        for i, v in enumerate(V):
            assert near(ws[f"{col}{16 + i}"].value, want[v]), (name, v)
        assert ws[f"{col}20"].value == m.leader(want), name


def test_category_sweep_matches(wb):
    ws = wb["Sensitivity"]
    assert ws["B25"].value == d.CATEGORIES[0]
    for k in range(21):
        share, r = k / 20, 31 + k
        want = m.sweep(0, share)
        for i, v in enumerate(V):
            assert near(ws[f"{b.L(2 + i)}{r}"].value, want[v]), (share, v)
        assert ws[f"F{r}"].value == m.leader(want), share


def test_sweep_at_todays_share_gives_todays_score():
    base = m.by_category()[0][0] / 100
    got, want = m.sweep(0, base), m.overall()
    assert all(near(got[v], want[v]) for v in V)


def test_cost_what_if_matches(wb):
    ws = wb["Sensitivity"]
    r = 60
    while ws[f"A{r}"].value is not None and isinstance(ws[f"A{r}"].value, (int, float)):
        a = ws[f"A{r}"].value
        want = m.overall({"Plex": a})
        for i, v in enumerate(V):
            assert near(ws[f"{b.L(2 + i)}{r}"].value, want[v]), (a, v)
        r += 1
    assert r == 71  # eleven cases checked


def test_no_formula_errors(wb):
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                assert c.value not in ERRORS, (ws.title, c.coordinate, c.value)


def test_readme_quotes_the_model():
    root = os.path.dirname(BOOK)
    text = open(os.path.join(root, "README.md"), encoding="utf-8").read()
    for v, s in m.overall().items():
        assert f"{s:.2f}" in text, v
    for k, (w, sc) in m.by_category().items():
        for v in V:
            assert f"{sc[v]:.2f}" in text, (d.CATEGORIES[k], v)
    for name, note, weights in d.SCENARIOS:
        first, second = m.ranked(m.with_weights(weights))[:2]
        assert f"{first[0]} {first[1]:.2f}" in text and f"{second[0]} {second[1]:.2f}" in text, name
    for v, s in m.sweep(0, 0).items():
        assert f"{v} {s:.2f}" in text
    assert f"{m.first_share_where(2, 'NetSuite'):.0%}" in text
    assert str(len(d.SOURCES)) + " sources" in text
