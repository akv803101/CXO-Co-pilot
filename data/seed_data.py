import sqlite3, json, csv, os

BASE      = os.path.dirname(os.path.abspath(__file__))
DB_PATH   = os.path.join(BASE, "glowkart.db")
JSON_PATH = os.path.join(BASE, "pipeline.json")
CSV_PATH  = os.path.join(BASE, "campaigns.csv")

# ── 1. SQLite ───────────────────────────────────────────────────────────────
def seed_sqlite():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("DROP TABLE IF EXISTS forecast")
    cur.execute("""CREATE TABLE orders (
        id INTEGER PRIMARY KEY, date TEXT, region TEXT,
        product TEXT, units INTEGER, revenue REAL, quarter TEXT)""")
    cur.execute("""CREATE TABLE forecast (
        quarter TEXT, region TEXT, target REAL, actual REAL)""")

    orders = [
        ("2024-01-15","North","Serum",       420, 840000,  "Q1"),
        ("2024-01-20","South","Moisturiser", 300, 540000,  "Q1"),
        ("2024-02-10","East", "Serum",       510, 1020000, "Q1"),
        ("2024-02-14","West", "Sunscreen",   280, 420000,  "Q1"),
        ("2024-03-05","South","Serum",       190, 380000,  "Q1"),
        ("2024-03-18","North","Sunscreen",   350, 525000,  "Q1"),
        ("2024-04-02","East", "Moisturiser", 400, 720000,  "Q2"),
        ("2024-04-22","West", "Serum",       330, 660000,  "Q2"),
        ("2024-05-10","North","Sunscreen",   490, 735000,  "Q2"),
        ("2024-05-28","South","Serum",       210, 420000,  "Q2"),
    ]
    cur.executemany(
        "INSERT INTO orders (date,region,product,units,revenue,quarter) VALUES (?,?,?,?,?,?)",
        orders)

    forecasts = [
        ("Q1","North", 1500000, 1365000),
        ("Q1","South", 1200000, 920000),   # missed 23%
        ("Q1","East",  1400000, 1020000),
        ("Q1","West",  900000,  420000),   # missed 53%
        ("Q2","North", 1600000, 1735000),  # beat target
        ("Q2","South", 1300000, 420000),
        ("Q2","East",  1500000, 720000),
        ("Q2","West",  1000000, 660000),
    ]
    cur.executemany("INSERT INTO forecast VALUES (?,?,?,?)", forecasts)
    conn.commit(); conn.close()
    print("OK SQLite seeded")

# ── 2. JSON ─────────────────────────────────────────────────────────────────
def seed_json():
    pipeline = {
        "deals": [
            {"id":1,"name":"BigBasket Enterprise","rep":"Priya", "stage":"Proposal",   "value":2400000,"close_date":"2024-06-30","risk":"High"},
            {"id":2,"name":"Nykaa Direct",        "rep":"Rohan", "stage":"Negotiation","value":1800000,"close_date":"2024-07-15","risk":"Medium"},
            {"id":3,"name":"Flipkart Beauty",     "rep":"Anita", "stage":"Discovery",  "value":3200000,"close_date":"2024-09-01","risk":"Low"},
            {"id":4,"name":"Myntra Skincare",     "rep":"Vikram","stage":"Proposal",   "value":1500000,"close_date":"2024-07-30","risk":"High"},
            {"id":5,"name":"Amazon Launchpad",    "rep":"Priya", "stage":"Closed Won", "value":2100000,"close_date":"2024-05-01","risk":"None"},
        ],
        "summary":{"total_pipeline_value":11000000,"deals_at_risk":3,"avg_deal_size":2200000,"q2_target":8000000}
    }
    with open(JSON_PATH,"w") as f: json.dump(pipeline, f, indent=2)
    print("OK JSON seeded")

# ── 3. CSV ──────────────────────────────────────────────────────────────────
def seed_csv():
    rows = [
        ["campaign","channel","spend","impressions","clicks","revenue_attributed","quarter"],
        ["Diwali_IG",    "Instagram",180000,420000,18200,920000, "Q1"],
        ["Diwali_Google","Google",   220000,680000,24400,1340000,"Q1"],
        ["Diwali_FB",    "Facebook", 150000,310000,9800, 480000, "Q1"],
        ["NewYear_IG",   "Instagram",95000, 210000,8900, 360000, "Q1"],
        ["Summer_Google","Google",   175000,540000,19200,840000, "Q2"],
        ["Summer_IG",    "Instagram",130000,380000,14100,610000, "Q2"],
        ["IPL_Sponsor",  "TV/OTT",   500000,2100000,0,  1200000,"Q2"],
    ]
    with open(CSV_PATH,"w",newline="") as f: csv.writer(f).writerows(rows)
    print("OK CSV seeded")

if __name__ == "__main__":
    seed_sqlite(); seed_json(); seed_csv()
    print("All GlowKart data ready!")