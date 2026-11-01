"""BBIM713 Capstone: field-level accuracy report (no OpenAI calls).

Compares the extracted catalogue with the hand-labelled answer key and prints,
for every field: correct / wrong / missing, precision, recall, F1 and accuracy.
  precision = correct / (correct + wrong)             (when it gives a value, is it right?)
  recall    = correct / (correct + wrong + missing)   (of all labelled values, how many found?)
  accuracy  = correct / products checked
Run:  py -3.11 field_accuracy.py
It only READS files that an earlier main.py run already saved in data/processed/, so you do NOT need to run main.py again.
"""
import csv
import glob
import json
import os
import re
from difflib import SequenceMatcher

TRUTH_PATH = "data/benchmark/ground_truth_sample.json"
CATALOG_PATH = "data/processed/master_beverage_catalog.json"
CATALOG_CSV = "data/processed/master_beverage_catalog.csv"   # used if the JSON is not there
MERCHANT_GLOB = "data/processed/merchants/*.json"            # last fallback: files main.py already wrote
METRICS_PATH = "data/processed/pipeline_metrics.json"
OUT_PATH = "data/processed/field_accuracy.json"
CSV_PATH = "data/processed/validation_results.csv"

FIELDS = ["product_name", "brand", "category", "abv", "bottle_size", "country_of_origin",
          "tasting_notes", "packaging", "product_description", "price"]
NUMERIC_TOL = {"abv": 0.05, "bottle_size": 0.5, "price": 0.01}   # absolute tolerance
FUZZY_MIN = {"tasting_notes": 0.6, "product_description": 0.6}   # long text: similarity >= this
NAME_MATCH_MIN = 0.6                                              # to pair a product with its answer-key row


def norm(s):
    return re.sub(r"\s+", " ", str(s).strip().lower())


def is_empty(v):
    return v is None or str(v).strip() in ("", "Unknown", "None", "nan")


def to_num(v):
    m = re.search(r"-?\d+(?:\.\d+)?", str(v).replace(",", ""))
    return float(m.group()) if m else None


def same(field, got, want):
    if field in NUMERIC_TOL:
        a, b = to_num(got), to_num(want)
        return a is not None and b is not None and abs(a - b) <= NUMERIC_TOL[field]
    if field in FUZZY_MIN:
        return SequenceMatcher(None, norm(got), norm(want)).ratio() >= FUZZY_MIN[field]
    return norm(got) == norm(want)


def load_list(path, keys):
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, dict):
        for k in keys:
            if isinstance(d.get(k), list):
                return d[k]
        raise SystemExit(f"{path}: expected a list or one of the keys {keys}")
    return d


def load_catalog():
    if os.path.exists(CATALOG_PATH):
        return load_list(CATALOG_PATH, ["beverages", "products"])
    if os.path.exists(CATALOG_CSV):
        with open(CATALOG_CSV, "r", encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))
    files = sorted(glob.glob(MERCHANT_GLOB))
    if files:
        rows = []
        for path in files:
            with open(path, "r", encoding="utf-8") as fh:
                rows.extend(json.load(fh).get("products", []))
        return rows
    raise SystemExit("No extracted data found in data/processed/. It is created by main.py (run it once).")


def find_match(truth_row, catalog, used):
    tid = truth_row.get("product_id")
    if tid:
        for i, c in enumerate(catalog):
            if i not in used and c.get("product_id") == tid:
                return i
    best, best_i = 0.0, None
    for i, c in enumerate(catalog):
        if i in used:
            continue
        r = SequenceMatcher(None, norm(c.get("product_name", "")), norm(truth_row.get("product_name", ""))).ratio()
        if r > best:
            best, best_i = r, i
    return best_i if best >= NAME_MATCH_MIN else None


