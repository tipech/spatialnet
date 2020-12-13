"""Region Stream

Implements the RegionStream class, a subclass of BaseStream
that represents an iterator of Regions.

"""

from spatialnet.common.generic.iterators import BaseStream
from spatialnet.common.regions import Region


class RegionStream(BaseStream):
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


    def calculate_bounds(self):
        """Automatically calculate and set this Stream's bounds.

        By necessity, this has to use a checkpoint of the iterator,
        then calculate bounds.

        Returns
        -------
        Region
            The new bounds.
        """

        item_list = self.checkpoint()

        lower = [min(r.factors[d].lower for r in item_list)
                 for d in range(self.dimension)]
        upper = [max(r.factors[d].upper for r in item_list)
                 for d in range(self.dimension)]

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