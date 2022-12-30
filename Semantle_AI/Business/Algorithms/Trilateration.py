from Business.Algorithms.Algorithm import Algorithm
import numpy as np


class Trilateration(Algorithm):
    def __init__(self, on_guess, vocab):
        super().__init__(on_guess)
        self.vocab = vocab

    def calculate(self, *args):
        data = args[2]
        point = self.trilateration(data.get_points(), data.get_distances())
        return point

    def trilateration(self, points, dists):
        point_sub = points[len(points) - 1]
        A = []
        b = []
        point_sub_power_2 = list(map(lambda x: x ** 2, point_sub))
        dist_last_power = dists[len(points) - 1] ** 2
        for i in range(len(points) - 1):
            A += [2 * points[i] - 2 * point_sub]
            pointi_sub_power_2 = list(map(lambda x: x ** 2, points[i]))
            zipped1 = list(zip(pointi_sub_power_2, point_sub_power_2))
            di = dists[i] ** 2

            sum = dist_last_power - di
            for c1, c2 in zipped1:
                sum += (c1 - c2)
            b = b + [sum]
        point_location = np.linalg.solve(A, b)
        print(point_location)
        return point_location
