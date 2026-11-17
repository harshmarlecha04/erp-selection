"""Writes Selection-Memo.pdf. Every number in the memo comes from model.py,
which test_model.py checks against the workbook.

    python src/build_memo.py

Needs Playwright with a Chromium browser (playwright install chromium). Set
MEMO_FONT to a .woff2 file to use a custom typeface, otherwise it uses Arial.
Set CHROME to a browser path if Playwright's own is not installed.
"""
import asyncio
import html
import os

import data as d
import model as m

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Selection-Memo.pdf")
e = html.escape
V = d.VENDORS


def money(x):
    return f"${round(x, -3):,.0f}"


def bars(scores):
    order = m.ranked(scores)
    w, row, left, right = 400, 27, 104, 40
    scale = (w - left - right) / 5
    out = [f'<svg viewBox="0 0 {w} {row * len(order) + 22}" role="img" aria-label="Overall score for each system">']
    for t in range(6):
        x = left + t * scale
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{row * len(order)}" stroke="#d9d9d9"/>')
        out.append(f'<text x="{x}" y="{row * len(order) + 15}" text-anchor="middle" class="tick">{t}</text>')
    for i, (v, s) in enumerate(order):
        y = i * row + 5
        color = "#1433ff" if i == 0 else "#000"
        out.append(f'<text x="0" y="{y + 14}" class="lab">{e(v)}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{s * scale:.1f}" height="19" fill="{color}"/>')
        out.append(f'<text x="{left + s * scale + 6:.1f}" y="{y + 14}" class="val">{s:.2f}</text>')
    return "".join(out) + "</svg>"


