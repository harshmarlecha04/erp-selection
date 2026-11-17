"""Writes scores.csv and results.csv so the numbers can be read on GitHub without opening Excel.

    python src/export_csv.py
"""
import csv
import os

import data as d
import model as m

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    cs = m.cost_scores()
    with open(os.path.join(ROOT, "scores.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "criterion", "weight"] + d.VENDORS + ["how_sure", "why", "sources"])
        for cid, cat, name, weight, sc, basis, why, src in d.CRITERIA:
            sc = [round(cs[v], 2) for v in d.VENDORS] if cid == d.COST_ID else sc
            w.writerow([cid, d.CATEGORIES[cat], name, weight] + list(sc) + [basis, why, src])
    with open(os.path.join(ROOT, "results.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row", "weight"] + d.VENDORS + ["comes_first"])
        for k, (weight, sc) in m.by_category().items():
            w.writerow([d.CATEGORIES[k], weight] + [f"{sc[v]:.2f}" for v in d.VENDORS] + [m.leader(sc)])
        tot = m.overall()
        w.writerow(["Overall", 100] + [f"{tot[v]:.2f}" for v in d.VENDORS] + [m.leader(tot)])
        cost = m.costs()
        w.writerow(["Five-year cost, USD", ""] + [f"{cost[v]['total']:.0f}" for v in d.VENDORS] + [min(cost, key=lambda v: cost[v]["total"])])
    with open(os.path.join(ROOT, "sources.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "publisher", "title", "kind", "what_i_took_from_it", "link"])
        w.writerows(d.SOURCES)


if __name__ == "__main__":
    main()
