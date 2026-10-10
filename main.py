We need to write a small, complete, runnable Python project about CSV profiling script. Requirements:

- single file
- under 60 lines
- short module docstring
- standard library only
- include a __main__ block

So a script that takes a CSV file path as argument, profiles columns: counts of rows, missing values, data types, maybe unique values. Under 60 lines. We'll produce code only.

Let's design:

- docstring: "CSV profiling script: provides basic statistics for each column."
- Use argparse for CLI
- Use csv module to read
- Count rows, per column: unique values, missing counts, sample/detect numeric vs string by trying to convert to float.

We'll implement:

- parse arguments: file path
- read header
- initialize counters: for each column: count, missing, unique set, numeric flag (assume numeric if all non-missing convertible to float)
- For performance, maybe use list of sets for unique but limit memory.

Simplify: just compute row count, missing count per column, sample unique values count (maybe up to 10).

We can just compute:

- rows
- for each column: missing count, unique values (set size), numeric flag (if all values convertible)
- also maybe average length.

Return printed summary.

Under 60 lines: let's draft.

We need to count rows and store for each column stats:

We'll use:

import sys, csv, argparse, math

Define main(file_path):

with open(file_path, newline='') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames
    stats = {col: {'rows':0,'missing':0,'unique':set(),'numeric':True} for col in header}
    for row in reader:
        stats['rows']? Actually we want total_rows. We'll keep separate.

Let's code:

total_rows = 0
for row in reader:
    total_rows += 1
    for col in header:
        val = row[col].strip()
        if val == '':
            stats[col]['missing'] += 1
            stats[col]['numeric'] = False
        else:
            stats[col]['unique'].add(val)
            if stats[col]['numeric']:
                try:
                    float(val)
                except:
                    stats[col]['numeric'] = False

Then after processing, print.

We need to truncate unique set memory: maybe just keep count? Use set for unique but could be big; but requirement minimal.

We'll print:

print(f"Total rows: {total_rows}")
for col, data in stats.items():
    print(f"Column: {col}")
    print(f"  Missing: {data['missing']} ({data['missing']/total_rows*100:.1f}%)")
    print(f"  Unique values: {len(data['unique'])}")
    print(f"  Data type: {'numeric' if data['numeric'] else 'string'}")

Add __main__ block: parse args.

Under 60 lines; we need to count lines. Let's draft code and then count.

We'll include a short docstring at top (line 1). Then imports (lines 2-3). Then main function (lines 4-...). Let's write code and count.

Draft:

"""
CSV profiling script: provides basic statistics for each column.
"""

import csv
import argparse
import sys

def profile_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        if not header:
            print("No columns found.")
            return
        stats = {col: {'missing':0,'unique':set(),'numeric':True} for col in header}
        total_rows = 0
        for row in reader:
            total_rows += 1
            for col in header:
                val = row[col].strip()
                if val == '':
                    stats[col]['missing'] += 1
                    stats[col]['numeric'] = False
                else:
                    stats[col]['unique'].add(val)
                    if stats[col]['numeric']:
                        try:
                            float(val)
                        except ValueError:
                            stats[col]['numeric'] = False
        print(f"Total rows: {total_rows}")
        for col, data in stats.items():
            pct_missing = data['missing']/total_rows*100 if total_rows else 0
            print(f"Column: {col}")
            print(f"  Missing: {data['missing']} ({pct_missing:.1f}%)")
            print(f"  Unique values: {len(data['unique'])}")
            print(f"  Data type: {'numeric' if data['numeric'] else 'string'}")

def main():
    parser = argparse.ArgumentParser(description="CSV profiling script")
    parser.add_argument('csvfile', help='Path to CSV file')
    args = parser.parse_args()
    profile_csv(args.csvfile)

if __name__ == "__main__":
    main()

Now count lines:

Line 1: """
Line 2: CSV profiling script...
Line 3: """
Line 4: import csv
Line 5: import argparse
Line 6: import sys
Line 7:
Line 8: def profile_csv(path):
Line 9:     with open(path, newline='', encoding='utf-8') as f:
Line 10:         reader = csv.DictReader(f)
Line 11:         header = reader.fieldnames
Line 12:         if not header:
Line 13:             print("No columns found.")
Line 14:             return
Line 15:         stats = {col: {'missing':0,'unique':set(),'numeric':True} for col in header}
Line 16:         total_rows = 0
Line 17:         for row in reader:
Line 18:             total_rows += 1
Line 19:             for col in header:
Line 20:                 val = row[col].strip()
Line 21:                 if val == '':
Line 22:                     stats[col]['missing'] += 1
Line 23:                     stats[col]['numeric'] = False
Line 24:                 else:
Line 25:                     stats[col]['unique'].add(val)
Line 26:                     if stats[col]['numeric']:
Line 27:                         try:
Line 28:                             float(val)
Line 29:                         except ValueError:
Line 30:                             stats[col]['numeric'] = False
Line 31:         print(f"Total rows: {total_rows}")
Line 32:         for col, data in stats.items():
Line 33:             pct_missing = data['missing']/total_rows*100 if total_rows else 0
Line 34:             print(f"Column: {col}")
Line 35:             print(f"  Missing: {data['missing']} ({pct_missing:.1f}%)")
Line 36:             print(f"  Unique values: {len(data['unique'])}")
Line 37:             print(f"  Data type: {'numeric' if data['numeric'] else 'string'}")
Line 38:
Line 39: def main():
Line 40:     parser = argparse.ArgumentParser(description="CSV profiling script")
Line