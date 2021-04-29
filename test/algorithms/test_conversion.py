import unittest

from functional import seq
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

import spatialnet as sn
from spatialnet import Frame, Trajectory


frames = [  Frame(0, {'ped1': [1.0, 2.0], 'ped2': [10.0, 20.0]}),
            Frame(1, {'ped1': [2.0, 3.0], 'ped2': [11.0, 21.0]})]

trajectories = [Trajectory('ped1', {0: [1.0, 2.0], 1: [2.0, 3.0]}),
                Trajectory('ped2', {0: [10.0, 20.0], 1: [11.0, 21.0]})]

trajectory_gdf = gpd.GeoDataFrame({
    'pIDs': ['ped1', 'ped2'],
    'geometry': [   LineString([(1.0, 2.0), (2.0, 3.0)]),
                    LineString([(10.0, 20.0), (11.0, 21.0)])]})


class TestConversion(unittest.TestCase):

    def test_frames_trajectories(self):

        self.assertEqual(trajectories, sn.frames_to_trajectories(frames))
        self.assertEqual(frames, sn.trajectories_to_frames(trajectories))
        
        pd.testing.assert_frame_equal(trajectory_gdf, sn.trajectories_to_gdf(trajectories))
