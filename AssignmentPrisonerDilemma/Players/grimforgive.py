import random
from Player import Player
from Game import Action

class GrimWithForgiveness(Player):

    UIN = "11552249"

 
    defected = False

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == Action.Confess:
            self.defected = True
        if self.defected and random.random() < 0.2:  # 20% chance to forgive
            self.defected = False
        return Action.Confess if self.defected else Action.Silent

    def __str__(self):
        return "Grim with Forgiveness"
