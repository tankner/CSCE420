from Player import Player
from Game import Action

class Tester(Player):

    UIN = "11552251"

  
    first_move = True
    exploit = False

    def play(self, opponent_prev_action):
        if self.first_move:
            self.first_move = False
            return Action.Confess  # Start by defecting to test opponent
        if opponent_prev_action == Action.Silent:
            self.exploit = True  # Opponent is a cooperator, so exploit them
        return Action.Confess if self.exploit else Action.Silent

    def __str__(self):
        return "Tester Strategy"
