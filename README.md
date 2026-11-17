# Picking an ERP

Four cloud ERPs scored on 25 criteria for a made-up $40M automotive parts supplier, with a workbook you can change and a two-page memo that says what the result depends on.

**Start here:** [Selection-Memo.pdf](Selection-Memo.pdf) (2 pages), then [ERP-Selection-Scorecard.xlsx](ERP-Selection-Scorecard.xlsx).

Corvane Metalform is a company I made up. The four vendors are real, and what I say about them comes from public sources I checked on November 17, 2026. All 25 are listed in [sources.csv](sources.csv) and on the last sheet of the workbook.

## The company

Corvane Metalform makes metal stampings and welded assemblies in one plant in northwest Ohio. It has 185 people, 14 presses and 6 weld cells, and sells $40 million a year to nine Tier 1 customers. 78% of that revenue ships against EDI releases, and the plant is IATF 16949 certified. Its ERP is 19 years old and no longer supported.

That profile is what makes this an automotive decision and not a general manufacturing one. Customers send demand as 830 and 862 release files, expect an ASN and their own label on every container, and track cumulative shipments (CUMs) against what they asked for.

## The result

| | NetSuite | Business Central | Epicor Kinetic | Plex |
|---|---:|---:|---:|---:|
| Automotive requirements (30%) | 2.53 | 2.53 | 3.77 | **5.00** |
| Manufacturing and shop floor (22%) | 3.05 | 2.59 | 4.18 | **4.27** |
| Finance and reporting (14%) | **4.29** | 4.00 | 4.07 | 3.29 |
| Technology (10%) | 4.30 | **4.60** | 3.70 | 3.80 |
| Vendor and implementation (12%) | 3.58 | **3.83** | 3.58 | **3.83** |
| Cost (12%) | 3.76 | **5.00** | 3.75 | 4.02 |
| **Overall, out of 5** | 3.34 | 3.41 | 3.87 | **4.22** |

Plex came first with my weights. My recommendation in the memo is to take Plex and Epicor Kinetic to demos, not to sign with anyone on the strength of a scorecard.

## What the result depends on

Six of the 25 criteria are specific to automotive, and I gave them 30% of the weight. Take those six out and the four systems are nearly level: Epicor Kinetic 3.91, Plex 3.89, Business Central 3.79, NetSuite 3.69. Almost the whole gap comes from that one block.

So I reran the scores with other people's weights:

| Whose weights | What they stress | Comes first | Second |
|---|---|---|---|
| Mine | 30% automotive, 22% shop floor | Plex 4.22 | Epicor Kinetic 3.87 |
| Plant manager | 35% shop floor, 30% automotive | Plex 4.31 | Epicor Kinetic 3.91 |
| CFO | 30% finance, 20% cost, 10% automotive | Business Central 3.98 | Plex 3.86 |
| Equal | All six categories the same | Plex 4.04 | Epicor Kinetic 3.84 |
| Cost first | 35% cost | Plex 4.14 | Business Central 3.89 |

If you score this as a finance system, Business Central wins. I think that is the wrong way to score it for this company, and the memo says why, but it is a fair reading of the same numbers. NetSuite comes first only when finance and reporting is at least 75% of the decision.

## What I am least sure of

- **Cost.** Only Microsoft publishes prices. For the other three I used third-party starting prices plus my own assumptions, and every assumed cell is yellow in the workbook. The four land between $825,000 and $951,000 over five years, which is closer together than my error on any one of them.
- **Scores from reading, not demos.** 6 of the 25 rows rest fully on sources, 12 partly, and 7 are my judgment. Each row says which.
- **Weighted scoring has a blind spot.** Cost has 9% of the weight, so even doubling Plex's cost leaves it first. A big price gap should be its own decision.

## The workbook

Every result is a formula. Blue cells are inputs.

| Sheet | What is on it |
|---|---|
| Read me | The company, the scale, the color key |
| Scores | 25 criteria, weights, four scores each, the reason and the sources for every row |
| Cost | Five-year cost for 32 office users and 24 floor users, with where each number came from |
| Results | Scores by category, overall ranking, chart |
| Sensitivity | The five weight sets above, a table that changes one category's weight from 0 to 100%, and a what-if on any vendor's cost |
| Sources | 25 sources with links |

Things to try: change the dropdown on the Sensitivity sheet from "Automotive requirements" to "Finance and reporting" and watch the lines cross. Or put 50% in a vendor's "Adjust this vendor's total" cell on the Cost sheet.

## Files

```
Selection-Memo.pdf             the recommendation, 2 pages
ERP-Selection-Scorecard.xlsx   the workbook
scores.csv                     the Scores sheet as plain text
results.csv                    the Results sheet as plain text
sources.csv                    the sources
src/data.py                    criteria, scores, prices and sources, all in one place
src/model.py                   the same sums as the workbook, in plain Python
src/build_workbook.py          writes the workbook
src/build_memo.py              writes the memo
src/export_csv.py              writes the CSV files
src/test_model.py              checks the workbook and model.py agree
```

## Rebuild it

```
pip install -r requirements.txt
python src/build_workbook.py
python src/export_csv.py
python src/build_memo.py        # needs: playwright install chromium
pytest src/test_model.py
```

The workbook is written with formulas and no stored results. Open it in Excel or LibreOffice and save it once before running the tests, so the calculated values are there to check.

The tests compare two separate calculations: the workbook's formulas, worked out by a spreadsheet program, and `model.py`. The memo takes its numbers from `model.py`, so if the tests pass, the memo and the workbook say the same thing.

## What this is not

It is a portfolio case study. It is not advice to any real company and not an endorsement of any vendor. I did not sit through demos or collect quotes, and products change: Business Central only gained built-in quality inspections in April 2026. If you are choosing an ERP for real, use the structure and replace my scores with your own.
