import io
from Tkinter import *
from os import path

from PIL import Image

from ptcpy.ptcio.positionsio import trajectories_read, position_read, trajectories2file
from ptcpy.trajectory_clustering.clustering import Clustering

COLORS = ["#FF0000",  # red
          "#00FF00",  # lime
          "#0000FF",  # blue
          "#FFFF00",  # yellow
          "#FF00FF",  # fuchsia
          "#800000",  # maroon
          "#808000",  # olive
          "#00FFFF",  # aqua
          "#008000",  # green
          "#008080",  # teal
          "#000080",  # navy
          "#800080",  # purple
          "#808080",  # gray
          "#C0C0C0",  # silver
          "#FFFFFF"]  # white



if __name__ == "__main__":
    # DATA_PATH = "C:\\Users\\sasce\\PycharmProjects\\PedestrianTrajectoryClustering\\ptcpy\\ptcio\\tests\\data\\"
    DATA_PATH = "C:\\Users\\sasce\\Desktop\\dataset"
    file = '3_3_A.csv'
    positions = position_read(path.join(DATA_PATH, file))
    trajectories = trajectories_read(path.join(DATA_PATH, file)).values()
    OUT_PATH = "C:\\Users\\sasce\\Desktop\\dataset\\traclus"
    # postions2traclus(path.join(DATA_PATH, file), path.join(OUT_PATH, file))

    clust = Clustering()
    clust.cluster_spectral(trajectories)

    canvas_width = 500
    canvas_height = 500

    master = Tk()
    master.title("Trajectory clustering")
    w = Canvas(master, width=canvas_width, height=canvas_height)
    w.pack(expand=YES, fill=BOTH)
    w.focus_set()

    for t in trajectories:
        t.draw(w, COLORS[t.get_cluster_idx()], y_offset=250)

    trajectories_dict = {}
    for t in trajectories:
        trajectories_dict[t.get_id()] = t.get_cluster_idx()

    ps = w.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save('test.jpg')

    trajectories2file(positions, trajectories_dict, path.join(OUT_PATH, file))

    mainloop()
