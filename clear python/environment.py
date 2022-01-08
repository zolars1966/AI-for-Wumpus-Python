from room import Room
from object import Object
import random

class Environment:
    def __init__(self):
        self.cave = []

        self.create_cave()
        self.wumpus, self.agent, self.bats_1, self.bats_2, self.pit_1, self.pit_2, self.gold = self.create_objects()

        self.state = [False for _ in range(9)]

    def create_cave(self):
        for i in range(1, 21):
            self.cave.append(Room(number=i))

        for i, room in enumerate(self.cave):
            if i == 9:
                room.connects_to.append(self.cave[0].number)
            elif i == 19:
                room.connects_to.append(self.cave[10].number)
            else:    
                room.connects_to.append(self.cave[i + 1].number)

            if i == 0:
                room.connects_to.append(self.cave[9].number)
            elif i == 10:
                room.connects_to.append(self.cave[19].number)
            else:
                room.connects_to.append(self.cave[i - 1].number)

            if i < 10:
                room.connects_to.append(self.cave[i + 10].number)
                self.cave[i + 10].connects_to.append(room.number)

    def create_objects(self):
        obj = []
        Samples = random.sample(self.cave, 7)
        for room in Samples:
            obj.append(Object(location=room))

        return obj

    def update(self, index):
        self.agent.move(self.cave, index)

        if self.agent.location == self.wumpus.location and not self.wumpus.awaken:
            print("... OOPS! BUMPED A WUMPUS!")
            self.wumpus.wake_up(self.cave)
            
            self.state[0] = True
        else:
            self.state[0] = False
        
        if self.agent.location == (self.bats_1.location or self.bats_2.location):
            print("ZAP--SUPER BAT SNATCH!\n ELSEWHEREVILLE FOR YOU!")
            while self.agent.location == (self.bats_1.location or self.bats_2.location):
                self.agent.location = random.choice(self.cave)
            
            self.state[1] = True
        else:
            self.state[1] = False

        if self.agent.location == self.wumpus.location and self.wumpus.awaken:
            print("Num, num... Tasty!")

            self.cave = []

            self.create_cave()
            self.wumpus, self.agent, self.bats_1, self.bats_2, self.pit_1, self.pit_2, self.gold = self.create_objects()
            
            self.state[8] = True
        else:
            self.state[8] = False

        if self.agent.location == (self.pit_1.location or self.pit_2.location):
            print("YYYIIIIEEEE . . . FELL INTO A PIT!\n China here we come!")

            self.cave = []

            self.create_cave()
            self.wumpus, self.agent, self.bats_1, self.bats_2, self.pit_1, self.pit_2, self.gold = self.create_objects()
            
            self.state[2] = True
        else:
            self.state[2] = False

        if self.agent.location == self.gold.location:
            print("Money, money, money...\nMust be funny!")
            while self.gold.location == (self.pit_1.location or self.pit_2.location\
                                      or self.bats_1.location or self.bats_2.location\
                                      or self.wumpus.location or self.agent.location):
                self.gold.location = random.choice(self.cave)
            self.state[3] = True
        else:
            self.state[3] = False

        if self.wumpus.location.number in self.agent.location.connects_to:
            print("Ew... That smell!")
            self.state[4] = True
        else:
            self.state[4] = False

        if (self.pit_1.location.number or self.pit_2.location.number) in self.agent.location.connects_to:
            print("Hm... windy")
            self.state[5] = True
        else:
            self.state[5] = False

        if (self.bats_1.location.number or self.bats_2.location.number) in self.agent.location.connects_to:
            print("Bats noise! They are nearby...")
            self.state[6] = True
        else:
            self.state[6] = False
        
        if self.gold.location.number in self.agent.location.connects_to:
            print("That shine... It's so... WONDERFUL!")
            self.state[7] = True
        else:
            self.state[7] = False

        print("-------------------------------------")
