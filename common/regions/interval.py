"""Interval Data Class

Implements the Interval class, a data class that defines lower and
upper bounding values for an interval. Intervals are the building
blocks for representing multi-dimensional region objects.

Provides methods for determining if there is an overlap between two
intervals and what that overlap interval is.
"""

from functools import reduce
from common.generic.objects import SerializableObject


class Interval(SerializableObject):
    """The lower and upper bounding values for an interval.

    Building block for representing multi-dimensional regions and
    computing for overlap between those regions. Provides methods for
    determining if there is an overlap between two intervals and what
    the intersection length between the two intervals is.


    """

    def __init__(self, lower, upper):
        """Initialize a new Interval

        Initialize a new Interval with lower and upper bounding values.
        Converts input values to floating point numbers, and assigns
        the float value to the lower and upper fields. If lower is
        greater than upper, swaps the lower and upper values.

        Params
        ------
        lower, upper : float or int
            the lower and upper bounding values.
        """

        lower = float(lower)
        upper = float(upper)

        if lower > upper:
            self.lower = upper
            self.upper = lower
        else:
            self.lower = lower
            self.upper = upper



    ### Properties: Getters

    @property
    def length(self):
        """Compute the length of this Interval.

        Returns
        -------
        float
            The distance between the lower and
            upper bounding values.
        """

        return abs(self.upper - self.lower)


    @property
    def midpoint(self):
        """Compute the midpoint between lower and upper bounds.

        Returns
        -------
        float
            The value equal distance between the lower and
            upper bounding values.
        """

        return (self.lower + self.upper) / 2


    ### Methods: Queries

    def __eq__(self, other):
        """Determine if this interval is equivalent to another.

        Params
        ------
        other : Interval
            The other Interval to test for equality. If for both
            intervals lower and upper values match, they are equal.

        Returns
        -------
        bool
            True, if intervals are equal. False, otherwise.
        """

        if other is None:
            return self is None


        return self.lower == other.lower and self.upper == other.upper


    def __add__(self, offset):
        """Shift the interval coords by some offset.

        Params
        ------
        offset : float or int
            The value of the offset.
        """

        return Interval(self.lower + offset, self.upper + offset)
        

    def contains(self, value, inc_lower=True, inc_upper=True):
        """Determine if value lies between lower and upper bounds.

        Params
        ------
        value : float or int
            The value to test if it lies within
            this Interval's bounds.
        inc_lower, inc_upper : bool (optional, default: True)
            Boolean flag for whether or not to include or
            to exclude the lower or upper bounding values
            of this Interval. If inc_lower is True, includes
            the lower bounding value, otherwise excludes it.
            Likewise, if inc_upper is True, includes the
            upper bounding value, otherwise excludes it.

        Returns
        -------
        bool
            True, if values lies between the lower and upper
            bounding values. False, otherwise.
        """

        gte_lower = self.lower <= value if inc_lower else self.lower < value
        lte_upper = self.upper >= value if inc_upper else self.upper > value

        return gte_lower and lte_upper


    def encloses(self, other, inc_lower=True, inc_upper=True):
        """Determine if other Interval lies within this Interval.

        Params
        ------
        other : Interval
            The other Interval to test if it lies
            entirely within this Interval's bounds.
        inc_lower, inc_upper : bool (optional, default: True)
            Boolean flag for whether or not to include or
            to exclude the lower or upper bounding values
            of this Interval. If inc_lower is True, includes
            the lower bounding value, otherwise excludes it.
            Likewise, if inc_upper is True, includes the
            upper bounding value, otherwise excludes it.

        Returns
        -------
        bool
            True, if other Interval lies entirely within this
            Interval's bounds. False, otherwise.
        """


        return all([self.length >= other.length,
                    self.contains(other.lower, inc_lower, inc_upper),
                    self.contains(other.upper, inc_lower, inc_upper)])


    def is_intersecting(self, other, inc_bounds=False):
        """Determine if the given Interval overlaps with this Interval.
        
        To be overlapping, one Interval must contain the other's lower
        or upper bounding value.

        If the intervals are exactly adjacent (one's lower is equal to
        other's upper), then whether they intersect or not is decided
        by the inc_bounds flag.

        Return True if given Interval overlaps with this Interval,
        otherwise False.

        Params
        ------
        other : Interval
            The other Interval to test if it overlaps
            with this Interval.
        inc_bounds : bool (optional, default: False)
            If intervals considered intersecting when
            lower/upper bounds are exactly equal
            (zero-length intersection)

        Returns
        -------
        bool
            True, if that Interval overlaps with this Interval
            False, otherwise.

        Examples
        --------

        Overlapping:
        - |<---- Interval A ---->|
            |<---- Interval B ---->|
        - |<---- Interval A ---->|
                    |<- Interval B ->|
        -        |<- Interval A ->|
            |<---- Interval B ---->|
        - |<- Interval A ->|
                        |<- Interval B ->|
        -             |<- Interval A ->|
            |<- Interval B ->|

        Not overlapping:
        - |<- Interval A ->|     |<- Interval B ->|
        - |<- Interval B ->|     |<- Interval A ->|

        Conditionally overlapping:
        - |<- Interval A ->|<- Interval B ->|
        - |<- Interval B ->|<- Interval A ->|

        """


        if self == other:
            return True

        if inc_bounds:
            return self.upper >= other.lower and other.upper >= self.lower

        return self.upper > other.lower and other.upper > self.lower


    def get_intersection(self, other, inc_bounds=False):
        """Compute the overlap between this and other Interval.
        
        If the intervals are exactly adjacent (one's lower is equal to
        other's upper), then whether they intersect or not is decided
        by the inc_bounds flag.

        Return the overlapping Interval or None if the Intervals
        do not overlap.

        Params
        ------
        other : Interval
            The other Interval to test if it overlaps
            with this Interval.
        inc_bounds : bool (optional, default: False)
            If intervals considered intersecting when
            lower/upper bounds are exactly equal
            (zero-length intersection)

        Returns
        -------
        Interval
            The overlapping Interval if the Intervals overlap.
            None if the Intervals do not overlap.
        """


        if not self.is_intersecting(other, inc_bounds):
            return None

        return Interval(max(self.lower, other.lower),
                                        min(self.upper, other.upper))



    ### Class Methods: Generators

    @classmethod
    def from_intersection(cls, intervals):
        """Construct a new Interval from the intersection of others.
        
        Return the common intersection Interval if all given Intervals
        intersect, or otherwise return None.

        Params
        ------
        intervals : list
            List of Intervals to compute the intersecting
            Interval amongst.

        Returns
        -------
        Interval
            Interval that intersects with all given Intervals.
            None if not all the Intervals intersect.
        """
        

        def intersect(a: Interval, b: Interval) -> Interval:
            return a.get_intersection(b)


        try:
            return reduce(intersect, intervals)
        except AssertionError:
            return None


    @classmethod
    def from_dict(cls, dictObject):
        """Restore an Interval object using a dict representation.

        Params
        ------
        dictObject : dict
            A dictionary representation of this object.
            
        Returns
        -------
        Interval
            The corresponding serializable object.
        """

        return Interval(**dictObject)