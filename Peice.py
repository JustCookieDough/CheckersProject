import pygame as p, random as r
import Variables as v

class Peice(): # parent class of the two peices. Everything in this class is common to both of the peice classes
    def __init__(self, x, y):
        self.x = x # x-cord
        self.y = y # y-cord
        self.isKing = False # bool telling if peice is a king or not
        self.color = (255, 30, 190) # placeholder color

    def draw(self, screen):
        p.draw.circle(screen, self.color, (int(v.SQ_SIZE * self.x + v.SQ_SIZE/2), int(v.SQ_SIZE * self.y + v.SQ_SIZE/2)), v.SQ_SIZE // 2) #draws main check body
        if self.isKing: # if its a king, the code below draws a crown
            crown = p.image.load("Crown.png")
            screen.blit(crown, ((v.SQ_SIZE * self.x + v.SQ_SIZE / 2) - 17, (v.SQ_SIZE * self.y + v.SQ_SIZE / 2) - 10))

    def king(self):
        self.isKing = True

    def move(self, direction): # takes in strings "ur" "ul" "dr" "dl", moves in a certain direction
        if direction == "ur":
            self.x += 1
            self.y -= 1
        if direction == "ul":
            self.x -= 1
            self.y -= 1
        if direction == "dr":
            self.x += 1
            self.y += 1
        if direction == "dl":
            self.x -= 1
            self.y += 1

    def attack(self, direction, peiceList):  # takes in a direction and attacks in that diection, removing a peice from the list
        if direction == "ur":
            for peice in peiceList:
                if peice.x == self.x + 1 and peice.y == self.y - 1:
                    peiceList.remove(peice)
            self.x += 2
            self.y -= 2
        if direction == "ul":
            for peice in peiceList:
                if peice.x == self.x - 1 and peice.y == self.y - 1:
                    peiceList.remove(peice)
            self.x -= 2
            self.y -= 2
        if direction == "dr":
            for peice in peiceList:
                if peice.x == self.x + 1 and peice.y == self.y + 1:
                    peiceList.remove(peice)
            self.x += 2
            self.y += 2
        if direction == "dl":
            for peice in peiceList:
                if peice.x == self.x - 1 and peice.y == self.y + 1:
                    peiceList.remove(peice)
            self.x -= 2
            self.y += 2

    def removeDirections(self, directions):
        """
        this is a placeholder function so that the game wont error out if a colorless peice ever gets created.
        it isn't used in this code and is overriden in both of the children classes.
        """
        pass

    def getPossibleMovements(self, redPeiceList, blackPeiceList):  # returns a list with all possible directions to move
        directions = ["ul", "ur", "dr", "dl"] # creates
        for list in [redPeiceList, blackPeiceList]:
            for peice in list:
                if (peice.x == self.x + 1 and peice.y == self.y - 1) or self.y == 0 or self.x == v.NUM_OF_SQUARES - 1:
                    if "ur" in directions:
                        directions.remove("ur")
                if (peice.x == self.x - 1 and peice.y == self.y - 1) or self.y == 0 or self.x == 0:
                    if "ul" in directions:
                        directions.remove("ul")
                if (peice.x == self.x + 1 and peice.y == self.y + 1) or self.y == v.NUM_OF_SQUARES - 1 or self.x == v.NUM_OF_SQUARES - 1:
                    if "dr" in directions:
                        directions.remove("dr")
                if (peice.x == self.x - 1 and peice.y == self.y + 1) or self.y == v.NUM_OF_SQUARES - 1 or self.x == 0:
                    if "dl" in directions:
                        directions.remove("dl")
            if not self.isKing:
                self.removeDirections(directions)  # makes sure a peice cant move backward if its not a King
        return directions

    def getPossibleAttacks(self, selfTeamList, opposingTeamList):  # returns a list with all possible attack directions
        directions = []
        for peice in opposingTeamList: # tests if a peice is diagonally from the attacking peice
            if peice.x == self.x + 1 and peice.y == self.y - 1:
                if "ur" not in directions:
                    directions.append("ur")
            if peice.x == self.x - 1 and peice.y == self.y - 1:
                if "ul" not in directions:
                    directions.append("ul")
            if peice.x == self.x + 1 and peice.y == self.y + 1:
                if "dr" not in directions:
                    directions.append("dr")
            if peice.x == self.x - 1 and peice.y == self.y + 1:
                if "dl" not in directions:
                    directions.append("dl")
        for list in [selfTeamList, opposingTeamList]: # makes sure there is no peice blocking
            for peice in list:
                if (peice.x == self.x + 2 and peice.y == self.y - 2) or self.x >= v.NUM_OF_SQUARES - 2 or self.y <= 1:
                    if "ur" in directions:
                        directions.remove("ur")
                if (peice.x == self.x - 2 and peice.y == self.y - 2) or self.x <= 1 or self.y <= 1:
                    if "ul" in directions:
                        directions.remove("ul")
                if (peice.x == self.x + 2 and peice.y == self.y + 2) or self.x >= v.NUM_OF_SQUARES - 2 or self.y >= v.NUM_OF_SQUARES - 2:
                    if "dr" in directions:
                        directions.remove("dr")
                if (peice.x == self.x - 2 and peice == self.y + 2) or self.x <= 1 or self.y >= v.NUM_OF_SQUARES - 2:
                    if "dl" in directions:
                        directions.remove("dl")
        if not self.isKing:
            self.removeDirections(directions)  # see above
        return directions

class RedPeice(Peice):
    def __init__(self, x, y): # gives the peice its color param and calls the init of the parent class
        """
        params: x, y, team
        other atts: color, king or not?
        """
        super().__init__(x, y)
        self.color = (255, 0, 0)

    def update(self, redPeiceList, blackPeiceList):  # peice does everything below every frame
        attackDirections = self.getPossibleAttacks(redPeiceList, blackPeiceList)
        moveDirections = self.getPossibleMovements(redPeiceList, blackPeiceList)
        if attackDirections:
            self.attack(r.choice(attackDirections), blackPeiceList)
        elif moveDirections:
            self.move(r.choice(moveDirections))
        if self.y == 0:
            self.king()

    def removeDirections(self, directions):  # see above
        if "dl" in directions:
            directions.remove("dl")
        if "dr" in directions:
            directions.remove("dr")

class BlackPeice(Peice):
    def __init__(self, x, y):  # see above
        """
        params: x, y, team
        other atts: color, king or not?
        """
        super().__init__(x, y)
        self.color = (0, 0, 0)

    def update(self, redPeiceList, blackPeiceList):
        attackDirections = self.getPossibleAttacks(blackPeiceList, redPeiceList)
        moveDirections = self.getPossibleMovements(redPeiceList, blackPeiceList)
        if attackDirections:
            self.attack(r.choice(attackDirections), redPeiceList)
        elif moveDirections:
            self.move(r.choice(moveDirections))
        if self.y == v.NUM_OF_SQUARES - 1:
            self.king()

    def removeDirections(self, directions):
        if "ul" in directions:
            directions.remove("ul")
        if "ur" in directions:
            directions.remove("ur")
