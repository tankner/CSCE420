from Player import Player
from Game import Action

class MirrorStrategy(Player):

    UIN = "11552258"

    def __init__(self, *args, **kwargs):
        self.history = []

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        self.history.append(opponent_prev_action)
        defect_rate = self.history.count(Action.Confess) / len(self.history)
        return Action.Confess if defect_rate > 0.5 else Action.Silent

    def __str__(self):
        return "Mirror Strategy"
