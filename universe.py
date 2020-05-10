from random import uniform
from math import cos, sin

from blob import Blob
from brain import RandomBrain, SmartBrain
from food import MovingFood
from settings import settings
from copy import copy


class Universe:
    ACTIONS = ['move', 'eat', 'rotate', 'reproduce']

    def __init__(self):
        self.universe_size = settings['universe_size']
        self.blobs = []
        self.food = MovingFood(radius=settings['food_radius'],
                               omega=settings['food_omega'],
                               strength=settings['food_strength'],
                               depletion_factor=settings['food_depletion_factor'])
        self.brain_prototype = SmartBrain(actions=None,
                                          eat_threshold=settings['smartbrain_eat_threshold'],
                                          move_threshold=settings['smartbrain_move_threshold'])
        self.generate_blobs(nb_blobs=settings['nb_blobs'])
        self.time = 0
        self.breed_type = RandomBrain.random_breed
        self.cost_reproduction = settings['cost_reproduction']
        self.nearest_blob_max_dist = settings['nearest_blob_max_dist']

    def generate_blobs(self, nb_blobs):
        mid = self.universe_size // 2
        for _ in range(nb_blobs):
            x, y = uniform(-mid, mid), uniform(-mid, mid)
            self.blobs.append(Blob(x, y,
                                   energy=settings['blob_initial_energy'],
                                   speed=settings['blob_speed'],
                                   energy_per_move=settings['energy_per_move'],
                                   energy_per_rotate=settings['energy_per_rotate'],
                                   brain=copy(self.brain_prototype))
                              )

    def give_information_for(self, i):
        # Find nearest blob
        d, nearest = self.nearest_blob(i)
        if d > self.nearest_blob_max_dist:
            d, nearest = 0, None
        # Find food level at blob location
        blob = self.blobs[i]
        food_level = self.food.depletion(blob.x, blob.y)
        # Find direction of food : gradient of food level dot heading vector
        eps = 0.1
        grad_x = (self.food.depletion(blob.x + eps, blob.y) - food_level) / eps
        grad_y = (self.food.depletion(blob.x, blob.y + eps) - food_level) / eps
        food_dir = grad_x * cos(blob.heading) + grad_y * sin(blob.heading)
        return d, nearest, food_level, 1000 * food_dir

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
            blob.energy -= self.cost_reproduction
            new_brain = self.breed_type(blob, nearest_blob)
            x, y = (blob.x + nearest_blob.x) / 2, (blob.y + nearest_blob.y) / 2
            self.blobs.append(Blob(x, y, brain=RandomBrain(new_brain)))
            return
        if verb == 'rotate':
            blob.rotate()
            return

    def terminate(self):
        self.blobs = [blob for blob in self.blobs if blob.is_alive()]

    def tick(self):
        self.food.move(self.time)
        decisions = [blob.decide(self.give_information_for(i))
                     for i, blob in enumerate(self.blobs)]
        [self.resolve_decision_for(i, decision)
         for i, decision in enumerate(decisions)]
        self.terminate()
        self.time += 1

    def __str__(self):
        state_of_world = [(blob.x, blob.y, blob.energy) for blob in self.blobs]
        return str(state_of_world)
