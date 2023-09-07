from enum import Enum
import math

class Gender(Enum):
    MALE = 1
    FEMALE = 2

class User:
    current_id = 0

    def __init__(self, age, x_loc, y_loc, gender, interest):
        self.userId = User.current_id
        User.current_id += 1
        self.age = age
        self.xLoc = x_loc
        self.yLoc = y_loc
        self.gender = gender
        self.set = set()
        self.interest = interest

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def get_x_loc(self):
        return self.xLoc

    def set_x_loc(self, x_loc):
        self.xLoc = x_loc

    def get_y_loc(self):
        return self.yLoc

    def set_y_loc(self, y_loc):
        self.yLoc = y_loc

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender

    def get_interest(self):
        return self.interest

    def set_interest(self, interest):
        self.interest = interest

class PotentialData:
    def __init__(self, user):
        self.user = user
        self.distance_between_potentie_and_potential = 0
        self.age_diff = 0

class PotentialPoints:
    def __init__(self, user_id, points):
        self.user_id = user_id
        self.points = points

class OnlineDating:
    def __init__(self):
        self.current_id = 0
        self.matched_in_app = {}
        self.users_info = {}
        self.male_users = []
        self.female_users = []

    def create_user(self, gender, age, interest, x_loc, y_loc):
        user = User(age, x_loc, y_loc, gender, interest)
        self.users_info[user.userId] = user
        self.save_to_gender_data(user)
        return user

    def save_to_gender_data(self, user):
        if user.get_gender() == Gender.MALE:
            self.male_users.append(user)
        else:
            self.female_users.append(user)

    def liked_user(self, user_id, liked_user_id):
        user = self.users_info.get(user_id)
        liked_user = self.users_info.get(liked_user_id)
        if user is None or liked_user is None:
            print("One of the users does not exist for these IDs.")
            return
        if liked_user.userId in user.set:
            self.save_match_for_users(user.userId, liked_user.userId)
            self.save_match_for_users(liked_user.userId, user.userId)
        user.set.add(liked_user_id)
        print(f"user={user.userId} likes user with id={liked_user.userId}")

    def save_match_for_users(self, user_id, liked_user_id):
        print(f"Match for user={user_id} and user with id={liked_user_id}")
        if user_id not in self.matched_in_app:
            self.matched_in_app[user_id] = set()
        self.matched_in_app[user_id].add(liked_user_id)

    def show_all_matches(self):
        for user in self.matched_in_app:
            self.show_matches_with_user(user)

    def show_matches_with_user(self, user_id):
        matches = self.matched_in_app.get(user_id, set())
        if len(matches) == 0:
            print(f"There are no matches for user={user_id}")
            return
        print(f"Matches of user={user_id}")
        for match_user_id in matches:
            print(self.users_info[match_user_id].userId)

    def delete_account(self, user_id):
        user = self.users_info.get(user_id)
        if user is not None:
            user.set.clear()
            for match_user_id in self.matched_in_app.get(user_id, set()):
                if user_id in self.matched_in_app.get(match_user_id, set()):
                    self.matched_in_app[match_user_id].remove(user_id)
            self.matched_in_app.pop(user_id, None)
            print(f"Deleting likes and matches for user={user_id}")

    def potential_matches_for_user(self, user_id):
        potentie_user = self.users_info.get(user_id)
        potential_points = []
        if potentie_user is not None:
            potential_datas = []
            if potentie_user.get_gender() == Gender.MALE:
                other_users = self.female_users
            else:
                other_users = self.male_users

            for other_user in other_users:
                potential_datas.append(self.create_potential_data_for_user(potentie_user, other_user))

            for data in potential_datas:
                points = self.calculate_points(data)
                potential_points.append(PotentialPoints(data.user.userId, points))

            potential_points.sort(key=lambda x: x.points)

        return potential_points

    def calculate_points(self, data):
        points = 0.0
        points += data.age_diff
        points += data.distance_between_potentie_and_potential
        return points

    def create_potential_data_for_user(self, user, other_user):
        data = PotentialData(other_user)
        data.age_diff = abs(user.age - other_user.age)
        dist = self.calculate_distance(user.xLoc, user.yLoc, other_user.xLoc, other_user.yLoc)
        data.distance_between_potentie_and_potential = dist
        return data

    def calculate_distance(self, x_loc, y_loc, x_loc1, y_loc1):
        value = abs(x_loc1 - x_loc)
        value2 = abs(y_loc1 - y_loc)
        distance_calculated = math.sqrt((value ** 2) + (value2 ** 2))
        return distance_calculated

