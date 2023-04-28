class Product:
    def __init__(self, name, description, price, stock_level):
        self.name = name
        self.description = description
        self.price = price
        self.stock_level = stock_level

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_price(self):
        return self.price

    def set_price(self, price):
        self.price = price

    def get_stock_level(self):
        return self.stock_level

    def set_stock_level(self, stock_level):
        self.stock_level = stock_level

    def __eq__(self, other):
        return (self.name == other.name and
                self.description == other.description and
                self.price == other.price and
                self.stock_level == other.stock_level)


class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def total_cost(self):
        total = 0
        for product in self.products:
            total += product.get_price()
        return total


class Customer:
    def __init__(self, name, address, email):
        self.name = name
        self.address = address
        self.email = email

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def __eq__(self, other):
        return self.name == other.name and self.address == other.address and self.email == other.email


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product, stock):
        self.products[product] = stock

    def update_stock(self, product, stock):
        self.products[product] = stock

    def is_in_stock(self, product):
        return self.products[product] > 0

    def restock(self, product, quantity):
        self.products[product] += quantity


class Payment:
    def __init__(self):
        self.amount = 0
        self.payment_method = ""

    def __init__(self, amount, payment_method):
        self.amount = amount
        self.payment_method = payment_method

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_payment_method(self):
        return self.payment_method

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def pay_with_credit_card(self):
        # code to process credit card payment
        pass

    def pay_with_debit_card(self):
        # code to process debit card payment
        pass

    def pay_with_net_banking(self):
        # code to process net banking payment
        pass


class Shipping:
    def __init__(self, shipping_method="", shipping_cost=0.0):
        self.shipping_method = shipping_method
        self.shipping_cost = shipping_cost
    
    def get_shipping_method(self):
        return self.shipping_method
    
    def get_shipping_cost(self):
        return self.shipping_cost
    
    def set_shipping_method(self, shipping_method):
        self.shipping_method = shipping_method
    
    def set_shipping_cost(self, shipping_cost):
        self.shipping_cost = shipping_cost


class Order:
    def __init__(self, customer, products, total_cost, payment, shipping):
        self.customer = customer
        self.products = products
        self.total_cost = total_cost
        self.payment = payment
        self.shipping = shipping
    
    def get_customer(self):
        return self.customer
    
    def get_products(self):
        return self.products
    
    def get_total_cost(self):
        return self.total_cost
    
    def get_payment(self):
        return self.payment
    
    def get_shipping(self):
        return self.shipping
    
    def set_customer(self, customer):
        self.customer = customer
    
    def set_products(self, products):
        self.products = products
    
    def set_total_cost(self, total_cost):
        self.total_cost = total_cost
    
    def set_payment(self, payment):
        self.payment = payment
    
    def set_shipping(self, shipping):
        self.shipping = shipping
    
    def __eq__(self, other):
        return (self.customer == other.customer and
                self.products == other.products and
                self.total_cost == other.total_cost)


class Admin:
    def __init__(self):
        self.inventory = Inventory()
        self.products = []
        self.customers = []
        self.orders = []
    
    def add_product(self, product):
        self.products.append(product)
    
    def update_product(self, product):
        for i, p in enumerate(self.products):
            if p == product:
                self.products[i] = product
                break
    
    def update_stock_level(self, product, stock_level):
        for i, p in enumerate(self.products):
            if p == product:
                p.set_stock_level(stock_level)
                break
    
    def add_order(self, order):
        self.orders.append(order)
    
    def update_order(self, order):
        for i, o in enumerate(self.orders):
            if o == order:
                self.orders[i] = order
                break
    
    def add_customer(self, customer):
        self.customers.append(customer)
    
    def update_customer(self, customer):
        for i, c in enumerate(self.customers):
            if c == customer:
                self.customers[i] = customer
                break
def main():
    # Create a new product
    p1 = Product("iPhone", "New iPhone", 999.99, 10)
    
    # Create a new inventory
    inventory = Inventory()
    
    # Add the product to the inventory
    inventory.addProduct(p1, 10)
    
    # Create a new customer
    c1 = Customer("John Smith", "123 Main St", "johnsmith@email.com")
    
    # Create a new shopping cart
    cart = ShoppingCart()
    
    # Add the product to the cart
    cart.addProduct(p1)
    
    # Check if the product is in stock
    if inventory.isInStock(p1):
        print("Product is in stock")
    else:
        print("Product is out of stock")
    
    # Print the total cost of items in the cart
    print("Total cost: Rs", cart.totalCost())
    
    # Create a new payment
    payment = Payment(cart.totalCost(), "Credit Card")
    
    # Print the payment details
    print("Payment amount: Rs", payment.getAmount())
    print("Payment method:", payment.getPaymentMethod())
    
