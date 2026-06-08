import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BASE = os.path.join(os.path.dirname(__file__), "..")

files = [("data/crop_lookup.json", "crop lookup"), ("data/schema.sql", "DB schema")]
for path, label in files:
    abspath = os.path.join(BASE, path)
    assert os.path.exists(abspath), "%s not found at %s" % (label, abspath)
    print("%s OK (%d bytes)" % (abspath, os.path.getsize(abspath)))

with open(os.path.join(BASE, "data/crop_lookup.json")) as fh:
    data = json.load(fh)
assert len(data["zones"]) == 6
assert len(data["demo_locations"]) == 3
print("crop_lookup.json: %d zones, %d demos" % (len(data["zones"]), len(data["demo_locations"])))

from modules.ndvi_loader import NDVI_FILES, NDVI_DIR
for key in ("vidarbha_cotton", "nashik_onion", "pune_sugarcane"):
    assert key in NDVI_FILES, "%s not in NDVI_FILES" % key
    abspath = os.path.join(NDVI_DIR, NDVI_FILES[key])
    assert os.path.exists(abspath), "%s not found at %s" % (key, abspath)
    print("%s: %s OK" % (key, os.path.basename(abspath)))

print("All data files verified OK")
