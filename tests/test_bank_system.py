import unittest
from bank_system import BankSystem
from accounts import Account
from errors import InvalidAccountCreationError, InvalidTransferError, InvalidAccountRetrievalError


class TestAccountCreation(unittest.TestCase):

    def setUp(self):
        self.bank_system = BankSystem()
        self.bank_system.create_account("user1", "password1", 100)
        self.bank_system.create_account("user2", "password2", 50)
        self.bank_system.create_account("user3", "password3")

    def test_create_account(self):

        self.assertIn("user1", self.bank_system._accounts)
        self.assertEqual(self.bank_system._accounts["user1"].balance, 100)
        self.assertEqual(self.bank_system._accounts["user1"].user_name, "user1")
        self.assertEqual(self.bank_system._accounts["user1"]._password, "password1")

    def test_create_account_no_username_or_password(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("", "")

    def test_create_account_no_username(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("", "password123")

    def test_create_account_no_password(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("username", "")

    def test_create_account_duplicate_username(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("user3", "password3")

    def test_create_account_starting_balance_not_integer(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("user3", "password3", "dfwe4234jl")  # type: ignore

    def test_create_account_starting_balance_negative_value(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("user3", "password3", "-5000")  # type: ignore

    def test_create_account_incorrect_user_name_type(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account(5, "test")  # type: ignore

    def test_create_account_incorrect_password_type(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("test", 5)  # type: ignore

    def test_create_account_incorrect_starting_balance_type(self):
        with self.assertRaises(InvalidAccountCreationError):
            self.bank_system.create_account("test", "test", "test")  # type: ignore


class TestTransferFunds(unittest.TestCase):

    def setUp(self):
        self.bank_system = BankSystem()
        self.bank_system.create_account("user1", "password1", 100)
        self.bank_system.create_account("user2", "password2", 50)

    def test_transfer_funds_success(self):
        account_from = self.bank_system._accounts["user1"]
        account_to = self.bank_system._accounts["user2"]

        self.bank_system.transfer_funds(account_from, account_to.user_name, 50)

        self.assertEqual(account_from.balance, 50)
        self.assertEqual(account_to.balance, 100)

    def test_transfer_funds_insufficient_balance(self):
        account_from = self.bank_system._accounts["user1"]
        account_to = self.bank_system._accounts["user2"]

        with self.assertRaises(InvalidTransferError):
            self.bank_system.transfer_funds(account_from, account_to.user_name, 150)

        self.assertEqual(account_from.balance, 100)
        self.assertEqual(account_to.balance, 50)

    def test_transfer_funds_account_does_not_exist(self):
        account_from = self.bank_system._accounts["user1"]
        account_to = Account("user4", "password4", 50)  # not in the bank system

        with self.assertRaises(InvalidTransferError):
            self.bank_system.transfer_funds(account_from, account_to.user_name, 50)

    def test_transfer_funds_negative_amount_to_transfer(self):
        account_from = self.bank_system._accounts["user1"]
        account_to = self.bank_system._accounts["user2"]

        with self.assertRaises(InvalidTransferError):
            self.bank_system.transfer_funds(account_from, account_to.user_name, -10)

    def test_transfer_funds_zero_amount_to_transfer(self):
        account_from = self.bank_system._accounts["user1"]
        account_to = self.bank_system._accounts["user2"]

        with self.assertRaises(InvalidTransferError):
            self.bank_system.transfer_funds(account_from, account_to.user_name, 0)


class TestRetrieveAccount(unittest.TestCase):

    def setUp(self):
        self.bank_system = BankSystem()
        self.bank_system.create_account("user1", "password1", 100)

    def test_retrieve_account_success(self):
        account = self.bank_system.retrieve_account("user1", "password1")
        self.assertEqual(account.user_name, "user1")
        self.assertEqual(account._password, "password1")

    def test_retrieve_account_incorrect_password(self):
        with self.assertRaises(InvalidAccountRetrievalError):
            self.bank_system.retrieve_account("user1", "wrongpassword")


if __name__ == "__main__":
    unittest.main()
