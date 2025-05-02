import random
from Player import Player
from Game import Action

class Randomized(Player):

    UIN = "11552247"

    def play(self, opponent_prev_action):
        return Action.Silent if random.random() < 0.5 else Action.Confess  # 50/50 chance

    def __str__(self):
        return "Randomized Strategy"
