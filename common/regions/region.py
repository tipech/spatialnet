"""Region Data Class

Implements the Region class, a data class that defines a
multidimensional region, with an upper and a lower vertex.

Provides methods for determining if there is an overlap between
two regions and what that intersection region is.
"""

from functools import reduce

from common.generic.objects import IdObject, TracedObject, SerializableObject
from common.regions import Interval
        

class Region(IdObject,TracedObject,SerializableObject):
    """A multidimensional region, with an upper and lower vertex.

    Params
    ------
    factors : list
        List of Intervals for each dimension within the Region.
        A Region of N dimensions is created from a list of N Intervals.
    id : str or int
        The unique identifier for this Region.
        Randonly generated with UUID v4, if not provided.
    ancestors : set, list or dict (optional, default: None-origin)
        Parents of this object, if they exist.       
    """

    def __init__(self, factors, id='', ancestors=None):
        """
        Construct a new Region from the given a list of Intervals

        Params
        ------
        factors : list
            List of Intervals for each dimension within the Region.
            A Region of N dimensions is created from a list
            of N Intervals.
        id : str or int
            The unique identifier for this Region.
            Randonly generated with UUID v4, if not provided.
        ancestors : set, list or dict (optional, default: None-origin)
            Parents of this object, if they exist.
        """

        super().__init__(id=id,ancestors=ancestors)

        if all([isinstance(f, Interval) for f in factors]):
            self.factors = factors
        elif all([isinstance(f, (tuple,list)) for f in factors]):
            self.factors = [Interval(f[0],f[1]) for f in factors]

        self.dimension = len(factors)


    ### Properties: Getters

    @property
    def lower(self):
        """The lower bounding vertex of this Region.

        Calculate and return a copy of the vector that represents
        the lower bounding values for this Region in each dimension.

        Returns
        -------
        float
            The lower bounding vertex of this Region.
        """
        return [d.lower for d in self.factors]

    @property
    def upper(self):
        """The upper bounding vertex of this Region.
        Calculate and return a copy of the vector that represents
        the upper bounding values for this Region in each dimension.

        Returns
        -------
        float
            The upper bounding vertex of this Region.
        """
        return [d.upper for d in self.factors]

    @property
    def lengths(self):
        """The distances between the lower and upper in each dimension.

        Returns
        -------
        list
            List of lengths for each dimension.
        """
        return [d.length for d in self.factors]

    @property
    def midpoint(self):
        """The mean point between lower and upper in each dimension.

        Returns
        -------
        list
            The point at the midpoint or center of the
            Region along all dimensions.
        """
        return [d.midpoint for d in self.factors]

    @property
    def size(self):
        """The magnitude size of the Region; length, area, volume.

        Computed by multiplying all dimensional lengths (sides).

        Returns
        -------
        float
            The magnitude size of the Region.
        """
        return reduce(lambda x, y: x * y, self.lengths)


    ### Methods: Intersection and other spatial queries

    def contains(self, point, inc_lower=True, inc_upper=True):
        """Determine if a point lies within lower and upper bounds.

        Params
        ------
        point : list
            The point to test if it lies within
            this Region's bounds.
        inc_lower, inc_upper : bool (optional, default: True)
            Boolean flag for whether or not to include or
            to exclude the lower or upper bounding vertics
            of this Region. If inc_lower is True, includes
            the lower bounding vertex, otherwise excludes it.
            Likewise, if inc_upper is True, includes the
            upper bounding vertex, otherwise excludes it.

        Returns
        -------
        bool
            True, if values lies within the region. False, otherwise.
        """


        return all([d.contains(point[i], inc_lower, inc_upper)
                    for i, d in enumerate(self.factors)])


    def encloses(self, other, inc_lower=True, inc_upper=True):
        """Determine if other Region lies within this Region.

        Params
        ------
        other : Region
            The other Region to test if it lies
            entirely within this Region's bounds.
        inc_lower, inc_upper : bool (optional, default: True)
            Boolean flag for whether or not to include or
            to exclude the lower or upper bounding values
            of this Region. If inc_lower is True, includes
            the lower bounding value, otherwise excludes it.
            Likewise, if inc_upper is True, includes the
            upper bounding value, otherwise excludes it.

        Returns
        -------
        bool
            True, if other Region lies entirely within this
            Region's bounds. False, otherwise.
        """


        if self == other:
            return True

        return all([d.encloses(other.factors[i], inc_lower, inc_upper)
                    for i, d in enumerate(self.factors)])


    def is_intersecting(self, other, inc_bounds=False):
        """Determine if the given Region intersects with this Region.

        If the regions are exactly adjacent (one's lower is equal to
        other's upper), then whether they intersect or not is decided
        by the inc_bounds flag.

        To be intersecting, one Region must contain the other's lower
        or upper bounding vertices. As long as all corresponding
        Intervals for each dimension intersect in both Regions, then
        the Regions are intersecting.

        Return True if given Region intersects with this Region,
        otherwise False.

        Params
        ------
        other : Region
            The other Region to test if it intersects with this Region.
        inc_bounds : bool (optional, default: False)
            If regions considered intersecting when lower/upper bounds
            are exactly equal (zero-length intersection)

        Returns
        -------
        bool
            True, if other Region intersects with this Region
            False, otherwise.

        Examples
        --------

        Intersecting:
        - |--------------|          -         |--------------|
          |      |-------|------|     |-------|------|       |
          |<- Region A ->|      |     |       |<- Region B ->|
          |      |<- Region B ->|     |<- Region A ->|       |
          |------|-------|      |     |       |------|-------|
                 |--------------|     |--------------|

        - |--------------------|    - |--------------------|
          |  |--------------|  |      |  |--------------|  |
          |<-|-- Region A --|->|      |<-|-- Region A --|->|
          |  |<- Region B ->|  |      |  |<- Region B ->|  |
          |--|--------------|--|      |  |--------------|  |
             |--------------|         |--------------------|

        -        |--------------|   - |==============|
         |-------|------|       |     |              |
         |       |<- Region B ->|     |<- Region A ->|
         |<- Region A ->|       |     |<- Region B ->|
         |-------|------|       |     |              |
                 |--------------|     |==============|

        Not Intersecting:

        - |--------------| 
          |<- Region A ->| |--------------|
          |--------------| |<- Region B ->|
                           |--------------|

        Conditionally Intersecting:
        - |--------------|
          |<- Region A ->|
          |==============|
          |<- Region B ->|
          |--------------|

        """


        return all([d.is_intersecting(other.factors[i])
            for i, d in enumerate(self.factors)])


    def __eq__(self, other):
        """ Determine if the given Region equals to this Region.

        If the two Region have the same factors (same Intervals;
        lower and upper bounds for all dimensions), then they
        are equal, otherwise they are not.

        Return True if the two Regions are equal, otherwise False.

        Is syntactic sugar for:
            self == other

        Params
        ------
        other : Region
            The other Region to test if it has the
            same Intervals (lower and upper bounds) for
            all dimensions within this Region's bounds.

        Returns
        -------
        bool
            True, if the two Regions are equal. False, otherwise.
        """
        return (isinstance(other, Region) and
                self.dimension == other.dimension and
                all([d == other.factors[i]
                    for i, d in enumerate(self.factors)]))


    def get_intersection(self, other, inc_bounds=False):
        """Compute the intersecting Region between this and another.

        Params
        ------
        other : Region
            The other Region with which to compute
            the common intersecting Region.
        inc_bounds : bool (optional, default: False)
            If regions considered intersecting when
            lower/upper bounds are exactly equal
            (results in zero-length intersection)

        Returns
        -------
        Region
            The intersecting Region, None if Regions do not intersect.

        Examples
        --------

        - |---Region A---|          -        |---Region B---|
          |     |---Region B---|      |---Region A---|      |
          |     |########|     |      |      |#######|      |
          |     |########|     |      |      |#######|      |
          |-----|--------|     |      |      |-------|------|
                |--------------|      |--------------|

        - |------Region A------|    - |------Region A------|
          |  |---Region B---|  |      |  |---Region B---|  |
          |  |##############|  |      |  |##############|  |
          |  |##############|  |      |  |##############|  |
          |--|--------------|--|      |  |--------------|  |
             |--------------|         |--------------------|

        -       |---Region B---|    - |===Region A===|
          |---Region A---|     |      |##############|
          |     |########|     |      |##############|
          |     |########|     |      |##############|
          |-----|--------|     |      |##############|
                |--------------|      |===Region B===|

        """


        if not self.is_intersecting(other, inc_bounds):
            return None

        return Region.from_intersection([self, other])


    ### Methods: Size queries

    def get_intersection_size(self, other):
        """Compute the size of intersection between this and another.

        There's no need to check for exact bounds,
        as the size would be 0 anyway.

        Params
        ------:
        other : Region
            The other Region with which to compute
            the common intersecting Region.

        Returns
        -------
        float 
            The size of the intersection
            0: If the Regions do not intersect.
        """


        if not self.is_intersecting(other):
            return 0

        return self.get_intersection(other).size


    def get_union_size(self, other):
        """Compute the size of the union of two Regions.

        Params
        ------
        other : Region
            The other Region which this Region is to compute
            the enclosing (union) Region with.

        Returns
        -------
        float
            The size of the union.

        Examples
        --------

        - |## Region A ##|^^^^^|    - |^^^^^|## Region B ##|
          |#####|%% Region B %%|      |%% Region A %%|#####|
          |#####|########|%%%%%|      |%%%%%|%%%%%%%%|#####|
          |#####|########|%%%%%|      |%%%%%|%%%%%%%%|#####|
          |#####|########|%%%%%|      |%%%%%|%%%%%%%%|#####|
          |.....|%%%%%%%%%%%%%%|      |%%%%%%%%%%%%%%|.....|

        - |%%%%% Region A %%%%%|    - |%%%%% Region A %%%%%|
          |%%|## Region B ##|%%|      |%%|## Region B %%|%%|
          |%%|##############|%%|      |%%|##############|%%|
          |%%|##############|%%|      |%%|##############|%%|
          |%%|##############|%%|      |%%|##############|%%|
          |..|##############|..|      |%%%%%%%%%%%%%%%%%%%%|

        - |^^^^^^|%% Region B %%|   - |## Region A ##|
          |## Region A ##|%%%%%%|     |##############|
          |######|#######|%%%%%%|     |##############|
          |######|#######|%%%%%%|     |##############|
          |######|#######|%%%%%%|     |##############|
          |......|%%%%%%%%%%%%%%|     |## Region B ##|
        """


        if not self.is_intersecting(that):
            return self.size + that.size

        return self.size + that.size - get_intersection_size(that)


    def project(self, dimension: int, interval=Interval(0, 0), **kwargs):
        """ Project this Region to the specified number of dimensions.

        If the given number of dimensions is greater than this Region's
        dimensionality, output a Region with additional factors with
        the given Interval or [0, 0] intervals.

        If the given number of dimensions is smaller than this Region's
        dimensionality, output a Region with the additional dimensions
        removed. If the given dimension number is equal to this
        Region's dimensionality, output a copy of this Region.

        Additional arguments passed through to Region.from_intervals.

        Params
        ------
        dimension : int
            The number of dimensions in the output
            projected Region.
        interval : Interval
            The Interval to add to each dimension if
            the projected number of dimension is greater
            than this Region.
        kwargs : dict
            Additional arguments passed through to
            Region.from_intervals.

        Returns
        -------
        Region
            The projected Region.
        """


        factors = [Interval(interval.lower, interval.upper)
                   if d >= self.dimension else self.factors[d] 
                   for d in range(dimension)]

        return Region.from_intervals(factors, **kwargs)


    ### Methods: Representations

    def __repr__(self) -> str:
        """Get a human-readable string representation of an object.

        Returns
        -------
        str
            String representation of an object.
        """

        dictobj = {
            'id': "{}..".format(self.id[0:8]) if len(self.id)>8 else self.id,
            'd': self.dimension,
            'lower': self.lower,
            'upper': self.upper,
            'ancestors': ["{}..".format(o[0:8]) if len(o) > 8 else o
                          for o in self.ancestors]
        }

        kvpairs = ', '.join('{}={}'.format(k,v) for k,v in dictobj.items())
        return '{}({})'.format(self.__class__.__name__,kvpairs)


    ### Class Methods: Generators

    @classmethod
    def from_coords(cls, lower, upper, id=''):
        """Construct a new Region from the given a list of Intervals.

        Params
        ------
        lower, upper : list
            The lower and upper bounding vertices.
        id : str or int
            The unique identifier for this Region
            Randonly generated with UUID v4, if not provided.

        Returns
        -------
        Region
            A Region of dimension N, for a list of
            Intervals of length N.
        """

        
        return cls([Interval(*i) for i in zip(lower, upper)], id)


    @classmethod
    def from_interval(cls, interval, dimension=1, id =''):
        """Construct a new Region from an Interval in all dimensions.

        Returns a Region of the specified dimensionality with
        each dimension having the same Interval.

        Params
        ------
        interval : Interval
            The Interval to be projected for each
            dimension in the new Region.
        dimension : int
            The number of dimensions in the new
            projected Region.
        id : str or int
            The unique identifier for this Region
            Randonly generated with UUID v4, if not provided.

        Returns
        -------
        Region
            A Region containing the specified dimensionality
            with each dimension having the same Interval.
        """


        return cls([interval for i in range(dimension)], id)


    @classmethod
    def from_intersection(cls, regions, id=''):
        """Construct new Region from the intersection of two or more.

        Params
        ------
        regions : list
            The list of Regions which the intersecting
            Region is generated with.
        id : str or int
            The unique identifier for this Region
            Made by combining original ids, if not provided.

        Returns
        -------
        Region
            The intersecting Region.
            None, if the Regions do not intersect.
        """


        if id == '':
            id = '_'.join(sorted(r.id for r in regions))

        factors = zip(*list(r.factors for r in regions))
        factors = [Interval.from_intersection(list(f)) for f in factors]

        if any([f == None for f in factors]):
            return None

        return cls(factors, id, [r.ancestors for r in regions])


    @classmethod
    def from_dict(cls, dictObject):
        """Restore a Region object using a dict representation.

        Params
        ------
        dictObject : dict
            A dictionary representation of this object.
            
        Returns
        -------
        Region
            The corresponding serializable object"""

        dictObject['factors'] = [Interval.from_dict(f)
                                 for f in dictObject['factors']]
        del dictObject['dimension']

        return Region(**dictObject)
