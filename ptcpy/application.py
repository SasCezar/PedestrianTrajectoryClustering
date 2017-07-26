from Tkinter import *
from os import path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from scipy.stats.kde import gaussian_kde

from ptcio.positionsio import trajectories_read, position_read, trajectories2file
from trajectory_clustering.clustering import Clustering

COLORS = ["#FF0000",  # red
          "#00FF00",  # lime
          "#0000FF",  # blue
          "#FF00FF",  # fuchsia
          # "#808080",  # gray
          "#000000",  # black
          "#00FFFF",  # aqua
          "#008000",  # green
          "#008080",  # teal
          "#000080",  # navy
          "#800080",  # purple
          "#C0C0C0"]  # silver


def draw_tk(trajectories, canvas_width, canvas_height):
    master = Tk()
    master.title("Trajectory clustering")
    w = Canvas(master, width=canvas_width, height=canvas_height)
    for t in trajectories:
        t.draw_plot(w, COLORS[t.get_cluster_idx()], y_offset=250)
    w.pack()
    w.focus_set()


def draw_png(trajectories, out_path, canvas_width, canvas_height, scaling, frequency):
    im = Image.new("RGB", (canvas_width * scaling, canvas_height * scaling), "white")
    draw = ImageDraw.Draw(im)
    for t in trajectories:
        t.draw_img(draw, COLORS[t.get_cluster_idx()], y_offset=250, scaling=scaling, frequency=frequency)
    im.save(out_path)


def list_points(trajectories):
    x = []
    y = []
    for t in trajectories:
        points = t.get_points()
        for point in points:
            x += [point[0]]
            y += [point[1]]

    return x, y


def heat_map(trajectories, out_path):
    x, y = list_points(trajectories)
    k = gaussian_kde(np.vstack([x, y]))
    xi, yi = np.mgrid[min(x):max(x):len(x) ** 0.5 * 1j, min(y):max(y):len(y) ** 0.5 * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # alpha=0.5 will make the plots semitransparent
    ax1.pcolormesh(xi, yi, zi.reshape(xi.shape))

    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(min(y), max(y))

    fig.show()


if __name__ == "__main__":
    DATA_PATH = "c:/Users/sasce/Desktop/dataset"
    OUT_PATH = "c:/Users/sasce/Desktop/dataset/traclus"
    file_name = '3_3_A.csv'

    trajectories = trajectories_read(path.join(DATA_PATH, file_name)).values()

    clust = Clustering(alpha=0.95)
    clust.cluster_spectral(trajectories)

    canvas_width = 500
    canvas_height = 500

    draw_tk(trajectories, canvas_width, canvas_height)

    # out_img = path.join(OUT_PATH, ["img", str(file_name).replace("csv", "png")])
    out_img = file_name.replace("csv", "png")
    draw_png(trajectories, out_img, canvas_width, canvas_height, scaling=3, frequency=10)

    heat_map(trajectories, out_path="")

    trajectories_dict = {}
    for t in trajectories:
        trajectories_dict[t.get_id()] = t.get_cluster_idx()

    positions = position_read(path.join(DATA_PATH, file_name))
    trajectories2file(positions, trajectories_dict, path.join(OUT_PATH, file_name))

    mainloop()
