from pathlib import Path
import json

import xifty


fixture = Path(__file__).resolve().parents[1] / "fixtures" / "happy.jpg"
normalized = xifty.extract(fixture, view="normalized")
fields = {
    field["field"]: field["value"]["value"]
    for field in normalized["normalized"]["fields"]
}

asset = {
    "sourcePath": str(fixture),
    "format": normalized["input"]["detected_format"],
    "capturedAt": fields.get("captured_at"),
    "cameraMake": fields.get("device.make"),
    "cameraModel": fields.get("device.model"),
    "width": fields.get("dimensions.width"),
    "height": fields.get("dimensions.height"),
    "software": fields.get("software"),
}

print(json.dumps(asset, indent=2))
