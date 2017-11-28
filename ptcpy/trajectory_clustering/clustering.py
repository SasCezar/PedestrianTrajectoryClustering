"""
Created on 24. 4. 2015

@author: janbednarik
"""
import logging
import math
import random

import numpy as np
from scipy import spatial
from scipy.cluster.vq import kmeans
from scipy.cluster.vq import kmeans2

from common import euclid_dist


class Clustering(object):
    """
    A class implementing trajectory clustering. Based on [1] Clustering of Vehicle Trajectories (Stefan Atev)
    """

    def __init__(self, alpha=0.88, w=2.0, std_nn=2, std_min=0.4, std_max=20.0, distance=spatial.distance.euclidean):
        """
        Constructor

        :param alpha: robustness against outliers (see [1])
        :param w: neighborhood (see [1])
        :param std_nn: number of nearest neighbors to compute standard deviation used in similarity measure (see [1])
        :param std_min: minimum value for clipping (see [1])
        :param std_max: maximum value for clipping (see [1])
        """
        self.trajectories = []
        self.dist_mat = np.zeros((0, 0))
        self.std_devs = np.zeros((0, 0))
        self.alpha = alpha
        self.w = w
        self.std_nn = std_nn
        self.std_min = std_min
        self.std_max = std_max
        self.distance = distance

    def std(self, tidx):
        return self.std_devs[tidx]

    def mod_haus_dist(self, t1idx, t2idx):
        """
        Computes modified Hausdorf distance.

        :param t1idx:
        :param t2idx:
        :return:
        """
        t1 = self.trajectories[t1idx]
        t2 = self.trajectories[t2idx]

        distances = np.zeros(len(t1))
        t1_points_rel_pos = [t1.get_prefix_sum()[i] / t1.length() for i in range(len(t1))]
        t2_points_rel_pos = [t2.get_prefix_sum()[i] / t2.length() for i in range(len(t2))]

        for i in range(len(t1)):
            pt1 = t1.get_points()[i]

            # Find corresponding point pt2 in t2 for point pt1 = t1[i]
            pt2idx = np.argmin(
                np.array([abs(t1_points_rel_pos[i] - t2_points_rel_pos[j]) for j in range(len(t2_points_rel_pos))]))

            # Get set of points sp2 of t2 within neighborhood of point pt2
            ps = t2.get_prefix_sum()
            tmp = [abs(ps[j] - ps[pt2idx]) - (self.w / 2.0) for j in range(len(ps))]
            neighborhood_idxs = [j for j in range(len(tmp)) if tmp[j] <= 0]

            # Find minimum Euclidean distance between point pt1 and set of points sp2
            dist = float("inf")
            for idx in neighborhood_idxs:
                newdist = euclid_dist(pt1, t2.get_points()[idx])
                if newdist < dist:
                    dist = newdist

            distances[i] = dist

        # Find distance worse then self.alpha percent of the other distance
        distances = np.sort(distances)

        return distances[min(int(len(distances) * self.alpha), len(distances) - 1)]

    def create_distance_matrix(self):
        size = len(self.trajectories)
        self.dist_mat = np.ones((size, size))

        for r in range(size):
            for c in range(size):
                dist = self.mod_haus_dist(r, c)
                self.dist_mat[r, c] *= dist

    def create_std_devs(self):
        row_sorted_dist_mat = np.copy(self.dist_mat)
        row_sorted_dist_mat.sort(axis=1)

        self.std_devs = row_sorted_dist_mat[:, min(self.std_nn, row_sorted_dist_mat.shape[1] - 1)]
        for i in range(len(self.std_devs)):
            self.std_devs[i] = max(self.std_min, min(self.std_max, self.std_devs[i]))

    def similarity(self, t1idx, t2idx):
        """
        Computes the similarity measure of trajectories t1 and t2
        according to paper 'Clustering of Vehicle Trajectories (Stefan Atev)'
        :param t1idx:
        :param t2idx:
        :return:
        """
        return math.exp(
            -(self.dist_mat[t1idx, t2idx] * self.dist_mat[t2idx, t1idx]) / (2 * self.std(t1idx) * self.std(t2idx)))

    def cluster_agglomerative(self, trajectories, cn):
        """
        The function performs agglomerative clustering of trajectories
        and for each trajectory sets an index t.ci denoting estimated cluster.
        :param trajectories:  A list 'trajectories' of trajectories given as lists of
            objects of class Trajectory.
        :param cn:  The number of desired clusters.
        :return:
        """
        self.trajectories = trajectories

        # Update a distance matrix and std deviations
        self.create_distance_matrix()

        clusters = [[i] for i in range(len(trajectories))]

        while len(clusters) > cn:
            aff_mat = np.zeros((len(clusters), len(clusters)))
            for r in range(aff_mat.shape[0] - 1):
                for c in range(r + 1, aff_mat.shape[1]):
                    # count inter-cluster average distance
                    dist = 0

                    for t1idx in clusters[r]:
                        for t2idx in clusters[c]:
                            # distance of trajectory t1 (t1 in tA) and trajectory t2 (t2 in tB)
                            dist += 1 / ((self.dist_mat[t1idx, t2idx] * self.dist_mat[t2idx, t1idx]) + 1e-6)

                    dist *= 1.0 / (len(clusters[r]) * len(clusters[c]))
                    aff_mat[r, c] = dist

            # Find two closest clusters and merge them
            # First trajectory is given by row index, second trajectory is given by column index of affinity matrix
            t1idx = np.argmax(aff_mat) / aff_mat.shape[1]
            t2idx = np.argmax(aff_mat) % aff_mat.shape[0]

            clusters[t1idx].extend(clusters[t2idx])
            clusters = [clusters[i] for i in range(len(clusters)) if i != t2idx]

        # Assign an estimated cluster index to each trajectory
        for i in range(len(clusters)):
            for j in clusters[i]:
                self.trajectories[j].set_cluster_idx(i)

    def cluster_spectral(self, trajectories, clusters=-1):
        """
        The function performs spectral clustering of trajectories
        and for each trajectory sets an index t.ci denoting estimated cluster.
        the function estimates the number of resulting clusters automatically.

        :param trajectories: A list 'trajectories' of trajectories given as lists of
            objects of class Trajectory.
        :param clusters: A number of clusters. If the value is not specified, the
            algorithm estimates the best number itself
        :return:
        """
        # Need to be assigned as am object variable - other support functions use it (create_std_devs(), etc.)!
        self.trajectories = trajectories

        # Update a distance matrix and std deviations
        logging.info("Computing Hausdorf distance")
        self.create_distance_matrix()
        logging.info("Computing STD")
        self.create_std_devs()

        logging.info("Computing affinity matrix.")
        k = self._affinity_matrix(trajectories)

        # Diagonal matrix w for normalization
        w = np.diag(1.0 / np.sqrt(np.sum(k, 1)))

        # Normalized affinity matrix
        l = np.dot(np.dot(w, k), w)

        # Eigendecomposition
        logging.info("Computing eigendecomposition")
        eval, evec = np.linalg.eig(l)

        g_min, g_max = 0, 0
        for val in eval:
            if val > 0.8:
                g_max += 1
            if val > 0.99:
                g_min += 1

        # Sort eigenvalues and eigenvectors according to descending eigenvalue
        eval, evec = zip(*sorted(zip(eval, evec.T), reverse=True))
        evec = np.array(evec).T

        g = clusters
        logging.info("Estimating cluster numbers.")
        if g == -1:
            g = self._estimate_cluster_number(evec, g_max, g_min)

        logging.info("Number of centroids = {}".format(g))

        self._kmean_cluster(trajectories, g, evec)

    def _affinity_matrix(self, trajectories):
        """
        Computes the affinity matrix for the trajectories
        :param trajectories:
        :return:
        """
        k = np.zeros((len(trajectories), len(trajectories)))
        for r in range(len(trajectories)):
            for c in range(len(trajectories)):
                k[r, c] = self.similarity(r, c)

        return k

    @staticmethod
    def _estimate_cluster_number(evec, g_max, g_min):
        """
        Determines the optimal number of cluster using the eigenvectors
        :param evec: Eigenvectors
        :param g_max: max number of clusters
        :param g_min: min number of cluster
        :return:
        """
        rhog = np.zeros(g_max - g_min + 1)
        for g in range(g_min, g_max + 1):
            v = np.copy(evec[:, 0:g])
            s = np.diag(1.0 / np.sqrt(np.sum(np.multiply(v, v), 1)))
            r = np.dot(s, v)

            # k-means clustering of the row vectors of r
            cb, wc_scatt = kmeans(r, g, iter=20, thresh=1e-05)  # cb = codebook (centroids = rows of cb)

            # compute distortion score rho_g (within class scatter /  sum(within class scatter, total scatter))
            tot_scatt = np.sum([np.linalg.norm(r - c) for r in r for c in cb])
            rhog[g - g_min] = wc_scatt / (tot_scatt - wc_scatt) if (tot_scatt - wc_scatt) else 0

        # Best number of centroids.
        g = g_min + np.argmin(rhog)
        return g

    def _kmean_cluster(self, trajectories, g, evec):
        """
        Performs classification of trajectories using k-means clustering
        :param trajectories:
        :param g:
        :param evec:
        :return:
        """
        v = np.copy(evec[:, 0:g])
        s = np.diag(1.0 / np.sqrt(np.sum(np.multiply(v, v), 1)))
        r = np.dot(s, v)
        # Find g initial centroids (rows)
        init_centroids = np.zeros((g, r.shape[1]))
        # Matrix of distance of each observation (rows) to each initial centroid (columns)
        init_centroids_dist = np.zeros((r.shape[0], g))
        init_centroids[0] = r[random.randint(0, r.shape[0] - 1)]

        for i in range(g - 1):
            # get each observation's distance to the new centroid
            init_centroids_dist[:, i] = [self.distance(obs, init_centroids[i]) for obs in r]
            # get the observation which has the worst minimal distance to some already existing centroid
            newidx = np.argmax(np.min(init_centroids_dist[:, :(i + 1)], 1))
            init_centroids[i + 1] = r[newidx]

        centroids, labels = kmeans2(r, init_centroids, iter=10, thresh=1e-05, minit='matrix', missing='warn')
        assert (len(trajectories) == len(labels))

        for trajLab in zip(trajectories, labels):
            trajLab[0].set_cluster_idx(trajLab[1])
