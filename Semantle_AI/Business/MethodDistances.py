import math
##TODO use calculates with numpy
import numpy as np



def cosine_function():
    def getCosSim(v1, v2):
        def mag(a):
            return math.sqrt(sum(val ** 2 for val in a))

        def dot(f1, f2):
            return sum(a * f2[idx] for idx, a in enumerate(f1))

        v1 = list(v1)
        v2 = list(v2)
        return dot(v1, v2) / (mag(v1) * (mag(v2)))
    return getCosSim


def euclid_function():
    def get_sqrt_dis(v1, v2):
        ans = sum([(xi - yi) ** 2 for xi, yi in zip(v1, v2)])
        return math.sqrt(ans)
    return get_sqrt_dis
