
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CANONICAL_FILE = ROOT / "data" / "canonical" / "intelligence_data.csv"
PUBLISHED_FILE = ROOT / "data" / "published" / "intelligence_data.json"
MANIFEST_FILE = ROOT / "data" / "manifest.json"

print("Starting canonical JSON publication...")

if not CANONICAL_FILE.is_file():
    raise SystemExit("ERROR: Canonical CSV does not exist.")

with MANIFEST_FILE.open("r", encoding="utf-8") as file:
    manifest = json.load(file)

with CANONICAL_FILE.open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

if not rows:
    raise SystemExit("ERROR: Canonical CSV is empty.")

if len(rows) != manifest["canonical"]["records"]:
    raise SystemExit("ERROR: Canonical record count does not match manifest.")

# Convert numeric fields into JSON numbers and boolean fields into JSON booleans.
numeric_fields = {"metric_value", "latitude", "longitude"}
boolean_fields = {"is_synthetic"}

published_records = []

for row in rows:
    record = {}

    for key, value in row.items():
        if value == "":
            record[key] = None
        elif key in numeric_fields:
            record[key] = float(value)
        elif key in boolean_fields:
            record[key] = value.strip().lower() == "true"
        else:
            record[key] = value

    published_records.append(record)

PUBLISHED_FILE.parent.mkdir(parents=True, exist_ok=True)

with PUBLISHED_FILE.open("w", encoding="utf-8") as file:
    json.dump(published_records, file, indent=2, ensure_ascii=False)
    file.write("\n")

# Verify the published JSON can be read and has the expected record count.
with PUBLISHED_FILE.open("r", encoding="utf-8") as file:
    verification = json.load(file)

if len(verification) != len(rows):
    raise SystemExit("ERROR: Published JSON verification failed.")

print("JSON publication completed successfully.")
print(f"Canonical records: {len(rows)}")
print(f"Published records: {len(verification)}")
print(f"Output: {PUBLISHED_FILE.relative_to(ROOT)}")
