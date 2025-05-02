import random
from Player import Player
from Game import Action

class GenerousTitForTat(Player):

    UIN = "11552248"

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == Action.Confess and random.random() < 0.1:  # 10% chance to forgive
            return Action.Silent
        return opponent_prev_action

    def __str__(self):
        return "Generous Tit for Tat"
