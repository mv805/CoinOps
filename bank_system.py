from accounts import Account
from errors import (
    InvalidAccountCreationError,
    InsufficientFundsError,
    InvalidAccountRetrievalError,
    InvalidTransferError,
)
from typing import Dict


class BankSystem:

    def __init__(self) -> None:
        self._accounts: Dict[str, Account] = {}

    def create_account(self, user_name: str, password: str, starting_balance: int = 0) -> None:
        """
        Args:
            user_name (str): The username for the new account.
            password (str): The password for the new account.
            starting_balance (int, optional): The starting balance for the new account. Defaults to 0.

        Raises:
            InvalidAccountCreationError: If the username or password is not
            provided, or if the username already exists, or starting balance is negative.

        Returns:
            None
        """
        self._validate_account_creation(user_name, password, starting_balance)

        starting_balance = int(starting_balance)  # must be integer

        new_account = Account(user_name, password, starting_balance)
        self._accounts[user_name] = new_account

    def _validate_account_creation(self, user_name: str, password: str, starting_balance: int) -> None:
        """
        Validates the account creation parameters.
        Args:
            user_name (str): The username for the new account.
            password (str): The password for the new account.
            starting_balance (int): The initial balance for the new account.
        Raises:
            InvalidAccountCreationError: If any of the validation checks fail.
                - Username and password must be strings.
                - Username and password must not be empty.
                - Starting balance must be an integer.
                - Username must not already exist in the accounts.
                - Starting balance must not be negative.
        """
        if not isinstance(user_name, str) or not isinstance(password, str):
            raise InvalidAccountCreationError("Username and password must be strings.")

        if not user_name or not password:  # theres no user name or password provided
            raise InvalidAccountCreationError("Invalid new account information. Must provide a user name and password.")
        try:
            starting_balance = int(starting_balance)  # starting balance is valid integer
        except ValueError:
            raise InvalidAccountCreationError("Starting balance must be an integer.")

        if user_name in self._accounts:  # the account name doesnt already exist
            raise InvalidAccountCreationError("An account already exists with that user name.")

        if starting_balance < 0:  # the initial balance is not negative
            raise InvalidAccountCreationError("Invalid starting balance.")

    def retrieve_account(self, user_name: str, account_password: str) -> Account:
        """
        Retrieve an account from the bank system.

        Args:
            user_name (str): The username of the account.
            account_password (str): The password of the account.

        Raises:
            InvalidAccountRetrieved: If the account does not exist or the password is incorrect.
        Returns:
            Account: The account object corresponding to the provided username and password.
        """
        if user_name not in self._accounts:
            raise InvalidAccountRetrievalError("Account with the provided username does not exist.")

        user_account = self._accounts[user_name]

        if user_account.password != account_password:
            raise InvalidAccountRetrievalError("The provided password is incorrect for the account.")
        return user_account

    def transfer_funds(self, account_from: Account, recipient_user_name: str, amount_to_transfer: int) -> None:
        """
        Transfer funds from one account to another.

        Args:
            account_from (Account): The account to transfer funds from.
            recipient_user_name (str): The username of the account to transfer funds to.
            amount_to_transfer (int): The amount of funds to transfer.

        Raises:
            AccountDoesNotExistError: If either account does not exist in the bank system.
            InsufficientFundsError: If the account_from does not have enough funds to perform the transfer.
        """
        try:
            amount_to_transfer = int(amount_to_transfer)
        except ValueError:
            raise InvalidTransferError("Invalid value for transfer. Must be integer.")

        if amount_to_transfer <= 0:
            raise InvalidTransferError("Invalid transfer amount.")

        source_account = self._accounts.get(account_from.user_name)
        destination_account = self._accounts.get(recipient_user_name)

        if source_account is None or destination_account is None:
            raise InvalidTransferError("Invalid user accounts for transfer.")

        try:
            source_account.remove_funds(amount_to_transfer)
        except (InsufficientFundsError, ValueError) as e:
            raise InvalidTransferError(f"Transfer Error: {e}")

        try:
            destination_account.add_funds(amount_to_transfer)
        except ValueError as e:
            raise InvalidTransferError(f"Transfer Error: {e}")
