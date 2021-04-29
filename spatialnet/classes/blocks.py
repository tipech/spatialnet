import math, geopy
from geopy.distance import distance
import geopandas as gpd


class GeoGrid():
    """Handles construction and querying geographical grids."""

        def __init__(self, bounds, cells):
         """Initialize a generic geographic Grid.

        Params
        ------
        bounds : 4-tuple/list of floats: (north, south, west, east)
            Boundary geocoordinates of input area bounding box
        cells : GeoSeries,GeoDataFrame or list of cell Polygons
            The geometry of 
        """

        self.bounds = bounds

        # determine cell and grid dimensions
        if cell_size is not None:
            w = cell_size
        else:
            
        

        x_size = 