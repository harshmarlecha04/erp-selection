"""The same sums the workbook does, in plain Python.

The workbook is the thing to read. This file exists so the memo can quote numbers
without anyone retyping them, and so test_model.py can prove the workbook's
formulas and this code agree.
"""
import data as d

V = d.VENDORS


def costs(shared=None, cost=None, adjust=None):
    """Five-year cost per vendor. adjust = {vendor: 0.5} makes that vendor 50% dearer."""
    s, c, adjust = shared or d.SHARED, cost or d.COST, adjust or {}
    g, n = s["increase"], s["years"]
    factor = n if g == 0 else ((1 + g) ** n - 1) / g
    out = {}
    for v in V:
        x = c[v]
        year1 = 12 * (x["full"] * s["full_users"] + x["light"] * s["light_users"] + x["platform"]) + x["modules"] + x["edi"]
        total = year1 * factor + x["impl"] * (1 + s["contingency"]) + s["hardware"]
        out[v] = {"year1": year1, "subscription": year1 * factor, "total": total * (1 + adjust.get(v, 0))}
    return out


def cost_scores(adjust=None):
    t = {v: x["total"] for v, x in costs(adjust=adjust).items()}
    low = min(t.values())
    return {v: 5 * low / t[v] for v in V}


def score_rows(adjust=None):
    """Every criterion with its four scores filled in, cost row included."""
    cs = cost_scores(adjust)
    rows = []
    for cid, cat, name, w, sc, basis, why, src in d.CRITERIA:
        sc = [cs[v] for v in V] if cid == d.COST_ID else list(sc)
        rows.append((cid, cat, name, w, sc))
    return rows


def overall(adjust=None):
    rows = score_rows(adjust)
    tw = sum(r[3] for r in rows)
    return {v: sum(r[3] * r[4][i] for r in rows) / tw for i, v in enumerate(V)}


def by_category(adjust=None):
    """{category index: (weight, {vendor: weighted average score})}"""
    rows, out = score_rows(adjust), {}
    for k in range(len(d.CATEGORIES)):
        rs = [r for r in rows if r[1] == k]
        w = sum(r[3] for r in rs)
        out[k] = (w, {v: sum(r[3] * r[4][i] for r in rs) / w for i, v in enumerate(V)})
    return out


def with_weights(cat_weights):
    """Overall score when the six categories carry these weights instead."""
    cats, tw = by_category(), sum(cat_weights)
    return {v: sum(cat_weights[k] * cats[k][1][v] for k in cats) / tw for v in V}


def sweep(cat, share):
    """Overall score when one category carries `share` of the weight and the rest keep their proportions."""
    cats, tot = by_category(), overall()
    w, sc = cats[cat]
    base = w / sum(x[0] for x in cats.values())
    return {v: share * sc[v] + (1 - share) * (tot[v] - base * sc[v]) / (1 - base) for v in V}


def leader(scores):
    best = max(scores.values())
    top = [v for v in V if abs(scores[v] - best) < 1e-9]
    return top[0] if len(top) == 1 else "Tie"


def ranked(scores):
    return sorted(scores.items(), key=lambda kv: -kv[1])


def first_share_where(cat, vendor, step=0.001):
    """Smallest share of weight for one category at which `vendor` leads. None if never."""
    k = 0.0
    while k <= 1.0 + 1e-9:
        if leader(sweep(cat, k)) == vendor:
            return round(k, 3)
        k += step
    return None


def basis_counts():
    out = {}
    for c in d.CRITERIA:
        out[c[5]] = out.get(c[5], 0) + 1
    return out


if __name__ == "__main__":
    print("Five-year cost")
    for v, x in costs().items():
        print(f"  {v:18s} ${x['total']:>10,.0f}   cost score {cost_scores()[v]:.2f}")
    print("\nOverall")
    for v, s in ranked(overall()):
        print(f"  {v:18s} {s:.2f}")
    print("\nBy category")
    for k, (w, sc) in by_category().items():
        print(f"  {d.CATEGORIES[k]:30s} {w:3d}  " + "  ".join(f"{sc[v]:.2f}" for v in V))
    print("\nScenarios")
    for name, note, w in d.SCENARIOS:
        r = ranked(with_weights(w))
        print(f"  {name:14s} {r[0][0]} {r[0][1]:.2f}, then {r[1][0]} {r[1][1]:.2f}")
    print("\nWithout the automotive block:", {v: round(s, 2) for v, s in sweep(0, 0).items()})
    print("Plex leads once automotive is at least", first_share_where(0, "Plex"))
    print("NetSuite leads once finance is at least", first_share_where(2, "NetSuite"))
    print("Epicor leads once finance is at least", first_share_where(2, "Epicor Kinetic"))
    for a in (0.5, 1.0, 1.5, 2.0):
        print(f"Plex {a:+.0%} cost:", {v: round(s, 2) for v, s in overall({'Plex': a}).items()})
    print(basis_counts())
