"""Everything the comparison is built from: the company, the criteria, the scores,
the cost inputs and the sources. Change something here and rebuild.

Corvane Metalform is a made-up company. The four vendors are real, and what is
said about them comes from the public sources listed at the bottom of this file,
checked on the date in CHECKED.
"""

AUTHOR = "Harsh Marlecha"
CHECKED = "November 17, 2026"
COMPANY = "Corvane Metalform"

PROFILE = [
    ("What it makes", "Metal stampings and welded assemblies for seats, brackets and body structures"),
    ("Position", "Tier 2 automotive supplier. Sells to nine Tier 1 customers."),
    ("Revenue", "$40 million a year"),
    ("Site", "One plant in northwest Ohio, two shifts, 185 people"),
    ("Equipment", "14 presses, 6 robotic weld cells"),
    ("How orders arrive", "78% of revenue ships against EDI releases (830 and 862). Customers expect an ASN (856) and their own label on every container."),
    ("Quality", "IATF 16949 certified. PPAP on every new part, traceability from steel coil to shipped container."),
    ("Today", "A 19 year old on-premise ERP the vendor stopped supporting, a separate EDI translator, paper travelers on the floor, and spreadsheets for scheduling and CUMs."),
    ("People who would use it", "32 office users and 24 shop-floor users"),
    ("IT team", "Two people"),
]

VENDORS = ["NetSuite", "Business Central", "Epicor Kinetic", "Plex"]
VENDOR_FULL = {
    "NetSuite": "Oracle NetSuite",
    "Business Central": "Microsoft Dynamics 365 Business Central (Premium)",
    "Epicor Kinetic": "Epicor Kinetic",
    "Plex": "Plex Smart Manufacturing Platform (Rockwell Automation)",
}

SCALE = [
    (5, "Built in, and a known strength for automotive suppliers"),
    (4, "Built in and solid"),
    (3, "Built in but basic, or needs a separate module from the same vendor"),
    (2, "Needs a third-party product or custom work"),
    (1, "Not available"),
]

BASIS = {
    "Sourced": "Every score in the row rests on a listed source.",
    "Partly sourced": "At least one vendor's score is my judgment. Check it in a demo.",
    "Judgment": "No direct source. My reading of the products. Check it in a demo.",
}

CATEGORIES = [
    "Automotive requirements",
    "Manufacturing and shop floor",
    "Finance and reporting",
    "Technology",
    "Vendor and implementation",
    "Cost",
]

COST_ID = "F1"  # this row's scores are calculated from the cost model

