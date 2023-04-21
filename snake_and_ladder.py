import random

class Snake:
    def __init__(self, start, end):
        self.start = start
        self.end = end
   
    def getEnd(self):
        return self.end
   
    def getStart(self):
        return self.start

class Ladder:
    def __init__(self, start, end):
        self.start = start
        self.end = end
   
    def getEnd(self):
        return self.end
   
    def getStart(self):
        return self.start

class Player:
    def __init__(self, name):
        self.name = name
        self.id = self.getUniqueId()
        self.currentPosition = 0
   
    def getCurrentPosition(self):
        return self.currentPosition
   
    def setCurrentPosition(self, currentPosition):
        self.currentPosition = currentPosition
   
    def getId(self):
        return self.id
   
    def getName(self):
        return self.name
   
    def getUniqueId(self):
        Player.playerId = getattr(Player, 'playerId', 0) + 1
        return Player.playerId

class Game:
    def __init__(self, snakes, ladders, players):
        self.players = players
        self.snakesAndLadders = dict()
        for snake in snakes:
            self.snakesAndLadders[snake.getStart()] = snake.getEnd()
        for ladder in ladders:
            self.snakesAndLadders[ladder.getStart()] = ladder.getEnd()
        self.currentTurn = 0
        self.winner = None
   
    def roll(self, player, diceValue):
        if self.winner is not None or diceValue > 6 or diceValue < 1 or self.players[self.currentTurn].getId() != player.getId():
            return False
        destination = self.players[self.currentTurn].getCurrentPosition() + diceValue
        if destination <= 100:
            if destination in self.snakesAndLadders:
                self.players[self.currentTurn].setCurrentPosition(self.snakesAndLadders[destination])
            else:
                self.players[self.currentTurn].setCurrentPosition(destination)
        if destination == 100:
            self.winner = self.players[self.currentTurn]
        self.nextPlayer()
        return True
   
    def nextPlayer(self):
        self.currentTurn = (self.currentTurn + 1) % len(self.players)
   
    def getPlayers(self):
        return self.players
   
    def getWinner(self):
        return self.winner

if __name__ == "__main__":
    p1 = Player("Robert")
    p2 = Player("Stannis")
    p3 = Player("Renly")
   
    s1 = Snake(17, 7)
    s2 = Snake(54, 34)
    s3 = Snake(62, 19)
    s4 = Snake(64, 60)
    s5 = Snake(87, 36)
    s6 = Snake(92, 73)
    s7 = Snake(95, 75)
    s8 = Snake(98, 79)
   
    l1 = Ladder(1, 38)
    l2 = Ladder(4, 14)
    l3 = Ladder(9, 31)
    l4 = Ladder(21, 42)
    l5 = Ladder(28, 84)
    l6 = Ladder(51, 67)
    l7 = Ladder(72, 91)
    l8 = Ladder(80, 99)
   
    s = [s1, s2, s3, s4, s5, s6, s7, s8]
    l = [l1, l2, l3,l4,l5,l6,l7,l8]
    p = [p1,p2,p3]
    game = Game(s,l,p)
    while game.getWinner() is None:
        diceVal = random.randint(1, 6)
        game.roll(p1, diceVal)
        diceVal = random.randint(1, 6)
        game.roll(p2, diceVal)
        diceVal = random.randint(1, 6)
        game.roll(p3, diceVal)

    print("The winner is:", game.getWinner().getName())
   
    print("All Scores:", end=" ")
    for p in game.getPlayers():
        print(p.getCurrentPosition(), end=" ")