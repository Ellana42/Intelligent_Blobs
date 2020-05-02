from math import cos, sin

class Blob:
    def __init__(self, x, y, brain,energy=50, heading=0, omega=0.5, speed=10):
        self.brain = brain
        self.x, self.y = x, y
        self.energy = energy
        self.heading = heading
        self.omega = omega
        self.speed = speed

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