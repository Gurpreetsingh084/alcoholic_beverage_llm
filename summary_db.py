import sqlite3

c = sqlite3.connect("database/beverages.db")
print("Total rows:", c.execute("select count(*) from products").fetchone()[0])
print("Excluding TEST rows:", c.execute("select count(*) from products where product_id not like 'TEST%'").fetchone()[0])
print("Distinct merchants:", c.execute("select count(distinct merchant_id) from products where product_id not like 'TEST%'").fetchone()[0])
print()
print("Rows per merchant:")
for m, n in c.execute("select merchant_id, count(*) from products group by merchant_id order by merchant_id"):
    print(" ", m, n)
print()
print("Names appearing more than once:")
for name, n in c.execute("select product_name, count(*) from products where product_id not like 'TEST%' group by product_name having count(*) > 1"):
    print(" ", name, n)
