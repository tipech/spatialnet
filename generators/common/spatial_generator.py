"""Spatial Generator class

Implements the SpatialGenerator class, a generic class that provides common
behavior for all generators dealing with creating objects within a space.

"""

import random

from spatialnet.common.regions import Region,Interval
from spatialnet.generators.common import Randoms


class SpatialGenerator():
    """Generic spatial generator singleton class.

    Random generation of spatial objects.

    Params
    ------
    bounds : Region (optional, default: None)
        A region with the outer bounds of the observation space
    dimension : int (optional, default: bounds or 2)
        The number of dimensions of all objects generated
    posrng: method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing the position of objects.
    """

    def __init__(self, bounds=None, dimension=None, posrng=Randoms.uniform(),
                 **kwargs):
        """Initialize data generator with user-specified parameters.

        Params
        ------
        bounds : Region (optional, default: 1000x1000)
            A region with the outer bounds of the observation space
        dimension : int (optional, default: bounds or 2)
            The number of dimensions of all objects generated
        posrng: method or list of methods (optional, default: uniform)
            The random number generator or list of random number
            generator options for choosing the position of objects.
        """

        super().__init__(**kwargs)

        # bounds & dimensions pc init
        if bounds is not None:
            if isinstance(bounds, Interval):
                bounds = Region.from_interval(bounds, 2)

            self.dimension = bounds.dimension
            self.bounds = bounds

        else:
            if dimension == None:
                dimension = 2


            self.dimension = dimension
            self.bounds = Region.from_interval(Interval(0,1000), dimension)

        # random functions init
        if not isinstance(posrng, list):
            posrng = [posrng for d in range(self.dimension)]


        self.posrng = posrng


    def get_point(self, padding=None):
        """Get a random multi-dimensional point according to posrng

        Params
        ------
        padding : float or list of floats
            Optional right-padding for non-point objects, expects
            a number or a list with values per dimension.

        Returns
        -------
        list of floats
            A list with the coords of the point in each dimension.
        """    

        if padding is not None and not isinstance(padding, list):
            padding = [padding for d in range(self.dimension)]

        if padding is None:
            return [self.posrng[d](self.bounds.lower[d], self.bounds.upper[d])
                    for d in range(self.dimension)]
        else:
            return [self.posrng[d](self.bounds.lower[d],
                                   self.bounds.upper[d] - padding[d])
                    for d in range(self.dimension)]
        