from os import path

import pandas

from ptcio.positionsio import trajectories_read, position_read, trajectories2file
from ptcpy.evaluation.performance_measures import rand_score_measure
from ptcpy.ptcio.visualization import draw_trajectories, heat_map
from trajectory_clustering.clustering import Clustering

canvas_width = 500
canvas_height = 500

DATA_PATH = "c:/Users/sasce/Desktop/dataset"
GT_PATH = "c:/Users/sasce/Desktop/dataset/ground_truth"
OUT_PATH = "c:/Users/sasce/Desktop/dataset/traclus"
PERFORMANCE_PATH = "../results/performance"
file_name = ""
tkv = False
png = True
heatmap = False

RESULT_OUT = "../results/trajectories"


def visualize():
    if png:
        out_img = file_name.replace("csv", "png")
        im = draw_trajectories(trajectories, canvas_width, canvas_height, scaling=3, frequency=10)
        im.save(path.join(RESULT_OUT, out_img))
    if heatmap:
        heat_map(trajectories)


if __name__ == "__main__":

    for x in range(3, 5):
        for l in ["A", "B", "C", "D"]:

            scores = {}

            c = 6 - x
            file_name = str(x) + '_' + str(c) + '_' + str(l) + '.csv'

            # ------------------------------------------------------

            trajectories = trajectories_read(path.join(DATA_PATH, file_name)).values()

            clust = Clustering(alpha=0.95)
            clust.cluster_spectral(trajectories)

            visualize()

            trajectories_dict = {}
            for t in trajectories:
                trajectories_dict[t.get_id()] = t.get_cluster_idx()

            positions = position_read(path.join(DATA_PATH, file_name))
            trajectories2file(positions, trajectories_dict, path.join(OUT_PATH, file_name))

            ground_truth = dict(pandas.read_table(path.join(GT_PATH, file_name), sep=",").values)

            # intersection_matrix = get_confusion_matrix(trajectories_dict, ground_truth)

            rand_score = rand_score_measure(trajectories_dict, ground_truth)
            scores["rand_score"] = rand_score

            print(file_name + " " + str(rand_score))

            with open(path.join(PERFORMANCE_PATH, file_name), "w") as fout:
                for k in scores:
                    fout.write("{} : {}".format(k, scores[k]))

            """
            POINTS_OUT = "c:/Users/sasce/Desktop/dataset/points"
            points = positions2matrix(path.join(DATA_PATH, file_name))
            numpy.savetxt(path.join(POINTS_OUT, "Y_POINTS_" + file_name), points, fmt="%s")
            """
