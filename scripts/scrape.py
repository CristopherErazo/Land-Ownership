import requests
import time

# ─── CONFIG ─────────────────────────────────────────

WFS_URL = "https://api.uredjenazemlja.hr/services/inspire/cp/wfs"
PARCEL_INFO_URL = "https://oss.uredjenazemlja.hr/oss/public/cad/parcel-info"

LAYER = "cp:CadastralParcel"

# Small test area (you can change this)
# BBOX = "16.37,45.81,16.371,45.811,EPSG:4326"

BBOX = "13.507446,45.502031,13.511507,45.504528,EPSG:4326"






BATCH_SIZE = 20        # features per WFS request
MAX_FEATURES = 50      # safety limit (set None for full download)

SLEEP_WFS = 0.5        # delay between WFS requests
SLEEP_API = 1          # delay between parcel-info calls

# ───────────────────────────────────────────────────


def fetch_parcels():
    """
    Step 1: Get parcel geometries + IDs from WFS
    """
    print("\n🔍 Fetching parcels from WFS...")

    start = 0
    all_features = []

    while True:
        params = {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "typeNames": LAYER,
            "outputFormat": "application/json",
            "count": BATCH_SIZE,
            "startIndex": start,
            "bbox": BBOX
        }

        r = requests.get(WFS_URL, params=params, timeout=30)
        r.raise_for_status()

        data = r.json()
        features = data.get("features", [])

        if not features:
            break

        all_features.extend(features)

        print(f"   → {len(all_features)} parcels downloaded")

        if MAX_FEATURES and len(all_features) >= MAX_FEATURES:
            print("   ⏹️ Reached limit")
            break

        start += len(features)
        time.sleep(SLEEP_WFS)

    return all_features


# def extract_parcel_ids(features):
#     """
#     Step 2: Extract parcel IDs from WFS features
#     """
#     ids = []

#     for f in features:
#         props = f.get("properties", {})

#         # IMPORTANT: field name may vary → inspect if needed
#         parcel_id = props.get("id") or props.get("inspireId")

#         if isinstance(parcel_id, dict):
#             parcel_id = parcel_id.get("localId")

#         if parcel_id:
#             try:
#                 ids.append(int(parcel_id))
#             except:
#                 continue

#     print(f"\n📦 Extracted {len(ids)} parcel IDs")
#     return ids

def extract_parcel_ids(features):
    ids = []

    for f in features:
        try:
            local_id = f["properties"]["inspireId"]["localId"]

            # Extract numeric part from "CP.19612784"
            parcel_id = int(local_id.split(".")[1])

            ids.append(parcel_id)

        except Exception as e:
            print("Error extracting ID:", e)

    print(f"📦 Extracted {len(ids)} parcel IDs")
    return ids


def get_parcel_info(parcel_id):
    """
    Step 3: Call parcel-info API
    """
    try:
        r = requests.get(
            PARCEL_INFO_URL,
            params={"parcelId": parcel_id},
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code != 200:
            return None

        return r.json()

    except Exception as e:
        print(f"   ⚠️ Error for {parcel_id}: {e}")
        return None


def extract_useful_data(data):
    """
    Step 4: Extract only relevant info
    """
    if not data:
        return None

    # Owner
    owner = None
    try:
        sheets = data.get("possessionSheets", [])
        if sheets:
            poss = sheets[0].get("possessors", [])
            if poss:
                owner = poss[0].get("name")
    except:
        pass

    # Land use
    uses = []
    for part in data.get("parcelParts", []):
        if part.get("name"):
            uses.append(part["name"])

    return {
        "parcel_id": data.get("parcelId"),
        "parcel_number": data.get("parcelNumber"),
        "area": data.get("area"),
        "owner": owner,
        "land_use": ", ".join(uses)
    }


def main_remove():
    print("=" * 50)
    print("Croatia Parcel Extractor")
    print("=" * 50)

    # Step 1: WFS
    features = fetch_parcels()
    print(f"\n📌 Total features fetched: {len(features)}")

    print(features[0]["properties"])
    # we will print this to check the field names for IDs, as they can vary (id, inspireId, etc.)

    # Step 2: IDs
    parcel_ids = extract_parcel_ids(features)
    print(f"Sample parcel ID: {parcel_ids[0] if parcel_ids else 'N/A'}")

    # Step 3–4: Parcel info
    results = []

    print("\n📡 Fetching parcel details...")

    for i, pid in enumerate(parcel_ids):
        print(f"   [{i+1}/{len(parcel_ids)}] Parcel {pid}")

        data = get_parcel_info(pid)
        clean = extract_useful_data(data)

        if clean:
            results.append(clean)

        time.sleep(SLEEP_API)

    # Output preview
    print("\n📊 Sample results:")
    for r in results[:5]:
        print(r)

    print(f"\n✅ Done. Total records: {len(results)}")

def main():
    print("=" * 50)
    print("DEBUG MODE")
    print("=" * 50)

    features = fetch_parcels()

    print(f"\n📌 Total features: {len(features)}")

    # 🔍 Inspect multiple features
    print("\n🔎 Inspecting first 3 features:\n")

    for i, f in enumerate(features[:3]):
        print(f"\n--- Feature {i+1} ---")
        props = f.get("properties", {})

        for key, value in props.items():
            print(f"{key}: {value}")

    # 🔍 Extract inspireId
    print("\n🔑 Extracting inspireId values:")

    for f in features[:5]:
        inspire = f["properties"].get("inspireId", {})
        print(inspire.get("localId"))

    print("\n⚠️ Notice: No numeric parcelId yet")


if __name__ == "__main__":
    main_remove()

    # url = "https://oss.uredjenazemlja.hr/oss/public/cad/parcel-info" 
    # params = { "parcelId": 19612805 } 
    # r = requests.get(url, params=params) 
    # print(r.json())