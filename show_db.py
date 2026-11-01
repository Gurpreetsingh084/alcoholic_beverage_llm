"""Prints the SQLite database in a readable table (for report screenshots).
Run:  py -3.11 show_db.py
Real pipeline rows have IDs like nz_01_PROD_001; test rows (e.g. TEST_PROD_999) are hidden."""
import sqlite3

DB = "database/beverages.db"
con = sqlite3.connect(DB)

tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
print("Database:", DB)
print("Tables  :", tables)

total = con.execute("select count(*) from products").fetchone()[0]
rows = con.execute(
    "select product_id, merchant_id, product_name, brand, category, abv, bottle_size, "
    "country_of_origin, price from products order by product_id"
).fetchall()
real = [r for r in rows if "_PROD_" in r[0] and r[0][:3] in ("nz_", "int")]
print(f"Rows in products table: {total}  (pipeline rows shown below: {len(real)}, test rows hidden: {total - len(real)})")
print()

head = ["product_id", "merchant", "product_name", "brand", "category", "abv", "size", "country", "price"]
widths = [16, 8, 34, 12, 9, 5, 7, 14, 7]
def fmt(vals):
    out = []
    for v, w in zip(vals, widths):
        s = "" if v is None else str(v)
        out.append(s[:w].ljust(w))
    return " | ".join(out)
print(fmt(head))
print("-" * (sum(widths) + 3 * (len(widths) - 1)))
for r in real:
    print(fmt(r))
con.close()
