import sqlite3

c = sqlite3.connect("database/beverages.db")
cur = c.execute("select * from products")
cols = [d[0] for d in cur.description]
print("COLUMNS:", cols)
print()
for r in cur.fetchall():
    print(r)
