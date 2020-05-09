from numpy.random import choice
from random import randint


class Brain:
    def __init__(self, actions):
        pass

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
    def __init__(self, actions):
        super().__init__(actions)
        self.nb_options = len(actions)

    def decide(self, information):
        dist, blob, food, food_dir = information
        if food > 1:
            return 'eat', ()

        if food_dir > 0.6:
            return ('move', ())
        return ('rotate', ())
