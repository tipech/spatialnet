import numpy as np
import pandas as pd
import geopandas as gpd
from collections import UserDict
from shapely.geometry import Point
import functional
from numbers import Number

from .json_serializable import JSONSerializable
from .trajectory import Trajectory

class Frame(UserDict, JSONSerializable):
    """Contains a set of particles and their positions in a timestep."""

    def __init__(self, time, particles):
        """Create a Frame object.

        Params
        ------
        time : int
            The timestamp of this frame.
        particles : array/iterable/DataFrame/GeoDataFrame of (pID, pos)
            The collection of particle IDs and positions
            pos can be either a tuple (x, y [,...]) or shapely.geometry.Point
        """
        self.time = time

        # input data given as geopandas geodataframe, convert to dict
        if isinstance(particles, gpd.GeoDataFrame):
            super().__init__({
                list(f['properties'].values())[0]:f['geometry']['coordinates']
                for f in particles.iterfeatures()})

        # input data given in row dict format {'id1':(), 'id2':(), ...}
        elif isinstance(particles, dict) and len(particles) != 2:
            super().__init__(particles)

        # uncertain input (row/column format, column order)
        else:

            # input data given as pandas dataframe, convert to dict
            if isinstance(particles, pd.DataFrame):
                p_list = list(particles.to_dict('list').values())

            # numpy array given, convert to list
            elif isinstance(particles, np.ndarray):
                p_list = particles.tolist()

            # input data given as dict with length 2
            elif isinstance(particles, dict):
                p_list = list(particles.items())

            # anything else gets converted to list of lists
            else:
                p_list = list(particles)

            # anything in row format
            if len(p_list) != 2:
                super().__init__(p_list)

            else:
                v0, v1 = p_list
                # first item is ids, second is points
                if all(isinstance(i, (str,int)) for i in v0):
                    super().__init__(dict(zip(v0, v1)))

                # first item is points, second is ids
                elif all(isinstance(i, (str,int)) for i in v1):
                    super().__init__(dict(zip(v1, v0)))

                # column format with column names, first is ids
                elif (not isinstance(v1[1], Point)
                        and all(isinstance(i, (tuple,Point)) for i in v1[1])):
                    super().__init__(dict(zip(v0[1], v1[1])))

                # column format with column names, first is points
                elif (not isinstance(v0[1], Point)
                        and all(isinstance(i, (tuple,Point)) for i in v0[1])):
                    super().__init__(dict(zip(v1[1], v0[1])))

                # row format with 2 items
                else:
                    super().__init__(p_list)

        # make sure particle coords are lists, not Points or tuples
        if len(self.data) > 0:
            if isinstance(next(iter(self.data.values())), Point):
                self.data = {k:list(v.coords[0]) for k,v in self.data.items()}
            else:
                self.data = {k:list(v) for k,v in self.data.items()}


    def __eq__(self, other):
        """Compare self and other frame based on time and points."""
        return self.time == other.time and super().__eq__(other)


    def to_dict(self):
        """Get a dict representation of this object."""
        return {'time':self.time, 'particles': self.data}


    def __str__(self):
        """Get a string representation of this object."""
        return "Frame(t={},#points={})".format(self.time, len(self.data))


    @classmethod
    def from_dict(cls, d):
        """Get a Frame object from a dict object.

        Params
        ------
        d : dict
            dict object to turn into a Frame.
        """
        return Frame(**d)


    @staticmethod
    def frames_to_trajectories(frames):
        """Convert a list or sequence of frames into one of trajectories.

        Params
        ------
        frames : list, iterable or pyfunctional.Sequence of Frame objects
            Input collection of Frame objects.

        Returns
        -------
        pyfunctional.Sequence if frames is Sequence, else list
            Collection of Trajectory objects, same type as frames
        """

        # determine if input was sequence, if not convert it and remember
        nonseq = False
        if not isinstance(frames, functional.pipeline.Sequence):
            nonseq = True
            frames = functional.seq(frames)

        # flatten, group by particle id and convert to Trajectory objects
        records = frames.flat_map(lambda f: ( (pID,(f.time,pos))
            for pID,pos in f.items()) )
        trajectories = records.group_by_key().map(lambda x: Trajectory(*x))

        if nonseq:
            return trajectories.to_list()
        return trajectories
