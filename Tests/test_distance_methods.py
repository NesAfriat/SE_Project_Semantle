import unittest
import numpy as np
from Semantle_AI.Business.MethodDistances import cosine_function, euclid_function


class TestDistances(unittest.TestCase):
    def test_cosine_similarity_identical_vectors(self):
        cosine = cosine_function()

        v1 = [1, 2, 3]
        v2 = [1, 2, 3]
        similarity = cosine(v1, v2)

        self.assertAlmostEqual(similarity, 1.0)

    def test_cosine_similarity_orthogonal_vectors(self):
        cosine = cosine_function()

        v1 = [1, 0, 0]
        v2 = [0, 1, 0]
        similarity = cosine(v1, v2)

        self.assertAlmostEqual(similarity, 0.0)

    def test_cosine_similarity_opposite_vectors(self):
        cosine = cosine_function()

        v1 = [1, 1, 1]
        v2 = [-1, -1, -1]
        similarity = cosine(v1, v2)

        self.assertAlmostEqual(similarity, -1.0)

    def test_cosine_similarity_vectors_different_dimensions(self):
        cosine = cosine_function()

        v1 = [1, 2, 3]
        v2 = [4, 5]
        with self.assertRaises(IndexError):
            cosine(v1, v2)

    def test_cosine_similarity_empty_vectors(self):
        cosine = cosine_function()

        v1 = []
        v2 = []
        with self.assertRaises(ZeroDivisionError):
            cosine(v1, v2)

    def test_euclidean_distance_identical_points(self):
        euclid = euclid_function()

        p1 = [1, 2, 3]
        p2 = [1, 2, 3]
        distance = euclid(p1, p2)

        self.assertAlmostEqual(distance, 0.0)

    def test_euclidean_distance_points_different_coordinates(self):
        euclid = euclid_function()

        p1 = [1, 2, 3]
        p2 = [4, 5, 6]
        distance = euclid(p1, p2)

        self.assertAlmostEqual(distance, 5.19615242, places=8)


if __name__ == '__main__':
    unittest.main()
