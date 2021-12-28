import unittest
from unittest.mock import patch

from paper_rock_scissors import Match, Player, Computer, MoveChoice, Outcome


class MatchTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.computer = Computer()

    def test_outcome(self):
        # rock vs scissors
        self.assertEqual(
            Match._outcome(MoveChoice(1), MoveChoice(3)), Outcome.WIN)
        # paper vs scissors
        self.assertEqual(
            Match._outcome(MoveChoice(2), MoveChoice(3)), Outcome.LOSE)
        # paper vs paper
        self.assertEqual(
            Match._outcome(MoveChoice(2), MoveChoice(2)), Outcome.DRAW)

    def test_negative_target_score(self):
        match = Match(self.player, self.computer, target_score=-1)
        with self.assertWarns(RuntimeWarning):
            match._check_params()
        self.assertEqual(match.target_score, 10)

    def test_invalid_max_rounds(self):
        match = Match(self.player, self.computer, target_score=10, max_rounds=5)
        with self.assertWarns(RuntimeWarning):
            match._check_params()
        self.assertEqual(match.max_rounds, match.target_score)

    def test_negative_sleep(self):
        match = Match(self.player, self.computer, sleep=-1)
        with self.assertWarns(RuntimeWarning):
            match._check_params()
        self.assertEqual(match._sleep, 1)

    @patch('builtins.input', side_effect=[1, 2, 1, 3, 2, 3, 1, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 1])
    def test_reach_target_score_play(self, input):
        computer = Computer(seed=0)
        match = Match(self.player,
                      computer,
                      target_score=5,
                      max_rounds=20,
                      sleep=0)
        match.play()
        self.assertEqual(match.winner, self.player)

    @patch('builtins.input', side_effect=[1, 2, 1, 3, 2, 3, 1, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 1])
    def test_reach_max_score_play(self, input):
        computer = Computer(seed=0)
        match = Match(self.player,
                      computer,
                      target_score=10,
                      max_rounds=10,
                      sleep=0)
        match.play()
        self.assertEqual(match.winner, computer)

    # TODO: more tests


if __name__ == '__main__':
    unittest.main()
