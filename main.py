from random import uniform, choice
from math import sqrt, cos, sin, pi


class Blob:
    def __init__(self, x, y):
        self.brain = Brain()
        self.x, self.y = x, y
        self.energy = 100

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]
        self.energy -= sqrt(direction[0] ** 2 + direction[1] ** 2)

    def choose(self, information):
        decision = self.brain.decide(information)
        return decision

    def eat(self, quantity):
        self.energy += quantity

    def is_alive(self):
        return self.energy > 0


class Brain:
    def __init__(self):
        pass

    def decide(self, information):
        dist, blob, food = information
        decisions = [('move', ()), ('eat', ())]
        decision = choice(decisions)
        return decision


class Universe:
    def __init__(self):
        self.universe_size = 10
        self.blobs = []
        self.food = MovingFood(self.universe_size / 2, pi / 20)
        self.generate_blobs(nb_blobs=1)
        self.time = 0

    def generate_blobs(self, nb_blobs):
        for _ in range(nb_blobs):
            x, y = self.random_coordinates()
            self.blobs.append(Blob(x, y))

    def random_coordinates(self):
        return uniform(0, self.universe_size), uniform(0, self.universe_size)

    def give_informations_for(self, i):
        d, nearest = self.nearest_blob(i)
        food_level = self.food.depletion(self.blobs[i].x, self.blobs[i].y)
        return (d, nearest, food_level)

    def nearest_blob(self, ind):
        distance_min = 10 * self.universe_size * self.universe_size
        blob_min = None
        x, y = self.blobs[ind].x, self.blobs[ind].y
        for i, blob in enumerate(self.blobs):
            if i == ind:
                continue
            d = abs(blob.x - x) + abs(blob.y - y)
            if d < distance_min:
                distance_min = d
                blob_min = blob
        return distance_min, blob_min

    def resolve_decision_for(self, i, decision):
        verb, parameter = decision
        if verb == 'move':
            parameter = (uniform(0, 1), uniform(0, 1))
            self.blobs[i].move(parameter)
            return
        if verb == 'eat':
            quantity = self.food.depletion(self.blobs[i].x, self.blobs[i].y)
            self.blobs[i].eat(quantity)
            return

    def terminate(self):
        self.blobs = [blob for blob in self.blobs if blob.is_alive()]

    def tick(self):
        self.food.move(self.time)
        decisions = [blob.choose(self.give_informations_for(i))
                     for i, blob in enumerate(self.blobs)]
        [self.resolve_decision_for(i, decision)
         for i, decision in enumerate(decisions)]
        self.terminate()
        self.time += 1

    def __str__(self):
        state_of_world = [(blob.x, blob.y, blob.energy) for blob in self.blobs]
        return str(state_of_world)


class Food:
    def __init__(self):
        self.x, self.y = 0, 0
        self.strength = 10
        self.depletion_factor = 2

    def depletion(self, x, y):
        return self.strength / (1 + self.depletion_factor * self.distance(x, y))

    def distance(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

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


universe = Universe()
# while True:
for _ in range(5):
    print(universe)
    universe.tick()
