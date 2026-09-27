from pathlib import Path
from collections import defaultdict

LABELS_DIR = r"C:\Users\User\Documents\coen545 project\exam hall monitoring\dataset\combined\labels"

class_counts = defaultdict(int)
bad_files = []

for lbl in Path(LABELS_DIR).glob("*.txt"):
    for i, line in enumerate(lbl.read_text().splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split()
        try:
            cls = int(parts[0])
            class_counts[cls] += 1
        except ValueError:
            bad_files.append((lbl.name, i, line.strip()))

print("Class index  |  Total instances")
print("-" * 34)
for cls in sorted(class_counts):
    print(f"  {cls:<13}  {class_counts[cls]}")

print(f"\nBad files found: {len(bad_files)}")
print("-" * 50)
for fname, lineno, content in bad_files[:20]:   # show first 20
    print(f"  {fname}  line {lineno}: '{content}'")