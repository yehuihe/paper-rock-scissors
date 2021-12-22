import unittest
from unittest.mock import patch

from paper_rock_scissors import Player, Computer


class PlayerTestCase(unittest.TestCase):
    def test_invalid_name(self):
        player = Player(name=4)
        with self.assertRaises(ValueError):
            player._check_params()

    def test_negative_score(self):
        player = Player(score=-1)
        with self.assertWarns(RuntimeWarning):
            player._check_params()
        self.assertEqual(player.score, 0)

    @patch('builtins.input', return_value=1)
    def test_valid_move(self, input):
        player = Player()
        self.assertEqual(player.get_move("Choose a move for this round: "), 1)

    @patch('builtins.input', side_effect=[5, 1])
    def test_invalid_move(self, input):
        player = Player()
        self.assertEqual(player.get_move("Choose a move for this round: "), 1)


class ComputerTestCase(unittest.TestCase):
    def test_invalid_name(self):
        computer = Computer(name=4)
        with self.assertRaises(ValueError):
            computer._check_params()

    def test_negative_score(self):
        computer = Computer(score=-1)
        with self.assertWarns(RuntimeWarning):
            computer._check_params()
        self.assertEqual(computer.score, 0)

    def test_invalid_seed(self):
        computer = Computer(seed='d')
        with self.assertWarns(RuntimeWarning):
            computer._check_params()
        self.assertEqual(computer.seed, None)

    def test_random_move(self):
        computer = Computer(seed=0)
        self.assertEqual(computer.get_move(), 2)


if __name__ == '__main__':
    unittest.main()
