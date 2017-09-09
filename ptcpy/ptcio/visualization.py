import glob
import os
import subprocess
from os import path

import matplotlib
import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

from ptcpy.ptcio.positionsio import position_read

COLORS = ["#FF0000",  # red
          "#00FF00",  # lime
          "#0000FF",  # blue
          "#FF00FF",  # fuchsia
          "#000000",  # black
          "#00FFFF",  # aqua
          "#008000",  # green
          "#008080",  # teal
          "#000080",  # navy
          "#800080",  # purple
          "#C0C0C0"]  # silver


def draw_trajectories(trajectories, canvas_width, canvas_height, scaling, frequency):
    im = Image.new("RGB", (canvas_width * scaling, canvas_height * scaling), "white")
    draw = ImageDraw.Draw(im)
    for t in trajectories:
        t.draw_img(draw, COLORS[t.get_cluster_idx()], y_offset=250, scaling=scaling, frequency=frequency)

    return im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)


def list_points(trajectories):
    x = []
    y = []
    for t in trajectories:
        points = t.get_points()
        for point in points:
            x += [point[0]]
            y += [point[1]]

    return x, y


def heat_map(trajectories):
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
    plt.show()
    plt.clf()
    plt.close()


def pedestrian_plot(positions, out_path):
    matplotlib.use('Agg')
    i = 0
    for time in sorted(positions.keys()):
        i += 1
        print(time)
        xs = []
        ys = []
        labels = []
        for pedestrian in positions[time]:
            xs += [pedestrian[2]]
            ys += [pedestrian[3]]
            labels += [pedestrian[0]]

        plt.scatter(xs, ys)

        for label, x, y in zip(labels, xs, ys):
            plt.annotate(
                label,
                xy=(x, y), xytext=(0, 0),
                textcoords='offset points', ha='center', va='center',
                bbox=dict(boxstyle='circle,pad=0.5', fc='yellow', alpha=1))

        plt.xlim(-500, 500)
        plt.ylim(-200, 200)
        plt.savefig(path.join(out_path, "frame_%05d.png" % int(i)))
        plt.clf()


def create_video(in_path, out_file, framerate):
    os.chdir(in_path)
    subprocess.call(['ffmpeg', "-y", '-framerate', str(framerate), '-i', 'frame_%05d.png',
                     '-r', str(framerate), '-pix_fmt', 'yuv420p', str(out_file)])

    for file_name in glob.glob(path.join(in_path, "*.png")):
        os.remove(file_name)


def create_labeled_videos():
    DATA_PATH = "c:/Users/sasce/Desktop/dataset"
    IMAGES = "c:/Users/sasce/Desktop/dataset/video"

    for x in range(4, 7):
        for l in ["A", "B", "C", "D"]:
            c = 6 - x
            file_name = str(x) + '_' + str(c) + '_' + str(l) + '.csv'

            VIDEO_OUT = file_name[:-4] + ".mp4"
            positions = position_read(path.join(DATA_PATH, file_name), 29.97)

            pedestrian_plot(positions, IMAGES)

            create_video(IMAGES, VIDEO_OUT, 29.97)

# create_labeled_videos()
