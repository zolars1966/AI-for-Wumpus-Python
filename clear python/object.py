import random
from room import Room

class Object:
    def __init__(self, location):
        self.location = location
        self.awaken = False
        self.exp = 0

    def move(self, cave, index):
        self.location = cave[self.location.connects_to[index] - 1]
        return True

    def wake_up(self, cave):
        if self.awaken:
            if random.randint(0, 3):
                self.location = cave[random.choice(self.location.connects_to) - 1]
                self.awaken = False
        else:
            self.awaken = True
            self.location = cave[random.choice(self.location.connects_to) - 1]
 
    def is_hit(self, room):
        return self.location == room