# id, category, criterion, weight, [NetSuite, Business Central, Epicor Kinetic, Plex], basis, why, sources
CRITERIA = [
    ("A1", 0, "EDI releases in, ASNs and invoices out (830, 862, 856, 810)", 8, [2, 2, 4, 5], "Sourced",
     "NetSuite and Business Central have no EDI engine of their own and rely on a third-party service. Kinetic has an EDI and demand management module, though one automotive customer added a partner product on top of it. Plex sells EDI as part of the same platform.",
     "S03 S16 S10 S11 S06"),
    ("A2", 0, "Cumulative (CUM) tracking and release accounting", 5, [2, 2, 4, 5], "Partly sourced",
     "This is where automotive differs most from general manufacturing. NetSuite and Business Central get there through partner work. Kinetic handles release schedules in demand management; how well it reconciles CUMs is my judgment. Plex has sold release accounting for over ten years.",
     "S15 S18 S11 S19"),
    ("A3", 0, "Customer labels and container tracking", 3, [2, 2, 3, 5], "Partly sourced",
     "Plex tracks stock by labeled container as part of how it works (my judgment, not sourced). Kinetic prints labels, but the customer in S11 added a partner product to meet automotive label rules. The other two need an add-on.",
     "S11 S15"),
    ("A4", 0, "Lot and heat traceability, steel coil to shipped part", 6, [4, 4, 4, 5], "Sourced",
     "All four track lots without add-ons. Plex scores higher because production and inventory share one database, so the trail from coil to container needs no stitching together.",
     "S04 S15 S09 S07"),
    ("A5", 0, "Inspections, nonconformance and corrective action", 4, [3, 3, 4, 5], "Sourced",
     "NetSuite's quality module is a SuiteApp that a NetSuite consultancy calls basic. Business Central only got built-in inspections in April 2026. Kinetic has quality assurance in the core product and a separate QMS. Plex includes a QMS.",
     "S24 S16 S02 S23 S10 S05"),
    ("A6", 0, "PPAP and APQP, control plans, gauge calibration", 4, [2, 2, 3, 5], "Partly sourced",
     "NetSuite partners set up PPAP on top of the quality SuiteApp. Business Central's new module covers inspections only. Kinetic covers PPAP and APQP documents through Epicor QMS, a separate product. Plex's coverage of gauges and control plans is my judgment.",
     "S15 S02 S20 S07"),

    ("B1", 1, "MRP driven by customer release demand", 5, [3, 3, 4, 4], "Partly sourced",
     "All four run MRP. In NetSuite and Business Central the release demand has to arrive through the EDI add-on first, which is one more thing to keep in step.",
     "S15 S10"),
    ("B2", 1, "Finite scheduling of presses and weld cells", 4, [3, 2, 5, 4], "Partly sourced",
     "Kinetic lists infinite, finite and constraint-based scheduling plus an advanced planning module. Plex has constraint-based scheduling. NetSuite users often add a scheduling SuiteApp. Business Central's score is my judgment: finite scheduling there usually means a partner product.",
     "S10 S05 S17"),
    ("B3", 1, "Shop-floor reporting and machine data (MES)", 6, [3, 2, 4, 5], "Partly sourced",
     "Plex's MES is part of the ERP. Kinetic has data collection built in and sells an advanced MES module. NetSuite has a mobile app for production reporting but consultancies list shop-floor data collection as an integration. Business Central's score is my judgment.",
     "S05 S07 S10 S17 S16"),
    ("B4", 1, "Tooling, dies and preventive maintenance", 3, [2, 2, 4, 4], "Judgment",
     "Die life and press maintenance matter in a stamping plant. Plex and Kinetic both sell maintenance as part of their own suites. NetSuite partners list asset maintenance as SuiteApp territory. Business Central's score is my judgment.",
     "S17 S05"),
    ("B5", 1, "Inventory, bins and barcode scanning", 4, [4, 4, 4, 4], "Partly sourced",
     "No real difference. All four handle bin locations and scanning with their own warehouse features.",
     "S15 S22 S10"),

    ("C1", 2, "General ledger, payables, receivables and month-end close", 5, [5, 4, 4, 3], "Partly sourced",
     "NetSuite started as an accounting system and it shows. Plex was built from the shop floor up. That its finance is thinner than the others is my judgment.",
     "S14 S07"),
    ("C2", 2, "Standard cost and variance by part", 4, [3, 4, 5, 4], "Judgment",
     "Kinetic's roots are in job costing for manufacturers. NetSuite's costing is fine for simple routings and thinner once labor and overhead need to be split by operation.",
     ""),
    ("C3", 2, "Reporting and dashboards", 3, [5, 4, 3, 3], "Judgment",
     "NetSuite's saved searches and Business Central with Power BI are both stronger for a controller building their own reports than what Kinetic or Plex ship with.",
     ""),
    ("C4", 2, "Purchasing and supplier schedules", 2, [4, 4, 4, 3], "Partly sourced",
     "A third-party comparison marks procurement as a weaker area for Plex. The other three are my judgment.",
     "S25"),

    ("D1", 3, "Cloud delivery and upgrades", 3, [5, 5, 3, 5], "Sourced",
     "NetSuite, Business Central and Plex are cloud products with upgrades handled by the vendor. Kinetic runs in the cloud, on premise or both, and its newer screens do not yet cover everything the older client did.",
     "S14 S02 S07 S20 S25"),
    ("D2", 3, "APIs and integration tools", 3, [4, 5, 4, 3], "Judgment",
     "Business Central sits inside Microsoft's platform, which a two-person IT team can do a lot with. Kinetic has REST services. Plex's score is my judgment.",
     "S10"),
    ("D3", 3, "Changes without custom code", 2, [4, 4, 4, 3], "Judgment",
     "NetSuite, Business Central and Kinetic each have their own tools for adding fields, forms and workflows. Plex is more fixed.",
     "S10"),
    ("D4", 3, "Roles, approvals and audit trail", 2, [4, 4, 4, 4], "Judgment",
     "No meaningful difference that I could find.",
     ""),

    ("E1", 4, "Automotive suppliers of this size already using it", 4, [2, 2, 4, 5], "Sourced",
     "Plex was designed by an auto supplier. A third-party guide names QAD, Plex and Epicor Kinetic as the automotive picks. NetSuite and Business Central reach automotive through partners.",
     "S05 S18 S15"),
    ("E2", 4, "Implementation partners within reach of Ohio", 3, [4, 5, 3, 2], "Judgment",
     "Business Central is only sold through partners and there are many of them. Plex has the smallest partner bench of the four.",
     ""),
    ("E3", 4, "Vendor stability and product roadmap", 3, [5, 5, 4, 4], "Partly sourced",
     "Oracle and Microsoft are not going anywhere. Plex is owned by Rockwell Automation. Epicor is a large private company.",
     "S05 S06"),
    ("E4", 4, "Ease of use for office and floor staff", 2, [4, 4, 3, 4], "Partly sourced",
     "A third-party review calls Plex easy to navigate. Kinetic is midway through moving its screens to a new interface. NetSuite and Business Central are my judgment.",
     "S07 S25"),

    ("F1", 5, "Five-year cost (calculated on the Cost sheet)", 9, [None, None, None, None], "Partly sourced",
     "Scored by formula: 5 times the cheapest five-year cost, divided by this vendor's. Only Business Central publishes its prices. The other three are third-party starting prices plus my assumptions.",
     "S01 S08 S13"),
    ("F2", 5, "Published, predictable pricing", 3, [2, 5, 2, 2], "Sourced",
     "Microsoft publishes Business Central's price per user. Oracle has no public price list for NetSuite. Epicor and Plex both price by quote.",
     "S01 S13 S21"),
]

