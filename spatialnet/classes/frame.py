import numpy as np
import pandas as pd
import geopandas as gpd
from collections import UserDict
from shapely.geometry import Point

from .json_serializable import JSONSerializable

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


def read_frame(source):
    """Get a Frame object from a JSON file, buffer or string.

    Params
    ------
    source : str or file handle
        File path, object or JSON string.
    """
    return Frame.from_json(source)
