from datetime import datetime, timedelta

class PaymentProcessor:
    @staticmethod
    def get_current_date():
        return datetime.now().strftime('%Y-%m-%d')

class Purchase:
    def __init__(self, purchase_date):
        self.purchase_date = purchase_date

class OneTimePurchase(Purchase):
    def __init__(self, amount_to_pay, purchase_date):
        super().__init__(purchase_date)
        self.amount_to_pay = amount_to_pay

class EmiPurchase(Purchase):
    def __init__(self, emi_amount, total_emis, purchase_date):
        super().__init__(purchase_date)
        self.emi_amount = emi_amount
        self.total_emis = total_emis
        self.next_payment_date = None

    def update_next_payment_date(self):
        self.next_payment_date = (datetime.strptime(self.purchase_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
        # Adjust next payment date if the next month doesn't have enough days
        while datetime.strptime(self.next_payment_date, '%Y-%m-%d').day != 1:
            self.next_payment_date = (datetime.strptime(self.next_payment_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

class User:
    def __init__(self, user_id, name, credit_limit):
        self.user_id = user_id
        self.name = name
        self.credit_limit = credit_limit
        self.balance = credit_limit
        self.one_time_purchases = []
        self.emi_purchases = []

    def make_one_time_purchase(self, purchase):
        if self.balance >= purchase.amount_to_pay:
            self.balance -= purchase.amount_to_pay
            purchase.purchase_date = PaymentProcessor.get_current_date()
            self.one_time_purchases.append(purchase)
            return True
        return False

    def make_emi_purchase(self, purchase):
        if self.balance >= purchase.emi_amount:
            self.balance -= purchase.emi_amount
            purchase.purchase_date = PaymentProcessor.get_current_date()
            purchase.update_next_payment_date()
            self.emi_purchases.append(purchase)
            return True
        return False

    def pay_emi(self):
        for purchase in self.emi_purchases:
            if purchase.next_payment_date <= PaymentProcessor.get_current_date():
                if self.balance >= purchase.emi_amount:
                    self.balance -= purchase.emi_amount
                    purchase.update_next_payment_date()
                    return True
                else:
                    self.notify_due_payment(purchase)
        return False

    def notify_due_payment(self, purchase):
        print(f"Due payment notification sent to user {self.user_id} for purchase {purchase.purchase_date}")

class BNPLSystem:
    def __init__(self):
        self.users = []

    def add_user(self, user_id, name, credit_limit):
        user = User(user_id, name, credit_limit)
        self.users.append(user)

    def get_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def make_one_time_purchase(self, user_id, amount_to_pay):
        user = self.get_user(user_id)
        if user:
            purchase = OneTimePurchase(amount_to_pay, PaymentProcessor.get_current_date())
            if user.make_one_time_purchase(purchase):
                print(f"One-time Purchase successful. User Balance: {user.balance}")
                return True
            else:
                print("Insufficient balance for one-time purchase.")
        else:
            print("User not found.")
        return False

    def make_emi_purchase(self, user_id, emi_amount, total_emis):
        user = self.get_user(user_id)
        if user:
            purchase = EmiPurchase(emi_amount, total_emis, PaymentProcessor.get_current_date())
            if user.make_emi_purchase(purchase):
                print(f"EMI Purchase successful. User Balance: {user.balance}")
                return True
            else:
                print("Insufficient balance for EMI purchase.")
        else:
            print("User not found.")
        return False

    def send_due_notifications(self):
        for user in self.users:
            user.pay_emi()

# Example usage:
system = BNPLSystem()
system.add_user(1, 'John Doe', 1000)
system.make_one_time_purchase(1, 200)
system.make_emi_purchase(1, 100, 6)

# Sending due notifications
system.send_due_notifications()
