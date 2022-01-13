"""Role classes for paper rock scissors game
"""

# Author: Yehui He <yehui.he@hotmail.com>

import random
import warnings
from abc import ABCMeta, abstractmethod

from ._base import ListInstanceMixin, MoveChoice


class BaseRole(metaclass=ABCMeta):
    """Base class for roles in paper_rock_scissors.

    Warning: This class should not be used directly.
    Use derived classes instead.
    """

    @abstractmethod
    def __init__(self, role, name, score):
        self.role = role
        self.name = name
        self.score = score
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

    # @abstractmethod
    # def _check_params(self):
    #     # name
    #     if not isinstance(self.name, str):
    #         raise ValueError(f"name should be string, "
    #                          f"got {self.name} instead.")
    #
    #     # score
    #     if not isinstance(self.score, int) or self.score < 0:
    #         warnings.warn(
    #             "Score must be positive integer or zero; "
    #             f"got {self.score} instead.",
    #             RuntimeWarning,
    #         )
    #         self.score = 0

    @abstractmethod
    def get_move(self, prompt):
        """Generate current move."""
        pass


class Player(ListInstanceMixin, BaseRole):
    """Player role in paper_rock_scissors.

    Parameters
    ----------
    name : str, default='player'
        Player's name.

    role : str, default='Player'
        Player's role in the GameEnvironment.

    score : int, default=0
        Player's current score of the game.
    """

    def __init__(self, name='player', role='Player', score=0):
        super().__init__(role, name, score)

    # def _check_params(self):
    #     super()._check_params()

    def _pprint_moves(self):
        res = f"{self.name}'s turn. Choose current round move within the following: \n"
        for name, member in MoveChoice.__members__.items():
            res = res + str(name) + '. ' + str(member.value) + '\n'
        return res

    def get_move(self, prompt):
        """Prompt input from user for current move

        Parameters
        ----------
        prompt : str
            Prompt input.

        Returns
        -------
        move : MoveChoice
            Current round move.
        """
        while True:
            print(self._pprint_moves())
            try:
                move = int(input(prompt))
            except ValueError:
                print(f"Warning: Invalid input. "
                      f"Please enter a integer from 1 to {len(MoveChoice)}")
                continue
            if move < 1 or move > len(MoveChoice):
                print(f"Warning: Invalid input. "
                      f"Please enter a integer from 1 to {len(MoveChoice)}")
            else:
                break
        return MoveChoice(move)


class Computer(ListInstanceMixin, BaseRole):
    """Computer role in paper_rock_scissors.

    Parameters
    ----------
    name : str, default='player'
        Player's name.

    role : str, default='Player'
        Player's role in the GameEnvironment.

    score : int, default=0
        Player's current score of the game.

    seed : int or None, default=None
        Random number generator's seed.
    """

    def __init__(self, name='ai', role='Computer', score=0, seed=None):
        super().__init__(role, name, score)
        self.seed = seed
        # seed
        if self.seed and not isinstance(self.seed, int):
            warnings.warn(
                "Seed must be integer or None; "
                f"got {self.seed} instead.",
                RuntimeWarning,
            )
            # Default seed set to None
            self.seed = None
        random.seed(self.seed)

    # def _check_params(self):
    #     super()._check_params()
    #
    #     # seed
    #     if self.seed and not isinstance(self.seed, int):
    #         warnings.warn(
    #             "Seed must be integer or None; "
    #             f"got {self.seed} instead.",
    #             RuntimeWarning,
    #         )
    #         # Default seed set to None
    #         self.seed = None
    #     random.seed(self.seed)

    def get_move(self, prompt):
        """Randomized AI move

        Returns
        -------
        move : MoveChoice
            Random AI move.
        """
        return MoveChoice(random.randint(1, len(MoveChoice)))
