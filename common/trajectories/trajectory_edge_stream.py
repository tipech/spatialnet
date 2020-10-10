"""Trajectory Edge Stream

Implements the TrajectoryEdgeStream class, a subclass of BaseStream
that represents an iterator of Particle streams.

"""

from networkx import Graph
from common.generic.iterators import BaseStream


class TrajectoryEdgeStream(BaseStream):
    """An iterator over static graph snapshots.

    Provides methods for reading and saving streams of Graph
    objects to and from storage, as well as merging different streams.
    
    Params
    ------
    items : Iterator
        The Graph objects to be used for this stream.
    id : str or int
        The unique identifier for this TrajectoryEdgeStream.
        Randonly generated with UUID v4, if not provided.
    """

    def __init__(self, items, id=''):
        """Initialize a new objects collection iterator from a source.

        Optionally provide an id.

        Params
        ------
        items : Iterator
            The Graph objects to be used for this stream.
        id : str or int
            The unique identifier for this TrajectoryEdgeStream.
            Randonly generated with UUID v4, if not provided.
        """

        super().__init__(items=items, id=id)