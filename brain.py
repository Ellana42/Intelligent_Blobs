from numpy.random import choice
class Brain:
    def __init__(self, decision_matrix):
        self.decision_matrix = decision_matrix
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