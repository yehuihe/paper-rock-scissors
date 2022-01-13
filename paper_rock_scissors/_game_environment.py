"""Game Environment classes and various game modes
    for paper rock scissors game
"""

# Author: Yehui He <yehui.he@hotmail.com>
import time
import warnings

from _base import MoveChoice, Outcome, ListInstanceMixin
from mode import StandardMode, DualMode, AIMode
from _role import Player, Computer


class GameEnvironment(ListInstanceMixin):
    """GameEnvironment class for paper_rock_scissors.

    This class controls the flow of the game.

    Parameters
    ----------
    _first_player : _role.Player
        Player role in the GameEnvironment.

    _second_player : _role.Computer
        Computer role in the GameEnvironment.

    _target_score : int, default=10
        Target score of the game. Anyone reaches this score
        will end the game.

    _curr_round : int, default=0
        Current round of the game.

    _max_rounds : int, default=20
        Maximum round of the game. Once _curr_round reaches
        the max the game ends.

    _sleep : int, default=1
        Sleep time between each rounds.

    _verbose : int, default=0
        Verbosity level.

    _winner : {_role.Player, _role.Computer}
        Winner of the game.
    """

    _ROLES_MAPPING = {
        MoveChoice.ROCK: [MoveChoice.SCISSORS],
        MoveChoice.SCISSORS: [MoveChoice.PAPER],
        MoveChoice.PAPER: [MoveChoice.ROCK],
    }

    def __init__(
            self,
            factory,
            target_score=10,
            curr_round=0,
            max_rounds=20,
            sleep=1,
            verbose=0,
            winner=None):
        self.first_player = factory.make_first_player()
        self.second_player = factory.make_second_player()
        self.target_score = target_score
        self.curr_round = curr_round
        self.max_rounds = max_rounds
        self.sleep = sleep
        self.verbose = verbose
        self.winner = winner

    # @property
    # def target_score(self):
    #     return self.target_score
    #
    # @target_score.setter
    # def target_score(self, value):
    #     self.target_score = value
    #
    # @property
    # def curr_round(self):
    #     return self.curr_round
    #
    # @curr_round.setter
    # def curr_round(self, value):
    #     self.curr_round = value
    #
    # @property
    # def max_rounds(self):
    #     return self.max_rounds
    #
    # @max_rounds.setter
    # def max_rounds(self, value):
    #     self.max_rounds = value
    #
    # @property
    # def winner(self):
    #     return self.winner
    #
    # @winner.setter
    # def winner(self, value):
    #     self.winner = value
    #
    # @property
    # def sleep(self):
    #     return self.sleep
    #
    # @sleep.setter
    # def sleep(self, value):
    #     self.sleep = value
    #
    # @property
    # def verbose(self):
    #     return self.verbose
    #
    # @verbose.setter
    # def verbose(self, value):
    #     self.verbose = value

    def _check_params(self):
        # target_score
        if not isinstance(self.target_score, int) or self.target_score <= 0:
            warnings.warn(
                "target_score must be positive integer; "
                f"got {self.target_score} instead.",
                RuntimeWarning,
            )
            # Default target_score set to 10
            self.target_score = 10

        # max_rounds
        if not isinstance(self.max_rounds, int) or \
                self.max_rounds < self.target_score:
            warnings.warn(
                "max_rounds must greater or equal to target_score; "
                f"got {self.max_rounds} instead.",
                RuntimeWarning,
            )
            # Default max_rounds set to target_score
            self.max_rounds = self.target_score

        # sleep
        if not isinstance(self.sleep, int) or self.sleep < 0:
            warnings.warn(
                "sleep must be positive integer;"
                f"got {self.sleep} instead.",
                RuntimeWarning,
            )
            # Default sleep set to 1
            self.sleep = 1

        # verbose
        if not isinstance(self.verbose, int) or \
                self.verbose < 0 or self.verbose > 3:
            warnings.warn(
                "verbose must be positive integer between 0 and 3"
                f"got {self.verbose} instead.",
                RuntimeWarning,
            )
            # Default verbose set to 1
            self.verbose = 1

    @staticmethod
    def _pprint_rules():
        """Return rules of the current game."""

        return "Current winning conditions of the Paper-Rock-Scissors: \n" \
               "Paper beats (wraps) rock \n" \
               "Rock beats (blunts) scissors \n " \
               "Scissors beats (cuts) paper. \n" \
               "Game ends while there is a winner " \
               "(score reach preset target score) or " \
               "total rounds reach the maximum. \n" \
               "Press ctrl + C quit the game."

    def _pprint_state(self):
        """Return state of the current game."""

        return "Current state of the game: \n" \
               "%(first_player_name)s score: %(first_player_score)d \n" \
               "%(second_player_name)s score: %(second_player_score)d \n" \
               "Target Score: %(target_score)d\n" \
               "Current Round: %(curr_round)d\n" \
               "Maximum Rounds: %(max_rounds)d\n" \
               "Sleep: %(sleep)d\nWinner: %(winner)s\n" % \
               {'first_player_name': self.first_player.name,
                'first_player_score': self.first_player.score,
                'second_player_name': self.second_player.name,
                'second_player_score': self.second_player.score,
                'target_score': self.target_score,
                'curr_round': self.curr_round,
                'max_rounds': self.max_rounds,
                'sleep': self.sleep,
                'winner': self.winner}

    @staticmethod
    def _outcome(player_move, ai_move):
        """Determine the outcome of current round.

        Paper beats (wraps) rock.
        Rock beats (blunts) scissors.
        Scissors beats (cuts) paper.

        Parameters
        ----------
        player_move : MoveChoice
            Player's move for current round.

        ai_move : MoveChoice
            AI's move for current round.

        Returns
        -------
        outcome : Outcome
            Outcome of the current round.
        """
        if player_move is ai_move:
            return Outcome.DRAW
        elif ai_move in GameEnvironment._ROLES_MAPPING[player_move]:
            return Outcome.WIN
        else:
            return Outcome.LOSE

    def play(self):
        # Validate input parameters
        self._check_params()

        # Display game rules
        print(self._pprint_rules())
        # Game ends while there is a winner or total rounds reach the maximum
        while not self.winner and self.curr_round <= self.max_rounds:
            # Print current game state
            if self.verbose >= 1:
                print(self._pprint_state())

            # Prompt input from player
            # Return MoveChoice
            move = self.first_player.get_move("Choose a move for this round: ")

            if self.verbose >= 1:
                # Notify player's choice
                print("%s's move: %s" % (self.first_player.name, move.name))

                # Computer's turn
                print("\n%s is making a decision..." % self.second_player.name)
            time.sleep(self.sleep)

            second_player_move = self.second_player.get_move(
                "Choose a move for this round: ")
            if self.verbose >= 1:
                print("%s's move: %s" % (self.second_player.name,
                                         second_player_move.name))
                print("Current round is: %s vs %s" % (move.name,
                                                      second_player_move.name))

            outcome = GameEnvironment._outcome(move, second_player_move)

            if outcome is Outcome.WIN:
                if self.verbose >= 1:
                    print("Winner of the current round is: %s \n"
                          % self.first_player.name)
                self.first_player.score += 1
            elif outcome is Outcome.LOSE:
                if self.verbose >= 1:
                    print("Winner of the current round is: %s \n"
                          % self.second_player.name)
                self.second_player.score += 1
            else:
                if self.verbose >= 1:
                    print("It's a draw for this round")
            self.curr_round += 1

            if self.first_player.score == self.target_score:
                self.winner = self.first_player
            elif self.second_player.score == self.target_score:
                self.winner = self.second_player

        # Display final winner of the game
        # Whoever has the highest score is the winner
        # if there is not winner decided
        # If draw then computer wins
        if not self.winner:
            self.winner = self.first_player if \
                self.first_player.score > self.second_player.score else \
                self.second_player

        print(f"Winner of the game: {self.winner.name}\n")
        print(self._pprint_state())
