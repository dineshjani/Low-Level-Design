class Handler:
    def set_next_handler(self, handler):
        raise NotImplementedError(f"{self.__class__} has not implemented the set_next_handler method.")
    def handle(self, request):
        raise NotImplementedError(f"{self.__class__} has not implemented the handle method.")
        
class MafiaHandler(Handler):
    
    def set_next_handler(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, request):
        if hasattr(self, "next_handler"):
            return self.next_handler.handle(request)
        return None
        
class Godfather(MafiaHandler):
    def handle(self, request):
        return super().handle(request)

class Underboss(MafiaHandler):
    def handle(self, request):
        if request == "collect_profits":
            return "Underboss orders collection of profits from criminal enterprises"
        elif request == "serve_as_acting_boss":
            return "Underboss instated as acting boss or Godfather"
        else:
            return super().handle(request)

class Consigliere(MafiaHandler):
    def handle(self, request):
        if request == "attend_meeting":
            return "Consigliere represents the Godfather at meeting with another Mafia family"
        elif request == "provide_counsel":
            return "Consigliere provides advise to the Godfather"
        else:
            return super().handle(request)

class Caporegime(MafiaHandler):
    def handle(self, request):
        if request == "recruit_soldier":
            return "Caporegime recruits a soldier"
        elif request == "order_murder":
            return "Caporegime orders a murder"
        else:
            return super().handle(request)

class Soldier(MafiaHandler):
    def handle(self, request):
        if request == "murder":
            return "Soldier commits a murder on order"
        elif request == "beat_up":
            return "Soldier commits beats up the targetted person on order"
        elif request == "threaten":
            return "Soldier commits intimidates the targetted person on order"
        else:
            return super().handle(request)

# Create a handler instances
godfather = Godfather()
underboss = Underboss()
consigliere = Consigliere()
caporegime = Caporegime()
soldier = Soldier()

# Create the chain of responsibility
godfather.set_next_handler(underboss).set_next_handler(consigliere).set_next_handler(caporegime).set_next_handler(soldier)
print(underboss.handle("recruit_soldier")) # Caporegime recruits a soldier
print(godfather.handle("attend_meeting")) # Consigliere represents the Godfather at meeting with another Mafia family


