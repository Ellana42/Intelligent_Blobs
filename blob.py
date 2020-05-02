from math import cos, sinr

class Blob:
    def __init__(self, x, y, brain):
        self.brain = brain
        self.x, self.y = x, y
        self.energy = 50
        self.heading = 0
        self.omega = 0.5
        self.speed = 10

    # Actions : 

    def move(self):
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)
        self.energy -= self.speed

    def rotate(self):
        self.heading += self.omega

    def eat(self, quantity):
        self.energy += quantity
    # -----------------------------------------------
    def choose(self, information):
        decision = self.brain.decide(information)
        return decision

    def is_alive(self):
        return self.energy > 0