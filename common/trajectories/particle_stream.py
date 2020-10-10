"""Particle Stream

Implements the RegionStream class, a subclass of BaseStream
that represents an iterator of Regions.

"""

from common.generic.iterators import BaseStream
from common.trajectories import Particle


class ParticleStream(BaseStream):
    """An iterator over Particles.

    Provides methods for reading and saving streams of Particle objects
    to and from storage, as well as merging different streams.
    
    Params
    ------
    items : Iterator
        The Particle data items to be used for this stream.
    dimension : int
        The number of dimensions of items in this stream
    id : str
        The id for this stream
    time : int (optional)
        The timestamp this corresponds to.
    """

    def __init__(self, items, dimension=2, id='', time=None):
        """Initialize a new particle iterator from a source, with time.

        Params
        ------
        items : Iterator
            The data source to be used for this stream.
        dimension : int
            The number of dimensions of items in this stream
        id : str
            The id for this stream
        time : int (optional)
            The timestamp this corresponds to.
        """

        if len(id) == 0:
            id = time

        super().__init__(items=items, dimension=dimension, id=id)

        self.time = time



    @classmethod
    def from_dict(cls, dictObject):
        """Restore a ParticleStream using a dict representation.

        Params
        ------
        dictObject : dict
            A dictionary representation of a ParticleStream.
            
        Returns
        -------
        ParticleStream
            The corresponding serialized ParticleStream
        """

        return cls(time=dictObject['time'], items=(Particle.from_dict(p)
            for p in dictObject['items']))


    @staticmethod
    def deserialize_item(item_dict):
        """Deserialize and add a Particle to the stream.
        
        Params
        ------
        item_dict : dict
            Deserialized Particle dict object

        Returns
        -------
        item
            Particle item for this stream
        """
        
        return Particle.from_dict(item_dict)
