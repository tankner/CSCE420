from Player import Player
from Game import Action

class Pavlov(Player):

    UIN = "11552246"


    last_action = Action.Silent  # Starts by cooperating

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == self.last_action:
            return self.last_action
        self.last_action = Action.Confess if self.last_action == Action.Silent else Action.Silent
        return self.last_action

    def __str__(self):
        return "Pavlov (Win-Stay, Lose-Shift)"
