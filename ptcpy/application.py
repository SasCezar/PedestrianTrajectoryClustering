from os import path

import numpy

from ptcio.positionsio import trajectories_read, position_read, trajectories2file, positions2matrix
from ptcpy.ptcio.visualization import draw_trajectories, heat_map
from trajectory_clustering.clustering import Clustering

canvas_width = 500
canvas_height = 500

DATA_PATH = "c:/Users/sasce/Desktop/dataset"
OUT_PATH = "c:/Users/sasce/Desktop/dataset/traclus"
file_name = '3_3_A.csv'
tkv = False
png = True
heatmap = True

RESULT_OUT = "../results/trajectories"


def visualize():
    if png:
        out_img = file_name.replace("csv", "png")
        im = draw_trajectories(trajectories, canvas_width, canvas_height, scaling=3, frequency=10)
        im.save(path.join(RESULT_OUT, out_img))
    if heatmap:
        heat_map(trajectories)


if __name__ == "__main__":

    trajectories = trajectories_read(path.join(DATA_PATH, file_name)).values()

    clust = Clustering(alpha=0.95)
    clust.cluster_spectral(trajectories)

    visualize()

    trajectories_dict = {}
    for t in trajectories:
        trajectories_dict[t.get_id()] = t.get_cluster_idx()

    positions = position_read(path.join(DATA_PATH, file_name))
    trajectories2file(positions, trajectories_dict, path.join(OUT_PATH, file_name))

    POINTS_OUT = "c:/Users/sasce/Desktop/dataset/points"
    points = positions2matrix(path.join(DATA_PATH, file_name))
    numpy.savetxt(path.join(POINTS_OUT, "Y_POINTS_" + file_name), points, fmt="%s")
