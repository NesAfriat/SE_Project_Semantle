import numpy as np


def cosine_function():
    def getCosSim(v1, v2):
        dot_product = np.dot(v1, v2)
        magnitude_v1 = np.linalg.norm(v1)
        magnitude_v2 = np.linalg.norm(v2)

        cosine_similarity = dot_product / (magnitude_v1 * magnitude_v2)
        return cosine_similarity

    return getCosSim


def euclid_function():
    def get_sqrt_dis(a, b):
        return np.linalg.norm(a - b)

    return get_sqrt_dis

