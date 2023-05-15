import random
import numpy as np
from unittest.mock import MagicMock
from Semantle_AI.Business.Algorithms.MultiLateration import in_range,MultiLateration
from Semantle_AI.Business.Algorithms.NLateration import Trilateration
from Semantle_AI.Business.Algorithms.Naive import Naive
from Semantle_AI.Business.MethodDistances import euclid_function
import unittest


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.trilateration = Trilateration()

    def test_trilateration(self):
        points = np.array([
            [1, 1],
            [1, 5],
            [5, 1]
        ])
        distances = np.array([2, 2, 2])
        expected_location = np.array([3, 3])
        result = self.trilateration.trilateration(points, distances)
        np.testing.assert_array_almost_equal(result, expected_location, decimal=6)

    def test_in_range(self):
        self.assertTrue(in_range(95, 100, 5))
        self.assertTrue(in_range(100, 100, 5))
        self.assertFalse(in_range(90, 100, 5))

    def test_multi_lateration(self):
        distance_formula = euclid_function()
        multilateration = MultiLateration(distance_formula)
        multilateration.data = MagicMock()

        # Mocking the data instance
        multilateration.data.last_word = "test"
        multilateration.data.last_score = 1
        multilateration.data.error = 1

        # Use fixed seed to make the test deterministic
        random.seed(42)

        # Create a dictionary to map words to dummy vectors
        word_vec_mapping = {word: [random.random() for _ in range(5)] for word in range(5, 15)}
        word_vec_mapping["test"] = [0.5, 0.5, 0.5, 0.5, 0.5]
        word_vec_mapping["test2"] = [1.5, 0.5, 0.5, 0.5, 0.5]

        # Use the dictionary's `get` method as the side effect for the `get_word_vec` method
        multilateration.data.get_word_vec.side_effect = word_vec_mapping.get

        multilateration.data.remain_words = list(range(5, 15))
        multilateration.data.remain_words.append("test2")

        result = multilateration.calculate()
        self.assertEqual(result,"test2")

    def test_naive(self):
        naive = Naive()
        naive.data = MagicMock()
        naive.data.remain_words = ['apple', 'banana', 'cherry']

        result = naive.calculate()
        self.assertIn(result, ['apple', 'banana', 'cherry'])
        self.assertNotIn(result, naive.data.remain_words)
        self.assertEqual(len(naive.data.remain_words), 2)

    def test_naive_bas(self):
        # Test when remain_words is not empty
        naive = Naive()
        naive.data = MagicMock()
        naive.data.remain_words = ['apple', 'banana', 'cherry']

        result = naive.calculate()
        self.assertIn(result, ['apple', 'banana', 'cherry'])
        self.assertNotIn(result, naive.data.remain_words)
        self.assertEqual(len(naive.data.remain_words), 2)

        # Test when remain_words is empty
        naive_empty = Naive()
        naive_empty.data = MagicMock()
        naive_empty.data.remain_words = []

        with self.assertRaises(ValueError):
            naive_empty.calculate()

    def test_calculate_no_words_left(self):
        naive = Naive()
        naive.data = MagicMock()
        naive.data.remain_words = []

        with self.assertRaises(ValueError):
            naive.calculate()

    def test_naive_edge_cases(self):
        # Test when remain_words is None
        naive_none = Naive()
        naive_none.data = MagicMock()
        naive_none.data.remain_words = None

        with self.assertRaises(TypeError):
            naive_none.calculate()

        # Test when remain_words is empty
        naive_empty = Naive()
        naive_empty.data = MagicMock()
        naive_empty.data.remain_words = []

        with self.assertRaises(ValueError):
            naive_empty.calculate()


if __name__ == '__main__':
    unittest.main()