[![Build Status](https://travis-ci.org/samroon2/bank_project.svg?branch=main)](https://travis-ci.org/samroon2/bank_project)

```shell
 ____              _
| __ )  __ _ _ __ | | __
|  _ \ / _` | '_ \| |/ /
| |_) | (_| | | | |   <
|____/ \__,_|_| |_|_|\_\
```
##  Just a Demo Project.

Of course there are a lot of differences in this example code that would not be used in a real life implementation.
- A lot of the work here is assuming there is no backend, no persistent storage, caching services, optimized application components etc.
- There's plenty of complexities and corner cases we'd want to account for in a real system race conditions, deadlocks, HW failures etc.
- In this code there are an abundance of member variables for which one wouldn't want in a prod system etc.

The relationship structure used in this code:

- We have a bank/financial institution.
- who has customers (account holders).
- who may have various accounts (checking, credit, savings etc.) to store their money.
- they may access their money in various ways (via cards, electronically, via a teller).
- they perform different transactions changing the state of their accounts (deposit, withdraw etc.).
- there may be other elements that change the account state as well (incur fees, interest etc.).
- etc etc.

## General Code Comments:
The there's no fancy data structures or algorithms in the code base give the nature of the task, the main thing is basically taking advantage of hashmaps (dicts) and pointers for O(1) access to account holder - accounts - cards mappings, so that we reduce the time for transactions to process so we don't leave customers waiting!

## Assumptions for this code:
-  Assuming all transactions are coming from within the same country where there are no conversions needed and foreign charges etc.
-  Assuming auth/verification is happening prior to these interactions.
-  Assuming all inputs to the bank are pre-vetted and validated, floats are floats, ids are valid ids, no one is submitting invalid non ascii names etc (assuming an ascii based language location).
-  Assuming there will be services to create unique IDs for account holders, accounts, cards etc.  
-  Assuming all the transactions are done through the use of issued cards tied to accounts issued by a given bank.
-  Assuming we are not too interested in recording much information about the transaction (we definitely would in real life but here we don't even have a back end!).
-  Assuming there's no minimum balance amount required in an account, withdrawing to $0 is okay.
-  Assuming a given bank only processes transactions made by cards and accounts it has issued.
-  Assuming not fees are charged for transactions.
-  Assuming there might be card holders who might not necessarily have an account (their card is linked to some account holder account though).

## Instructions for running the code:

### Using docker to run tests.
- Using docker we're going to build the image and run the tests.
```shell
bank_task$ docker build -t banktests:latest .
bank_task$ docker run banktests
```
This should run the tests in the container and display the test results.

### Installing code as a package in python and using from the python repl.

You can also opt. to pip install the .whl file located in the project directory. Note that the package does not have any external dependencies but DOES REQUIRE python >= 3.6 (only tested on 3.6 however) you may want to create a python venv and install within the venv if there are any environment concerns.
```shell
bank_task$ pip install --user bank-0.0.1-py3-none-any.whl
```
### Running the tests given a local installation of Python.
Given the code uses only the standard library it's *plausible* that running the tests directly from the project directory *MAY* work (only tested in 2 different envs - not making the claim "it runs on my machine so it should run on yours").
If using unittest:
```shell
bank_task$ python -m unittest discover -s tests -p '*_test.py'
```
If using pytest (needs to be installed):
```shell
bank_task$ pytest .
```
OR 
```shell
bank_task$ pytest tests/*
```

## Brief walk through of main modules.
Note that all classes and methods have included doc strings giving more information on all of these.
### banks.py *(module)*
The banks module is the main struct __Bank()__ that holds everything together and overall represents a bank which encompases all account holders, accounts and issued cards. All transactions go through the bank.
#### bank_balance *(property)*:
Is a method that calculates the overall money the bank possesses (sum of all account holder accounts). I opted to create this as a property so it is dynamically calculated, and chose this over say manipulating the bank balance as a static balance and then updating it as transactions occur adds a large point for error.
The complexity for the overall bank balance is O(n*a) where n = account holders and a is the # of accounts a given holder possesses. This can also be viewed as O(A) where A is the total number of accounts that have been issued by the bank.
#### withdrawal_transaction & deposit_transaction *(methods)*:
Two methods that process account transactions. These methods handle the custom exceptions that are raised by the account methods that actually do the deducting and notify if there are problems. These methods will return a bool True or False status, an updated balance and time stamp of the transaction. OR in the case of a failed transaction an error message outlining the problem. Given the design patterns used we can take a card number and have an account to process in O(1).
```shell
>>> bank = Bank()
>>> cormo = AccountHolder(bank, "101", "Mathias", "Cormann")
>>> cormo_checking = CheckingAccount(
...     "101-checking-1", "checking", cormo.accounts, "101", opening_balance=1000.00
... )
>>> cormo_checking_card = Card(
...     cormo,
...     cormo_checking,
...     "Mathias",
...     "Cormann",
...     "40001|101-checking-1",
...     "0101",
...     "12-12-2024",
...     "432",
...     "active",
... )
>>>
>>> trans = bank.withdrawal_transaction(
...             cormo_checking_card.card_number, cormo_checking.balance + 1.00
...         )
>>> trans
{'status': False, 'error': InsufficientBalance(1000.0, 1001.0)}
```

Of course there can be more than one exception at a given time (exceed limit and overdraft) but due to the time
constraints these aren't accounted for.

#### account_holders *(attribute)*:
Bank has an attribute 'account_holders' that is a hash map (dictionary) containing all registered account holders via key (accountholder_id) value(AccountHolder).

### account_holder.py *(module)*
The account holder module contains the AccountHolder struct that maintains the relationships between bank and account holders accounts and cards. It possess the following attributes:
```python
self.bank = bank # Bank object for whom the AccountHolder is registered to.
self.accountholder_id = accountholder_id # Unique Identifier for each AccountHolder
self.first_name = first_name
self.last_name = last_name
self.accounts = Accounts(self, accountholder_id) # Accounts struct that contains all accounts registered to the AccountHolder.
self.cards = self.accounts.issued_cards # All the cards issued to accounts tied to this AccountHolder.
self.bank.account_holders[accountholder_id] = self # Pass in the bank object to register the AccountHolder.
```

### accounts.py *(module)*
All of the code/classes pertaining to offered accounts.
### Account *(class)*
The base class for all of the different account classes.
__Some attributes of Account()__
```python
self.account_id = account_id # Unique ID associated with the account.
self.account_type = account_type # Type of account (savings, checkings, credit).
self.holder_accounts = holder_accounts # An AccountHolder.Accounts() class to link the account with.
self.accountholder_id = account_id # Unique ID of the account holder.
self.balance = opening_balance if opening_balance >= 0 else 0 # When account is created the opening amount of $ inits the balance.
self.open_date = open_date # Date the account was opened. 
self.status = status # Status of the account (open, closed, locked).
self.linked_cards = {} # Cards linked to the account
self.withdrawal_limit = 5000 # Max amount allowed to be withdrawn in one transaction.
```
#### withdraw & deposit *(methods)*
These methods check the validity of the transaction and adjust the balance of an account accordingly. The withdraw method does three simple checks:
  -  If the transaction is more than the balance in the account -> raise a InsufficientBalance exception.
  -  If the transaction is more than the account's withdrawal limit -> raise ExceedsLimit exception.
  -  If the account doesn't have an 'open' status -> raise AccountError.
Deposit will only do the last of those checks and raise AccountError.

### CheckingAccount & SavingsAccount *(class)*
Both inherit the Account base class and have minor differences from Account. CreditAccount was more of a eg. of some other account type we'd probably want to implement but wasn't intended for use in this project.

### Accounts *(class)*
Accounts is the struct that ties all accounts to one account holder and provides account information. From Accounts any given account is still easily accessible.
#### holder_info *(property)*:
Returns a __repr__ of the account holders to give  a quick summary of who the account holder is.
#### accounts *(property)*:
Returns a str summary of the number of accounts a given account holder has.
#### total_balance *(property)*:
Returns the total balance of all accounts registered to the given account holder. There are also methods for the totals of the individual account types, and any given account can be directly accessed to get it's balance.

### cards.py *(module)*
Struct __Card()__ is for tying a card to an account and an account holder and is the main tool used for connecting a transaction request to an account.
```python
self.account_holder = account_holder # AccountHolder object the card is linked to.
self.account = account # Account object the card is linked to.
self.holder_firstname = holder_firstname
self.holder_lastname = holder_lastname
self.card_number = card_number
self.__pin = pin # Private attr.
self.expiry_date = expiry_date
self.cvv = cvv
self.status = status
self.account.linked_cards[self.card_number] = self # Link the card with the account.
self.account_holder.cards[self.card_number] = {  # Also directly with the holder.
    "account": self.account,
    "card": self,
}
```
#### verify *(method)*:
Wasn't implemented in the processes but offers verification that the card attempting to make the transaction matches what's on record.

### exceptions.py *(module)*
#### InsufficientBalance *(Exception)*:
Raised when an amount greater than the account balance is attempted to be withdrawn.
#### AccountError *(Exception)*:
Raised if account doesn't have the right status for a given operation.
#### AccountNotExists *(Exception)*:
Raised if an account or card is not associated with the given bank. 
#### ExceedsLimit *(Exception)*:
Raised if there is a withdrawal attempt made that is greater than the limit set on the account, $5000 default.


## More
Please look through the tests (all in the tests directory) which contain further test case examples and provide demonstration of the project.