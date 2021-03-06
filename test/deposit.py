# Ricky Galliani
# Hanna
# test/deposit.py

from src.deposit import Deposit
from src.purchase import Purchase
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.deposit


class DepositTest(unittest.TestCase):
    def test_inequality(self):
        d1: Deposit = Deposit()
        sec: Security = Security("sec", "SEC", price=10.0)
        d1.add_purchase("ac", Purchase(sec, 5))
        d2: Deposit = Deposit()
        self.assertNotEqual(d1, d2)

    def test_equality(self):
        sec: Security = Security(
            "sec", "SEC", price=10.0, buy_restricted=False
        )
        pur: Purchase = Purchase(sec, 5)
        d1: Deposit = Deposit()
        d1.add_purchase("ac", pur)
        d2: Deposit = Deposit()
        d2.add_purchase("ac", pur)
        self.assertEqual(d1, d2)

    def test_add_purchase(self):
        d: Deposit = Deposit()
        sec: Security = Security("sec", "SEC", price=10.0)
        pur: Purchase = Purchase(sec, 5)
        d.add_purchase("ac", pur)
        self.assertEqual(d.get_total(), 50.0)
        self.assertEqual(d.get_num_shares(), 5)
        self.assertTrue(pur in d.get_purchases_for_asset_class("ac"))

    def test_involves_asset_class_false(self):
        d: Deposit = Deposit()
        self.assertFalse(d.involves_asset_class("ac"))

    def test_involves_asset_class_true(self):
        d: Deposit = Deposit()
        sec: Security = Security("sec", "SEC", "sec_name", 10.0)
        pur: Purchase = Purchase(sec, 5)
        d.add_purchase("ac", pur)
        self.assertTrue(d.involves_asset_class("ac"))

    def test_get_purchases_for_asset_class(self):
        sec: Security = Security("sec", "SEC", "sec_name", 10.0, False)
        pur: Purchase = Purchase(sec, 5)
        d: Deposit = Deposit()
        d.add_purchase("ac", pur)
        self.assertEqual(d.get_purchases_for_asset_class("ac"), [pur])

    def test_get_asset_class_expenditures(self):
        d: Deposit = Deposit()
        sec1: Security = Security(
            "sec1", "SEC1", price=10.0, buy_restricted=False
        )
        sec2: Security = Security(
            "sec2", "SEC2", price=5.0, buy_restricted=False
        )
        d.add_purchase("ac", Purchase(sec1, 5))
        d.add_purchase("ac", Purchase(sec2, 10))
        self.assertEqual(d.get_asset_class_expenditures("ac"), 100.0)


if __name__ == "__main__":
    unittest.main()
