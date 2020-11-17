"""
bank.cards
~~~~~~~~~~
This module contains code for managing cards.
"""


class Card:
    """
    Class for recording the attributes of an issued card to some cardholder
    not neccessarily the account holder.
    :param account: Account object associated with the card.
    :param holder_firstname: First name of cardholder.
    :param holder_lastname: Last name of cardholder.
    :param card_number: Unique card number/id tied to the card.
    :param __pin: Pin associated with the card.
    :param expiry_date: Date the card expires.
    :param cvv: CVV associated with the card.
    :param status: Status of the card (active, locked, expired)
    :param withdrawal_limit: Maximum amount account is able to withdraw with a single transaction.
    """

    def __init__(
        self,
        account_holder,
        account,
        holder_firstname: str,
        holder_lastname: str,
        card_number: str,
        pin: str,
        expiry_date: str,
        cvv: str,
        status: str,
    ):
        self.account_holder = account_holder
        self.account = account
        self.holder_firstname = holder_firstname
        self.holder_lastname = holder_lastname
        self.card_number = card_number
        self.__pin = pin
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.status = status
        self.account.linked_cards[self.card_number] = self
        self.account_holder.cards[self.card_number] = {
            "account": self.account,
            "card": self,
        }

    def verify(self, pin: str, expiry: str, cvv: str) -> bool:
        """
        Method for validating card information.
        :param pin: Pin sent in with the request.
        :param expiry: Expiry date sent in with the request.
        :param cvv: CVV sent in with the request.
        """
        if self.status != "active":
            return False
        return pin == self.__pin and expiry == self.expiry_date and cvv == self.cvv
