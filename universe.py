from random import uniform
from math import cos, sin

from blob import Blob
from brain import RandomBrain, SmartBrain, RandomSmartBrain
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
        '''
        self.brain_prototype = RandomSmartBrain(actions=None,
                                          eat_threshold=settings['smartbrain_eat_threshold'],
                                          move_threshold=settings['smartbrain_move_threshold'],
                                          reprod_distance_threshold=settings['smartbrain_reproduce_distance_threshold'])
        '''
        self.brain_prototype = RandomSmartBrain(actions=None,
                                                eat_threshold=settings['randomsmartbrain_eat_threshold'],
                                                move_threshold=settings['randomsmartbrain_move_threshold'],
                                                reprod_distance_threshold=settings['randomsmartbrain_reproduce_distance_threshold'])
        self.generate_blobs(nb_blobs=settings['nb_blobs'])
        self.time = 0
        self.breed_type = RandomSmartBrain.smart_breed
        self.cost_reproduction = settings['cost_reproduction']
        self.nearest_blob_max_dist = settings['nearest_blob_max_dist']
        self.reproduction_maturity = settings['reproduction_maturity']
        self.stats = []
        self.tick_stats = {}

    def generate_blobs(self, nb_blobs):
        mid = self.universe_size // 2
        for _ in range(nb_blobs):
            x, y = uniform(-mid, mid), uniform(-mid, mid)
            brain = copy(self.brain_prototype)
            self.blobs.append(Blob(x, y,
                                   energy=settings['blob_initial_energy'],
                                   speed=settings['blob_speed'],
                                   energy_per_move=settings['energy_per_move'],
                                   energy_per_rotate=settings['energy_per_rotate'],
                                   energy_when_idle=settings['energy_when_idle'],
                                   brain=brain)
                              )

    def give_information_for(self, i):
        blob = self.blobs[i]
        d, nearest = 0, None
        if blob.age > self.reproduction_maturity:
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
            if i == ind or blob.age < self.reproduction_maturity:
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
            self.tick_stats['n_move'] += 1
            return
        if verb == 'eat':
            quantity = self.food.depletion(blob.x, blob.y)
            blob.eat(quantity)
            self.tick_stats['n_eat'] += 1
            return
        if verb == 'reproduce':
            nearest_blob = parameter
            energy_loss = blob.energy * self.cost_reproduction
            blob.energy -= energy_loss
            new_brain = self.breed_type(blob, nearest_blob)
            x, y = (blob.x + nearest_blob.x) / 2, (blob.y + nearest_blob.y) / 2
            blob.age = 0
            nearest_blob.age = 0
            new_blob = Blob(x, y, brain=new_brain)
            new_blob.energy = energy_loss
            self.blobs.append(new_blob)
            self.tick_stats['n_reproduce'] += 1
            return
        if verb == 'rotate':
            blob.rotate()
            self.tick_stats['n_rotate'] += 1
            return

    def terminate(self):
        self.blobs = [blob for blob in self.blobs if blob.is_alive()]

    def tick(self):
        self.tick_stats = {'n_move': 0, 'n_eat': 0, 'n_reproduce': 0, 'n_rotate': 0}
        self.food.move(self.time)
        before = len(self.blobs)
        decisions = [blob.decide(self.give_information_for(i)) for i, blob in enumerate(self.blobs)]
        [self.resolve_decision_for(i, decision) for i, decision in enumerate(decisions)]
        self.tick_stats['born'] = - before + len(self.blobs)
        before = len(self.blobs)
        self.terminate()
        self.tick_stats['die'] = before - len(self.blobs)
        [b.tick() for b in self.blobs]
        self.time += 1
        self.tick_stats['n'] = len(self.blobs)

        # Compute stats on blob population
        blob_stats = {k: 0 for k in self.brain_prototype.PARAMETERS}
        if len(self.blobs) > 0:
            for blob in self.blobs:
                for k in self.brain_prototype.PARAMETERS:
                    blob_stats[k] += blob.brain.__getattribute__(k)
            for k in self.brain_prototype.PARAMETERS:
                self.tick_stats[k] = blob_stats[k] / len(self.blobs)
        self.stats.append(self.tick_stats)

        print(self.tick_stats)


    def __str__(self):
        state_of_world = [(blob.x, blob.y, blob.energy) for blob in self.blobs]
        return str(state_of_world)
