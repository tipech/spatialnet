import numpy as np
import pandas as pd
import geopandas as gpd
from collections import UserDict
from shapely.geometry import Point, LineString
from numbers import Number

from . import JSONSerializable

class Trajectory(UserDict, JSONSerializable):
    """Contains a sequence of times and positions for a given particle."""

    def __init__(self, pID, trace):
        """Create a Trajectory object.

        Params
        ------
        pID : int
            The id of this particle.
        trace : array/iterable/DataFrame/GeoDataFrame of (pID, pos)
            The sequence of timestamps and positions
            pos can be either a tuple (x, y [,...]) or shapely.geometry.Point
        """
        self.pID = pID

        # input data given as geopandas geodataframe, convert to dict
        if isinstance(trace, gpd.GeoDataFrame):
            super().__init__({
                list(f['properties'].values())[0]:f['geometry']['coordinates']
                for f in trace.iterfeatures()})

        # input data given in row dict format {'id1':(), 'id2':(), ...}
        elif isinstance(trace, dict) and len(trace) != 2:
            super().__init__(trace)

        # uncertain input (row/column format, column order)
        else:

            # input data given as pandas dataframe, convert to dict
            if isinstance(trace, pd.DataFrame):
                t_list = list(trace.to_dict('list').values())

            # numpy array given, convert to list
            elif isinstance(trace, np.ndarray):
                t_list = trace.tolist()

            # input data given as dict with length 2
            elif isinstance(trace, dict):
                t_list = list(trace.items())

            # anything else gets converted to list of lists
            else:
                t_list = list(trace)

            # anything in row format
            if len(t_list) != 2:
                super().__init__(t_list)

            else:
                v0, v1 = t_list

                # second item is LineString, split to points
                if isinstance(v1, LineString):
                    super().__init__(dict(zip(v0, v1.coords)))

                # first item is LineString, split to points
                elif isinstance(v0, LineString):
                    super().__init__(dict(zip(v1, v0.coords)))

                # first item is ids, second is points
                elif all(isinstance(i, (int)) for i in v0):
                    super().__init__(dict(zip(v0, v1)))

                # first item is points, second is ids
                elif all(isinstance(i, (int)) for i in v1):
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
                    super().__init__(t_list)

        # make sure particle coords are lists, not Points or tuples
        # also make sure times are ints
        if len(self.data) > 0:
            if isinstance(next(iter(self.data.values())), Point):
                self.data = {int(k):list(v.coords[0])
                                for k,v in self.data.items()}
            else:
                self.data = {int(k):[float(c) for c in v]
                                for k,v in self.data.items()}

    def get_linestring(self):
        """Get the trajectory points as a LinString."""
        return LineString(list(self.data.values()))


    def __eq__(self, other):
        """Compare self and other trajectory based on pID and points."""
        return self.pID == other.pID and super().__eq__(other)


    def to_dict(self):
        """Get a dict representation of this object."""
        return {'pID':self.pID, 'trace': self.data}


    def __str__(self):
        """Get a string representation of this object."""
        return "Trajectory(id={},#points={})".format(self.pID, len(self.data))


    @classmethod
    def from_dict(cls, d):
        """Get a Trajectory object from a dict object.

        Params
        ------
        d : dict
            dict object to turn into a Trajectory.
        """
        return Trajectory(**d)

