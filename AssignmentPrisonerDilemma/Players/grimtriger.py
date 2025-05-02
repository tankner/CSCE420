from Player import Player
from Game import Action

class GrimTrigger(Player):

    UIN = "11552245"


    defected = False  # Tracks if opponent has defected

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == Action.Confess:
            self.defected = True
        return Action.Confess if self.defected else Action.Silent

    def __str__(self):
        return "Grim Trigger"
