import csv
import os
import requests
from pathlib import Path

KOBO_SERVER = os.environ.get("KOBO_SERVER", "https://kf.kobotoolbox.org").rstrip("/")
KOBO_API_KEY = os.environ["KOBO_API_KEY"]
KOBO_ASSET_UID = os.environ["KOBO_ASSET_UID"]

OUTPUT = Path("volunteers.csv")

HEADERS = {
    "Authorization": f"Token {KOBO_API_KEY}",
    "Accept": "application/json",
}

def get_all_records():
    url = f"{KOBO_SERVER}/api/v2/assets/{KOBO_ASSET_UID}/data/"
    records = []

    while url:
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        payload = r.json()

        if isinstance(payload, dict):
            page = payload.get("results", [])
            records.extend(page)
            url = payload.get("next")
        elif isinstance(payload, list):
            records.extend(payload)
            url = None
        else:
            raise RuntimeError("Unexpected Kobo API response.")

    return records

def field(record, name):
    # KPI v2 responses can expose fields directly or under a data object.
    if name in record:
        return record.get(name)
    data = record.get("data")
    if isinstance(data, dict):
        return data.get(name)
    return None

def main():
    records = get_all_records()

    rows = []
    seen = set()

    for rec in records:
        vid = field(rec, "volunteer_id")
        vname = field(rec, "volunteer_name")
        iid = field(rec, "investigator_id")
        iname = field(rec, "investigator_name")

        if not vid:
            continue

        vid = str(vid).strip()
        if not vid or vid in seen:
            continue

        seen.add(vid)
        vname = "" if vname is None else str(vname).strip()
        iname = "" if iname is None else str(iname).strip()
        iid = "" if iid is None else str(iid).strip()

        label = f"{vid} - {vname}" if vname else vid

        rows.append({
            "name": vid,
            "label": label,
            "volunteer_name": vname,
            "investigator_id": iid,
            "investigator_name": iname,
        })

    rows.sort(key=lambda x: x["name"])

    with OUTPUT.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "label",
                "volunteer_name",
                "investigator_id",
                "investigator_name",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} volunteers to {OUTPUT}")

if __name__ == "__main__":
    main()
