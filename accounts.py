from errors import InsufficientFundsError


class Account:
    def __init__(self, user_name: str, password: str, starting_balance: int = 0) -> None:
        self._user_name = user_name
        self._balance = starting_balance
        self._password = password

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def password(self) -> str:
        return self._password

    def add_funds(self, amount_to_add: int) -> None:
        """
        Adds the specified amount to the account balance.

        Args:
            amount_to_add (int): The amount of funds to add to the account balance.

        Raises:
            ValueError: If the amount to add is a non-positive value.
        """
        try:
            amount_to_add = int(amount_to_add)
        except ValueError:
            raise ValueError("Invalid value. Must be integer")

        if amount_to_add < 0:
            raise ValueError("Invalid amount to add. Must be positive integer.")

        self._balance += amount_to_add

    def remove_funds(self, amount_to_remove: int) -> None:
        """
        Remove a specified amount of funds from the account balance.
        Args:
            amount_to_remove (int): The amount of funds to remove from the account.

        Raises:
            InsufficientFundsError: If the amount to remove is greater than the current balance.
        """
        try:
            amount_to_remove = int(amount_to_remove)
        except ValueError:
            raise ValueError("Invalid value. Must be integer")

        if amount_to_remove > self._balance:
            raise InsufficientFundsError("Insufficient funds to complete the transaction.")

        self._balance -= amount_to_remove
