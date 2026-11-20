
import unittest
import pandas as pd
import tempfile
from pathlib import Path
from unittest.mock import patch

from src import commodity_price_analysis as analysis

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "commodity_prices.csv"


class TestCommodityPriceData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(DATA_FILE)

    def test_all_records_loaded(self):
        self.assertEqual(len(self.df), 8)

    def test_four_commodities_exist(self):
        self.assertEqual(self.df["COMMODITY"].nunique(), 4)

    def test_two_markets_exist(self):
        self.assertEqual(self.df["MARKET"].nunique(), 2)

    def test_prices_are_positive(self):
        self.assertTrue((self.df["PRICE_PER_KG"] > 0).all())

    def test_no_missing_values(self):
        self.assertFalse(self.df.isnull().any().any())

    def test_coffee_average_price(self):
        coffee = self.df[self.df["COMMODITY"] == "Coffee"]
        self.assertAlmostEqual(coffee["PRICE_PER_KG"].mean(), 330.0)

   
class TestCommodityPriceAnalysis(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)

        self.input_file = self.base / "commodity_prices.csv"
        self.output_file = self.base / "processed" / "summary.csv"
        self.chart_file = self.base / "static" / "charts" / "comparison.html"

        self.output_file.parent.mkdir(parents=True)
        self.chart_file.parent.mkdir(parents=True)

        self.sample_data = pd.DataFrame([
            ["Rice", "Tirupati", 42.50, "INR", "KG", "2026-11-12", "SAMPLE"],
            ["Rice", "Bengaluru", 44.00, "INR", "KG", "2026-11-12", "SAMPLE"],
            ["Wheat", "Tirupati", 35.00, "INR", "KG", "2026-11-12", "SAMPLE"],
            ["Coffee", "Bengaluru", 340.00, "INR", "KG", "2026-11-12", "SAMPLE"],
        ], columns=analysis.REQUIRED_COLUMNS)

    def run_analysis(self, data):
        data.to_csv(self.input_file, index=False)

        with patch.object(analysis, "INPUT_FILE", self.input_file), \
             patch.object(analysis, "OUTPUT_FILE", self.output_file), \
             patch.object(analysis, "CHART_FILE", self.chart_file):
            analysis.analyze_commodity_prices()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_analysis_function_output(self):
        self.run_analysis(self.sample_data)
        self.assertTrue(self.output_file.exists())
        self.assertTrue(self.chart_file.exists())

        summary = pd.read_csv(self.output_file)
        rice = summary[summary["COMMODITY"] == "Rice"]
        self.assertAlmostEqual(rice.iloc[0]["average_price"], 43.25)

    def test_invalid_and_missing_prices(self):
        data = self.sample_data.copy()
        data["PRICE_PER_KG"] = data["PRICE_PER_KG"].astype(object)

        data.loc[0, "PRICE_PER_KG"] = "invalid"
        data.loc[1, "PRICE_PER_KG"] = None
        data.loc[2, "PRICE_PER_KG"] = -10

        self.run_analysis(data)
        summary = pd.read_csv(self.output_file)

        self.assertNotIn("Rice", summary["COMMODITY"].values)
        self.assertNotIn("Wheat", summary["COMMODITY"].values)
        self.assertIn("Coffee", summary["COMMODITY"].values)

    def test_duplicate_records_removed(self):
        duplicate = self.sample_data.iloc[[0]].copy()
        duplicate.loc[:, "PRICE_PER_KG"] = 99.00

        data = pd.concat([self.sample_data, duplicate], ignore_index=True)
        self.run_analysis(data)

        summary = pd.read_csv(self.output_file)
        rice = summary[summary["COMMODITY"] == "Rice"]

        self.assertEqual(rice.iloc[0]["market_count"], 2)
        self.assertAlmostEqual(rice.iloc[0]["average_price"], 43.25)

    def test_summary_csv_generated(self):
        self.run_analysis(self.sample_data)
        self.assertTrue(self.output_file.exists())

        summary = pd.read_csv(self.output_file)

        self.assertIn("average_price", summary.columns)
        self.assertIn("minimum_price", summary.columns)
        self.assertIn("maximum_price", summary.columns)
        self.assertIn("price_difference", summary.columns)
        self.assertEqual(len(summary), 3)

    def test_comparison_chart_generated(self):
        self.run_analysis(self.sample_data)
        self.assertTrue(self.chart_file.exists())
        self.assertGreater(self.chart_file.stat().st_size, 0)

        chart_content = self.chart_file.read_text(encoding="utf-8")
        self.assertIn(
            "Commodity Price Comparison Across Markets",
            chart_content
        )


if __name__ == "__main__":
    unittest.main()
