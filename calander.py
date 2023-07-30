from datetime import datetime, timedelta
import uuid

class Event:
    def __init__(self, start, end, location, owner, user_list, title):
        self.event_id = str(uuid.uuid4())  # Generate a unique ID for each event
        self.start = start
        self.end = end
        self.location = location
        self.owner = owner
        self.user_list = user_list
        self.title = title
        self.user_responses = {user: "neutral" for user in user_list}

    def get_user_response(self, user):
        return self.user_responses[user]

    def set_user_response(self, user, response):
        if response in ["accepted", "rejected", "neutral"]:
            self.user_responses[user] = response


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.events = []  # List to store events associated with the user

    def add_event(self, event):
        self.events.append(event)

    def respond_to_event(self, event, response):
        event.set_user_response(self, response)

    def available_slots(self, duration_hours):
        slots = set()
        for event in self.events:
            current_slot = event.start
            while current_slot < event.end:
                slots.add(current_slot)
                current_slot += timedelta(hours=duration_hours)
        return slots


class Calendar:
    def __init__(self):
        self.events = []
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def add_event(self, event):
        self.events.append(event)
        event.calendar = self  # Associate the event with this calendar
        # Send event invitations to all users in the event's user list
        for user in event.user_list:
            user.respond_to_event(event, "neutral")

    def get_user_events(self, user):
        return [event for event in self.events if user in event.user_list]

    def get_event_details(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None
   def update_event(self, event_id, start=None, end=None, location=None, title=None):
        for event in self.events:
            if event.event_id == event_id:
                if start is not None:
                    event.start = start
                if end is not None:
                    event.end = end
                if location is not None:
                    event.location = location
                if title is not None:
                    event.title = title
                return True
        return False
    def find_common_free_slots(self, users, duration_hours):
        # Get the intersection of all user's event timeslots
        common_slots = set(users[0].available_slots(duration_hours))
        for user in users[1:]:
            common_slots.intersection_update(user.available_slots(duration_hours))

        # Find the start and end times of common free slots
        common_free_slots = []
        current_slot_start = None
        for slot in sorted(common_slots):
            if current_slot_start is None:
                current_slot_start = slot
            elif slot == current_slot_start + timedelta(hours=duration_hours):
                common_free_slots.append((current_slot_start, slot))
                current_slot_start = None
            else:
                current_slot_start = slot

        return common_free_slots


# Example usage:
if __name__ == "__main__":
    # Sample data creation
    user1 = User("user1_id", "John Doe", "john@example.com")
    user2 = User("user2_id", "Jane Smith", "jane@example.com")

    event1 = Event("2023-07-30 10:00", "2023-07-30 12:00", "Meeting Room A", user1, [user2], "Team Meeting")
    event2 = Event("2023-07-31 14:00", "2023-07-31 16:00", "Cafe B", user2, [user1], "Coffee Break")

    calendar = Calendar()
    calendar.add_user(user1)
    calendar.add_user(user2)
    calendar.add_event(event1)
    calendar.add_event(event2)

    # Perform actions on the calendar
    user1_calendar = calendar.get_user_events(user1)
    print("User 1 Calendar:")
    for event in user1_calendar:
        print(event.title, event.start, event.end, event.get_user_response(user1))

    user2_calendar = calendar.get_user_events(user2)
    print("User 2 Calendar:")
    for event in user2_calendar:
        print(event.title, event.start, event.end, event.get_user_response(user2))

    # User2 accepts event2 invitation
    user2.respond_to_event(event2, "accepted")

    # Perform actions on the calendar after user responses
    user2_calendar = calendar.get_user_events(user2)
    print("Updated User 2 Calendar:")
    for event in user2_calendar:
        print(event.title, event.start, event.end, event.get_user_response(user2))

    # Find common free slots for user1 and user2 with 1-hour duration
    common_free_slots = calendar.find_common_free_slots([user1, user2], duration_hours=1)
    print("Common Free Slots:")
    for start, end in common_free_slots:
        print(start, "to", end)
