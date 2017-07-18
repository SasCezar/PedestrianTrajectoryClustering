"""
Created on 24. 4. 2015

@author: janbednarik
"""

from ptcpy.trajectory_clustering.common import euclid_dist


class Trajectory(object):
    """A class implementing one trajectory"""

    def __init__(self, id):
        self.id = id
        self.points = []
        self.ci = -1
        self.prefix_sum = [0.0]

    def add_point(self, p):
        # compute prefix sum
        if len(self.points) > 0:
            self.prefix_sum.append(self.prefix_sum[len(self.prefix_sum) - 1] +
                                   euclid_dist(p, self.points[len(self.points) - 1]))

        # add point
        self.points.append(p)

    def get_points(self):
        return self.points

    def get_prefix_sum(self):
        return self.prefix_sum

    def get_cluster_idx(self):
        return self.ci

    def set_cluster_idx(self, ci):
        self.ci = ci

    def length(self):
        return self.prefix_sum[len(self.prefix_sum) - 1]

    def draw(self, widget, color):
        xlast, ylast = None, None
        for p in self.points:
            # paint a point
            widget.create_oval(p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2, fill=color)

            # paint a line
            if xlast is not None and ylast is not None:
                widget.create_line(xlast, ylast, p[0], p[1], smooth=True)
            xlast = p[0]
            ylast = p[1]

    def __str__(self):
        str = "=== Trajectory ===\n"
        str += "cluster: %d\n" % self.ci
        for p in self.points:
            str += repr(p) + ", "
        str += "\n"
        return str

    def __len__(self):
        return len(self.points)
