# Main script for paper rock scissors game

# Author: Yehui He <yehui.he@hotmail.com>

from paper_rock_scissors import parser
from paper_rock_scissors import GameEnvironment
from paper_rock_scissors import Computer, Player
from paper_rock_scissors.mode import StandardMode, DualMode, AIMode


args = parser.parse_args()


def validate_factory(factories):
    try:
        input_msg = 'Which game mode would you like to play, ' \
                    '[s]tandard, [d]ual, or [a]i?'
        game_mode = input(input_msg)
        factory = factories[game_mode]()
        valid_input = True
    except KeyError:
        error_msg = 'Sorry, only standard (key s), ' \
                    'dual (key d) and ai (key a) are available'
        print(error_msg)
        return False, None
    return True, factory


def main():
    factories = dict(s=StandardMode, d=DualMode, a=AIMode)
    valid_input = False
    while not valid_input:
        valid_input, factory = validate_factory(factories)
    print()
    environment = GameEnvironment(factory,
                                  target_score=args.target_score,
                                  max_rounds=args.max_rounds,
                                  sleep=args.sleep,
                                  verbose=args.verbose)


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
