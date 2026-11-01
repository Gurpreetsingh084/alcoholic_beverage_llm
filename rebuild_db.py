"""Re-saves the products already extracted by main.py (from data/processed/merchants/*.json)
into the SQLite database. Makes NO OpenAI calls, so your benchmark numbers do not change.
Use it only if database/beverages.db is empty or missing the pipeline rows.
Run:  py -3.11 rebuild_db.py   then   py -3.11 show_db.py"""
import glob
import json

from database.crud import save_product_to_db

files = sorted(glob.glob("data/processed/merchants/*.json"))
if not files:
    raise SystemExit("No files in data/processed/merchants/. Run main.py first.")

saved = 0
for path in files:
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    for product in doc.get("products", []):
        save_product_to_db(product)
        saved += 1
print(f"Re-saved {saved} products from {len(files)} merchant files into database/beverages.db")
