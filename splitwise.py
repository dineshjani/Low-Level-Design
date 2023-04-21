from typing import List, Tuple
from enum import Enum
import itertools

class Split(Enum):
    EQUAL = 1
    EXACT = 2
    PERCENT = 3

class User:
    def __init__(self, name: str):
        self.name = name
        self.id = self.get_unique_id()
        self.total_expense_so_far = 0
        self.user_expense_sheet = []

    def add_to_user_expense_sheet(self, user, value):
        if self == user:
            return

        self.total_expense_so_far += value
        for i, (new_expense_user, new_expense_value) in enumerate(self.user_expense_sheet):
            if new_expense_user == user:
                self.user_expense_sheet[i] = (new_expense_user, new_expense_value + value)
                return
        self.user_expense_sheet.append((user, value))

    def print_total_balance(self):
        if self.total_expense_so_far > 0:
            print(f"{self.name} owes a total of {self.total_expense_so_far}")
        else:
            print(f"{self.name} gets back a total of {self.total_expense_so_far * (-1)}")

    def __eq__(self, other):
        return self.id == other.id

    def get_unique_id(self):
        User.unique_id = User.unique_id + 1 if hasattr(User, "unique_id") else 1
        return User.unique_id
        
    def getId(self):
        return self.id

class Expense:
    def __init__(self, creditor: User, split: Split, defaulters: List[User], exact_total_amount: float):
        self.creditor = creditor
        self.split = split
        self.defaulters = defaulters
        self.exact_total_amount = exact_total_amount
        self.id = self.get_unique_id()

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_exact_distribution(self):
        return self.exact_distribution

    def set_exact_distribution(self, exact_distribution):
        self.exact_distribution = exact_distribution

    def get_id(self):
        return self.id

    def get_percent_distribution(self):
        return self.percent_distribution

    def set_percent_distribution(self, percent_distribution):
        self.percent_distribution = percent_distribution

    def get_split(self):
        return self.split

    def get_creditor(self):
        return self.creditor

    def get_defaulters(self):
        return self.defaulters

    def get_exact_total_amount(self):
        return self.exact_total_amount

    def get_unique_id(self):
        Expense.unique_id = Expense.unique_id + 1 if hasattr(Expense, "unique_id") else 1
        return Expense.unique_id




class Splitwise:
    def __init__(self):
        self.userIdMap = {}
        self.users = []

    def registerUser(self, user: User):
        self.userIdMap[user.getId()] = user
        self.users.append(user)

    def calculateExpenses(self, expense: Expense) -> bool:
        creditor = expense.get_creditor()
        defaulters = expense.get_defaulters()
        amtPerHead = []
        if expense.get_split() == Split.EQUAL:
            amtPerHead = self.divideEqually(expense.get_exact_total_amount(), len(defaulters))
            for i, defaulter in enumerate(defaulters):
                self.userIdMap[creditor.getId()].add_to_user_expense_sheet(defaulter, (-1) * amtPerHead[i])
                self.userIdMap[defaulter.getId()].add_to_user_expense_sheet(creditor, amtPerHead[i])
        elif expense.get_split() == Split.EXACT:
            amtPerHead = expense.get_exact_distribution()
            if expense.get_exact_total_amount() != sum(amtPerHead):
                print("Can't create expense. Total amount doesn't equal sum of individual amounts. Please try again!")
                return False
            if len(amtPerHead) != len(defaulters):
                print("The amounts and value numbers don't match. Expense can't be created. Please try again!")
                return False
            for i, defaulter in enumerate(defaulters):
                self.userIdMap[creditor.getId()].add_to_user_expense_sheet(defaulter, (-1) * amtPerHead[i])
                self.userIdMap[defaulter.getId()].add_to_user_expense_sheet(creditor, amtPerHead[i])
        elif expense.get_split() == Split.PERCENT:
            amtPerHead = expense.get_percent_distribution()
            if 100 != sum(amtPerHead):
                print("Can't create expense. All percentages don't add to 100. Please try again!")
                return False
            if len(amtPerHead) != len(defaulters):
                print("The percents and value numbers don't match. Expense can't be created. Please try again!")
                return False
            for i, defaulter in enumerate(defaulters):
                amount = (amtPerHead[i] * expense.get_exact_total_amount()) / 100.0
                amount = round(amount, 2)
                self.userIdMap[creditor.getId()].add_to_user_expense_sheet(defaulter, (-1) * amount)
                self.userIdMap[defaulter.getId()].add_to_user_expense_sheet(creditor, amount)
        return True

    def printBalanceForAllUsers(self):
        for user in self.users:
            user.print_total_balance()

    def getUsers(self) -> List[User]:
        return self.users

    @staticmethod
    def divideEqually(amount: float, n: int) -> List[float]:
        return [round(amount/n, 2) for _ in range(n)]

    def simplifyExpenses(self):
        amounts = []
        for user in self.users:
            amounts.append((-1) * user.total_expense_so_far)
   
        min_amount = min(amounts)
        max_amount = max(amounts)
   
        while min_amount or max_amount:
            min_index = amounts.index(min_amount)
            max_index = amounts.index(max_amount)
   
            min_amount_to_pay = min(-min_amount, max_amount)
   
            amounts[min_index] += min_amount_to_pay
            amounts[max_index] -= min_amount_to_pay
   
            it_min = iter(self.users)
            it_max = iter(self.users)
   
            for i in range(min_index):
                next(it_min)
            for i in range(max_index):
                next(it_max)
   
            print(f"{next(it_min).name} pays the amount {min_amount_to_pay} to {next(it_max).name}")
   
            min_amount = min(amounts)
            max_amount = max(amounts)
            
    def addExpense(self, expense: Expense):
        if not self.verify_users(expense.creditor, expense.defaulters):
            print("Can't process expense. Kindly register all users and retry")
            return
        self.calculateExpenses(expense)

    def verify_users(self, user: User, users: List[User]):
        if user not in users:
            users.append(user)

        for usr in users:
            if usr.id not in self.userIdMap:
                return False
        return True
        


def main():
    s1 = "Jitu"
    s2 = "Navin"
    s3 = "Yogi"
    s4 = "Mandal"
    u1 = User(s1)
    u2 = User(s2)
    u3 = User(s3)
    u4 = User(s4)

    users = [u1, u2, u3, u4]

    sp = Splitwise()
    sp.registerUser(u1)
    sp.registerUser(u2)
    sp.registerUser(u3)
    sp.registerUser(u4)

    expense = Expense(u1, Split.EQUAL, users, 2000)
    sp.addExpense(expense)

    sp.printBalanceForAllUsers()

    users2 = [u2, u3]

    expense2 = Expense(u1, Split.EXACT, users2, 1400)
    expense2.set_exact_distribution([500, 900])
    sp.addExpense(expense2)
    sp.printBalanceForAllUsers()

    db2 = [40, 20, 20, 20]
    users3 = [u1, u2, u3, u4]

    expense3 = Expense(u4, Split.PERCENT, users3, 1200)
    expense3.set_percent_distribution(db2)
    sp.addExpense(expense3)
    sp.printBalanceForAllUsers()
    print("\n")
    print("\n")

    for user in sp.getUsers():
        for p in user.user_expense_sheet:
            if p[1] > 0:
                print(user.name + " owes a total of " + str(p[1]) + " to " + p[0].name)
            else:
                print(user.name + " gets back a total of " + str(abs(p[1])) + " from " + p[0].name)

    print("\n")
    sp.simplifyExpenses()

if __name__ == "__main__":
    main()
