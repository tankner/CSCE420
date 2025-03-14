from Player import Player
from Game import Action


class MyPlayer(Player):
    # 1. Add your UINs seperated by a ':'
    #    DO NOT USE A COMMA ','
    #    We use CSV files and commas will cause trouble
    # 2. Write your strategy under the play function
    # 3. Add your team's name (this will be visible to your classmates on the leader board)

    UIN = "133002867"

    def play(self, opponent_prev_action):
        # Write your strategy as a function of the opponent's previous action and the error rate for prev action report
        # For example, the below implementation returns the opponent's prev action if the error is smaller than 0.5
        # else it returns the opposite of the opponent's reported action
        # Don't forget to remove the example...

        # error rate encodes state
        # 0.01 - opponent is a nice guy
        # 0.02 - we just checked if the opponent was cooperative
        # 0.03 - opponent seems to be cooperative, we are rolling silent
        # 0.04 - bot is tough guy

        # Trust at first
        print(self.error_rate)
        if opponent_prev_action == Action.Noop:
            self.error_rate = 0.01
            return Action.Confess
        elif self.error_rate == 0.01 and opponent_prev_action == Action.Silent:
            return Action.Confess
        elif self.error_rate == 0.01 and opponent_prev_action == Action.Confess:
            self.error_rate = 0.02
            return Action.Silent
        elif self.error_rate == 0.02 and opponent_prev_action == Action.Silent:
            self.error_rate = 0.04
            return Action.Confess
        elif self.error_rate == 0.02 and opponent_prev_action == Action.Confess:
            self.error_rate = 0.03
            return Action.Silent
        elif self.error_rate == 0.03 and opponent_prev_action == Action.Silent:
            return Action.Silent
        elif self.error_rate == 0.03 and opponent_prev_action == Action.Confess:
            self.error_rate == 0.04
            return Action.Confess
        elif self.error_rate == 0.04:
            return Action.Confess
        return Action.Confess


        # if opponent_prev_action == Action.Noop:
        #     return Action.Silent
        # if self.error_rate < 0.5:
        #     return opponent_prev_action
        # else:
        #     return Action(-(opponent_prev_action.value - 1))

    def __str__(self):
        return "tankner"