# ---- Cost model -------------------------------------------------------------------------
SHARED = {
    "full_users": 32,
    "light_users": 24,
    "years": 5,
    "increase": 0.05,
    "contingency": 0.15,
    "hardware": 45000,
}
SHARED_NOTES = {
    "full_users": "From the company profile.",
    "light_users": "From the company profile.",
    "years": "The usual horizon for an ERP decision.",
    "increase": "My assumption. A NetSuite consultancy says to expect 5 to 8% at renewal (S13). Applied to all four.",
    "contingency": "My assumption.",
    "hardware": "My assumption. Scanners, label printers and floor terminals. Same for all four.",
}

# per vendor: full user $/mo, light user $/mo, platform $/mo, modules $/yr, EDI $/yr, implementation $
COST = {
    "NetSuite":         {"full": 129, "light": 20,  "platform": 999, "modules": 30000, "edi": 25000, "impl": 200000},
    "Business Central": {"full": 110, "light": 8,   "platform": 0,   "modules": 23000, "edi": 30000, "impl": 210000},
    "Epicor Kinetic":   {"full": 100, "light": 40,  "platform": 0,   "modules": 45000, "edi": 15000, "impl": 260000},
    "Plex":             {"full": 120, "light": 120, "platform": 0,   "modules": 0,     "edi": 12000, "impl": 280000},
}

PUB, TP, MINE = "Published price", "Third-party estimate", "My assumption"
COST_BASIS = [
    ("NetSuite", "Full user", TP, "A NetSuite consultancy puts full users at $129 to $199 a month. I used the low end.", "S13"),
    ("NetSuite", "Shop-floor user", TP, "Self-service users are quoted at $15 to $25. Whether floor reporting can run on that tier needs confirming.", "S13"),
    ("NetSuite", "Platform fee", TP, "Base platform is commonly quoted from $999 a month.", "S13 S14"),
    ("NetSuite", "Modules and add-ons", MINE, "Manufacturing, warehouse, quality and demand planning modules. No public price.", ""),
    ("NetSuite", "EDI", MINE, "Third-party EDI service plus the release and CUM logic it needs.", ""),
    ("NetSuite", "Implementation", MINE, "Above the $25K to $150K a consultancy quotes for general projects, because release accounting has to be built.", "S13"),
    ("Business Central", "Full user", PUB, "Premium, $110 per user per month, paid yearly. Premium is the plan that includes manufacturing.", "S01 S22"),
    ("Business Central", "Shop-floor user", PUB, "Team Member, $8 per user per month. Floor reporting would likely run through a partner product instead.", "S01"),
    ("Business Central", "Platform fee", PUB, "None.", "S01"),
    ("Business Central", "Modules and add-ons", MINE, "Partner products for shop-floor data collection and finite scheduling. No single public price.", ""),
    ("Business Central", "EDI", MINE, "Partner EDI product and service with automotive releases and labels.", "S03"),
    ("Business Central", "Implementation", MINE, "Includes fitting three partner products together.", ""),
    ("Epicor Kinetic", "Full user", TP, "Third-party research lists Kinetic from $100 per user per month. Epicor prices by quote.", "S08 S21"),
    ("Epicor Kinetic", "Shop-floor user", MINE, "No public price for data collection seats.", ""),
    ("Epicor Kinetic", "Platform fee", MINE, "None assumed.", ""),
    ("Epicor Kinetic", "Modules and add-ons", MINE, "Advanced MES, QMS and advanced planning on top of the starting price.", "S10"),
    ("Epicor Kinetic", "EDI", MINE, "EDI and demand management module plus trading partner fees.", "S10"),
    ("Epicor Kinetic", "Implementation", MINE, "Inside the $100K to $500K typical project range from third-party research.", "S08"),
    ("Plex", "Full user", TP, "Third-party research lists Plex from $120 per user per month. Plex prices by quote.", "S08 S21"),
    ("Plex", "Shop-floor user", MINE, "I assumed no cheaper tier for floor users, so the same $120.", ""),
    ("Plex", "Platform fee", MINE, "None assumed.", ""),
    ("Plex", "Modules and add-ons", MINE, "I assumed MES and QMS come with the platform. That may be generous. The Sensitivity sheet tests it.", "S06"),
    ("Plex", "EDI", MINE, "Trading partner and network fees.", ""),
    ("Plex", "Implementation", MINE, "Inside the $100K to $600K typical project range. Higher than the others because the MES goes onto the floor at the same time.", "S08"),
]

