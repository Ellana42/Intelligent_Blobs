from random import uniform, randint
from math import sqrt, cos, sin, pi

from blob import Blob
from brain import Brain
from food import MovingFood


class Universe:
    def __init__(self):
        self.universe_size = 1000
        self.blobs = []
        self.food = MovingFood(self.universe_size / 4, pi / 100)
        self.nb_options = 4
        self.generate_blobs(nb_blobs=100)
        self.time = 0

    def generate_blobs(self, nb_blobs):
        for _ in range(nb_blobs):
            x, y = self.random_coordinates()
            decision_matrix = self.random_decision_matrix()
            brain = Brain(decision_matrix)
            self.blobs.append(Blob(x, y, brain))

    def random_decision_matrix(self):
        weights = [randint(1, 100) for _ in range(self.nb_options)]
        decision_matrix = [i / sum(weights) for i in weights]
        return decision_matrix

    def random_coordinates(self):
        return uniform(-self.universe_size // 2, self.universe_size // 2), uniform(-self.universe_size // 2, self.universe_size // 2)

    def give_informations_for(self, i):
        d, nearest = self.nearest_blob(i)
        if d > 10:
            d, nearest = 0, None
        blob = self.blobs[i]
        food_level = self.food.depletion(blob.x, blob.y) 
        eps = 0.1
        grad_x = (self.food.depletion(blob.x + eps, blob.y)- food_level )/ eps
        grad_y = (self.food.depletion(blob.x, blob.y + eps)- food_level )/ eps
        food_dir = grad_x * cos(blob.heading) + grad_y * sin(blob.heading)
        return (d, nearest, food_level, food_dir)

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
        blob = self.blobs[i]
        verb, parameter = decision
        if verb == 'move':
            blob.move()
            return
        if verb == 'eat':
            quantity = self.food.depletion(blob.x, blob.y)
            blob.eat(quantity)
            return
        if verb == 'reproduce':
            nearest_blob = self.nearest_blob(i)[1]
            blob.energy -= 100
            self.random_breed(blob, nearest_blob)
            return
        if verb == 'rotate':
            blob.rotate()
            return

    def average_breed(self, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        brain2 = blob2.brain.decision_matrix
        new_brain = [(brain1[i] + brain2[i]) /
                     2 for i in range(self.nb_options)]
        x, y = (blob1.x + blob2.x) / 2, (blob1.y + blob2.y) / 2
        self.blobs.append(Blob(x, y, Brain(new_brain)))

    def duplication_breed(self, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        x, y = (blob1.x + blob2.x) / 2, (blob1.y + blob2.y) / 2
        self.blobs.append(Blob(x, y, Brain(brain1)))

    def random_breed(self, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        brain2 = blob2.brain.decision_matrix
        brains = [brain1, brain2]
        new_brain = [brains[randint(0, 1)][i]
                     for i in range(self.nb_options)]
        new_brain = [i / sum(new_brain) for i in new_brain]
        x, y = (blob1.x + blob2.x) / 2, (blob1.y + blob2.y) / 2
        self.blobs.append(Blob(x, y, Brain(new_brain)))

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



