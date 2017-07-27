import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde

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

    return im


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
