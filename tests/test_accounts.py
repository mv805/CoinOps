import unittest
from accounts import Account, InsufficientFundsError


class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account("testuser", "password123", 100)

    def test_account_creation(self):
        self.assertEqual(self.account.user_name, "testuser")
        self.assertEqual(self.account.password, "password123")
        self.assertEqual(self.account.balance, 100)

    def test_add_funds(self):
        self.account.add_funds(50)
        self.assertEqual(self.account.balance, 150)

    def test_remove_funds(self):
        self.account.remove_funds(50)
        self.assertEqual(self.account.balance, 50)

    def test_add_negative_funds(self):
        with self.assertRaises(ValueError):
            self.account.add_funds(-50)

    def test_remove_more_funds_than_available(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.remove_funds(150)


if __name__ == "__main__":
    unittest.main()
