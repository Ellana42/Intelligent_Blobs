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
        self.grid = None
        self.grid_size = self.nearest_blob_max_dist * 2

    def initialize_accelerator(self):
        # Split the universe into a grid of squares os size self.nearest_blob_max_dist
        # Attribute each blob to one cell
        # In summary: create an spatial index
        self.grid = {}
        for i, blob in enumerate(self.blobs):
            if blob.age < self.reproduction_maturity:
                continue
            x, y = int(blob.x // self.grid_size), int(blob.y // self.grid_size)
            if (x, y) not in self.grid:
                self.grid[(x, y)] = [(i, blob)]
            else:
                self.grid[(x, y)].append((i, blob))

    def nearest_blob(self, ind):
        distance_min = 10 * self.universe_size * self.universe_size
        blob_min = None
        x, y = self.blobs[ind].x, self.blobs[ind].y
        # Find the cell of the blob
        cell_x, cell_y = int(x // self.grid_size), int(y // self.grid_size)
        # Look only for the blobs in the adjacent cells
        for delta_x, delta_y in [(0, -1), (-1, -1), (1, -1), (0, 0), (-1, 0), (1, 0), (0, 1), (-1, 1), (1, 1)]:
            if (cell_x + delta_x, cell_y + delta_y) not in self.grid:
                continue
            for i, blob in self.grid[(cell_x + delta_x, cell_y + delta_y)]:
                if i == ind or blob.age < self.reproduction_maturity:
                    continue
                d = abs(blob.x - x) + abs(blob.y - y)
                if d < distance_min:
                    distance_min = d
                    blob_min = blob
        return distance_min, blob_min

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
        # Only mature enough blobs can reproduce
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

    def resolve_decision_for(self, i, decision):
        blob = self.blobs[i]
        verb, parameter = decision
        # Update statistics
        self.tick_stats['n_{}'.format(verb)] += 1

        if verb == 'move':
            blob.move()
            return
        if verb == 'eat':
            quantity = self.food.depletion(blob.x, blob.y)
            blob.eat(quantity)
            return
        if verb == 'reproduce':
            nearest_blob = parameter

            energy_loss = blob.energy * self.cost_reproduction
            # Create a new Brain
            new_brain = self.breed_type(blob, nearest_blob)

            # Create a new Blob at the middle of the 2 parents, equipped with the new Brain
            x, y = (blob.x + nearest_blob.x) / 2, (blob.y + nearest_blob.y) / 2
            new_blob = Blob(x, y, brain=new_brain)
            # The enerfy level of the new Blob is taken from its parents (no energy creation in the process)
            new_blob.energy = 2 * energy_loss
            self.blobs.append(new_blob)

            # The parent can't reproduce immediately
            blob.age = 0
            nearest_blob.age = 0
            # The lose the energy the child takes
            blob.energy -= energy_loss
            nearest_blob.energy -= energy_loss

            return
        if verb == 'rotate':
            blob.rotate()
            return

    def terminate(self):
        self.blobs = [blob for blob in self.blobs if blob.is_alive()]

    def tick(self):
        # Prepare statistics for this tick
        self.tick_stats = {'t': self.time, 'n_move': 0, 'n_eat': 0, 'n_reproduce': 0, 'n_rotate': 0}
        # Prepare the "nearest blob" acceleration
        self.initialize_accelerator()
        # Move the food
        self.food.move(self.time)

        # Compute each blob's decision
        before = len(self.blobs)
        decisions = [blob.decide(self.give_information_for(i)) for i, blob in enumerate(self.blobs)]

        # Resolve the blob's decision (apply them in the universe)
        [self.resolve_decision_for(i, decision) for i, decision in enumerate(decisions)]
        self.tick_stats['born'] = - before + len(self.blobs)
        before = len(self.blobs)

        # Kill the blobs when they have negative energy
        self.terminate()
        self.tick_stats['die'] = before - len(self.blobs)

        # Age each blob
        [b.tick() for b in self.blobs]

        # Advance the universe clock
        self.time += 1

        # Compute stats on blob population
        self.tick_stats['n'] = len(self.blobs)
        blob_stats = {k: 0 for k in self.brain_prototype.PARAMETERS}
        if len(self.blobs) > 0:
            for blob in self.blobs:
                for k in self.brain_prototype.PARAMETERS:
                    blob_stats[k] += blob.brain.__getattribute__(k)
            for k in self.brain_prototype.PARAMETERS:
                self.tick_stats[k] = blob_stats[k] / len(self.blobs)

        # Save stat history
        self.stats.append(self.tick_stats)

        print(self.tick_stats)

    def __str__(self):
        state_of_world = [(blob.x, blob.y, blob.energy) for blob in self.blobs]
        return str(state_of_world)
