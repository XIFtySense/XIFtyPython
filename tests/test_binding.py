from pathlib import Path
import unittest

import xifty


ROOT = Path(__file__).resolve().parents[1]


class XiftyBindingTests(unittest.TestCase):
    def test_version_is_non_empty(self) -> None:
        self.assertTrue(xifty.version())

    def test_probe_returns_detected_format(self) -> None:
        output = xifty.probe(ROOT / "fixtures/happy.jpg")
        self.assertEqual(output["input"]["detected_format"], "jpeg")

    def test_extract_normalized_returns_expected_field(self) -> None:
        output = xifty.extract(ROOT / "fixtures/happy.jpg", view="normalized")
        fields = {field["field"]: field for field in output["normalized"]["fields"]}
        self.assertEqual(fields["device.make"]["value"]["value"], "XIFtyCam")

    def test_missing_file_raises_xifty_error(self) -> None:
        with self.assertRaises(xifty.XiftyError):
            xifty.probe(ROOT / "fixtures/does-not-exist.jpg")

    def test_invalid_view_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            xifty.extract(ROOT / "fixtures/happy.jpg", view="nope")


if __name__ == "__main__":
    unittest.main()

