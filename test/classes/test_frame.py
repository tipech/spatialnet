import unittest

from functional import seq
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from spatialnet import Frame, read_frame


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
frame1 = Frame(1, {'ped1': [1.0, 2.0], 'ped2': [2.0, 1.0]})
frame2 = Frame(2, {'ped1': [1.0, 2.0], 'ped2': [2.0, 1.0]})

class TestFrame(unittest.TestCase):

    def test_dict(self):
        self.assertEqual(Frame(1, dict_tuple1), frame1)
        self.assertEqual(Frame(1, dict_shape1), frame1)
        self.assertEqual(Frame(1, dict_tuple2), frame1)
        self.assertEqual(Frame(1, dict_shape2), frame1)
        self.assertNotEqual(Frame(2, dict_tuple1), frame1)

    def test_numpy(self):
        self.assertEqual(Frame(1, np_tuple1), frame1)
        self.assertEqual(Frame(1, np_tuple2), frame1)
        self.assertNotEqual(Frame(2, np_tuple1), frame1)

    def test_df(self):
        self.assertEqual(Frame(1, df_tuple), frame1)
        self.assertEqual(Frame(1, df_shape1), frame1)
        self.assertEqual(Frame(1, df_shape2), frame1)
        self.assertEqual(Frame(1, gdf), frame1)
        self.assertNotEqual(Frame(2, df_tuple), frame1)
        self.assertNotEqual(Frame(2, gdf), frame1)

    def test_list(self):
        self.assertEqual(Frame(1, list_tuple1), frame1)
        self.assertEqual(Frame(1, list_shape1), frame1)
        self.assertEqual(Frame(1, list_tuple2), frame1)
        self.assertEqual(Frame(1, list_shape2), frame1)
        self.assertNotEqual(Frame(2, list_tuple1), frame1)

        self.assertEqual(Frame(1, seq(list_tuple1)), frame1)
        self.assertEqual(Frame(1, seq(list_shape1)), frame1)
        self.assertEqual(Frame(1, seq(list_tuple2)), frame1)
        self.assertEqual(Frame(1, seq(list_shape2)), frame1)

    def test_json(self):
        json_frame = frame1.to_json()
        self.assertEqual(Frame.from_json(json_frame), frame1)
        self.assertEqual(read_frame(json_frame), frame1)

    def test_sequence(self):
        test_seq = seq([frame1, frame2])
        self.assertEqual(test_seq, test_seq.map(lambda x:x.to_dict()).map(Frame.from_dict))


if __name__ == '__main__':
    unittest.main()
