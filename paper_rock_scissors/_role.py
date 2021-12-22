"""Role classes for paper rock scissors game
"""

# Author: Yehui He <yehui.he@hotmail.com>

import random
import warnings

from ._base import ListInstanceMixin, BaseRole, MOVE_CHOICE


class Player(ListInstanceMixin, BaseRole):
    """Player role in paper_rock_scissors.

    Parameters
    ----------
    _name : str, default='player'
        Player's name.

    _role : str, default='Player'
        Player's role in the match.

    _score : int, default=0
        Player's current score of the game.
    """

    def __init__(self, name='player', role='Player', score=0):
        super().__init__(role, name, score)

    def _check_params(self):
        super()._check_params()

    def _pprint_moves(self):
        res = f"{self.name}'s turn. Choose current round move within the following: \n"
        for k, v in MOVE_CHOICE.items():
            res = res + str(k) + '. ' + v + '\n'
        return res

    def get_move(self, prompt):
        """Prompt input from user for current move

        Parameters
        ----------
        prompt : str
            Prompt input.

        Returns
        -------
        move : int
            Current round move.
        """
        while True:
            print(self._pprint_moves())
            try:
                move = int(input(prompt))
            except ValueError:
                print(f"Warning: Invalid input. "
                      f"Please enter a integer from 1 to {len(MOVE_CHOICE)}")
                continue
            if move < 1 or move > len(MOVE_CHOICE):
                print(f"Warning: Invalid input. "
                      f"Please enter a integer from 1 to {len(MOVE_CHOICE)}")
            else:
                break
        return move


class Computer(ListInstanceMixin, BaseRole):
    """Computer role in paper_rock_scissors.

    Parameters
    ----------
    _name : str, default='player'
        Player's name.

    _role : str, default='Player'
        Player's role in the match.

    _score : int, default=0
        Player's current score of the game.

    _seed : int or None, default=None
        Random number generator's seed.
    """

    def __init__(self, name='ai', role='Computer', score=0, *, seed=None):
        super().__init__(role, name, score)
        self._seed = seed

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value

    def _check_params(self):
        super()._check_params()

        # seed
        if self.seed and not isinstance(self.seed, int):
            warnings.warn(
                "Seed must be integer or None; "
                f"got {self.seed} instead.",
                RuntimeWarning,
            )
            self.seed = None

    def get_move(self):
        """Randomized AI move

        Returns
        -------
        move : int
            Random AI move.
        """
        random.seed(self.seed)
        return random.randint(1, len(MOVE_CHOICE))
