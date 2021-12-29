"""Base classes for paper rock scissors game
"""

# Author: Yehui He <yehui.he@hotmail.com>

from abc import ABCMeta, abstractmethod
from enum import Enum, auto
import time
import warnings


class MoveChoice(Enum):
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()


class Outcome(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()


class ListInstanceMixin:
    """Mixin class for all class in paper_rock_scissors."""

    def __attrnames(self):
        return ''.join('\t%s=%s\n' % (attr, self.__dict__[attr])
                       for attr in sorted(self.__dict__))

    def __repr__(self):
        return '<Instance of %s, address %s:\n%s>' % (
            self.__class__.__name__,
            id(self),
            self.__attrnames())


class BaseRole(metaclass=ABCMeta):
    """Base class for roles in paper_rock_scissors.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """

    @abstractmethod
    def __init__(self, role, name, score):
        self._role = role
        self._name = name
        self._score = score

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        raise AttributeError("Role cannot be altered")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError(
                "Score must be positive integer or zero; got "
                "(score=%d)" % value)
        self._score = value

    @abstractmethod
    def _check_params(self):
        # name
        if not isinstance(self.name, str):
            raise ValueError(f"name should be string, "
                             f"got {self.name} instead.")

        # score
        if not isinstance(self.score, int) or self.score < 0:
            warnings.warn(
                "Score must be positive integer or zero; "
                f"got {self.score} instead.",
                RuntimeWarning,
            )
            self.score = 0

    @abstractmethod
    def get_move(self):
        """Generate current move."""
        pass


class Match(ListInstanceMixin):
    """Match class for paper_rock_scissors.

    This class controls the flow of the game.

    Parameters
    ----------
    _player : _role.Player
        Player role in the match.

    _computer : _role.Computer
        Computer role in the match.

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
            player,
            computer,
            target_score=10,
            curr_round=0,
            max_rounds=20,
            sleep=1,
            verbose=0,
            winner=None):
        self._player = player
        self._computer = computer
        self._target_score = target_score
        self._curr_round = curr_round
        self._max_rounds = max_rounds
        self._sleep = sleep
        self._verbose = verbose
        self._winner = winner

    @property
    def player(self):
        return self._player

    @property
    def computer(self):
        return self._computer

    @property
    def target_score(self):
        return self._target_score

    @target_score.setter
    def target_score(self, value):
        self._target_score = value

    @property
    def curr_round(self):
        return self._curr_round

    @curr_round.setter
    def curr_round(self, value):
        self._curr_round = value

    @property
    def max_rounds(self):
        return self._max_rounds

    @max_rounds.setter
    def max_rounds(self, value):
        self._max_rounds = value

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    @property
    def sleep(self):
        return self._sleep

    @sleep.setter
    def sleep(self, value):
        self._sleep = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

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
        if not isinstance(self._sleep, int) or self._sleep < 0:
            warnings.warn(
                "sleep must be positive integer;"
                f"got {self._sleep} instead.",
                RuntimeWarning,
            )
            # Default sleep set to 1
            self._sleep = 1

        # verbose
        if not isinstance(self._verbose, int) or \
            self._verbose < 0 or self._verbose > 3:
            warnings.warn(
                "verbose must be positive integer between 0 and 3"
                f"got {self._verbose} instead.",
                RuntimeWarning,
            )
            # Default verbose set to 1
            self._verbose = 1

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
               "%(player_name)s score: %(player_score)d \n" \
               "%(computer_name)s score: %(computer_score)d \n" \
               "Target Score: %(target_score)d\n" \
               "Current Round: %(curr_round)d\n" \
               "Maximum Rounds: %(max_rounds)d\n" \
               "Sleep: %(sleep)d\nWinner: %(winner)s\n" %\
               {'player_name': self.player.name,
                'player_score': self.player.score,
                'computer_name': self.computer.name,
                'computer_score': self.computer.score,
                'target_score': self.target_score,
                'curr_round': self.curr_round,
                'max_rounds': self.max_rounds,
                'sleep': self._sleep,
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
        elif ai_move in Match._ROLES_MAPPING[player_move]:
            return Outcome.WIN
        else:
            return Outcome.LOSE

    def play(self):
        # Validate roles input parameters
        self.player._check_params()
        self.computer._check_params()

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
            move = self.player.get_move("Choose a move for this round: ")

            if self.verbose >= 1:
                # Notify player's choice
                print("%s's move: %s" % (self.player.name, move.name))

                # Computer's turn
                print("\n%s is making a decision..." % self.computer.name)
            time.sleep(self._sleep)

            ai_move = self.computer.get_move()
            if self.verbose >= 1:
                print("%s's move: %s" % (self.computer.name,
                                         ai_move.name))
                print("Current round is: %s vs %s" % (move.name,
                                                      ai_move.name))

            outcome = Match._outcome(move, ai_move)

            if outcome is Outcome.WIN:
                if self.verbose >= 1:
                    print("Winner of the current round is: %s \n"
                          % self.player.name)
                self.player.score += 1
            elif outcome is Outcome.LOSE:
                if self.verbose >= 1:
                    print("Winner of the current round is: %s \n"
                          % self.computer.name)
                self.computer.score += 1
            else:
                if self.verbose >= 1:
                    print("It's a draw for this round")

            if self.player.score == self.target_score:
                self.winner = self.player
            elif self.computer.score == self.target_score:
                self.winner = self.computer

        # Display final winner of the game
        # Whoever has the highest score is the winner
        # if there is not winner decided
        # If draw then computer wins
        if not self.winner:
            self.winner = self.player if \
                self.player.score > self.computer.score else self.computer

        print(f"Winner of the game: {self.winner.name}\n")
        print(self._pprint_state())
