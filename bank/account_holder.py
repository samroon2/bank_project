"""
bank.account_holder
~~~~~~~~~~~~~~~~~~~
This module contains code for managing account holders.
"""

from .accounts import Accounts, CheckingAccount, SavingsAccount, Account
from .cards import Card


class AccountHolder:
    """
    Class that maintains the information of an account holders.
    :param accountholder_id: Unique Identifier for a given account holder.
    :param first_name: First given name of account holder.
    :param last_name: Last name of account holder.
    """

    def __init__(self, bank, accountholder_id: str, first_name: str, last_name: str):
        self.bank = bank
        self.accountholder_id = accountholder_id
        self.first_name = first_name
        self.last_name = last_name
        self.accounts = Accounts(self, accountholder_id)
        self.cards = self.accounts.issued_cards
        self.bank.account_holders[accountholder_id] = self

    def __repr__(self):
        return f"accountholder: {self.accountholder_id}, {self.first_name} {self.last_name}"
