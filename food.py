from math import sqrt, cos, sin

class Food:
    def __init__(self):
        self.x, self.y = 0, 0
        self.strength = 100
        self.depletion_factor = 1

    def depletion(self, x, y):
        return self.strength / (1 + self.depletion_factor * self.distance(x, y))

    def distance(self, x, y):
        return sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, time):
        pass


class MovingFood(Food):
    def __init__(self, radius, omega):
        super().__init__()
        self.radius = radius
        self.omega = omega

    def move(self, time):
        self.x = cos(time * self.omega) * self.radius
        self.y = sin(time * self.omega) * self.radius