import numpy as np


def cluster_silouette(clustered_trajectories):
    x = np.array([])
    for t in clustered_trajectories:
        x_t = np.ndarray(shape=(len(t.points()), 3))
        for i, p in enumerate(t.points()):
            x_t[i] = np.array(list(t.points()[i]) + [t.direction])

        x = np.concatenate((x, x_t), axis=0)
