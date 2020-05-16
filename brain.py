from numpy.random import choice
from random import randint, uniform
from copy import copy


class Brain:
    PARAMETERS = []

    def __init__(self, actions):
        pass

    def decide(self, information):
        return 'move', ()


class SmartBrain(Brain):
    PARAMETERS = ['eat_threshold', 'move_threshold', 'reprod_energy_threshold']

    def __init__(self, actions, eat_threshold=1, move_threshold=0.6, reprod_energy_threshold=5):
        super().__init__(actions)
        self.eat_threshold = eat_threshold
        self.move_threshold = move_threshold
        self.reprod_energy_threshold = reprod_energy_threshold

    def __copy__(self):
        return SmartBrain(actions=None, eat_threshold=self.eat_threshold,
                          move_threshold=self.move_threshold,
                          reprod_energy_threshold=self.reprod_energy_threshold)

    def decide(self, information):
        dist, blob, food, food_dir, energy = information
        if blob is not None and energy > self.reprod_energy_threshold and food > self.eat_threshold:
            return 'reproduce', blob
        if food > self.eat_threshold:
            return 'eat', ()
        if food_dir > self.move_threshold:
            return 'move', ()
        return 'rotate', ()

    @classmethod
    def smart_breed(cls, blob1, blob2):
        return copy(blob1.brain)


class SmmartBrainGenerator:
    PARAMETERS = ['eat_threshold', 'move_threshold', 'reprod_energy_threshold']
    def __init__(self, actions, eat_threshold, move_threshold, reprod_energy_threshold):
        self.eat_threshold = eat_threshold
        self.move_threshold = move_threshold
        self.reprod_energy_threshold = reprod_energy_threshold

    def generate_brain(self):
        return SmartBrain(actions=None, eat_threshold=self.eat_threshold,
                          move_threshold=self.move_threshold,
                          reprod_energy_threshold=self.reprod_energy_threshold)


class RandomBrain(SmartBrain):
    PARAMETERS = ['eat_threshold', 'move_threshold', 'reprod_energy_threshold']

    def __init__(self, actions,
                 var_eat_threshold, var_move_threshold, var_reprod_energy_threshold,
                 eat_threshold, move_threshold, reprod_energy_threshold):
        super().__init__(actions)

        self.var_eat_threshold = var_eat_threshold
        self.var_move_threshold = var_move_threshold
        self.var_reprod_energy_threshold = var_reprod_energy_threshold

        self.eat_threshold = eat_threshold
        self.eat_threshold += self.eat_threshold * self.var_eat_threshold * uniform(-1, 1)

        self.move_threshold = move_threshold
        self.move_threshold += self.move_threshold * self.var_move_threshold * uniform(-1, 1)

        self.reprod_energy_threshold = reprod_energy_threshold
        self.reprod_energy_threshold += self.reprod_energy_threshold * self.var_reprod_energy_threshold * uniform(-1, 1)

    @classmethod
    def smart_breed(cls, blob1, blob2):
        brain1, brain2 = blob1.brain, blob2.brain
        new_brain = RandomBrain(None,
                                var_eat_threshold=0.5 * (brain1.var_eat_threshold + brain2.var_eat_threshold) ,
                                var_move_threshold=0.5 * (brain1.var_move_threshold + brain2.var_move_threshold),
                                var_reprod_energy_threshold=0.5 * (brain1.var_reprod_energy_threshold + brain2.var_reprod_energy_threshold),
                                eat_threshold=0.5 * (brain1.eat_threshold + brain2.eat_threshold),
                                move_threshold=0.5 * (brain1.move_threshold + brain2.move_threshold),
                                reprod_energy_threshold=0.5 * (brain1.reprod_energy_threshold + brain2.reprod_energy_threshold)
                                )
        return new_brain


class RandomBrainGenerator:
    PARAMETERS = ['eat_threshold', 'move_threshold', 'reprod_energy_threshold']
    def __init__(self, max_eat_threshold=1, max_move_threshold=0.6, max_reprod_energy_threshold=5,
                 var_eat_threshold=10, var_move_threshold=5, var_reprod_energy_threshold=20):

        self.max_eat_threshold = max_eat_threshold
        self.max_move_threshold = max_move_threshold
        self.max_reprod_energy_threshold = max_reprod_energy_threshold

        self.var_eat_threshold = var_eat_threshold
        self.var_move_threshold = var_move_threshold
        self.var_reprod_energy_threshold = var_reprod_energy_threshold

    def generate_brain(self):
        return RandomBrain(actions=None,
                           var_eat_threshold=self.var_eat_threshold,
                           var_move_threshold=self.var_move_threshold,
                           var_reprod_energy_threshold=self.var_reprod_energy_threshold,
                           eat_threshold=uniform(0, self.max_eat_threshold),
                           move_threshold=uniform(-self.max_move_threshold, self.max_move_threshold),
                           reprod_energy_threshold=uniform(0, self.max_reprod_energy_threshold)
                           )
