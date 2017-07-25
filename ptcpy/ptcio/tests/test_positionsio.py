import unittest
from os import path

from ptcpy.ptcio.positionsio import position_read, trajectories_read

DATA_PATH = path.join(path.dirname(__file__), 'data')


class TestPositionsIO(unittest.TestCase):
    reference_dict = {
        0.0: [(1, 1, -499.47, 125.64, -1.0)],
        0.033367: [(1, 1, -493.92, 125.11, -1.0)],
        0.066733: [(1, 1, -483.66, -90.325, -1.0),
                   (3, 2, -496.05, 17.25, -1.0)],
        0.1001: [(1, 1, -478.53, -90.325, -1.0),
                 (3, 2, -499.05, 18.25, -1.0)
                 ]
    }

    reference_trajectories = [[(-499.47, 125.64), (-493.92, 125.11), (-483.66, -90.325), (-478.53, -90.325)],
                              [(None, None), (None, None), (None, None), (None, None)],
                              [(None, None), (None, None), (-496.05, 17.25), (-499.05, 18.25)]
                              ]

    def test_read(self):
        self.dict_read = position_read(path.join(DATA_PATH, 'test_positions.csv'))

        self.assertDictEqual(self.dict_read, self.reference_dict)

    def trajectories_read(self):
        self.trajectories_read = trajectories_read(path.join(DATA_PATH, 'test_positions.csv'))

        self.assertListEqual(self.reference_trajectories, self.trajectories_read)


if __name__ == "__main__":
    unittest.main()
