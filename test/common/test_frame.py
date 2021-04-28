import unittest
from spatialnet.common import Frame

from functional import seq
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


class TestFrame(unittest.TestCase):

    # test inputs
    dict_tuple1 = {'pedID': ['ped1', 'ped2'], 'geometry': [(1, 2), (2, 1)]}
    dict_shape1 = {'pedID': ['ped1', 'ped2'], 'geometry': [Point(1, 2), Point(2, 1)]}
    dict_tuple2 = {'ped1': (1, 2), 'ped2': (2, 1)}
    dict_shape2 = {'ped1': Point(1, 2), 'ped2': Point(2, 1)}

    list_tuple1 = [['ped1', 'ped2'], [(1, 2), (2, 1)]]
    list_tuple2 = [['ped1', (1, 2)], ['ped2', (2, 1)]]
    list_shape1 = [['ped1', 'ped2'], [Point(1, 2), Point(2, 1)]]
    list_shape2 = [['ped1', Point(1, 2)], ['ped2', Point(2, 1)]]

    np_tuple1 = np.array([['ped1', 'ped2'], [(1, 2), (2, 1)]])
    np_tuple2 = np.array([['ped1', (1, 2)], ['ped2', (2, 1)]])

    df_tuple = pd.DataFrame({'pID': ['ped1', 'ped2'], 'geometry': [(1, 2), (2, 1)]})
    df_shape1 = pd.DataFrame({'pID': ['ped1', 'ped2'], 'geometry': [Point(1, 2), Point(2, 1)]})
    df_shape2 = pd.DataFrame({'geometry': [Point(1, 2), Point(2, 1)], 'pID': ['ped1', 'ped2']})
    gdf = gpd.GeoDataFrame({'pID': ['ped1', 'ped2'], 'geometry': [Point(1, 2), Point(2, 1)]})

    # true internal representation
    internal = {'ped1': [1.0, 2.0], 'ped2': [2.0, 1.0]}
    frame1 = Frame(1, internal)
    frame2 = Frame(2, internal)

    def test_dict(self):
        self.assertEqual(Frame(1, self.dict_tuple1), self.frame1)
        self.assertEqual(Frame(1, self.dict_shape1), self.frame1)
        self.assertEqual(Frame(1, self.dict_tuple2), self.frame1)
        self.assertEqual(Frame(1, self.dict_shape2), self.frame1)
        self.assertNotEqual(Frame(2, self.dict_tuple1), self.frame1)

    def test_numpy(self):
        self.assertEqual(Frame(1, self.np_tuple1), self.frame1)
        self.assertEqual(Frame(1, self.np_tuple2), self.frame1)
        self.assertNotEqual(Frame(2, self.np_tuple1), self.frame1)

    def test_df(self):
        self.assertEqual(Frame(1, self.df_tuple), self.frame1)
        self.assertEqual(Frame(1, self.df_shape1), self.frame1)
        self.assertEqual(Frame(1, self.df_shape2), self.frame1)
        self.assertEqual(Frame(1, self.gdf), self.frame1)
        self.assertNotEqual(Frame(2, self.df_tuple), self.frame1)
        self.assertNotEqual(Frame(2, self.gdf), self.frame1)

    def test_list(self):
        self.assertEqual(Frame(1, self.list_tuple1), self.frame1)
        self.assertEqual(Frame(1, self.list_shape1), self.frame1)
        self.assertEqual(Frame(1, self.list_tuple2), self.frame1)
        self.assertEqual(Frame(1, self.list_shape2), self.frame1)
        self.assertNotEqual(Frame(2, self.list_tuple1), self.frame1)

        self.assertEqual(Frame(1, seq(self.list_tuple1)), self.frame1)
        self.assertEqual(Frame(1, seq(self.list_shape1)), self.frame1)
        self.assertEqual(Frame(1, seq(self.list_tuple2)), self.frame1)
        self.assertEqual(Frame(1, seq(self.list_shape2)), self.frame1)

    def test_json(self):
        json_frame = self.frame1.to_json()
        self.assertEqual(Frame.from_json(json_frame), self.frame1)

    def test_sequence(self):
        test_seq = seq([self.frame1, self.frame2])
        self.assertEqual(test_seq, test_seq.map(lambda x:x.to_dict()).map(Frame.from_dict))


if __name__ == '__main__':
    unittest.main()
