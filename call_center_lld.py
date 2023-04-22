class Employee:
    def __init__(self, name, free, callManager):
        self.name = name
        self.free = free
        self.callManager = callManager
        self.rank = None

    def receive_call(self, call):
        self.free = False
        print(f"Call received by employee {self.name} for customer {call.customer.name}")

    def end_call(self, call):
        print(f"Call ended by employee {self.name} for customer {call.customer.name}"
        )
        self.free = True
        self.callManager.call_ended(call)

    def is_free(self):
        return self.free

    def set_free(self, free):
        self.free = free

    def get_rank(self):
        return self.rank

class Fresher(Employee):
    def __init__(self, name, free, callManager):
        super().__init__(name, free, callManager)
        self.rank = 1

    def escalate_call(self, call):
        self.set_free(True)
        call.set_rank(call.get_rank() + 1)
        self.callManager.call_handler(call)

class Lead(Employee):
    def __init__(self, name, free, callManager):
        super().__init__(name, free, callManager)
        self.rank = 2

    def escalate_call(self, call):
        self.set_free(True)
        call.set_rank(call.get_rank() + 1)
        self.callManager.call_handler(call)

class Manager(Employee):
    def __init__(self, name, free, callManager):
        super().__init__(name, free, callManager)
        self.rank = 3

class Call:
    def __init__(self, customer):
        self.rank = 1
        self.customer = customer

    def get_rank(self):
        return self.rank

    def set_rank(self, rank):
        self.rank = rank

    def get_customer(self):
        return self.customer

class Customer:
    def __init__(self, name, email, phoneNo):
        self.name = name
        self.email = email
        self.phoneNo = phoneNo

    def get_name(self):
        return self.name

class CallManager:
    levels = 3
    employee_call_map = {}

    def __init__(self, number_of_freshers, number_of_leads):
        self.employeesList = [[] for _ in range(self.levels)]
        self.callQueue = []
        for i in range(number_of_freshers):
            self.employeesList[0].append(Fresher(f"Fresher{i}", True, self))
        for i in range(number_of_leads):
            self.employeesList[1].append(Lead(f"Lead{i}", True, self))
        self.employeesList[2].append(Manager("Manager", True, self))

    def get_free_employee(self, rank):
        for i in range(rank-1, self.levels):
            employees = self.employeesList[i]
            for employee in employees:
                if employee.is_free():
                    return employee
        return None

    def call_handler(self, call):
        employee = self.get_free_employee(call.get_rank())
        if employee:
            call.set_rank(employee.get_rank())
            self.employee_call_map[call] = employee
            employee.receive_call(call)
        else:
            self.callQueue.append(call)

    def handle_call_from_queue(self):
        if self.callQueue:
            call = self.callQueue[0]
            call_rank = call.get_rank()
            employee = self.get_free_employee(call_rank)
            if employee:
                self.callQueue.pop(0)
                self.employee_call_map[call] = employee
                employee.receive_call(call)
    def end_call(self,call):
        emp = self.employee_call_map[call]
        emp.end_call(call)
        
    def call_ended(self,call):
        del self.employee_call_map[call]
        self.handle_call_from_queue()
    
    

def main():
    number_of_freshers = 3
    number_of_leads = 2
    call_manager = CallManager(number_of_freshers,number_of_leads)
    customer_1 = Customer("dinesh","dineshjani450@gmail.com",9511557211) 
    call_1 = Call(customer_1)
    customer_2 = Customer("praveen","dineshjani450@gmail.com",9511557211) 
    call_2 = Call(customer_2)
    customer_3 = Customer("suresh","dineshjani450@gmail.com",9511557211) 
    call_3 = Call(customer_3)
    customer_4 = Customer("hanu","dineshjani450@gmail.com",9511557211) 
    call_4 = Call(customer_4)
    customer_5 = Customer("Yuvi","dineshjani450@gmail.com",9511557211) 
    call_5 = Call(customer_5)
    customer_6 = Customer("Piyo","dineshjani450@gmail.com",9511557211) 
    call_6 = Call(customer_6)
    customer_7= Customer("mohan","dineshjani450@gmail.com",9511557211) 
    call_7 = Call(customer_7)
    call_manager.call_handler(call_1)
    call_manager.call_handler(call_2)
    call_manager.call_handler(call_3)
    call_manager.call_handler(call_4)
    call_manager.call_handler(call_5)
    call_manager.call_handler(call_6)
    call_manager.call_handler(call_7)
    call_manager.end_call(call_1)
    
    
main()
