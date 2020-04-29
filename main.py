from random import uniform, randint
from numpy.random import choice
from math import sqrt, cos, sin, pi
from display import Display


class Blob:
    def __init__(self, x, y, decision_matrix=[0.2, 0.8]):
        self.brain = Brain(decision_matrix)
        self.x, self.y = x, y
        self.energy = 50

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]
        self.energy -= 0.5 * sqrt(direction[0] ** 2 + direction[1] ** 2)

    def choose(self, information):
        decision = self.brain.decide(information)
        return decision

    def eat(self, quantity):
        self.energy += quantity

    def is_alive(self):
        return self.energy > 0


class Brain:
    def __init__(self, decision_matrix):
        self.decision_matrix = decision_matrix

    def decide(self, information):
        dist, blob, food = information
        decisions = [('move', ()), ('eat', ()), ('reproduce', ())]
        decision = decisions[choice(
            range(len(decisions)), p=self.decision_matrix)]
        return decision


class Universe:
    def __init__(self):
        self.universe_size = 1000
        self.blobs = []
        self.food = MovingFood(self.universe_size / 2, pi / 20)
        self.nb_options = 3
        self.generate_blobs(nb_blobs=50)
        self.time = 0

    def generate_blobs(self, nb_blobs):
        for _ in range(nb_blobs):
            x, y = self.random_coordinates()
            decision_matrix = self.random_decision_matrix()
            self.blobs.append(Blob(x, y, decision_matrix))

    def random_decision_matrix(self):
        weights = [randint(1, 100) for _ in range(self.nb_options)]
        decision_matrix = [i / sum(weights) for i in weights]
        return decision_matrix

    def random_coordinates(self):
        return uniform(-self.universe_size // 2, self.universe_size // 2), uniform(-self.universe_size // 2, self.universe_size // 2)

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
            parameter = (uniform(-self.universe_size / 40, self.universe_size / 40),
                         uniform(-self.universe_size / 40, self.universe_size / 40))
            self.blobs[i].move(parameter)
            return
        if verb == 'eat':
            quantity = self.food.depletion(self.blobs[i].x, self.blobs[i].y)
            self.blobs[i].eat(quantity)
            return
        if verb == 'reproduce':
            nearest_blob = self.nearest_blob(i)[1]
            self.blobs[i].energy -= 150
            self.duplication_breed(self.blobs[i], nearest_blob)
            return

    def average_breed(self, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        brain2 = blob2.brain.decision_matrix
        new_brain = [(brain1[i] + brain2[i]) /
                     2 for i in range(self.nb_options)]
        x, y = (blob1.x + blob2.x) / 2, (blob1.y + blob2.y) / 2
        self.blobs.append(Blob(x, y, new_brain))

    def duplication_breed(self, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        x, y = (blob1.x + blob2.x) / 2, (blob1.y + blob2.y) / 2
        self.blobs.append(Blob(x, y, brain1))

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
        self.strength = 500
        self.depletion_factor = 0.4

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
displayer = Display(universe)
running = True

while running:
    inp = displayer.show()
    if inp == 'quit':
        running = False
    universe.tick()
