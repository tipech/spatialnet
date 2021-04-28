import unittest
from spatialnet.common import Trajectory

from functional import seq
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString


class TestTrajectory(unittest.TestCase):

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

    def test_dict(self):
        self.assertEqual(Trajectory('ped1', self.dict_tuple1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.dict_shape1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.dict_tuple2), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.dict_shape2), self.trajectory1)
        self.assertNotEqual(Trajectory('ped2', self.dict_tuple1), self.trajectory1)

    def test_numpy(self):
        self.assertEqual(Trajectory('ped1', self.np_tuple1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.np_tuple2), self.trajectory1)
        self.assertNotEqual(Trajectory('ped2', self.np_tuple1), self.trajectory1)

    def test_df(self):
        self.assertEqual(Trajectory('ped1', self.df_tuple), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.df_shape1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.df_shape2), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.gdf), self.trajectory1)
        self.assertNotEqual(Trajectory('ped2', self.df_tuple), self.trajectory1)
        self.assertNotEqual(Trajectory('ped2', self.gdf), self.trajectory1)

    def test_list(self):
        self.assertEqual(Trajectory('ped1', self.list_tuple1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.list_shape1), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.list_tuple2), self.trajectory1)
        self.assertEqual(Trajectory('ped1', self.list_shape2), self.trajectory1)
        self.assertNotEqual(Trajectory('ped2', self.list_tuple1), self.trajectory1)

        self.assertEqual(Trajectory('ped1', seq(self.list_tuple1)), self.trajectory1)
        self.assertEqual(Trajectory('ped1', seq(self.list_shape1)), self.trajectory1)
        self.assertEqual(Trajectory('ped1', seq(self.list_tuple2)), self.trajectory1)
        self.assertEqual(Trajectory('ped1', seq(self.list_shape2)), self.trajectory1)

    def test_json(self):
        json_trajectory = self.trajectory1.to_json()
        self.assertEqual(Trajectory.from_json(json_trajectory), self.trajectory1)

    def test_sequence(self):
        test_seq = seq([self.trajectory1, self.trajectory2])
        self.assertEqual(test_seq, test_seq.map(lambda x:x.to_dict()).map(Trajectory.from_dict))

    def test_linestring(self):
        self.assertEqual(Trajectory('ped1', self.linestr), self.trajectory1)
        self.assertEqual(self.trajectory1.get_linestring(), self.linestr[1])


if __name__ == '__main__':
    unittest.main()
