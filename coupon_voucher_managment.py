# Assume we have getter and setters of all class properties.

from abc import ABC
from enum import Enum

class CouponStatus(Enum):
	ACTIVE, INACTIVE = 1, 2

class AccountStatus(Enum):
	ACTIVE, INACTIVE = 1, 2

class RuleTypes(Enum):
	AGE_LIMIT, TRANSACTION_VALUE_LIMIT, USAGE_LIMIT = 1, 2, 3

class Rule:
	def __init__(self, name, type):
		self.__name = name
		self.__type = type



# Each rule has different attributes and their own validations.

class AgeLimitRule(Rule):
	def __init__(self, name, type, initial_offset, final_offset=None):
		super(self).__init__(name, type)
		self.__initial_offset = initial_offset
		self.__final_offset = final_offset or float('INF')

	def can_apply(self, user, transaction, coupon):
		user_age = user.get_age()
		if user_age != None and user_age > self.__initial__offset and user_age < self.__final_offset:
			return True
		return False


# Similarlly we can add more rule classes... We can create rule for Overall usage limit similarlly.



class Token(ABC):
	def __init__(self, expiry_duration_in_days, name, description, creator, status=COUPON_STATUS.ACTIVE):
		self.__created_at = datetime.now()
		self.__exipiry_time = datetime.now + datetime.timedelta(expiry_duration_in_days)
		self.__name = name
		self.__status = status
		self.__description = description
		self.created_by = creator


class Coupon(Token):
	def __init__(self, id, expiry_duration_in_days, name, description, creator, status, rules)
		super(self).__init__(expiry_duration_in_days, name, description, creator, status)
		self.__id = id

		self.__rules = rules

		# <UserId>: <Number of times its been used>
		self.utilization = {}

	def add_rule(rule):
		self.__rules.append(rule)

	def apply_coupon(self, user, transaction):
		can_use_coupon = True
		for rule in self.__rules:
			if not rule.can_apply(user, transaction, coupon):
				can_use_coupon = False
				break
		can_use_coupon



class Voucher(Token):
	def __init__(self, expiry_duration_in_days, name, description, creator, status=COUPON_STATUS.ACTIVE, user=None):
		super(self).__init__(expiry_duration_in_days, name, description, creator, status)
		self.__user = user
		self.__is_used = False


# Singleton pattern
class System:
	self.instance = None
	class __OnlyOne:
		def __init__(self):
			self.__coupons = []
			self.__vouchers = []
			self.__admins = []
			self.__users = []


	def __init__(self):
		if not System.instance:
			self.instance = __OnlyOne()

	def add_voucher(expiry_duration_in_days, name, description, creator, status=COUPON_STATUS.ACTIVE, user=None):
		pass

class Person:
	def __init__(self, age, name):
		self.__age = age
		self.name = name

class Account:
	def __init__(self, email, password, status=AccountStatus.ACTIVE):
		self.__email = email
		self.__password = password
		self.__status = status

	def reset_password(self, password):
		pass

class Admin(Person):
	def __init__(self, account):
		self.__account = account
		self.system = system

	def create_voucher(expiry_duration_in_days, name, description, creator, status, user=None):
		system.create_voucher(expiry_duration_in_days, name, description, self, status, user=None)

	def update_voucher(voucher):
		pass

	def update_coupon(coupon):
		pass

class User(Person):
	def __init__(self, account):
		self.__account = account

	def get_coupons(self, transaction):
		# For all active coupons after checking rules it will return the list required.
		pass

	get_vouchers(self):
		voucher_list = []
		voucher_list.append(self.system.get_assigned_vouchers(user))
		voucher_list.append(self.system.get_unassigned_vouchers())
