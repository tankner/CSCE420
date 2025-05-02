import random
from Player import Player
from Game import Action

class Joss(Player):

    UIN = "11552259"

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == Action.Silent and random.random() < 0.1:  # 10% chance to defect
            return Action.Confess
        return opponent_prev_action

    def __str__(self):
        return "Joss Strategy"
