"""
Created on 24. 4. 2015

@author: janbednarik
"""

from trajectory_clustering.common import euclid_dist


class Trajectory(object):
    """A class implementing one trajectory"""

    def __init__(self, id, direction=None, distance=euclid_dist):
        self.id = id
        self.points = []
        self.ci = -1
        self.distance = distance
        self.direction = direction
        self.prefix_sum = [0.0]

    def add_point(self, p):
        # compute prefix sum
        if len(self.points) > 0:
            self.prefix_sum.append(self.prefix_sum[len(self.prefix_sum) - 1] +
                                   self.distance(p, self.points[len(self.points) - 1]))

        self.points.append(p)

    def get_id(self):
        return self.id

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

    def draw_plot(self, widget, color, x_offset=0, y_offset=0):
        x_last, y_last = None, None
        for p in self.points:
            # paint a point
            x = p[0] + x_offset
            y = p[1] + y_offset
            widget.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color)

            # paint a line
            if x_last is not None and y_last is not None:
                widget.create_line(x_last, y_last, x, y, smooth=True)
            x_last = x
            y_last = y

    def draw_img(self, img, color, x_offset=0, y_offset=0, scaling=1, frequency=1):
        x_last, y_last = None, None
        i = 1
        for p in self.points:
            # paint a point
            x = (p[0] + x_offset) * scaling
            y = (p[1] + y_offset) * scaling

            i += 1
            if not i % frequency:
                img.polygon([(x + (3 * self.direction), y), (x - (3 * self.direction), y - 3),
                             (x - (3 * self.direction), y + 3)], fill=color)
                i += 1
            # img.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color)

            # paint a line
            if x_last is not None and y_last is not None:
                img.line([(x_last, y_last), (x, y)], fill=color)
            x_last = x
            y_last = y

    def __str__(self):
        out = "=== Trajectory ===\n"
        out += "cluster: %d\n" % self.ci
        for p in self.points:
            out += repr(p) + ", "
        out += "\n"
        return out

    def __len__(self):
        return len(self.points)
