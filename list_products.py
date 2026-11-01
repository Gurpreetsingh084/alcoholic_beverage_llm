import sqlite3, csv, difflib

c = sqlite3.connect("database/beverages.db")
rows = c.execute(
    "select product_id, merchant_id, product_name, brand, price, raw_source_url "
    "from products where product_id not like 'TEST%' order by product_name, merchant_id"
).fetchall()

groups = {}
for r in rows:
    groups.setdefault(r[2].strip().lower(), []).append(r)

print("Listings:", len(rows), "| Unique products:", len(groups))
print()

with open("products_20.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["#", "product_name", "brand", "merchants", "prices", "urls"])
    for i, (key, items) in enumerate(groups.items(), 1):
        name = items[0][2]
        brand = items[0][3]
        merchants = " + ".join(x[1] for x in items)
        prices = " / ".join(str(x[4]) for x in items)
        urls = " | ".join(x[5] for x in items)
        w.writerow([i, name, brand, merchants, prices, urls])
        print(i, name, "|", brand, "|", merchants, "|", prices)

print()
print("Possible near-duplicates (check by eye):")
keys = list(groups.keys())
found = False
for a in range(len(keys)):
    for b in range(a + 1, len(keys)):
        s = difflib.SequenceMatcher(None, keys[a], keys[b]).ratio()
        if s >= 0.85:
            found = True
            print(" ", keys[a], "<->", keys[b], round(s, 2))
if not found:
    print("  none")
