from pathlib import Path

import xifty


fixture = Path(__file__).resolve().parents[1] / "fixtures" / "happy.jpg"

print(f"XIFty version: {xifty.version()}")
print(xifty.extract(fixture, view="normalized"))
