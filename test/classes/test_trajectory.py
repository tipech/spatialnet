import unittest

from functional import seq
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

from spatialnet import Trajectory, read_trajectory


# test inputs
dict_tuple1 = {'time': [0, 1], 'geometry': [(1, 2), (2, 1)]}
dict_shape1 = {'time': [0, 1], 'geometry': [Point(1, 2), Point(2, 1)]}
dict_tuple2 = {0: (1, 2), 1: (2, 1)}
dict_shape2 = {0: Point(1, 2), 1: Point(2, 1)}

list_tuple1 = [[0, 1], [(1, 2), (2, 1)]]
list_tuple2 = [[0, (1, 2)], [1, (2, 1)]]
list_shape1 = [[0, 1], [Point(1, 2), Point(2, 1)]]
list_shape2 = [[0, Point(1, 2)], [1, Point(2, 1)]]

np_tuple1 = np.array([[0, 1], [(1, 2), (2, 1)]])
np_tuple2 = np.array([[0, (1, 2)], [1, (2, 1)]])

df_tuple = pd.DataFrame({'time': [0, 1], 'geometry': [(1, 2), (2, 1)]})
df_shape1 = pd.DataFrame({'time': [0, 1], 'geometry': [Point(1, 2), Point(2, 1)]})
df_shape2 = pd.DataFrame({'geometry': [Point(1, 2), Point(2, 1)], 'time': [0, 1]})
gdf = gpd.GeoDataFrame({'time': [0, 1], 'geometry': [Point(1, 2), Point(2, 1)]})

linestr = ([0, 1], LineString([(1, 2), (2, 1)]))

# true internal representation
trajectory1 = Trajectory('ped1', {0: [1.0, 2.0], 1: [2.0, 1.0]})
trajectory2 = Trajectory('ped2', {0: [1.0, 2.0], 1: [2.0, 1.0]})


class TestTrajectory(unittest.TestCase):

    def test_dict(self):
        self.assertEqual(Trajectory('ped1', dict_tuple1), trajectory1)
        self.assertEqual(Trajectory('ped1', dict_shape1), trajectory1)
        self.assertEqual(Trajectory('ped1', dict_tuple2), trajectory1)
        self.assertEqual(Trajectory('ped1', dict_shape2), trajectory1)
        self.assertNotEqual(Trajectory('ped2', dict_tuple1), trajectory1)

    def test_numpy(self):
        self.assertEqual(Trajectory('ped1', np_tuple1), trajectory1)
        self.assertEqual(Trajectory('ped1', np_tuple2), trajectory1)
        self.assertNotEqual(Trajectory('ped2', np_tuple1), trajectory1)

    def test_df(self):
        self.assertEqual(Trajectory('ped1', df_tuple), trajectory1)
        self.assertEqual(Trajectory('ped1', df_shape1), trajectory1)
        self.assertEqual(Trajectory('ped1', df_shape2), trajectory1)
        self.assertEqual(Trajectory('ped1', gdf), trajectory1)
        self.assertNotEqual(Trajectory('ped2', df_tuple), trajectory1)
        self.assertNotEqual(Trajectory('ped2', gdf), trajectory1)

    def test_list(self):
        self.assertEqual(Trajectory('ped1', list_tuple1), trajectory1)
        self.assertEqual(Trajectory('ped1', list_shape1), trajectory1)
        self.assertEqual(Trajectory('ped1', list_tuple2), trajectory1)
        self.assertEqual(Trajectory('ped1', list_shape2), trajectory1)
        self.assertNotEqual(Trajectory('ped2', list_tuple1), trajectory1)

        self.assertEqual(Trajectory('ped1', seq(list_tuple1)), trajectory1)
        self.assertEqual(Trajectory('ped1', seq(list_shape1)), trajectory1)
        self.assertEqual(Trajectory('ped1', seq(list_tuple2)), trajectory1)
        self.assertEqual(Trajectory('ped1', seq(list_shape2)), trajectory1)

    def test_json(self):
        json_trajectory = trajectory1.to_json()
        self.assertEqual(Trajectory.from_json(json_trajectory), trajectory1)
        self.assertEqual(read_trajectory(json_trajectory), trajectory1)

    def test_sequence(self):
        test_seq = seq([trajectory1, trajectory2])
        self.assertEqual(test_seq, test_seq.map(lambda x:x.to_dict()).map(Trajectory.from_dict))

    def test_linestring(self):
        self.assertEqual(Trajectory('ped1', linestr), trajectory1)
        self.assertEqual(trajectory1.get_geometry(), linestr[1])


if __name__ == '__main__':
    unittest.main()
