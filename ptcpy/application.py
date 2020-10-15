import logging
import os
from os import path

import pandas

from ptcio.positionsio import gorrini_read, zhang_read
from ptcpy.evaluation.performance_measures import get_performance_measures, rand_score_measure
from ptcpy.ptcio.visualization import draw_trajectories, heat_map
from trajectory_clustering.clustering import Clustering

canvas_width = 2500
canvas_height = 3500
FREQ = 5

DATA_PATH = "../dataset"
ZHENG_DATA_PATH = "../dataset/zheng/grouped"
GT_PATH = "../dataset/ground_truth"
PERFORMANCE_PATH = "../results/performance"
CLUSTERS_PATH = "../results/clusters"
file_name = ""
tkv = False
png = True
heatmap = False

RESULT_OUT = "../results/trajectories"
HEAT_OUT = "../results/heat_map"


def visualize(file_name, trajectories):
    out_img = file_name.replace("csv", "png") if "csv" in file_name else file_name.replace("txt", "png")
    if png:
        im = draw_trajectories(trajectories, canvas_width, canvas_height, scaling=3, frequency=FREQ)
        im.save(path.join(RESULT_OUT, out_img))
    if heatmap:
        hmap = heat_map(trajectories)
        hmap.savefig(path.join(HEAT_OUT, out_img.replace))


def gorrini():
    for x in range(3, 5):
        for l in ["A", "B", "C", "D"]:
            c = 6 - x
            global file_name
            file_name = str(x) + '_' + str(c) + '_' + str(l) + '.csv'

            trajectories = list(gorrini_read(path.join(DATA_PATH, file_name)).values())

            analyze(file_name, trajectories)


def zhang():
    experiments = [f for f in os.listdir(ZHENG_DATA_PATH) if not os.path.isdir(f)]
    for experiment in experiments:
        logging.info("Working on: {}".format(experiment))
        trajectories = list(zhang_read(path.join(ZHENG_DATA_PATH, experiment)).values())

        analyze(experiment, trajectories)


def write_results(file, clusters):
    with open(path.join(CLUSTERS_PATH, file), "wt") as fout:
        fout.write("pedestrian, cluster\n")
        for pedestrian in clusters:
            fout.write("{}, {}\n".format(pedestrian, clusters[pedestrian]))


def analyze(file_name, trajectories):
    scores = {}
    clust = Clustering(alpha=0.95)
    clust.cluster_spectral(trajectories)
    visualize(file_name, trajectories)
    trajectories_dict = {}
    for t in trajectories:
        trajectories_dict[t.get_id()] = t.get_cluster_idx()

    write_results(file_name, trajectories_dict)

    ground_truth = dict(pandas.read_table(path.join(GT_PATH, file_name), sep=",").values)
    precision, recall, f1, support = get_performance_measures(trajectories_dict, ground_truth)
    rand_score = rand_score_measure(trajectories_dict, ground_truth)
    scores["rand_score"] = rand_score
    scores["precision"] = precision
    scores["recall"] = recall
    write_scores(file_name, scores)


def write_scores(file_name, scores):
    with open(path.join(PERFORMANCE_PATH, file_name), "wt") as fout:
        for k in scores:
            fout.write("{} : {}\r\n".format(k, scores[k]))


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    gorrini()
    # zhang()
