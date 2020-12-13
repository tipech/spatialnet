"""Region Generator class

Implements the RegionGenerator class, a class that handles random generation
of regions.

"""
import random

from spatialnet.common.regions import Region, Interval, RegionStream
from spatialnet.generators.common import Randoms, SpatialGenerator

class RegionGenerator(SpatialGenerator):
    """Region generator singleton class.

    Random generation of regions or graphs.

    Params
    ------
    bounds : Region (optional, default: None)
        A region with the outer bounds of the observation space
    dimension : int (optional, default: bounds or 2)
        The number of dimensions of all Regions generated
    posrng: method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing the position of Regions.
    sizepc: float (optional, default: 0.005)
        The size range as a percentage of the total Regions'
        length in every dimension.
    sizerng: method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing the size of Regions.
    square: bool (optional, default: False)
        A flag to specify whether the generated regions should be
        squares or regular rectangles. True for squares.
    """
    def __init__(self, bounds=None, dimension=None, posrng=Randoms.uniform(),
                 sizepc=0.05, sizerng=Randoms.uniform(), square=False):
        """Initialize data generator with user-specified parameters.

        Params
        ------
        bounds : Region (optional, default: None)
            A region with the outer bounds of the observation space
        dimension : int (optional, default: bounds or 2)
            The number of dimensions of all Regions generated
        posrng: method or list of methods (optional, default: uniform)
            The random number generator or list of random number
            generator options for choosing the position of Regions.
        sizepc: float (optional, default: 0.005)
            The size range as a percentage of the total Regions'
            length in every dimension.
        sizerng: method or list of methods (optional, default: uniform)
            The random number generator or list of random number
            generator options for choosing the size of Regions.
        square: bool (optional, default: False)
            A flag to specify whether the generated regions should be
            squares or regular rectangles. True for squares.
        """

        super().__init__(bounds=bounds, dimension=dimension, posrng=posrng)

        # size pc init
        ndunit_region = Region.from_interval(Interval(0,1), self.dimension)

        if sizepc is None:
            sizepc = ndunit_region
        if isinstance(sizepc, float) or isinstance(sizepc, int):
            sizepc = Region.from_interval(Interval(0,sizepc), self.dimension)
        elif isinstance(sizepc,Interval):
            sizepc = Region.from_interval(sizepc, self.dimension)


        self.sizepc = sizepc

        # random functions init
        if not isinstance(sizerng, list):
            sizerng = [sizerng for d in range(self.dimension)]


        self.sizerng = sizerng
        self.square = square



    def get_region(self):
        """Randomly generate a Region based on generator parameters.

        Returns
        -------
        Region
            The generated region.
        """

        window_size = [f.length for f in self.bounds.factors]

        if self.square:
            side_size=self.sizerng[0](
                self.sizepc.factors[0].lower * window_size[0],
                self.sizepc.factors[0].upper * window_size[0])
            size = [side_size for d in range(self.dimension)]

        else:
            size = [self.sizerng[d](
                    self.sizepc.factors[d].lower * window_size[d],
                    self.sizepc.factors[d].upper * window_size[d])
                        for d in range(self.dimension)]
        
        lower = self.get_point(size)
        upper = [lower[d] + size[d] for d in range(self.dimension)]
        
        return Region.from_coords(lower, upper)

        
    def get_region_stream(self, n, id=''):
        """Iteratively generate N random Regions based on parameters.

        Params
        ------
        n : int
            The number of regions the resulting set should contain.
        id : str (optional, default: parameter stream)
            An id to name the string after

        Returns
        -------
        RegionStream
            A stream of generated regions in a RegionStream.
        """

        iterator = (self.get_region() for r in range(n))

        if len(id) == 0:
            id = "regions_d{}_n{}_size({}-{})_{}".format(self.dimension, n,
                self.sizepc.lower[0], self.sizepc.lower[0],
                self.posrng[0].__name__)
            if self.square:
                id += "_square"

        return RegionStream(items=iterator, id=id, dimension=self.dimension)
        