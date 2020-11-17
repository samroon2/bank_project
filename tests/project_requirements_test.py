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

frydy = AccountHolder(bank, "202", "Josh", "Frydenberg")
frydy_savings = SavingsAccount(
    "202-savings-1", "savings", frydy.accounts, "202", opening_balance=0.25
)
frydy_savings_card = Card(
    frydy,
    frydy_savings,
    "Josh",
    "Frydenberg",
    "50001|101-savings-1",
    "4321",
    "12-12-2024",
    "342",
    "active",
)

assert bank.bank_balance == cormo_checking.balance + frydy_savings.balance


class BasicTests(unittest.TestCase):
    """
    Requirements:
    ● Deposit, withdraw and maintain a balance for multiple customers.
    ● Return a customer’s balance and the bank’s total balance.
    ● Prevent customers from withdrawing more money than they have in their account.
    """

    def test_a_withdraw_deposit(self):
        # ● Deposit, withdraw and maintain a balance for multiple customers.
        trans = bank.deposit_transaction(cormo_checking_card.card_number, 500.00)
        trans2 = bank.deposit_transaction(frydy_savings_card.card_number, 500.00)
        assert bank.bank_balance == cormo_checking.balance + frydy_savings.balance
        trans3 = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        trans4 = bank.withdrawal_transaction(frydy_savings_card.card_number, 500.00)
        assert bank.bank_balance == cormo_checking.balance + frydy_savings.balance

        def test_b_more_ahs(self):
            # Create 10K accounts, process withdrawals check balances.
            bank = Bank()
            n = 10000
            for i in range(n):
                ah = AccountHolder(bank, f"{i}1", "Mathias", "Cormann")
                ac = CheckingAccount(
                    f"{i}1-checking-1",
                    "checking",
                    ah.accounts,
                    f"{i}1",
                    opening_balance=1000.00,
                )
                c = Card(
                    ah,
                    ac,
                    "Mathias",
                    "Cormann",
                    f"40001|{i}1-checking-1",
                    "0101",
                    "12-12-2024",
                    "432",
                    "active",
                )
            print(bank.bank_balance, len(bank.account_holders))
            assert bank.bank_balance == 1000 * n
            for id, acchldr in bank.account_holders.items():
                bank.withdrawal_transaction(f"40001|{id}-checking-1", 500.00)
            assert bank.bank_balance == 500 * n

    def test_c_balance(self):
        # ● Return a customer’s balance and the bank’s total balance.
        trans = bank.deposit_transaction(cormo_checking_card.card_number, 500.00)
        trans2 = bank.deposit_transaction(cormo_checking_card.card_number, 500.00)
        assert bank.bank_balance == cormo_checking.balance + frydy_savings.balance
        print(f"{bank.institution} balance: ${bank.bank_balance}")
        print(f"{cormo_checking.account_id} balance: ${cormo_checking.balance}")
        print(f"{frydy_savings.account_id} balance: ${frydy_savings.balance}")

    def test_d_overdraw(self):
        # ● Prevent customers from withdrawing more money than they have in their account.
        # Attempt to withdraw $1 over current balance.
        previous_balance = cormo_checking.balance
        trans = bank.withdrawal_transaction(
            cormo_checking_card.card_number, cormo_checking.balance + 1.00
        )
        # Should False for an unsuccessful status/trans.
        assert not trans["status"]
        # We also get an eplaination (the negative balance shown is done on purpose).
        print(trans["error"])
        # There should be no change in balance as the transaction was denied.
        assert previous_balance == cormo_checking.balance

    # Other tests of similar nature.
    def test_e_stat(self):
        # Exceed withdrawal limit eg. max $5000 can be taken per transaction.
        # Deposit required amount.
        bank.deposit_transaction(cormo_checking_card.card_number, 5000.00)
        # Test the limit exception is handled and trans is denied + balance maintained.
        previous_balance = cormo_checking.balance
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 5001.00)
        assert not trans["status"]
        print(trans["error"])
        assert previous_balance == cormo_checking.balance

    def test_f_stat(self):
        # Account status if an account has been locked or closed.
        cormo_checking.status = "locked"
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        # Transaction should be denied.
        assert not trans["status"]
        print(trans["error"])
        # Reopen account.
        cormo_checking.status = "open"
        trans = bank.withdrawal_transaction(cormo_checking_card.card_number, 500.00)
        # We should have a successful transaction.
        assert trans["status"]


if __name__ == "__main__":
    unittest.main()