def prf(c, w, m):
    p = c / (c + w) if c + w else 0.0
    r = c / (c + w + m) if c + w + m else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def main():
    truth = load_list(TRUTH_PATH, ["products", "ground_truth", "items", "data"])
    catalog = load_catalog()
    stats = {f: {"correct": 0, "wrong": 0, "missing": 0, "checked": 0} for f in FIELDS}
    per_product, used, detail = [], set(), []
    name_lenient = 0   # product_name marked INCORRECT only because one name contains the other

    for row in truth:
        idx = find_match(row, catalog, used)
        got_row = catalog[idx] if idx is not None else {}
        if idx is not None:
            used.add(idx)
        ok = checked = 0
        for f in FIELDS:
            want = row.get(f)
            if is_empty(want):
                continue                      # not labelled in the answer key
            s = stats[f]
            s["checked"] += 1
            checked += 1
            got = got_row.get(f)
            if is_empty(got):
                s["missing"] += 1
                status = "MISSING"
            elif same(f, got, want):
                s["correct"] += 1
                ok += 1
                status = "Correct"
            else:
                s["wrong"] += 1
                status = "INCORRECT"
                if f == "product_name" and (norm(want) in norm(got) or norm(got) in norm(want)):
                    name_lenient += 1
            detail.append({"product": row.get("product_name"), "field": f,
                           "actual": want, "extracted": "" if is_empty(got) else got, "status": status})
        per_product.append({"product": row.get("product_name"), "matched": idx is not None,
                            "fields_correct": ok, "fields_checked": checked})

    print("=" * 92)
    print("FIELD-LEVEL ACCURACY vs ANSWER KEY".center(92))
    print("=" * 92)
    print(f"{'Field':<22}{'Correct':>8}{'Wrong':>7}{'Missing':>9}{'Prec':>8}{'Recall':>8}{'F1':>8}{'Accuracy':>10}")
    print("-" * 92)
    C = W = M = N = 0
    out_fields = {}
    for f in FIELDS:
        s = stats[f]
        if not s["checked"]:
            continue
        p, r, f1 = prf(s["correct"], s["wrong"], s["missing"])
        acc = s["correct"] / s["checked"]
        out_fields[f] = {**s, "precision": round(p, 4), "recall": round(r, 4),
                         "f1": round(f1, 4), "accuracy": round(acc, 4)}
        print(f"{f:<22}{s['correct']:>8}{s['wrong']:>7}{s['missing']:>9}{p:>8.3f}{r:>8.3f}{f1:>8.3f}{acc:>10.1%}")
        C += s["correct"]; W += s["wrong"]; M += s["missing"]; N += s["checked"]
    p, r, f1 = prf(C, W, M)
    print("-" * 92)
    print(f"{'ALL FIELDS (micro)':<22}{C:>8}{W:>7}{M:>9}{p:>8.3f}{r:>8.3f}{f1:>8.3f}{C / N if N else 0:>10.1%}")
    print("\nPer product (fields correct / fields checked):")
    for pp in per_product:
        flag = "" if pp["matched"] else "  <-- no extracted match found"
        print(f"  {str(pp['product'])[:46]:<46} {pp['fields_correct']}/{pp['fields_checked']}{flag}")

    found = sum(1 for pp in per_product if pp["matched"])
    full = sum(1 for pp in per_product if pp["fields_checked"] and pp["fields_correct"] == pp["fields_checked"])
    print("\n" + "=" * 92)
    print("FINAL ACCURACY".center(92))
    print("=" * 92)
    print(f"Products found in the catalogue : {found} of {len(per_product)}")
    print(f"Products with every field right : {full} of {len(per_product)}")
    print(f"Labelled values checked         : {N}   (correct {C}, wrong {W}, missing {M})")
    print(f"FINAL FIELD ACCURACY (strict)   : {C / N:.1%}   = {C} / {N}")
    if name_lenient:
        print(f"  if a name that contains the answer-key name counts as correct ({name_lenient} case): "
              f"{(C + name_lenient) / N:.1%}   = {C + name_lenient} / {N}")
    print(f"Precision {p:.3f}   Recall {r:.3f}   F1 {f1:.3f}   (micro-averaged over all fields)")

    def cut(v, n=34):
        v = "" if v is None else str(v)
        return v if len(v) <= n else v[: n - 3] + "..."

    issues = [d for d in detail if d["status"] != "Correct"]
    print("\n" + "=" * 118)
    print("VALIDATION RESULTS: actual vs extracted (problems only)".center(118))
    print("=" * 118)
    print(f"{'Product':<30}{'Field':<18}{'Actual (answer key)':<36}{'Extracted':<36}{'Result'}")
    print("-" * 118)
    for d in issues:
        print(f"{cut(d['product'], 28):<30}{d['field']:<18}{cut(d['actual']):<36}{cut(d['extracted']) or '(empty)':<36}{d['status']}")
    print("-" * 118)
    print(f"{len(issues)} problem(s): {sum(d['status'] == 'INCORRECT' for d in issues)} incorrect, "
          f"{sum(d['status'] == 'MISSING' for d in issues)} missing, out of {len(detail)} labelled values checked.")
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["product", "field", "actual", "extracted", "status"])
        w.writeheader()
        w.writerows(detail)
    print(f"Full table (all {len(detail)} values) saved: {CSV_PATH}")

    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as fh:
            mo = json.load(fh)["metrics_llm"]["macro_overall"]
        print(f"\nFor comparison, main.py reports (macro): precision {mo['precision']:.4f}, "
              f"recall {mo['recall']:.4f}, F1 {mo['f1_score']:.4f}")
        print("Small differences are expected: this table is micro-averaged over fields, main.py macro-averages.")
    except Exception:
        pass

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump({"fields": out_fields, "micro": {"precision": round(p, 4), "recall": round(r, 4),
                   "f1": round(f1, 4), "accuracy": round(C / N, 4) if N else 0.0,
                   "products_found": found, "products_fully_correct": full, "values_checked": N},
                   "per_product": per_product, "validation_rows": detail}, fh, indent=2)
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
