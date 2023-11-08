import abc

class account:
	def __init__(self, name, phone, email):
		self.name = name
		self.phone = phone
		self.email = email

class person (metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def create (self):
		pass	

class admin (person):
	def __init__(self, account, password, adminID):
		self.account = account
		self.password = password
		self.adminID = adminID

	def create(self):
		print("Create user of type ADMIN")

	def createContest(self, contestID):
		print("Add contest ID to the list of contest")

class user (person):
	def __init__(self, account, password, score):
		self.account = account
		self.password = password
		self.score = score
	
	def create(self):
		print("Create a type of user USER")

	def registerContest(self, contestID):
		pass

	def withDrawContest(self, contestID):
		pass

	def incScore(self):
		pass

	def decScore(self):
		pass

class contest:
	def __init__(self, name, contestID):
		self.name = name
		self.contestID = contestID
		self.status = status
		self.questions = []
		self.users = []

	def registerUser(self, user, contestID):
		pass
		
	def addQuestion(self, questionID):
		pass

	def setStatus(self):
		pass

	def getStatus(self):
		pass

	def getallQuestions(self):
		pass

	def getallUsersforContest(self):
		pass

class question:
	def __init__(self, points, description):
		self.description = description
		self.points = points
		self.level = level

	def editQuestion(self, description, score):
		pass

class CodingBlox:
	def __init__(self):
		self.users = []
		self.questions = []
		self.contests = []