class OnlineDatingDriver:
    def __init__(self):
        self.online_dating_service = OnlineDatingService()
        self.online_dating = OnlineDating()

    def get_online_dating_service(self):
        return self.online_dating_service

    def set_online_dating_service(self, online_dating_service):
        self.online_dating_service = online_dating_service

    def get_online_dating(self):
        return self.online_dating

    def set_online_dating(self, online_dating):
        self.online_dating = online_dating

    def main(self):
        online_dating_driver = OnlineDatingDriver()
        online_dating_driver.online_dating = OnlineDating()
        userA = online_dating_driver.get_online_dating().create_user(Gender.MALE, 20, "cricket", 1.0, 2.0)
        userB = online_dating_driver.get_online_dating().create_user(Gender.FEMALE, 22, "basket", 2.0, 3.0)

        online_dating_driver.get_online_dating().liked_user(userA.userId, userB.userId)
        online_dating_driver.get_online_dating().liked_user(userB.userId, userA.userId)

        online_dating_driver.get_online_dating().show_all_matches()

        online_dating_driver.get_online_dating().delete_account(userA.userId)
        print("after deleting account")
        online_dating_driver.get_online_dating().show_all_matches()

        print("creating other users")
        userC = online_dating_driver.get_online_dating().create_user(Gender.FEMALE, 27, "carrom", 3.0, 4.0)
        userD = online_dating_driver.get_online_dating().create_user(Gender.FEMALE, 26, "football", 3.0, 4.0)
        online_dating_driver.get_online_dating().liked_user(userA.userId, userB.userId)
        online_dating_driver.get_online_dating().liked_user(userB.userId, userA.userId)
        online_dating_driver.get_online_dating().show_all_matches()
        print("potential matches for user ")
        print(online_dating_driver.get_online_dating().potential_matches_for_user(userA.userId))

if __name__ == "__main__":
    driver = OnlineDatingDriver()
    driver.main()








#Problem Description:
'''
You have to create an online dating application. Every active user account will have location, age and
gender information. The application should show users their potential matches in order of relevance.
The ordering of relevance will be following:
1. Gender : Opposite gender to be given higher priority.
2. Proximity: Nearer matches should be given more priority. Use euclidean distance for computing
distance between two locations (*see appendix for euclidean distance).
3. Age: Less the age difference should be given more priority.
Operations:
A user can perform these operations in this application:
1. Create Account: A person can create an account with interest and profile details.
2. Potential Match: Provides all the potential match of a user in relevance order.
3. Like: User can like a potential match user.
4. Show Matches: Showing the users which match against a user. A match happens when both the
users have liked each other.
5. Show All Matches: Showing system view by displaying all the matches in the system.
6. Ignore: User can ignore a potential match user.
7. Delete Account: If a user deletes account, then all matches and likes will be removed.
Use case:
1. If a user A likes user B, the data should be stored for further processing.
2. All the matches(case where 2 users have liked each other) in the system should be shown.
Expectations:
1. Code should be demo-able. Either use a main driver program on command line or test cases.
2. Code should be functionally correct and complete.
3. Code should be readable, modular, testable and use proper naming conventions. It should be
easy to add/remove functionality without rewriting entire codebase.
4. Code should cover all the edge cases possible and work for them or fail gracefully for errors.
Guidelines:
1. Use language of your choice.
2. Output can be written to a file or STDOUT.
3. Feel free to store all interim/output data in-memory.
4. Restrict internet usage to looking up syntax.
5. Please discuss any doubts you have with an interviewer.
Appendix:
The distance between two points in the plane with coordinates (x, y) and (a, b) is given by:
dist((x, y), (a, b)) = sqrt((x - a)2 + (y - b)2)
'''










