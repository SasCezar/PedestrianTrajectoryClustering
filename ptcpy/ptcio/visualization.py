import glob
import os
import subprocess
from os import path

import matplotlib
import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

from ptcpy.ptcio.positionsio import GorriniFile, ZhangFile

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


def draw_trajectories(trajectories, canvas_width, canvas_height, scaling, frequency, y_offset=250):
    im = Image.new("RGB", (canvas_width * scaling, canvas_height * scaling), "white")
    draw = ImageDraw.Draw(im)
    for t in trajectories:
        t.draw_img(draw, COLORS[t.get_cluster_idx()], y_offset=y_offset, x_offset=600, scaling=scaling,
                   frequency=frequency)

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
    return plt


def pedestrian_plot(positions, out_path):
    matplotlib.use('Agg')
    i = 0

    xs = []
    ys = []
    for time, pedestrians in positions.items():
        for pedestrian in pedestrians:
            xs += [pedestrian[2]]
            ys += [pedestrian[3]]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.set_xlim(min(xs), max(xs))
    ax1.set_ylim(min(ys), max(ys))

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

        plt.savefig(path.join(out_path, "frame_%05d.png" % int(i)))
        plt.clf()


def create_video(in_path, out_file, framerate):
    os.chdir(in_path)
    subprocess.call(['ffmpeg', "-y", '-framerate', str(framerate), '-i', 'frame_%05d.png',
                     '-r', str(framerate), '-pix_fmt', 'yuv420p', str(out_file)])

    for file_name in glob.glob(path.join(in_path, "*.png")):
        os.remove(file_name)


def video_zhang(IMAGES):
    DATA_PATH = "c:/Users/sasce/Desktop/dataset/zheng"

    file_name = "bot-360-250-250_combined_MB.txt"

    VIDEO_OUT = file_name[:-4] + ".mp4"
    positions = ZhangFile(16).read(path.join(DATA_PATH, file_name))

    pedestrian_plot(positions, IMAGES)

    create_video(IMAGES, VIDEO_OUT, 16)


def create_labeled_videos():
    IMAGES = "c:/Users/sasce/Desktop/dataset/video"
    # video_gorrini(IMAGES)
    video_zhang(IMAGES)


def video_gorrini(IMAGES):
    DATA_PATH = "c:/Users/sasce/Desktop/dataset"
    for x in range(4, 7):
        for l in ["A", "B", "C", "D"]:
            c = 6 - x
            file_name = str(x) + '_' + str(c) + '_' + str(l) + '.csv'

            VIDEO_OUT = file_name[:-4] + ".mp4"
            positions = GorriniFile(29.97).read(path.join(DATA_PATH, file_name))

            pedestrian_plot(positions, IMAGES)

            create_video(IMAGES, VIDEO_OUT, 29.97)

# create_labeled_videos()
