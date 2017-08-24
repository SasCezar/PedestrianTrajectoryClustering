import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


class GroupsDetection(object):
    def __init__(self, trajectories, directions, threshold=0.5):
        self.trajectories = trajectories
        self.directions = directions
        self.similarity = None
        self.threshold = threshold

    def group_trajectories(self):
        self._similarities()
        self._group()

    def _similarities(self):
        similarity = np.zeros(shape=(len(self.trajectories)))
        for i in range(1, len(self.trajectories)):
            x = np.array(self.trajectories[i])
            for j in range(i):
                y = np.array(self.trajectories[j])
                similarity[i, j] = fastdtw(x, y, dist=euclidean)

        self.similarity = np.linalg.norm(similarity, axis=0)

    def _group(self):
        g_id = 0
        groups = {}
        grouped_ids = []
        for i in range(1, len(self.trajectories)):
            if i not in grouped_ids:
                grouped_ids += [i]
                groups[g_id] = [i] if g_id not in groups else groups[g_id] + [i]

            for j in range(i):
                if self.similarity[j] > self.threshold:
                    grouped_ids = grouped_ids + [j] if j not in grouped_ids else grouped_ids


                    ### Usare dict user_id group_id
