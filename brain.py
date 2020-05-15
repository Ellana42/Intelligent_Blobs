from numpy.random import choice
from random import randint, uniform
from copy import copy


class Brain:
    PARAMETERS = []

    def __init__(self, actions):
        pass

    def __copy__(self):
        return Brain(actions=None)

    def decide(self, information):
        return ('move', ())


class RandomBrain(Brain):
    def __init__(self, actions):
        super().__init__(actions)
        self.nb_options = len(actions)
        self.decision_matrix = self.random_decision_matrix()
        self.decision_matrix_wo_reproduce = self.normalize(
            self.decision_matrix[:-1])

    def decide(self, information):
        dist, blob, food, food_dir = information
        decisions = [('move', ()), ('eat', ()), ('rotate', ())]
        if blob is not None:
            decisions.append(('reproduce', (blob)))
            decision = decisions[choice(
                range(len(decisions)), p=self.decision_matrix)]
        else:
            decision = decisions[choice(
                range(len(decisions)), p=self.decision_matrix_wo_reproduce)]

        return decision

    def normalize(self, decision_matrix):
        n = sum(decision_matrix) if len(decision_matrix) > 0 else 0
        if n == 0:
            return []
        return [x / n for x in decision_matrix]

    def random_decision_matrix(self):
        weights = [randint(1, 100) for _ in range(self.nb_options)]
        decision_matrix = [i / sum(weights) for i in weights]
        return decision_matrix

    @classmethod
    def average_breed(cls, blob1, blob2):
        nb_options = blob1.brain.nb_options
        brain1 = blob1.brain.decision_matrix
        brain2 = blob2.brain.decision_matrix
        new_brain = [(brain1[i] + brain2[i]) /
                     2 for i in range(nb_options)]
        return new_brain

    @classmethod
    def duplication_breed(cls, blob1, blob2):
        brain1 = blob1.brain.decision_matrix
        return brain1

    @classmethod
    def random_breed(cls, blob1, blob2):
        nb_options = blob1.brain.nb_options
        brain1 = blob1.brain.decision_matrix
        brain2 = blob2.brain.decision_matrix
        brains = [brain1, brain2]
        new_brain = [brains[randint(0, 1)][i]
                     for i in range(nb_options)]
        new_brain = [i / sum(new_brain) for i in new_brain]
        return new_brain


class SmartBrain(Brain):
    def __init__(self, actions, eat_threshold=1, move_threshold=0.6, reprod_distance_threshold=5):
        super().__init__(actions)
        self.eat_threshold = eat_threshold
        self.move_threshold = move_threshold
        self.reprod_distance_threshold = reprod_distance_threshold

    def __copy__(self):
        return SmartBrain(actions=None, eat_threshold=self.eat_threshold,
                          move_threshold=self.move_threshold,
                          reprod_distance_threshold=self.reprod_distance_threshold)

    def decide(self, information):
        dist, blob, food, food_dir = information
        if blob is not None and dist < self.reprod_distance_threshold:
            return 'reproduce', (blob)
        if food > self.eat_threshold:
            return 'eat', ()
        if food_dir > self.move_threshold:
            return 'move', ()
        return 'rotate', ()

    @classmethod
    def smart_breed(cls, blob1, blob2):
        return copy(blob1.brain)


class RandomSmartBrain(SmartBrain):
    PARAMETERS = ['eat_threshold', 'move_threshold', 'reprod_distance_threshold']

    def __init__(self, actions,
                 max_eat_threshold=10, max_move_threshold=5, max_reprod_distance_threshold=20,
                 eat_threshold=None, move_threshold=None, reprod_distance_threshold=None):
        super().__init__(actions)
        self.max_eat_threshold = max_eat_threshold
        self.max_move_threshold = max_move_threshold
        self.max_reprod_distance_threshold = max_reprod_distance_threshold

        self.eat_threshold = eat_threshold
        if eat_threshold is None:
            self.eat_threshold = uniform(0, self.max_eat_threshold)

        self.move_threshold = move_threshold
        if move_threshold is None:
            self.move_threshold = uniform(-self.max_move_threshold, self.max_move_threshold)

        self.reprod_distance_threshold = reprod_distance_threshold
        if reprod_distance_threshold is None:
            self.reprod_distance_threshold = uniform(0, self.max_reprod_distance_threshold)

    def __copy__(self):
        return RandomSmartBrain(actions=None,
                                max_eat_threshold=self.max_eat_threshold,
                                max_move_threshold=self.max_move_threshold,
                                max_reprod_distance_threshold=self.max_reprod_distance_threshold)

    @classmethod
    def smart_breed(cls, blob1, blob2):
        brain1, brain2 = blob1.brain, blob2.brain
        new_brain = RandomSmartBrain(None,
                                     max_eat_threshold=brain1.max_eat_threshold,
                                     max_move_threshold=brain1.max_move_threshold,
                                     max_reprod_distance_threshold=brain1.max_reprod_distance_threshold,
                                     eat_threshold=0.5 * (brain1.eat_threshold + brain2.eat_threshold),
                                     move_threshold=0.5 * (brain1.move_threshold + brain2.move_threshold),
                                     reprod_distance_threshold=0.5 * (brain1.reprod_distance_threshold + brain2.reprod_distance_threshold)
                                    )
        return new_brain
