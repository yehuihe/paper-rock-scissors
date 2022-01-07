import random
import unittest
from unittest.mock import patch

from paper_rock_scissors import GameEnvironment, Player, Computer, MoveChoice, Outcome


class GameEnvironmentTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.computer = Computer()

    def test_outcome(self):
        # rock vs scissors
        self.assertEqual(
            GameEnvironment._outcome(MoveChoice(1), MoveChoice(3)), Outcome.WIN)
        # paper vs scissors
        self.assertEqual(
            GameEnvironment._outcome(MoveChoice(2), MoveChoice(3)), Outcome.LOSE)
        # paper vs paper
        self.assertEqual(
            GameEnvironment._outcome(MoveChoice(2), MoveChoice(2)), Outcome.DRAW)

    def test_negative_target_score(self):
        GameEnvironment = GameEnvironment(self.player, self.computer, target_score=-1)
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment.target_score, 10)

    def test_invalid_max_rounds(self):
        GameEnvironment = GameEnvironment(self.player, self.computer, target_score=10, max_rounds=5)
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment.max_rounds, GameEnvironment.target_score)

    def test_invalid_sleep(self):
        # Negative sleep
        GameEnvironment = GameEnvironment(self.player, self.computer, sleep=-1)
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment._sleep, 1)
        # Invalid sleep
        GameEnvironment.sleep = 'no'
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment._sleep, 1)

    def test_invalid_verbose(self):
        # Negative verbose
        GameEnvironment = GameEnvironment(self.player, self.computer, verbose=-1)
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment._verbose, 1)
        # Greater than 3 verbose
        GameEnvironment.verbose = 4
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment._verbose, 1)
        # Invalid verbose
        GameEnvironment.verbose = 'no'
        with self.assertWarns(RuntimeWarning):
            GameEnvironment._check_params()
        self.assertEqual(GameEnvironment._verbose, 1)

    @patch('builtins.input', side_effect=[1, 2, 1, 3, 2, 3, 1, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 1])
    def test_reach_target_score_play(self, input):
        computer = Computer(seed=0)
        GameEnvironment = GameEnvironment(self.player,
                      computer,
                      target_score=5,
                      max_rounds=20,
                      sleep=0,
                      verbose=0)
        GameEnvironment.play()
        self.assertEqual(GameEnvironment.winner, self.player)

    @patch('builtins.input', side_effect=[1, 2, 1, 3, 2, 3, 1, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 1])
    def test_reach_max_score_play(self, input):
        computer = Computer(seed=0)
        GameEnvironment = GameEnvironment(self.player,
                      computer,
                      target_score=10,
                      max_rounds=10,
                      sleep=0,
                      verbose=0)
        # random.seed(computer.seed)
        GameEnvironment.play()
        self.assertEqual(GameEnvironment.winner, computer)

    # TODO: more tests


if __name__ == '__main__':
    unittest.main()
