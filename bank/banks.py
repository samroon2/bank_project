"""
bank.banks
~~~~~~~~~~~~~
This module contains code for managing banks.
"""

from .account_holder import AccountHolder
from .accounts import Account, Accounts, CheckingAccount, SavingsAccount
from .exceptions import AccountNotExists, AccountError, InsufficientBalance


class Bank:
    """
    Class that maintains bank infornations and provides the interface
    between transaction requests and bank accounts.
    :param institution: Name of the financial institution.
    """

    def __init__(self, institution="Square"):
        self.institution = institution
        self.account_holders = {}

    @property
    def bank_balance(self) -> int:
        """
        Total balance of the bank.
        """
        tmp = 0
        for k, v in self.account_holders.items():
            tmp += v.accounts.total_balance
        return tmp

    def withdrawal_transaction(
        self, card_number: str, amount: float, via_teller=False
    ) -> dict:
        """
        Method for withdrawing money from a given account associated with this bank.
        :param card_number: Card number of the card attempting to withdraw funds.
        :param amount: The amount of money the card holder wishes to withdraw. 
        """
        account = self.account_holders.get(
            # Exaggeration of getting account number from a card number.
            card_number.split("|")[1].split("-")[0],
            False,
        )
        if account:
            # Will throw insufficient funds exception, exceed withdraw limit or account errors.
            try:
                return account.cards[card_number]["account"].withdraw(amount)
            except Exception as e:
                return {"status": False, "error": e}
        else:
            raise AccountNotExists("Account associated with that card does not exist.")

    def deposit_transaction(
        self, card_number: str, amount: float, via_teller=False
    ) -> dict:
        """
        Method for depositing money into a given account associated with this bank.
        :param card_number: Card number of the card attempting to withdraw funds.
        :param amount: The amount of money the card holder wishes to withdraw. 
        """
        account = self.account_holders.get(
            card_number.split("|")[1].split("-")[0], False
        )
        if account:
            # Will raise account error if account is not open.
            try:
                return account.cards[card_number]["account"].deposit(amount)
            except Exception as e:
                return {"status": False, "error": e}
        else:
            raise AccountNotExists("Account associated with that card does not exist.")

    # def create_account(self, account_holder: AccountHolder, account: Account, account_holder_id: int=False):
    #     if account_holder_id and account_holder_id in self.accounts:
    #         raise AccountExists('Account already exisits, update account instead.')
    # .
    # .
    # etc etc.

    # def electronic_transfer(self, account_1, account_2, amount):
    # .
    # .
    # etc etc.
