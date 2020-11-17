import unittest
import os, sys

test_dir = os.path.dirname(__file__)
src_dir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(test_dir, src_dir)))

from bank.accounts import Accounts, CheckingAccount, SavingsAccount
from bank.account_holder import AccountHolder
from bank.banks import Bank
from bank.cards import Card

bank = Bank()


class BasicTests(unittest.TestCase):
    def test_a_card(self):
        # Create checking account.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        assert cormo_checking.account_id in cormo.accounts.checking_accounts
        assert isinstance(
            cormo.accounts.checking_accounts[cormo_checking.account_id],
            CheckingAccount,
        )
        cormo_checking_card = Card(
            cormo,
            cormo_checking,
            "Mathias",
            "Cormann",
            "40001|101-checking-1",
            "0101",
            "12-12-2024",
            "432",
            "active",
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
