"""
THe :mod:`imc.paper_rock_scissors` module includes models based on the
game Paper-Rock-Scissors.
"""

from ._base import Match

from ._parser import parser

from ._role import Computer
from ._role import Player

__all__ = ["Match", "Computer", "Player", "parser"]
