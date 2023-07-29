from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, publication_date, rack_number):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.rack_number = rack_number

    def __str__(self):
        return f"{self.title} by {self.author}"

class BookItem:
    def __init__(self, book, barcode):
        self.book = book
        self.barcode = barcode
        self.status = "Available"

    def __str__(self):
        return f"{self.book.title} [{self.barcode}] - {self.status}"

class LibraryMember:
    def __init__(self, member_id, name, member_card):
        self.member_id = member_id
        self.name = name
        self.member_card = member_card
        self.checked_out_books = []
        self.reserved_books = []

    def __str__(self):
        return f"{self.name} (Member ID: {self.member_id}, Member Card: {self.member_card})"

class LibraryTransaction: 
    def __init__(self, book_item, member, due_date):
        self.book_item = book_item
        self.member = member
        self.due_date = due_date

    def calculate_fine(self):
        if datetime.now() > self.due_date:
            days_overdue = (datetime.now() - self.due_date).days
            return 0.5 * days_overdue  # Assuming a fine of $0.50 per day of delay
        return 0

    @staticmethod
    def is_book_item_available(book_item):
        return book_item.status == "Available"

    def reserve_book_item(self, book_item):
        if self.is_book_item_available(book_item):
            book_item.status = "Reserved"
            self.member.reserved_books.append(book_item)

    def checkout_book_item(self, book_item):
        if self.is_book_item_available(book_item):
            if len(self.member.checked_out_books) >= 5:
                print("Checkout failed: You have reached the maximum limit for book check-outs.")
                return False

            due_date = datetime.now() + timedelta(days=10)  # 10 days checkout period
            transaction = LibraryTransaction(book_item, self.member, due_date)
            self.member.checked_out_books.append(transaction)
            book_item.status = "Checked-Out"
            print("Book checked out successfully.")
            return True
        else:
            print("Checkout failed: The book item is not currently available.")
            return False

    def return_book_item(self, book_item):
        if book_item.status == "Checked-Out":
            book_item.status = "Available"
            self.member.checked_out_books.remove(self)

            fine_amount = self.calculate_fine()
            if fine_amount > 0:
                print(f"Fine for late return: ${fine_amount:.2f}")
        else:
            print("Book return failed: The book item is not currently checked out.")

class LibraryCatalog:
    def __init__(self):
        self.books = {}  # Dictionary to store books
        self.book_items = {}  # Dictionary to store book items
        self.members = {}
        self.transactions = []

    def add_book(self, book):
        self.books[book.book_id] = book

    def add_book_item(self, book_item):
        self.book_items[book_item.barcode] = book_item

    def add_member(self, member):
        self.members[member.member_id] = member

    def search_book_items_by_title(self, title):
        matching_items = []
        for item in self.book_items.values():
            if title.lower() in item.book.title.lower():
                matching_items.append(item)
        return matching_items

    def search_book_items_by_author(self, author):
        matching_items = []
        for item in self.book_items.values():
            if author.lower() in item.book.author.lower():
                matching_items.append(item)
        return matching_items

    def search_book_items_by_publication_date(self, publication_date):
        matching_items = []
        for item in self.book_items.values():
            if publication_date == item.book.publication_date:
                matching_items.append(item)
        return matching_items

    def is_book_item_available(self, book_item):
        return book_item.status == "Available"

    def is_book_available(self, book):
        for item in self.book_items.values():
            if item.book == book and item.status == "Available":
                return True
        return False

    def reserve_book_item(self, barcode, member_id):
        if barcode not in self.book_items or member_id not in self.members:
            print("Reservation failed: Invalid book item or member ID.")
            return False

        book_item = self.book_items[barcode]
        member = self.members[member_id]

        if self.is_book_item_available(book_item):
            print("Reservation failed: The book item is currently available for checkout.")
            return False

        # Check if the member already has this book item reserved
        if any(item.status == "Reserved" for item in member.reserved_books):
            print("Reservation failed: You have already reserved this book item.")
            return False

        # Reserve the book item
        self.transactions.append((barcode, member_id))
        book_item.status = "Reserved"
        member.reserved_books.append(book_item)
        print("Book item reserved successfully.")
        return True

class NotificationService:
    def send_notification(self, member, message):
        print(f"Sending notification to {member.name}: {message}")

    def notify_due_date(self, transaction):
        due_date = transaction.due_date.strftime("%Y-%m-%d")
        message = f"Reminder: The due date for '{transaction.book_item.book.title}' is {due_date}. Please return the book on time."
        self.send_notification(transaction.member, message)

    def notify_overdue(self, transaction):
        days_overdue = (datetime.now() - transaction.due_date).days
        message = f"Warning: The book '{transaction.book_item.book.title}' is {days_overdue} days overdue. Please return the book as soon as possible."
        self.send_notification(transaction.member, message)

    def check_overdue_books(self, catalog):
        today = datetime.now()
        for member in catalog.members.values():
            for transaction in member.checked_out_books:
                if transaction.due_date < today:
                    self.notify_overdue(transaction)

def simulate_cron_job(catalog, notification_service):
    while True:
        notification_service.check_overdue_books(catalog)
        time.sleep(86400)  # Sleep for 24 hours (86400 seconds) before checking again

# Example usage:
if __name__ == "__main__":
    # Create LibraryCatalog and NotificationService instances
    catalog = LibraryCatalog()
    # notification_service = NotificationService()  # Assume the implementation of NotificationService

    # Create and add books to the catalog
    book1 = Book(1, "Book Title 1", "Author A", "2023-07-29", "Rack-1")
    book2 = Book(2, "Book Title 2", "Author B", "2023-07-30", "Rack-2")
    catalog.add_book(book1)
    catalog.add_book(book2)

    # Create and add book items to the catalog
    book_item1 = BookItem(book1, "BK-101")
    book_item2 = BookItem(book1, "BK-102")
    book_item3 = BookItem(book2, "BK-201")
    catalog.add_book_item(book_item1)
    catalog.add_book_item(book_item2)
    catalog.add_book_item(book_item3)

    # Create and add a library member
    member1 = LibraryMember(101, "John Doe", "CARD-101")
    catalog.add_member(member1)

    # Reserve a book item that is not currently available
    catalog.reserve_book_item(book_item1.barcode, member1.member_id)

    # Try to reserve the same book item again (should fail)
    catalog.reserve_book_item(book_item1.barcode, member1.member_id)

    # Checkout a book item (should succeed)
    transaction1 = LibraryTransaction(book_item1, member1, datetime.now() + timedelta(days=5))
    member1.checked_out_books.append(transaction1)
    book_item1.status = "Checked-Out"

    # Try to reserve a book item that is currently available (should fail)
    catalog.reserve_book_item(book_item1.barcode, member1.member_id)

    # Search for books by title, author, and publication date
    print("Search results by title:")
    for item in catalog.search_book_items_by_title("title"):
        print(item)

    print("\nSearch results by author:")
    for item in catalog.search_book_items_by_author("author"):
        print(item)

    print("\nSearch results by publication date:")
    for item in catalog.search_book_items_by_publication_date("2023-07-29"):
        print(item)

    # Print member information
    print("\nMember information:")
    print(member1)
    print("Checked-out books:")
    for transaction in member1.checked_out_books:
        print(f"{transaction.book_item.book.title} - Due Date: {transaction.due_date}")

    print("\nReserved books:")
    for book_item in member1.reserved_books:
        print(book_item)

    # Return a book item
    transaction1.return_book_item(book_item1)

