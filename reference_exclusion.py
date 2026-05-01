import requests
import csv
from pathlib import Path


ACCESS_TOKEN = "" # enter a valid access token
CONTENT_OWNER = "" # enter a valid content owner ID

# Input CSV: one asset ID per line
INPUT_FILE = "/Users/saralunardelli/Downloads/assets.csv"

OUTPUT_FILE = "youtube_reference_exclusions.csv"
DOWNLOADS_PATH = str(Path.home() / "Downloads" / OUTPUT_FILE)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

asset_ids = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            asset_ids.append(row[0].strip())

print(f"📘 Loaded {len(asset_ids)} asset IDs from {INPUT_FILE}")

records = []

for asset_id in asset_ids:
    print(f"\n🔎 Fetching reference info for asset: {asset_id}")

    params = {
        "assetId": asset_id,
        "onBehalfOfContentOwner": CONTENT_OWNER
    }

    response = requests.get(
        "https://www.googleapis.com/youtube/partner/v1/references",
        headers=headers,
        params=params
    )

    if not response.ok:
        print(f"❌ Reference fetch failed ({response.status_code}): {response.text}")
        continue

    data = response.json()
    items = data.get("items", [])

    if not items:
        
        records.append({
            "assetId": asset_id,
            "referenceId": None,
            "status": None,
            "totalExcludedSeconds": None,
            "excludedPercent": None,
            "excludedIntervals": None
        })
        continue

    for item in items:
        ref_id = item.get("id")
        status = item.get("status")
        duration = item.get("duration")  # may be None
        excluded_intervals = item.get("excludedIntervals", [])

        if excluded_intervals:
            total_excluded = sum(interval["high"] - interval["low"] for interval in excluded_intervals)
            excluded_percent = (total_excluded / duration * 100) if duration else None
        else:
            total_excluded = 0
            excluded_percent = 0

        records.append({
            "assetId": asset_id,
            "referenceId": ref_id,
            "status": status,
            "totalExcludedSeconds": total_excluded,
            "excludedPercent": excluded_percent,
            "excludedIntervals": excluded_intervals if excluded_intervals else None
        })


if records:
    with open(DOWNLOADS_PATH, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "assetId",
            "referenceId",
            "status",
            "totalExcludedSeconds",
            "excludedPercent",
            "excludedIntervals"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\n✅ CSV saved to: {DOWNLOADS_PATH}")
else:
    print("⚠️ No data to save.")
