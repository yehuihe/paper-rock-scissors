# Main script for paper rock scissors game

# Author: Yehui He <yehui.he@hotmail.com>

from paper_rock_scissors import parser
from paper_rock_scissors import GameEnvironment
from paper_rock_scissors import Computer, Player


args = parser.parse_args()


def main():
    pass


if __name__ == '__main__':

    player = Player(name=args.player_name)
    computer = Computer(name=args.computer_name,
                        seed=args.seed)

    GameEnvironment = GameEnvironment(player,
                  computer,
                  target_score=args.target_score,
                  max_rounds=args.max_rounds,
                  sleep=args.sleep,
                  verbose=args.verbose)

    GameEnvironment.play()

    print("Thank you for playing!")
