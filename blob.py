from math import cos, sin


class Blob:
    def __init__(self, x, y, brain, energy=50, heading=0, omega=0.5, speed=10,
                 energy_per_move=5, energy_per_rotate=3, energy_when_idle=1):
        self.brain = brain
        self.x, self.y = x, y
        self.energy = energy
        self.heading = heading
        self.omega = omega
        self.speed = speed
        self.energy_per_move = energy_per_move
        self.energy_per_rotate = energy_per_rotate
        self.energy_when_idle = energy_when_idle
        self.age = 0

    # Actions :
    def move(self):
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)
        self.energy -= self.energy_per_move

    def rotate(self):
        self.heading += self.omega
        self.energy -= self.energy_per_rotate

    def eat(self, quantity):
        self.energy += quantity
        self.energy -= self.energy_when_idle

    # -----------------------------------------------

    def decide(self, information):
        return self.brain.decide(information)

    def is_alive(self):
        return self.energy > 0

    def tick(self):
        self.age += 1
