import random
from Player import Player
from Game import Action

class RandomTitForTat(Player):

    UIN = "11552257"

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if random.random() < 0.15:  # 15% chance to defect randomly
            return Action.Confess
        return opponent_prev_action

    def __str__(self):
        return "Random Tit for Tat"
