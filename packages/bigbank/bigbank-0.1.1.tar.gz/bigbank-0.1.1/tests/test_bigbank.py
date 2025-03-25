import unittest
from bigbank import BigBank, CooldownError
import time

class TestBigBank(unittest.TestCase):
    def setUp(self):
        self.bank = BigBank()

    def test_initial_balance(self):
        self.assertEqual(self.bank.get_balance(), 0)

    def test_generate_money(self):
        self.bank.generate_money()
        self.assertEqual(self.bank.get_balance(), 10)

    def test_cooldown(self):
        self.bank.generate_money()
        with self.assertRaises(CooldownError):
            self.bank.generate_money()

if __name__ == "__main__":
    unittest.main()