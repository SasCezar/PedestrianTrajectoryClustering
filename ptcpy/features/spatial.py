import numpy as np
from scipy.spatial import distance as pydistance

EUCLIDEAN = "euclidean"
MANHATTAN = "manhattan"


def distance(a, b, metric=EUCLIDEAN):
    """
    Returns the distance between the two points a and b using the given metric
    :param a:
    :param b:
    :param metric:
    :return:
    """
    result = {
        EUCLIDEAN: pydistance.euclidean,
        MANHATTAN: pydistance.cityblock,
    }[metric](a, b)

    return result


def unit_vector(vector):
    """
    Returns the unit vector of the vector.
    :param vector:
    :return:
    """
    return vector / np.linalg.norm(vector)


def angle(v1, v2):
    """
    Returns the angle in radians between vectors 'v1' and 'v2'
    :param v1:
    :param v2:
    :return:
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
