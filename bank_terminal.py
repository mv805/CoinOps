import sys
from bank_system import BankSystem
from errors import (
    InvalidAccountCreationError,
    InvalidAccountRetrievalError,
    InsufficientFundsError,
    InvalidTransferError,
)
from accounts import Account


def break_line():
    print("===============================")


class Command:
    def execute(self):
        raise NotImplementedError("Command must implement an execute method")


class MainMenuPageCommand(Command):
    def __init__(self, bank_system):
        self._bank_system = bank_system
        self._commands = {
            "create": CreateAccountPageCommand(self._bank_system),
            "login": LoginPageCommand(self._bank_system),
            "exit": ExitSystemCommand(),
        }

    def execute(self):
        command_input = input(
            "Available commands:\n"
            "- create: Create a new Account\n"
            "- login: Go to Login Page\n"
            "- exit: Exit the terminal\n"
            "Enter command: "
        ).strip()
        command = self._commands.get(command_input)
        if command:
            return command
        else:
            print("Invalid command. Please try again.")
            return self


class LoginPageCommand(Command):

    def __init__(self, bank_system: BankSystem):
        self._bank_system = bank_system

    def execute(self):
        user_name = input("Enter user name: ").strip()
        password = input("Enter an account password: ").strip()

        return LoginCommand(self._bank_system, user_name, password)


class LoginCommand(Command):

    def __init__(self, bank_system: BankSystem, user_name: str, password: str):
        self._bank_system = bank_system
        self._user_name = user_name
        self._password = password

    def execute(self):
        try:
            user_account = self._bank_system.retrieve_account(self._user_name, self._password)
            print(f"Account '{self._user_name}' retrieved.")
            return UserPageCommand(self._bank_system, user_account)
        except InvalidAccountRetrievalError as e:
            print(f"Failed to fetch the account: {e}")
            return LoginPageCommand(self._bank_system)


class TransferFundsPageCommand(Command):
    def __init__(self, bank_system: BankSystem, user_account: Account):
        self._bank_system = bank_system
        self._user_account = user_account

    def execute(self):
        recipient_name = input("Enter the recipient's account user name: ").strip()
        transfer_amount = input("Enter the amount to transfer: ").strip()
        # todo exit from here

        return TransferFundsCommand(self._bank_system, self._user_account, recipient_name, transfer_amount)


class TransferFundsCommand(Command):
    def __init__(self, bank_system, sender_account: Account, recipient_name: str, amount_to_transfer: str):
        self._bank_system = bank_system
        self._user_account = sender_account
        self._recipient_name = recipient_name
        self._amount_to_transfer = amount_to_transfer

    def execute(self):

        try:
            self._bank_system.transfer_funds(self._user_account, self._recipient_name, self._amount_to_transfer)
            print(
                f"Transferred {self._amount_to_transfer} from '{self._user_account.user_name}' "
                f"to '{self._recipient_name}'."
            )
            return UserPageCommand(self._bank_system, self._user_account)
        except (InvalidAccountRetrievalError, InsufficientFundsError, InvalidTransferError) as e:
            print(f"Failed to transfer funds: {e}")
            return TransferFundsPageCommand(self._bank_system, self._user_account)


class CheckBalanceCommand(Command):
    def __init__(self, bank_system: BankSystem, account_to_check: Account):
        self._bank_system = bank_system
        self._account_to_check = account_to_check

    def execute(self):
        print(f"Current Balance: ${self._account_to_check.balance}")
        return UserPageCommand(self._bank_system, self._account_to_check)


class UserPageCommand(Command):

    def __init__(self, bank_system: BankSystem, user_account: Account):
        self._bank_system = bank_system
        self._user_account = user_account

        self._commands = {
            "balance": CheckBalanceCommand(self._bank_system, self._user_account),
            "transfer": TransferFundsPageCommand(self._bank_system, self._user_account),
            "main": MainMenuPageCommand(self._bank_system),
        }

    def execute(self):
        command_input = input(
            "Available commands:\n"
            "- balance: Check your current balance\n"
            "- transfer: transfer funds to another account\n"
            "- main: go to the main menu\n"
            "Enter command: "
        ).strip()
        command = self._commands.get(command_input)
        if command:
            return command
        else:
            print("Invalid command. Please try again.")
            return self


class CreateAccountPageCommand(Command):

    def __init__(self, bank_system):
        self._bank_system = bank_system

    def execute(self):
        user_name = input("Enter user name: ").strip()
        password = input("Enter an account password: ").strip()
        initial_balance = input("Enter initial balance (ADMIN MODE): ")

        return CreateAccountCommand(self._bank_system, user_name, password, initial_balance)


class CreateAccountCommand(Command):
    def __init__(self, bank_system, user_name: str, password: str, initial_balance: str):
        self._bank_system = bank_system
        self._user_name = user_name
        self._password = password
        self._initial_balance = initial_balance

    def execute(self):
        try:
            self._bank_system.create_account(self._user_name, self._password, self._initial_balance)
            print(f"Account '{self._user_name}' created successfully with initial balance {self._initial_balance}.")
            return MainMenuPageCommand(self._bank_system)
        except InvalidAccountCreationError as e:
            print(f"Failed to create account: {e}")
            return MainMenuPageCommand(self._bank_system)


class ExitSystemCommand(Command):
    def execute(self):
        print("Shutting down the bank's computer system. Goodbye!")
        sys.exit(0)


class BankCLI:

    def __init__(self):
        self._bank_system = BankSystem()
        self._current_command = MainMenuPageCommand(self._bank_system)

    def start(self):
        print("Welcome to CoinOps Internal ATM service!")
        while True:
            break_line()
            self._current_command = self._current_command.execute()
            if isinstance(self._current_command, ExitSystemCommand):
                # do some cleanup...
                self._current_command.execute()


if __name__ == "__main__":
    cli = BankCLI()
    cli.start()