def table(head, rows, widths=None, cls=""):
    cols = "".join(f'<col style="width:{x}">' for x in widths) if widths else ""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><colgroup>{cols}</colgroup><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def body():
    tot = m.overall()
    rank = m.ranked(tot)
    cats = m.by_category()
    rest = m.sweep(0, 0)
    rest_rank = m.ranked(rest)
    cost = {v: x["total"] for v, x in m.costs().items()}
    doubled = m.overall({"Plex": 1.0})
    ns_fin = m.first_share_where(2, "NetSuite")
    counts = m.basis_counts()
    auto_w = cats[0][0]
    cost_w = [c[3] for c in d.CRITERIA if c[0] == d.COST_ID][0]

    cat_rows = []
    for k, (w, sc) in cats.items():
        best = max(sc.values())
        cells = [f'<b>{sc[v]:.2f}</b>' if abs(sc[v] - best) < 1e-9 else f"{sc[v]:.2f}" for v in V]
        cat_rows.append([e(d.CATEGORIES[k]), f"{w}%"] + cells)
    cat_rows.append(["<b>Overall</b>", "<b>100%</b>"] + [f"<b>{tot[v]:.2f}</b>" for v in V])

    scen = [("My weights", f"{auto_w}% on automotive, 22% on the shop floor", m.overall())]
    notes = {
        "Plant manager": "35% on the shop floor, 30% on automotive",
        "CFO": "30% on finance, 20% on cost, 10% automotive",
        "Equal": "All six categories count the same",
        "Cost first": "35% on cost",
    }
    for name, note, w in d.SCENARIOS:
        scen.append((name, notes[name], m.with_weights(w)))
    scen_rows = []
    for name, note, sc in scen:
        r = m.ranked(sc)
        scen_rows.append([f"<b>{e(name)}</b>", e(note), f"<b>{e(r[0][0])}</b> {r[0][1]:.2f}", f"{e(r[1][0])} {r[1][1]:.2f}"])
    cfo = m.ranked(dict(scen[2][2]))

    return f"""
<header>
  <p class="kind">Selection memo</p>
  <h1>Which ERP for {e(d.COMPANY)}</h1>
  <dl><div><dt>To</dt><dd>Owner, CFO, plant manager</dd></div><div><dt>From</dt><dd>{e(d.AUTHOR)}</dd></div><div><dt>Date</dt><dd>{d.CHECKED}</dd></div><div><dt>Goes with</dt><dd>ERP-Selection-Scorecard.xlsx</dd></div></dl>
</header>

<p class="lead">Take {e(rank[0][0])} and {e(rank[1][0])} to demos, with {e(rank[0][0])} as the one to beat. Leave NetSuite and Business Central off the shortlist unless you are willing to run customer EDI, labels and shop-floor reporting on other companies' add-ons.</p>

<h2>The result</h2>
<div class="split">
  <div>
    <p>I scored four cloud ERPs on 25 criteria, each from 1 to 5, and weighted them for a Tier 2 stamping supplier. {e(rank[0][0])} came first at {rank[0][1]:.2f} out of 5. {e(rank[1][0])} was second at {rank[1][1]:.2f}. {e(rank[2][0])} ({rank[2][1]:.2f}) and {e(rank[3][0])} ({rank[3][1]:.2f}) were well behind.</p>
    <p>No system is best everywhere. Plex is last on finance, where NetSuite is first.</p>
  </div>
  <figure>{bars(tot)}<figcaption>Overall weighted score, out of 5</figcaption></figure>
</div>
{table(["Category", "Weight"] + V, cat_rows, ["31%", "9%", "14%", "17%", "15%", "14%"], "num")}

<h2>The ranking depends on six rows</h2>
<p>Six of the 25 criteria are specific to automotive: EDI releases, CUM tracking, customer labels, lot traceability and two quality rows. I gave them {auto_w}% of the weight because 78% of Corvane's revenue ships against EDI releases and the plant is IATF 16949 certified.</p>
<p>Take those six rows out and the four systems are close: {", ".join(f"{e(v)} {s:.2f}" for v, s in rest_rank)}. Almost the whole gap between first and last comes from that one block. So the question for the three of you is how much those rows should count, and the workbook lets you change it.</p>
{table(["Whose weights", "What they stress", "Comes first", "Second"], scen_rows, ["16%", "38%", "23%", "23%"])}
<p class="after">The CFO column is the one that changes the answer. Scored that way, {e(cfo[0][0])} wins. I think that view is wrong for this company, because a late ASN or a wrong label costs chargebacks and delivery ratings with customers, and a slow month-end close does not. But it is a fair reading of the same scores and you should know it is there. NetSuite comes first only when finance and reporting is at least {ns_fin:.0%} of the decision.</p>

<h2>What I am least sure of</h2>
<ul class="gap">
<li><b>Cost.</b> Only Microsoft publishes prices. For the other three I used third-party starting prices and my own assumptions, marked yellow in the workbook. On those numbers the four land between {money(min(cost.values()))} and {money(max(cost.values()))} over five years, which is closer together than my error on any one of them.</li>
<li><b>What cost can and cannot decide here.</b> Cost carries {cost_w}% of the weight, so even at double my estimate Plex stays first ({doubled["Plex"]:.2f} against {doubled[rank[1][0]]:.2f}). That is a limit of weighted scoring. Once real quotes are in, treat a large price gap as its own decision.</li>
<li><b>Scores from reading, not from demos.</b> I worked from vendor pages, consultancy pages and third-party research. {counts["Sourced"]} of the 25 rows rest fully on sources, {counts["Partly sourced"]} partly, and {counts["Judgment"]} are my judgment. Every row in the workbook says which.</li>
<li><b>Business Central is moving.</b> It gained built-in quality inspections in April 2026. I scored that as basic because it is new and covers inspections only. It could look different in a year.</li>
<li><b>Epicor has two products.</b> It also sells CMS, an ERP built only for automotive suppliers. I scored Kinetic because it is the cloud product. Ask Epicor which of the two they would propose.</li>
<li><b>The long list.</b> QAD and Infor CloudSuite Automotive belong on a real one. I kept this comparison to four.</li>
</ul>

<h2>What I would do next</h2>
<ol class="gap">
<li>Give both vendors the same demo script, built from one real week: one customer's 830 and 862 files, a coil receipt, a press run with scrap, a welded assembly, a shipment with labels and an ASN, and a CUM that does not match the customer's.</li>
<li>Ask each for a written five-year quote for {d.SHARED["full_users"]} office users and {d.SHARED["light_users"]} floor users, with EDI, quality and MES priced line by line.</li>
<li>Call two metal-forming suppliers of similar size on each system.</li>
<li>Rescore the workbook after the demos, with the plant manager, quality manager, controller and EDI coordinator each scoring their own rows.</li>
</ol>

<p class="fict">{e(d.COMPANY)} is a made-up company and this is a portfolio case study. The four vendors are real. What is said about them comes from the public sources listed in the workbook, checked {d.CHECKED}, and is not an endorsement of any of them.</p>
"""


