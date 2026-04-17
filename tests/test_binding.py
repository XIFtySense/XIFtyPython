from pathlib import Path
import unittest

import xifty


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "happy.jpg"


def fields_by_name(output: dict) -> dict:
    return {field["field"]: field for field in output["normalized"]["fields"]}


class XiftyBindingTests(unittest.TestCase):
    def test_version_is_non_empty(self) -> None:
        self.assertRegex(xifty.version(), r"^\d+\.\d+\.\d+")

    def test_probe_returns_input_summary(self) -> None:
        output = xifty.probe(FIXTURE)
        self.assertEqual(output["schema_version"], "0.1.0")
        self.assertEqual(output["input"]["detected_format"], "jpeg")
        self.assertEqual(output["input"]["container"], "jpeg")

    def test_extract_defaults_to_full_envelope(self) -> None:
        output = xifty.extract(FIXTURE)
        self.assertIn("raw", output)
        self.assertIn("interpreted", output)
        self.assertIn("normalized", output)
        self.assertIn("report", output)

    def test_raw_view_preserves_container_and_metadata_evidence(self) -> None:
        output = xifty.extract(FIXTURE, view="raw")
        self.assertEqual(output["raw"]["containers"][0]["label"], "jpeg")
        self.assertEqual(output["raw"]["metadata"][0]["tag_name"], "ImageWidth")
        self.assertEqual(output["raw"]["metadata"][0]["value"]["value"], 800)

    def test_interpreted_view_exposes_decoded_exif_tags(self) -> None:
        output = xifty.extract(FIXTURE, view="interpreted")
        tag_names = [entry["tag_name"] for entry in output["interpreted"]["metadata"]]
        self.assertIn("Make", tag_names)
        self.assertIn("Model", tag_names)
        self.assertIn("DateTimeOriginal", tag_names)

    def test_normalized_view_returns_expected_fields(self) -> None:
        output = xifty.extract(FIXTURE, view="normalized")
        fields = fields_by_name(output)
        self.assertEqual(fields["captured_at"]["value"]["value"], "2024-04-16T12:34:56")
        self.assertEqual(fields["device.make"]["value"]["value"], "XIFtyCam")
        self.assertEqual(fields["device.model"]["value"]["value"], "IterationOne")
        self.assertEqual(fields["software"]["value"]["value"], "XIFtyTestGen")
        self.assertEqual(fields["dimensions.width"]["value"]["value"], 800)
        self.assertEqual(fields["dimensions.height"]["value"]["value"], 600)
        self.assertEqual(fields["device.make"]["sources"][0]["namespace"], "exif")

    def test_report_view_stays_explicit_when_empty(self) -> None:
        output = xifty.extract(FIXTURE, view="report")
        self.assertEqual(output["report"]["issues"], [])
        self.assertEqual(output["report"]["conflicts"], [])
        self.assertNotIn("normalized", output)

    def test_missing_file_raises_xifty_error(self) -> None:
        with self.assertRaises(xifty.XiftyError):
            xifty.probe(ROOT / "fixtures" / "does-not-exist.jpg")

    def test_invalid_view_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            xifty.extract(FIXTURE, view="nope")


if __name__ == "__main__":
    unittest.main()
