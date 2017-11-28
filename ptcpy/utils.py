import csv
import os


def write_trajectories(file):
    users = {}
    with open(file, "rt") as inf:
        reader = csv.reader(inf, delimiter=' ')
        for pid, frame, y, x, z in reader:
            users.setdefault(pid, []).append((pid, frame, x, y, z))

    result = {}
    for user in users:
        first_x = users[user][0][2]
        last_x = users[user][-1][2]

        group = 1 if last_x > first_x else -1

        for sample in users[user]:
            pid, frame, x, y, z = sample
            result.setdefault(user, []).append((pid, frame, group, x, y, z))

    basepath, filename = os.path.split(file)

    dest = os.path.join(basepath, "grouped", filename)

    with open(dest, "wb") as outf:
        writer = csv.writer(outf, delimiter=" ")

        for user in sorted(result.keys()):
            for sample in result[user]:
                writer.writerow(sample)


def zheng_direction(dest_path):
    files = [os.path.join(dest_path, f) for f in os.listdir(dest_path) if not os.path.isdir(os.path.join(dest_path, f))]

    for file in files:
        write_trajectories(file)


if __name__ == "__main__":
    ZHENG_DATA_PATH = "c:/Users/sasce/Desktop/dataset/zheng"
    zheng_direction(ZHENG_DATA_PATH)
