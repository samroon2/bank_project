import unittest
import os, sys

test_dir = os.path.dirname(__file__)
src_dir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(test_dir, src_dir)))

from bank.accounts import Accounts, CheckingAccount, SavingsAccount
from bank.account_holder import AccountHolder
from bank.banks import Bank
from bank.cards import Card
from bank.exceptions import InsufficientBalance, AccountError, ExceedsLimit

bank = Bank()


class BasicTests(unittest.TestCase):
    def test_a_create_checking(self):
        # Create checking account.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        assert cormo_checking.account_id in cormo.accounts.checking_accounts
        assert isinstance(
            cormo.accounts.checking_accounts[cormo_checking.account_id], CheckingAccount
        )

    def test_b_create_savings(self):
        # Create saving account.
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_saving = SavingsAccount(
            "101", "saving", cormo.accounts, "101-saving-1", opening_balance=1000
        )
        assert cormo_saving.account_id in cormo.accounts.saving_accounts
        assert isinstance(
            cormo.accounts.saving_accounts[cormo_saving.account_id], SavingsAccount
        )

    def test_c_account_deposit(self):
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        trans = cormo_checking.deposit(500.00)
        assert trans["status"]
        assert trans["new_balance"] == 1500.00
        assert cormo_checking.balance == 1500.00

    def test_c_account_withdraw(self):
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000
        )
        trans = cormo_checking.withdraw(500.00)
        assert trans["status"]
        assert trans["new_balance"] == 500.00
        assert cormo_checking.balance == 500.00
        # Test insufficient balance withdrawal.
        try:
            trans = cormo_checking.withdraw(700.00)
        except InsufficientBalance as e:
            assert isinstance(e, InsufficientBalance)
        assert cormo_checking.balance == 500.00
        # Test exceeds limit withdrawal.
        try:
            cormo_checking.deposit(7000.00)
            trans = cormo_checking.withdraw(7000.00)
        except ExceedsLimit as e:
            assert isinstance(e, ExceedsLimit)
        # test account status
        cormo_checking.status = "locked"
        try:
            trans = cormo_checking.withdraw(700.00)
        except AccountError as e:
            assert isinstance(e, AccountError)

    def test_d_accounts(self):
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101", "checking", cormo.accounts, "101-checking-1", opening_balance=1000.00
        )
        cormo_savings = SavingsAccount(
            "101", "savings", cormo.accounts, "101-saving-1", opening_balance=1000.00
        )
        assert cormo.accounts.total_balance == 2000.00
        assert cormo.accounts._checking_balance == 1000.00
        assert cormo.accounts._savings_balance == 1000.00
        assert cormo.accounts.accounts == "Accounts: Checking: 1, Savings: 1, Credit: 0"


if __name__ == "__main__":
    unittest.main()
