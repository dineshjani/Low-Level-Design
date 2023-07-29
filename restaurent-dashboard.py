from datetime import datetime, timedelta

class User:
    def __init__(self, email, name, area_code):
        self.email = email
        self.name = name
        self.area_code = area_code

class Restaurant:
    def __init__(self, restaurant_id, restaurant_code, name):
        self.restaurant_id = restaurant_id
        self.restaurant_code = restaurant_code
        self.name = name
        self.branches = []

class Branch:
    def __init__(self, branch_id, restaurant, location, capacity):
        self.branch_id = branch_id
        self.restaurant = restaurant
        self.location = location
        self.capacity = capacity
        self.visit_records = []

class VisitRecord:
    def __init__(self, user, branch, timestamp):
        self.user = user
        self.branch = branch
        self.timestamp = timestamp

class Dashboard:
    def __init__(self):
        self.restaurants = {}
        self.users = {}

    def add_user(self, email, name, area_code):
        user = User(email, name, area_code)
        self.users[email] = user

    def add_restaurant(self, restaurant_id, restaurant_code, name):
        restaurant = Restaurant(restaurant_id, restaurant_code, name)
        self.restaurants[restaurant_code] = restaurant

    def add_branch(self, branch_id, restaurant_code, location, capacity):
        if restaurant_code not in self.restaurants:
            raise ValueError("Restaurant not found.")
        restaurant = self.restaurants[restaurant_code]
        branch = Branch(branch_id, restaurant, location, capacity)
        restaurant.branches.append(branch)

    def record_visit(self, email, restaurant_code, branch_id, timestamp):
        if email not in self.users:
            raise ValueError("User not found.")
        if restaurant_code not in self.restaurants:
            raise ValueError("Restaurant not found.")
        restaurant = self.restaurants[restaurant_code]

        user = self.users[email]
        branch = next((b for b in restaurant.branches if b.branch_id == branch_id), None)
        if not branch:
            raise ValueError("Branch not found.")

        visit_record = VisitRecord(user, branch, timestamp)
        branch.visit_records.append(visit_record)

    def get_visits_by_branch(self, restaurant_code, branch_id, start_date, end_date):
        if restaurant_code not in self.restaurants:
            raise ValueError("Restaurant not found.")
        restaurant = self.restaurants[restaurant_code]

        branch = next((b for b in restaurant.branches if b.branch_id == branch_id), None)
        if not branch:
            raise ValueError("Branch not found.")

        visits = [record for record in branch.visit_records if start_date <= record.timestamp <= end_date]
        return visits

# Example usage:
if __name__ == "__main__":
    dashboard = Dashboard()

    # Add users
    dashboard.add_user("user1@example.com", "User 1", "Area-101")
    dashboard.add_user("user2@example.com", "User 2", "Area-102")

    # Add restaurants and branches
    dashboard.add_restaurant(1, "R1", "Restaurant 1")
    dashboard.add_branch(101, "R1", "Location A", 50)
    dashboard.add_branch(102, "R1", "Location B", 40)

    # Record visits
    dashboard.record_visit("user1@example.com", "R1", 101, datetime(2023, 7, 31, 10, 0, 0))
    dashboard.record_visit("user1@example.com", "R1", 101, datetime(2023, 8, 1, 12, 30, 0))
    dashboard.record_visit("user2@example.com", "R1", 101, datetime(2023, 8, 2, 15, 45, 0))
    dashboard.record_visit("user1@example.com", "R1", 102, datetime(2023, 8, 3, 11, 15, 0))
    dashboard.record_visit("user2@example.com", "R1", 102, datetime(2023, 8, 4, 9, 30, 0))

    # Get visits by branch for a specific period
    start_date = datetime(2023, 8, 1)
    end_date = datetime(2023, 8, 4)
    visits = dashboard.get_visits_by_branch("R1", 101, start_date, end_date)
    for visit in visits:
        print(f"{visit.user.name} visited {visit.branch.location} on {visit.timestamp}")
