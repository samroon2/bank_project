"""
bank.exceptions
~~~~~~~~~~~~~
This module contains custom exceptions.
"""


class InsufficientBalance(Exception):
    """
    Exception for when a cardholder attempts to overdraw an account.
    """

    def __init__(self, balance, amount):
        self.message = f"Overdrawing account is prohibited, short ${float(balance - amount)}, deposit funds or withdraw less."

    def __str__(self):
        return repr(self.message)


class AccountError(Exception):
    """
    Exception Raised when an account doesn't maintain "open" status and is attempted to be accessed.
    """

    def __init__(self, account_id, status):
        self.message = f"Account {account_id} is unable to withdraw funds because it maintains the status: {status}"

    def __str__(self):
        return repr(self.message)


class AccountNotExists(Exception):
    """
    Exception that is raised if an account not associated with the bank.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class ExceedsLimit(Exception):
    """
    Exception that is raised if awithdrawal exceeds limit.
    """

    def __init__(self, withdraw_limit):
        self.withdraw_limit = withdraw_limit
        self.message = f"Overdrawing account limit is prohibited, limited to {self.withdraw_limit} per transaction."

    def __str__(self):
        return repr(self.message)
