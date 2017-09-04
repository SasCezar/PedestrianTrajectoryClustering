import csv
import os
from abc import abstractmethod
from itertools import chain

import numpy
from six import string_types

from ptcpy.trajectory_clustering.trajectory import Trajectory


def position_read(source, frequency=29.97):
    result = PositionsFile(frequency).read(source)
    return result


def _get_pedestrian_number(positions):
    pedestrian_id = [item[0] for sublist in positions.values() for item in sublist]
    return max(pedestrian_id)


def _get_pedestrian_ids(positions):
    pedestrian_id = [item[0] for sublist in positions.values() for item in sublist]
    ids = list(set(pedestrian_id))
    return sorted(ids)


def positions2matrix(source, frequency=29.97, axis=1):
    positions = position_read(source, frequency)
    num_sample = len(positions)
    num_pedestrian = _get_pedestrian_number(positions)

    points = numpy.zeros(shape=(num_sample, num_pedestrian))

    for time in positions:
        int_time = int(time * frequency)
        for position in positions[time]:
            pedestrian_id = position[0] - 1
            point = position[axis + 2]
            points[int_time][pedestrian_id] = point

    return points


def positions2trajectories(positions):
    trajectories = {}
    for i, time in enumerate(sorted(positions.keys())):
        for pedestrian in positions[time]:
            pedestrian_id = pedestrian[0]
            x_pos = pedestrian[2]
            y_pos = pedestrian[3]
            direction = 1 if pedestrian[1] in [3, 4] else -1
            group_member = 1 if pedestrian[1] in [2, 4] else 0
            trajectories.setdefault(pedestrian_id, Trajectory(pedestrian_id, direction=direction,
                                                              group_member=group_member)).add_point((x_pos, y_pos))

    return trajectories


def postions2traclus(source, destination, frequency=29.97):
    positions = position_read(source, frequency)
    trajectories = positions2trajectories(positions).values()
    num_traj = len(trajectories)

    # with open(destination, "w", encoding="utf8", newline="") as outf:
    with open(destination, "w") as outf:
        outf.write("2")
        outf.write(os.linesep)
        outf.write(str(num_traj))
        outf.write(os.linesep)

        for traj in trajectories:
            positions = [x + 500 for x in list(chain.from_iterable(traj.get_points()))]
            line = str(traj.get_id()) + " " + str(int((len(positions) / 2)) - 1) + " " + " ".join(
                map(str, positions)) + " "
            outf.write(line)
            outf.write(os.linesep)


def trajectories_read(source, frequency=29.97):
    positions = position_read(source, frequency)
    trajectory_matrix = positions2trajectories(positions)
    return trajectory_matrix


def trajectories2file(samples, trajectories, destination):
    with open(destination, "wb") as outf:
        csvwriter = csv.writer(outf)
        for time in sorted(samples.keys()):
            for position in samples[time]:
                clustered_position = [time] + list(position) + [trajectories[position[0]]]
                csvwriter.writerow(clustered_position)


class File(object):
    @staticmethod
    def _open(filespec, mode='rt'):
        """
        :param filespec: str or file_name-like
            String giving file_name name or file_name-like object
        :param mode:  str, optional
            Mode with which to open file_name, if `filespec` is a file_name name.
        :return:
            fobj : file_name-like
                Open file_name-like object.
            close_it : bool
                True if the calling function should close this file_name when done, false otherwise.
        """

        close_it = False
        if isinstance(filespec, string_types):
            close_it = True
            # open for reading
            if mode[0] == 'r':
                stream = open(filespec, mode)
            # open for writing
            else:
                stream = open(filespec, mode)
        else:
            stream = filespec

        return stream, close_it

    @abstractmethod
    def _read(self, stream):
        """
        Defines how to read the file_name
        :param stream:
        :return:
        """
        pass

    def read(self, source):
        """
        Reads the content of a positions file_name
        :param source: str or file_name-like object containing the positions
        :return: A dictionary or a matrix, based on the `mode` parameter
        """
        stream, close_it = self._open(source)

        try:
            result = self._read(stream)
            return result
        finally:
            if close_it:
                stream.close()

    def write(self, target, a):
        """

        :param target:
        :param a:
        :return:
        """
        stream, close_it = self._open(target, 'wb')

        try:
            self._write(stream, a)

        finally:
            if close_it:
                stream.close()
            else:
                stream.flush()

    @abstractmethod
    def _write(self, stream, a):
        pass


class PositionsFile(File):
    def __init__(self, frequency=29.97, delimiter=','):
        self.FREQUENCY = frequency
        self.DELIMITER = delimiter

    def _read(self, source):
        """
        Reads the input source and generates a dictionary containing the measures grouped by time (dictionary key)
        :param source:  str or file_name-like object containing the positions
        :return: A dictionary
        """
        stream, close_it = self._open(source)
        reader = csv.reader(stream, delimiter=self.DELIMITER)
        result = {}

        try:
            next(reader)
            for ped_num, ped_type, time, x, y, density in reader:
                pedestrian = (int(ped_num), int(ped_type), float(x), float(y), float(density))
                result.setdefault(float(time), []).append(pedestrian)

            return result

        finally:
            if close_it:
                stream.close()

    def _write(self, stream, points):
        pass
