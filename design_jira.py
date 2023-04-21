from enum import Enum

class TaskType(Enum):
    FEATURE = 1
    BUG = 2
    SUBTRACT = 3

class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    TESTING = 3
    DONE = 4



class User:
    def __init__(self):
        self.taskList = []

    def createTask(self, taskType):
        if taskType == TaskType.FEATURE:
            task = Task(self, taskType, "Feature task")
        elif taskType == TaskType.BUG:
            task = Task(self, taskType, "Bug task")
        elif taskType == TaskType.SUBTRACT:
            task = Task(self, taskType, "Subtract task")
           
        else:
            print("Invalid task type")
        self.taskList.append(task)
        return task

    def createSprint(self, startDate, endDate, name):
        sprint = Sprint(startDate, endDate, name)
        sprint.taskList = []
        return sprint

    def addToSprint(self, sprint, task):
        if task in self.taskList and task not in sprint.taskList:
            sprint.taskList.append(task)
            return True
        else:
            return False

    def removeFromSprint(self, sprint, task):
        if task in sprint.taskList:
            sprint.taskList.remove(task)
            return True
        else:
            return False

    def changeStatus(self, task, status):
        for t in self.taskList:
            if t.getId() == task.getId():
                t.setTaskStatus(status)
                return True
        return False

    def printAllTasks(self):
        print("User task list:")
        for task in self.taskList:
            print(task.toString())

class Task:
    idCount = 0

    def __init__(self, user, taskType, description):
        Task.idCount += 1
        self.id = Task.idCount
        self.user = user
        self.taskType = taskType
        self.description = description
        self.taskStatus = TaskStatus.TODO

    def getId(self):
        return self.id

    def getTaskStatus(self):
        return self.taskStatus

    def setTaskStatus(self, status):
        self.taskStatus = status

    def toString(self):
        return f"Task {self.id} ({self.taskType}): {self.description}, {self.taskStatus}"

class Sprint:
    def __init__(self, startDate, endDate, name):
        self.startDate = startDate
        self.endDate = endDate
        self.name = name
        self.taskList = []

    def printDetails(self):
        print(f"Sprint {self.name}: {self.startDate} to {self.endDate}")
        print("Sprint tasks:")
        for task in self.taskList:
            print(task.toString())

if __name__ == "__main__":
    user1 = User()
    user2 = User()

    task1 = user1.createTask(TaskType.FEATURE)
    task11 = user1.createTask(TaskType.BUG)
    task2 = user2.createTask(TaskType.BUG)
    task22 = user2.createTask(TaskType.SUBTRACT)

    sprint1 = user1.createSprint(22, 33, "Sprint1")
    sprint2 = user2.createSprint(44, 55, "Sprint2")

    print(user1.changeStatus(task11, TaskStatus.IN_PROGRESS)) # 1

    print(user1.addToSprint(sprint1, task1))
    print(user1.addToSprint(sprint1, task11))
    print(user1.addToSprint(sprint2, task1))
    print(user1.removeFromSprint(sprint1, task11))
    print(user2.addToSprint(sprint1, task1))
    print(user2.removeFromSprint(sprint1, task2))
    print(user2.addToSprint(sprint2, task1))
