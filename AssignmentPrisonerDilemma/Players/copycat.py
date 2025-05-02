import random
from Player import Player
from Game import Action

class NoisyCopycat(Player):

    UIN = "11552255"

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if random.random() < 0.05:  # 5% chance to do the opposite
            return Action.Silent if opponent_prev_action == Action.Confess else Action.Confess
        return opponent_prev_action

    def __str__(self):
        return "Noisy Copycat"
