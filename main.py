# Main script for paper rock scissors game

# Author: Yehui He <yehui.he@hotmail.com>

from paper_rock_scissors import parser
from paper_rock_scissors import Match
from paper_rock_scissors import Computer, Player


args = parser.parse_args()


if __name__ == '__main__':

    player = Player(name=args.player_name)
    computer = Computer(name=args.computer_name,
                        seed=args.seed)

    match = Match(player, computer,
                  target_score=args.target_score, max_rounds=args.max_rounds)

    match.play()

    print("Thank you for playing!")
