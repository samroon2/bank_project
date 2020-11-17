import unittest
import os, sys

test_dir = os.path.dirname(__file__)
src_dir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(test_dir, src_dir)))

from bank.accounts import Accounts, CheckingAccount
from bank.account_holder import AccountHolder
from bank.banks import Bank
from bank.cards import Card

bank = Bank()

class BasicTests(unittest.TestCase):
    def test_a_create_ah(self):
        # Create a card holder.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        assert cormo.accountholder_id == "101"
        assert cormo.first_name == "Mathias"
        assert cormo.last_name == "Cormann"
        assert isinstance(cormo.accounts, Accounts)
        assert cormo.cards == {}

    def test_b_ch_account(self):
        # Create a card holder and assign an account.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        assert cormo.accountholder_id == "101"
        assert cormo.first_name == "Mathias"
        assert cormo.last_name == "Cormann"
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        assert cormo_checking.account_id in cormo.accounts.checking_accounts

    def test_c_ch_account_card(self):
        # Create card hold, account and card.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        assert cormo.accountholder_id == "101"
        assert cormo.first_name == "Mathias"
        assert cormo.last_name == "Cormann"
        # Create account verify it's in the registered account holders accounts.
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        assert cormo_checking.account_id in cormo.accounts.checking_accounts
        assert isinstance(
            cormo.accounts.checking_accounts[cormo_checking.account_id],
            CheckingAccount,
        )
        # Create a card, validate we can access card and account info.
        cormo_checking_card = Card(
            cormo,
            cormo_checking,
            "Mathias",
            "Cormann",
            "40001",
            "0101",
            "12-12-2024",
            "432",
            "active",
        )
        assert cormo_checking_card.card_number in cormo.accounts.issued_cards
        assert isinstance(
            cormo.accounts.issued_cards[cormo_checking_card.card_number]["account"],
            CheckingAccount,
        )
        assert isinstance(
            cormo.accounts.issued_cards[cormo_checking_card.card_number]["card"], Card
        )
        assert (
            cormo_checking_card.card_number
            in cormo.accounts.checking_accounts[cormo_checking.account_id].linked_cards
        )
        assert isinstance(
            cormo.accounts.checking_accounts[cormo_checking.account_id].linked_cards[
                cormo_checking_card.card_number
            ],
            Card,
        )


if __name__ == "__main__":
    unittest.main()
