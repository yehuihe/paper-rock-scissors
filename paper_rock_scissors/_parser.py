"""Argument parser for paper rock scissors game
"""

# Author: Yehui He <yehui.he@hotmail.com>

import argparse


VERSION = '1.0'

parser = argparse.ArgumentParser(
    description='Paper-Rock-Scissors.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)


parser.add_argument('-t', '--target-score', type=int, default=10,
                    help='Target score of the current game. '
                         'The game ends once one side reach the target score')
parser.add_argument('-m', '--max-rounds', type=int, default=20,
                    help='Maximum rounds of the current game. '
                         'The game ends once total rounds reach the max '
                         'rounds')
parser.add_argument('-pn', '--player-name', type=str, default='player',
                    help='Player name')
parser.add_argument('-cn', '--computer-name', type=str, default='ai',
                    help='Computer name')
parser.add_argument('-s', '--seed', default=None,
                    help='Computer random number generator seed')
parser.add_argument('-sp', '--sleep', type=int, default=1,
                    help='Sleep time when computer is making a decision')
parser.add_argument('-v', '--verbose', action='count', default=1,
                    help='Verbosity level')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {VERSION}')
