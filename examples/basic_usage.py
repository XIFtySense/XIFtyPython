from pathlib import Path

import xifty


fixture = Path(__file__).resolve().parents[1] / "fixtures" / "happy.jpg"
normalized = xifty.extract(fixture, view="normalized")
fields = {
    field["field"]: field["value"]["value"]
    for field in normalized["normalized"]["fields"]
}

print(f"XIFty version: {xifty.version()}")
print(f"Detected format: {normalized['input']['detected_format']}")
print(f"Camera: {fields['device.make']} {fields['device.model']}")
print(f"Captured at: {fields['captured_at']}")
print(f"Dimensions: {fields['dimensions.width']}x{fields['dimensions.height']}")
print(normalized)