def css():
    font = os.environ.get("MEMO_FONT", "")
    face = f'@font-face{{font-family:"Memo";font-weight:400 700;src:url("file://{font}") format("woff2")}}' if font and os.path.exists(font) else ""
    return face + """
*{box-sizing:border-box}
html{font-family:"Memo",Arial,Helvetica,sans-serif;font-size:9.6pt;line-height:1.46;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0}
h1,h2,p,ul,ol,figure,dl{margin:0}
.kind{font-size:10.5pt;color:#5f5f5f}
h1{margin-top:.2rem;font-weight:500;font-size:25pt;line-height:1.05;letter-spacing:-.04em}
header dl{display:grid;grid-template-columns:1.5fr .9fr 1fr 1.6fr;gap:0 1.2rem;margin-top:.8rem;padding:.45rem 0;border-top:1px solid #000;border-bottom:1px solid #000}
dt{font-size:8.2pt;color:#5f5f5f}dd{margin:.05rem 0 0;font-weight:500;font-size:9.6pt}
.lead{margin-top:.9rem;font-size:12pt;line-height:1.4;letter-spacing:-.01em}
h2{font-weight:500;font-size:13pt;letter-spacing:-.025em;margin:1.15rem 0 .45rem;break-after:avoid}
p{margin-bottom:.45rem}
p.after{margin-top:.8rem}
b{font-weight:600}
.split{display:grid;grid-template-columns:1fr 1.05fr;gap:0 1.6rem;align-items:start;margin-bottom:.5rem}
figure svg{width:100%;height:auto;display:block}
figcaption{margin-top:.2rem;font-size:8.2pt;color:#5f5f5f}
svg text{font-family:"Memo",Arial,sans-serif;font-size:11px}
svg .tick{fill:#5f5f5f;font-size:10px}svg .val{font-weight:600}
table{width:100%;border-collapse:collapse;font-size:8.9pt;line-height:1.4;table-layout:fixed;margin-top:.3rem}
th{text-align:left;font-weight:500;font-size:8.2pt;color:#5f5f5f;padding:.3rem .5rem .3rem 0;border-bottom:1px solid #000;vertical-align:bottom}
td{padding:.2rem .5rem .2rem 0;border-bottom:1px solid #d9d9d9;vertical-align:top}
table.num td:not(:first-child),table.num th:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
table.num tr:last-child td{border-bottom:0;border-top:1px solid #000}
ul,ol{padding-left:1.1rem}
table{break-inside:avoid}
.gap li{margin-bottom:.32rem}
.fict{margin-top:1rem;padding-top:.55rem;border-top:1px solid #000;font-size:8.6pt;color:#5f5f5f}
"""


def page():
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Which ERP for {e(d.COMPANY)}</title><style>{css()}</style></head><body>{body()}</body></html>'


async def render(path=OUT):
    from playwright.async_api import async_playwright
    src = os.path.join(ROOT, "_memo.html")
    open(src, "w", encoding="utf-8").write(page())
    async with async_playwright() as p:
        chrome = os.environ.get("CHROME")
        b = await p.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + src)
        await pg.wait_for_timeout(500)
        foot = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5pt;color:#5f5f5f;padding:0 0.9in;display:flex;justify-content:space-between">'
                f'<span>{e(d.COMPANY)} ERP selection memo. Made-up company, real vendors.</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
        await pg.pdf(path=path, format="Letter", print_background=True, display_header_footer=True, header_template="<span></span>",
                     footer_template=foot, margin={"top": "0.7in", "bottom": "0.8in", "left": "0.9in", "right": "0.9in"})
        await b.close()
    os.remove(src)
    return path


if __name__ == "__main__":
    print(asyncio.run(render()))
