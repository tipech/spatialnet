"""Trajectory Stream

Implements the TrajectoryStream class, a subclass of BaseStream
that represents an iterator of Particle streams.

"""

from common.generic.iterators import BaseStream
from common.generic.objects import IdObject
from common.trajectories import ParticleStream
from common.regions import Region


class TrajectoryStream(BaseStream, IdObject):
    """An iterator over ParticleStreams.

    Provides methods for reading and saving streams of ParticleStream
    objects to and from storage, as well as merging different streams.
    
    Params
    ------
    items : Iterator
        The ParticleStream data items to be used for this stream.
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

        # store trajectories to list and reset iterator
        trajectories = [p_stream.to_dict() for p_stream in self.items]
        if len(trajectories) == 0:
            raise StopIteration
            
        self.items = (ParticleStream.from_dict(p) for p in trajectories)
        dims = trajectories[0]['items'][0]['dimension']

        lower = [min(p['position'][d] for p_stream in trajectories
            for p in p_stream['items']) for d in range(dims)]
        upper = [max(p['position'][d] for p_stream in trajectories
            for p in p_stream['items']) for d in range(dims)]

        return Region.from_coords(lower=lower, upper=upper)


    @staticmethod
    def deserialize_item(item_dict):
        """Deserialize and add a ParticleStream to the stream.
        
        Params
        ------
        item_dict : dict
            Deserialized ParticleStream dict object

        Returns
        -------
        item
            ParticleStream item for this stream
        """
        
        return ParticleStream.from_dict(item_dict)
