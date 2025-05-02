from Player import Player
from Game import Action

class Detective(Player):

    UIN = "11552256"

    def __init__(self, *args, **kwargs):
        self.moves = [Action.Silent, Action.Confess, Action.Silent, Action.Silent]
        self.current_move = 0
        self.is_exploiting = False

    def play(self, opponent_prev_action):
        if self.current_move < len(self.moves):
            action = self.moves[self.current_move]
            self.current_move += 1
            return action
        if opponent_prev_action == Action.Confess:
            self.is_exploiting = True
        return Action.Confess if self.is_exploiting else Action.Silent

    def __str__(self):
        return "Detective Strategy"
