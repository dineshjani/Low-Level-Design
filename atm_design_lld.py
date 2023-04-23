class User:
    def __init__(self):
        self.card = None
        self.account = None
    # Other user methods

class Account:
    def __init__(self, amount):
        self.balance = amount

    def update_balance(self, amount):
        self.balance += amount
    # Other cash methods

class Card:
    def authenticate(self, pin):
        # PIN authentication login
        pass
    # Other card methods

class Cash:
    def __init__(self, amount):
        self.total_amount = amount

    def valid(self):
        return self.valid_amount() == self.total_amount

    def valid_amount(self):
        # Valid amount
        pass

    def invalid_amount(self):
        # Invalid amount
        pass
    # Other cash methods

class ATM:
    available_cash = 1000000

    def __init__(self, user):
        self.state = ReadyState()
        self.user = user
    
    def change_state(self, state):
        self.state = state

    def read_inserted_card(self):
        self.state = "enter_pin" if self.state == "ready" else self.state

    def authenticate_pin(self, pin):
        if self.state != "enter_pin":
            return
        if self.user.card.authenticate(pin):
            self.state = "select_transaction"
        else:
            self.exit()

    def select_transaction(self, transaction):
        if self.state != "select_transaction":
            return
        if transaction == "deposit":
            self.state = "deposit"
        elif transaction == "withdraw":
            self.state = "withdraw"
        elif transaction == "display_balance":
            self.state = "display_balance"

    def deposit_cash(self, cash):
        if self.state != "deposit":
            return
        self.process_deposited_cash(cash)

    def invalid_cash_returned(self):
        self.state = "display_balance" if self.state == "invalid_cash_returned" else self.state
        self.display_balance()

    def enter_withdrawal_amount(self, amount):
        if self.state != "withdraw":
            return
        if self.can_dispense_cash(amount):
            self.execute_transaction(-amount)
            self.state = "cash_dispensed"
        else:
            self.state = "error_message_displayed"

    def cash_dispensed(self):
        self.state = "display_balance" if self.state == "cash_dispensed" else self.state
        self.display_balance()

    def display_balance(self):
        if self.state != "display_balance":
            return
        print(f"Balance: Rs. {self.user.account.balance}")

    def transact_again(self):
        if self.state in ["deposit", "withdraw", "display_balance", "error_message_displayed"]:
            self.state = "select_transaction"

    def exit(self):
        if self.state in ["enter_pin", "select_transaction", "display_balance", "error_message_displayed"]:
            self.state = "exit_message_displayed"

    def return_card(self):
        # Logic to return card
        pass

    def can_dispense_cash(self, amount):
        return self.user.account.balance >= amount and self.available_cash >= amount

    def update_available_cash(self, amount):
        self.available_cash += amount

    def execute_transaction(self, amount):
        # Execute both or none
        self.update_available_cash(amount)
        self.user.account.update_balance(amount)

    def process_deposited_cash(self, cash):
        self.execute_transaction(cash.valid_amount())
        self.state = "display_balance" if cash.valid() else "invalid_cash_returned"

class ATMState:
    def __init__(self, atm):
        self.atm = atm

    def read_inserted_card(self):
        pass

    def authenticate_pin(self, pin):
        pass

    def select_transaction(self, transaction):
        pass

    def deposit_cash(self, cash):
        pass

    def invalid_cash_returned(self):
        pass

    def enter_withdrawal_amount(self, amount):
        pass

    def cash_dispensed(self):
        pass

    def display_balance(self):
        pass

    def transact_again(self):
        pass

    def exit(self):
        pass

    def return_card(self):
        pass


class ReadyState(ATMState):
    def read_inserted_card(self):
        self.atm.change_state(EnterPinState(self.atm))


class EnterPinState(ATMState):
    def authenticate_pin(self, pin):
        if self.atm.user.card.authenticate!(pin):
            self.atm.change_state(SelectTransactionState(self.atm))
        else:
            self.exit()

    def exit(self):
        self.atm.change_state(ExitMessageDisplayedState(self.atm))


class SelectTransactionState(ATMState):
    def select_transaction(self, transaction):
        if transaction == "deposit":
            self.atm.change_state(DepositState(self.atm))
        elif transaction == "withdraw":
            self.atm.change_state(WithdrawState(self.atm))
        elif transaction == "display_balance":
            self.atm.change_state(DisplayBalanceState(self.atm))

    def exit(self):
        self.atm.change_state(ExitMessageDisplayedState(self.atm))


class DepositState(ATMState):
    def deposit_cash(self, cash):
        self.atm.execute_transaction(cash.valid_amount)
        state = (
            DisplayBalanceState(self.atm)
            if cash.valid_
            else InvalidCashReturnedState(self.atm)
        )
        self.atm.change_state(state)

    def transact_again(self):
        self.atm.change_state(SelectTransactionState(self.atm))


class WithdrawState(ATMState):
    def enter_withdrawal_amount(self, amount):
        if self.atm.can_dispense_cash(amount):
            self.atm.execute_transaction(-amount)
            self.atm.change_state(CashDispensedState(self.atm))
        else:
            self.atm.change_state(ErrorMessageDisplayedState(self.atm))

    def transact_again(self):
        self.atm.change_state(SelectTransactionState(self.atm))


class DisplayBalanceState(ATMState):
    def display_balance(self):
        print(f"Balance: Rs. {self.atm.user.account.balance}")


class CashDispensedState(ATMState):
    def cash_dispensed(self):
        self.atm.change_state(DisplayBalanceState(self.atm))


class InvalidCashReturnedState(ATMState):
    def invalid_cash_returned(self):
        self.atm.change_state(DisplayBalanceState(self.atm))


class ErrorMessageDisplayedState(ATMState):
    def exit(self):
        self.atm.change_state(ExitMessageDisplayedState(self.atm))


class ExitMessageDisplayedState(ATMState):
    def return_card(self):
        # Logic to return card
        pass

