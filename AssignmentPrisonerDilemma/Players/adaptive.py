from Player import Player
from Game import Action

class AdaptiveStrategy(Player):

    UIN = "11552254"

    def __init__(self, *args, **kwargs):
        self.defection_count = 0
        self.threshold = 3  # After 3 defections, switch to permanent defection
        self.defecting = False

    def play(self, opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        if opponent_prev_action == Action.Confess:
            self.defection_count += 1
        if self.defection_count >= self.threshold:
            self.defecting = True  # Switch to Grim Trigger mode
        return Action.Confess if self.defecting else opponent_prev_action

    def __str__(self):
        return "Adaptive Strategy"
