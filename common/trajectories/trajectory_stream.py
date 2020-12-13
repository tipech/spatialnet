"""Trajectory Stream

Implements the TrajectoryStream class, a subclass of BaseStream
that represents an iterator of Particle streams.

"""

from spatialnet.common.generic.iterators import BaseStream
from spatialnet.common.trajectories import ParticleStream
from spatialnet.common.regions import Region


class TrajectoryStream(BaseStream):
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


    def calculate_bounds(self):
        """Automatically calculate and set this Stream's bounds.

        By necessity, this has to run the full iterator, store its
        contents as a list, calculate bounds and finally recreate it.

        Returns
        -------
        Region
            The new bounds.
        """

        trajectories = self.checkpoint()
        
        if len(trajectories) != 0:
            lower = [min(p.position[d] for p_stream in trajectories
                for p in p_stream) for d in range(self.dimension)]
            upper = [max(p.position[d] for p_stream in trajectories
                for p in p_stream) for d in range(self.dimension)]

        else:
            lower = [0] * self.dimension
            upper = [1] * self.dimension

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
