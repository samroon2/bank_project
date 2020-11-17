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
cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
cormo_checking = CheckingAccount(
    "101-checking-1", "checking", cormo.accounts, "101", opening_balance=1000.00
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


class BasicTests(unittest.TestCase):
    def test_a_bank(self):
        # Create checking account.
        bank = Bank()
        cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
        cormo_checking = CheckingAccount(
            "101-checking-1", "checking", cormo.accounts, "101", opening_balance=1000
        )
        assert cormo.accountholder_id in bank.account_holders
        assert cormo_checking.account_id in cormo.accounts.checking_accounts
        assert isinstance(bank.account_holders[cormo.accountholder_id], AccountHolder)
        assert isinstance(
            bank.account_holders[cormo.accountholder_id].accounts.checking_accounts[
                cormo_checking.account_id
            ],
            CheckingAccount,
        )
        # Bank balance == the only accounts balance.
        assert bank.bank_balance == cormo_checking.balance
        frydy = AccountHolder(bank, "202", "Josh", "Frydenberg")
        frydy_savings = SavingsAccount(
            "202-savings-1", "savings", frydy.accounts, "202", opening_balance=0.25
        )
        # Bank balance == total of accounts balances.
        assert bank.bank_balance == cormo_checking.balance + frydy_savings.balance

    def test_b_account_deposit(self):
        assert bank.bank_balance == cormo_checking.balance
        trans = bank.deposit_transaction(cormo_checking_card.card_number, 500.00)
        assert trans["status"]
        assert trans["new_balance"] == 1500.00
        assert bank.bank_balance == cormo_checking.balance
        cormo_checking.status = "locked"
        trans = bank.deposit_transaction(cormo_checking_card.card_number, 500.00)
        assert not trans["status"]

    def test_c_account_withdraw(self):
        prev_balance = cormo_checking.balance
        cormo_checking.status = "open"
        assert bank.bank_balance == cormo_checking.balance
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        assert trans["status"]
        assert trans["new_balance"] == cormo_checking.balance
        assert bank.bank_balance == cormo_checking.balance
        assert prev_balance != cormo_checking.balance

    def test_d_stat(self):
        # Insufficient funds.
        prev_balance = cormo_checking.balance
        trans = bank.withdrawal_transaction(
            cormo_checking_card.card_number, cormo_checking.balance + 1.00
        )
        assert not trans["status"]
        assert prev_balance == cormo_checking.balance

    def test_e_stat(self):
        # Exceed withdrawal limit.
        bank.deposit_transaction(cormo_checking_card.card_number, 5000.00)
        prev_balance = cormo_checking.balance
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 5001.00)
        assert not trans["status"]
        assert prev_balance == cormo_checking.balance

    def test_f_stat(self):
        # Account status
        prev_balance = cormo_checking.balance
        cormo_checking.status = "locked"
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        assert not trans["status"]
        assert prev_balance == cormo_checking.balance
        # Reopen account
        prev_balance = cormo_checking.balance
        cormo_checking.status = "open"
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        assert trans["status"]
        assert prev_balance != cormo_checking.balance


if __name__ == "__main__":
    unittest.main()
