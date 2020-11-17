"""
bank.accounts
~~~~~~~~~~~~~
This module contains code for managing accounts.
"""

from .cards import Card
from .exceptions import InsufficientBalance, AccountError, ExceedsLimit
import time, datetime


class Account:
    """
    Base class for accounts, handles balances & transactions.
    :param account_id: Unique ID associated with the account.
    :param account_type: Type of account (savings, checkings, credit).
    :param holder_accounts: An AccountHolder.Accounts() class.
    :param accountholder_id: Unique ID of the account holder.
    :param opening_balance: When account is created the opening amount of $.
    :param open_date: Date the account was opened. 
    :param status: Status of the account (open, closed, locked).
    """

    def __init__(
        self,
        account_id: int,
        account_type: str,
        holder_accounts,
        accountholder_id: str,
        opening_balance=0,
        open_date=datetime.date.today(),
        status: str = "open",
    ):
        self.account_id = account_id
        self.account_type = account_type
        self.holder_accounts = holder_accounts
        self.accountholder_id = account_id
        self.balance = opening_balance if opening_balance >= 0 else 0
        self.open_date = open_date
        self.status = status
        self.linked_cards = {}
        self.withdrawal_limit = 5000

    def withdraw(self, amount: float) -> dict:
        """'
        Method to withdraw funds from account.
        :param amount: Transaction amount.
        """
        # Assuming there can be $0.
        if self.status != "open":
            raise AccountError(self.account_id, self.status)
        elif amount > self.withdrawal_limit:
            raise ExceedsLimit(self.withdrawal_limit)
        elif amount > self.balance:
            raise InsufficientBalance(self.balance, amount)
        else:
            self.balance -= amount
            return {
                "status": True,
                "new_balance": self.balance,
                "transaction_time": time.time(),
            }

    def deposit(self, amount: float) -> dict:
        """
        Method to deposit funds to an account.
        :param amount: Transaction amount.
        """
        if self.status != "open":
            raise AccountError(self.account_id, self.status)
        self.balance += amount
        return {
            "status": True,
            "new_balance": self.balance,
            "transaction_time": time.time(),
        }


class CheckingAccount(Account):
    """
    Class for checking accounts, inherits base account class.
    :param account_id: Unique ID associated with the account.
    :param account_type: Type of account (savings, checkings, credit).
    :param holder_accounts: An AccountHolder.Accounts() class.
    :param accountholder_id: Unique ID of the account holder.
    :param opening_balance: When account is created the opening amount of $.
    :param open_date: Date the account was opened. 
    :param status: Status of the account (open, closed, frozen).
    """

    def __init__(
        self,
        account_id: int,
        account_type: str,
        holder_accounts,
        accountholder_id: str,
        opening_balance=0,
        open_date=datetime.date.today(),
        status: str = "open",
    ):
        super().__init__(
            account_id,
            account_type,
            holder_accounts,
            accountholder_id,
            opening_balance,
            open_date,
            status,
        )
        self.account_type = "checking"
        self.holder_accounts.checking_accounts[self.account_id] = self


class SavingsAccount(Account):
    """
    Class for savings accounts, inherits base account class.
    :param account_id: Unique ID associated with the account.
    :param account_type: Type of account (savings, checkings, credit).
    :param holder_accounts: An AccountHolder.Accounts() class.
    :param accountholder_id: Unique ID of the account holder.
    :param opening_balance: When account is created the opening amount of $.
    :param open_date: Date the account was opened. 
    :param status: Status of the account (open, closed, frozen).
    :kwarg interest: The interest of the savings account.
    """

    def __init__(
        self,
        account_id: int,
        account_type: str,
        holder_accounts,
        accountholder_id: str,
        opening_balance=0,
        open_date=datetime.date.today(),
        status: str = "open",
        interest_rate=0.001,
    ):
        super().__init__(
            account_id,
            account_type,
            holder_accounts,
            accountholder_id,
            opening_balance,
            open_date,
            status,
        )
        self.account_type = account_type
        self.interest_rate = interest_rate
        self.holder_accounts.saving_accounts[self.account_id] = self


class CreditAccount(Account):
    """
    Class for credit accounts, inherits base account class.
    :param account_id: Unique ID associated with the account.
    :param account_type: Type of account (savings, checkings, credit).
    :param holder_accounts: An AccountHolder.Accounts() class.
    :param accountholder_id: Unique ID of the account holder.
    :param opening_balance: When account is created the opening amount of $.
    :param open_date: Date the account was opened. 
    :param status: Status of the account (open, closed, frozen).
    :kwarg apr: the APR charged on outstanding balance.  
    """

    def __init__(
        self,
        account_id: int,
        account_type: str,
        holder_accounts,
        accountholder_id: str,
        opening_balance=0,
        open_date=datetime.date.today(),
        status: str = "open",
        apr_rate=0.15,
    ):
        super().__init__(
            account_id,
            account_type,
            accountholder_id,
            opening_balance,
            open_date,
            status,
        )
        self.account_type = account_type
        self.apr_rate = apr_rate
        self.holderaccounts.credit_accounts[self.account_id] = self
        # self.billing_end =
        # self.balance_due =
        # .
        # .
        # etc etc.


class Accounts:
    """
    Class that maintains the relations between account holders, accounts and cards.
    :param holder: AccountHolder object holding account holder information.
    :param accountholder_id: ID of account holder.
    """

    def __init__(self, holder, accountholder_id: str):
        self.holder = holder
        self.accountholder_id = accountholder_id
        self.checking_accounts = {}
        self.saving_accounts = {}
        self.credit_accounts = {}
        self.issued_cards = {}

    @property
    def holder_info(self):
        """
        Summary of the account holder who is linked with the accounts.
        """
        return self.holder.__repr__

    @property
    def accounts(self):
        """
        Str summary of number of accounts.
        """
        return "".join(
            [
                f"Accounts: Checking: {len(self.checking_accounts)}, ",
                f"Savings: {len(self.saving_accounts)}, ",
                f"Credit: {len(self.credit_accounts)}",
            ]
        )

    @property
    def total_balance(self) -> int:
        """
        Total balance of all accounts.
        """
        return self._checking_balance + self._savings_balance + self._credit_balance

    @property
    def _checking_balance(self) -> int:
        """
        Total balance of all checking accounts.
        """
        bal = 0
        for id, obj in self.checking_accounts.items():
            bal += obj.balance
        return bal

    @property
    def _savings_balance(self) -> int:
        """
        Total balance of all savings accounts.
        """
        bal = 0
        for id, obj in self.saving_accounts.items():
            bal += obj.balance
        return bal

    @property
    def _credit_balance(self) -> int:
        """
        Total balance of all credit accounts.
        """
        bal = 0
        for id, obj in self.credit_accounts.items():
            bal += obj.balance
        return bal
