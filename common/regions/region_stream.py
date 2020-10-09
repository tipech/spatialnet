"""Region Stream

Implements the RegionStream class, a subclass of BaseStream
that represents an iterator of Regions.

"""

from common.generic.iterators import BaseStream
from common.generic.objects import IdObject
from common.regions import Region


class RegionStream(BaseStream, IdObject):
    """An iterator over Regions.

    Provides methods for reading and saving streams of Region objects
    to and from storage, as well as merging different streams.
    
    Params
    ------
    items : Iterator
        The Region data source to be used for this stream.
    id : str or int
        The unique identifier for this SpatialSet.
        Randonly generated with UUID v4, if not provided.
    """

    def __init__(self, items, id=''):
        """Initialize a new objects collection iterator from a source.

        Optionally provide an id.

        Params
        ------
        items : Iterator
            The data source to be used for this stream.
        id : str or int
            The unique identifier for this BaseStream.
            Randonly generated with UUID v4, if not provided.
        """

        super().__init__(items=items, id=id)


    def calculate_bounds(self):
        """Automatically calculate and set this Stream's bounds.

        By necessity, this has to run the full iterator, store its
        contents as a list, calculate bounds and finally recreate it.

        Returns
        -------
        Region
            The new bounds.
        """

        # store regions to list and reset iterator
        regions = list(self.items)
        if len(regions) == 0:
            raise StopIteration
            
        self.items = iter(regions)

        lower = [min(r.factors[d].lower for r in regions)
                 for d in range(regions[0].dimension)]
        upper = [max(r.factors[d].upper for r in regions)
                 for d in range(regions[0].dimension)]

        return Region.from_coords(lower=lower, upper=upper)


    @staticmethod
    def deserialize_item(item_dict):
        """Deserialize and add a Region to the stream.
        
        Params
        ------
        item_dict : dict
            Deserialized Region dict object

        Returns
        -------
        item
            Region item for this stream
        """
        
        return Region.from_dict(item_dict)