# ---- Weight scenarios (by category, same order as CATEGORIES) ---------------------------
SCENARIOS = [
    ("Plant manager", "Shop floor first", [30, 35, 8, 7, 10, 10]),
    ("CFO", "Finance and cost first", [10, 10, 30, 15, 15, 20]),
    ("Equal", "Every category the same", [1, 1, 1, 1, 1, 1]),
    ("Cost first", "A third of the decision is cost", [20, 15, 10, 10, 10, 35]),
]

# ---- Sources ---------------------------------------------------------------------------
V, P, R, T = "Vendor", "Consultancy or reseller", "Third-party research", "Trade press"
SOURCES = [
    ("S01", "Microsoft", "Dynamics 365 Business Central pricing", V,
     "Essentials $80, Premium $110, Team Members $8 per user per month, paid yearly. Premium adds manufacturing.",
     "https://www.microsoft.com/en-us/dynamics-365/products/business-central/pricing"),
    ("S02", "Rand Group", "How quality management works in Dynamics 365 Business Central", P,
     "Built-in quality inspections arrived with 2026 release wave 1 (version 28), April 2026. Before that it took a partner product.",
     "https://www.randgroup.com/insights/microsoft/dynamics-365/business-central/how-quality-management-works-in-dynamics-365-business-central/"),
    ("S03", "ERP Software Blog", "Dynamics 365 EDI: complete guide (September 2026)", P,
     "Dynamics 365 has no complete EDI of its own. Most Business Central users add an extension or an outside EDI provider.",
     "https://erpsoftwareblog.com/2026/09/dynamics-365-edi-complete-guide/"),
    ("S04", "Rand Group", "Lot and serial number tracking in Dynamics 365 Business Central", P,
     "Business Central tracks lot, serial and package numbers without add-ons.",
     "https://www.randgroup.com/insights/microsoft/dynamics-365/business-central/lot-and-serial-number-tracking-in-dynamics-365-business-central/"),
    ("S05", "Rockwell Automation", "Plex: automotive manufacturing", V,
     "Plex was designed by an auto supplier. MES, QMS and constraint-based scheduling are part of the platform.",
     "https://www.rockwellautomation.com/content/plex/global/apac/en/industries/automotive.html"),
    ("S06", "Rockwell Automation", "Plex chosen by Somic America (press release, July 2024)", V,
     "Describes Plex as one platform for ERP, MES, QMS and EDI.",
     "https://plex.rockwellautomation.com/en-us/company/newsroom/plex-chosen-as-partner-by-somic-america-to-modernize-technology-systems.html"),
    ("S07", "ERP Research", "Plex ERP profile", R,
     "Cloud only, no on-premise option. MES and QMS are built in and share one database with the ERP. Described as easy to navigate.",
     "https://www.erpresearch.com/en-us/plex-erp"),
    ("S08", "ERP Research", "Epicor Kinetic vs Plex Manufacturing Cloud: 2026 comparison", R,
     "Kinetic from $100 per user per month, 5 to 10 months, $100K to $500K typical project. Plex from $120, 4 to 9 months, $100K to $600K.",
     "https://www.erpresearch.com/compare/epicor-kinetic-vs-plex"),
    ("S09", "Epicor", "Automotive industry page", V,
     "Lists automotive EDI, tracking and traceability, and MMOG/LE compliance.",
     "https://www.epicor.com/en-gb/solutions/industries/manufacturing/automotive/"),
    ("S10", "Epicor", "Kinetic production management suite brochure (copy hosted by a reseller)", V,
     "Module list: data collection, advanced MES, quality assurance, QMS, advanced planning and scheduling, finite and constraint-based scheduling, EDI and demand management, REST services.",
     "https://atc.gr/wp-content/uploads/2022/08/MFG-Kinetic-Production-Management-Suite-BR-ENS.pdf"),
    ("S11", "ERP Today", "DPC enhances automotive EDI with AIM AutoCOR and Epicor Kinetic", T,
     "An automotive plastics supplier on Kinetic added a partner product for EDI and barcode labels, working with Kinetic's demand management module.",
     "https://erp.today/dpc-enhances-automotive-edi-with-aim-autocor-and-epicor-kinetic/"),
    ("S12", "Epicor", "Epicor CMS product page", V,
     "Epicor also sells CMS, an ERP built only for automotive suppliers, with EDI for the major OEMs built in.",
     "https://www.epicor.com/en/products/enterprise-resource-planning-erp/cms/"),
    ("S13", "BrokenRubik", "NetSuite pricing: the definitive guide", P,
     "No public price list. About $999 a month base, $129 to $199 per full user, $15 to $25 self-service, implementation $25K to $150K, 5 to 8% increases at renewal.",
     "https://www.brokenrubik.com/blog/netsuite-pricing-the-definitive-guide"),
    ("S14", "ERP Research", "Oracle NetSuite ERP review 2026", R,
     "Multi-tenant cloud with two automatic updates a year. Pricing is base platform plus per user.",
     "https://www.erpresearch.com/pages/en-us/netsuite-erp"),
    ("S15", "Logan Consulting", "NetSuite for automotive", P,
     "A NetSuite partner's automotive offer: EDI integration, quality management SuiteApp for PPAP and inspections, lot and serial control, release-driven planning.",
     "https://www.loganconsulting.com/netsuite-for-automotive/"),
    ("S16", "BrokenRubik", "NetSuite for manufacturing: the complete capability guide", P,
     "Quality management is basic in NetSuite. EDI and shop-floor data collection come through integrations.",
     "https://brokenrubik.com/blog/netsuite-manufacturing-complete-guide"),
    ("S17", "Folio3", "NetSuite manufacturing SuiteApps", P,
     "Manufacturers add SuiteApps for scheduling, shop-floor data capture, quality, EDI and maintenance. NetSuite has a mobile app for manufacturing transactions.",
     "https://netsuite.folio3.com/?p=43403"),
    ("S18", "ERP Research", "Automotive ERP systems", R,
     "Names QAD, Plex and Epicor Kinetic as the automotive picks and lists what suppliers need: 830 and 862 releases, CUM reconciliation, ASNs with customer labels, PPAP and APQP.",
     "https://erpresearch.com/industries/manufacturing/automotive"),
    ("S19", "Manufacturing.net", "Must-have ERP features for the automotive industry (2014)", T,
     "Describes Plex's release accounting module. Old, which is the point: it has been there a long time.",
     "https://www.manufacturing.net/operations/article/13240634/musthave-erp-features-for-the-automotive-industry"),
    ("S20", "ERP Research", "Epicor Kinetic for automotive", R,
     "Lists EDI with OEMs and PPAP and APQP quality documents among Kinetic's automotive features. Cloud, on premise or hybrid.",
     "https://erpresearch.com/en-us/epicor-kinetic-for-automotive"),
    ("S21", "US Tech Automations", "Plex vs Epicor: manufacturing fit compared for 2026", R,
     "Both Plex and Epicor Kinetic price by quote.",
     "https://ustechautomations.com/resources/blog/plex-vs-epicor-2026"),
    ("S22", "Encore Business Solutions", "Licensing and pricing answers for Dynamics 365 Business Central", P,
     "Current prices took effect November 1, 2025. Essentials already includes warehouse management.",
     "https://www.encorebusiness.com/blog/dynamics-365-business-central-licensing-and-pricing-answers/"),
    ("S23", "Dynamics Communities", "Microsoft builds quality management for Business Central on Insight Works technology", T,
     "The new quality module is a licensed subset of a partner's product.",
     "https://dynamicscommunities.com/industries/microsoft-builds-quality-management-for-business-central-on-insight-works-technology/"),
    ("S24", "Anchor Group", "NetSuite quality management guide", P,
     "NetSuite quality management is a SuiteApp covering specifications, inspections and conformance actions.",
     "https://www.anchorgroup.tech/blog/netsuite-quality-management-guide"),
    ("S25", "ERP Research", "Epicor Kinetic vs Plex Manufacturing Cloud for manufacturing", R,
     "Plex scores weaker on procurement. Kinetic's new interface is still being extended to cover every older screen, and moving to its cloud from on-premise Epicor takes a re-implementation.",
     "https://www.erpresearch.com/compare/epicor-kinetic-vs-plex-for-manufacturing"),
]
