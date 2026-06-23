import json
import unittest
from pathlib import Path

import pandas as pd

from scripts.map_cdcr_ethnicity_to_census import apply_mapping, labels_needing_review


ROOT = Path(__file__).resolve().parents[1]
MAPPING_PATH = ROOT / "mappings" / "cdcr_census_ethnicity_mapping.json"


def load_mapping():
    with MAPPING_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


class EthnicityMappingTests(unittest.TestCase):
    def test_client_confirmed_mappings(self):
        mapping = load_mapping()
        df = pd.DataFrame(
            {
                "ethnicity": [
                    "Indian",
                    "Jamaican",
                    "Other",
                    "Unknown",
                ]
            }
        )

        out = apply_mapping(
            df=df,
            mapping=mapping,
            source_col="ethnicity",
            group_col="census race ethnicity group",
            status_col="census mapping status",
            note_col="census mapping note",
        )

        self.assertEqual(
            out["census race ethnicity group"].tolist(),
            [
                "nh_asian",
                "nh_black",
                "other",
                "other",
            ],
        )
        self.assertEqual(list(out.columns), ["ethnicity", "census race ethnicity group"])

    def test_unseen_future_label_is_flagged_for_review(self):
        mapping = load_mapping()
        df = pd.DataFrame({"ethnicity": ["New Future Label"]})

        out = apply_mapping(
            df=df,
            mapping=mapping,
            source_col="ethnicity",
            group_col="census race ethnicity group",
            status_col="census mapping status",
            note_col="census mapping note",
            include_audit_columns=True,
        )

        self.assertEqual(out.loc[0, "census race ethnicity group"], "review_needed")
        self.assertEqual(out.loc[0, "census mapping status"], "review")
        self.assertIn("needs review", out.loc[0, "census mapping note"])
        self.assertEqual(labels_needing_review(df, mapping, "ethnicity").to_dict(), {"New Future Label": 1})

    def test_mapping_dictionary_covers_expected_release_labels(self):
        mapping = load_mapping()
        expected_labels = {
            "American Indian",
            "Bangladeshi",
            "Black",
            "Cambodian",
            "Chinese",
            "Columbian",
            "Cuban",
            "Filipino",
            "Fijian",
            "Guamanian",
            "Guamanian or Chamorro",
            "Guatemalan",
            "Hawaiian",
            "Hispanic",
            "Hmong",
            "Indian",
            "Jamaican",
            "Japanese",
            "Korean",
            "Laotian",
            "Mexican",
            "Nicaraguan",
            "Other",
            "Other Asian",
            "Other Asian Not Listed",
            "Other Hispanic Not Listed",
            "Other Pacific Islander Not Listed",
            "Pacific Islander",
            "Pakistani",
            "Puerto Rican",
            "Salvadorian",
            "Samoan",
            "Thai",
            "Tongan",
            "Unknown",
            "Vietnamese",
            "White",
        }

        self.assertEqual(set(mapping), expected_labels)


if __name__ == "__main__":
    unittest.main()
