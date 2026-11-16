
import unittest
import pandas as pd
from pathlib import Path

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
        coffee = self.df[
            self.df["COMMODITY"] == "Coffee"
        ]
        self.assertAlmostEqual(
            coffee["PRICE_PER_KG"].mean(), 330.0
        )


if __name__ == "__main__":
    unittest.main()
