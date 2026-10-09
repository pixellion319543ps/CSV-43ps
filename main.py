"""CSV profiling script.
Prints row/column counts and simple stats for each column.
Usage: python csv_profile.py <csv_file>
"""

import csv
import sys
from collections import Counter
from statistics import mean

def is_numeric(values):
    try:
        return all(float(v) for v in values if v)
    except ValueError:
        return False

def numeric_stats(values):
    nums = [float(v) for v in values if v]
    return f"min={min(nums):.3g} max={max(nums):.3g} mean={mean(nums):.3g}"

def string_stats(values):
    cnt = Counter(v for v in values if v)
    uniq = len(cnt)
    tops = ", ".join([f"{k}({c})" for k, c in cnt.most_common(3)])
    return f"unique={uniq} top={tops}"

def profile(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print("Empty CSV.")
        return
    print(f"rows: {len(rows)}")
    print(f"columns: {', '.join(reader.fieldnames)}")
    for col in reader.fieldnames:
        vals = [r[col] for r in rows]
        if is_numeric(vals):
            print(f"{col}: {numeric_stats(vals)}")
        else:
            print(f"{col}: {string_stats(vals)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python csv_profile.py <csv_file>")
        sys.exit(1)
    profile(sys.argv[1])