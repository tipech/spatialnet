"""Trajectory Edge Stream

Implements the TrajectoryEdgeStream class, a subclass of BaseStream
that represents an iterator of Particle streams.

"""

import networkx as nx
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

    def get_graph(self):
        """Get this edge stream as an aggregated graph.

        Returns
        -------
        nx.Graph
            The aggregated graph.
        """
        G = nx.MultiGraph()
        for e in self:
            G.add_edge(e['from'], e['to'], first=e['first'], last=e['last'],
                duration=(e['last'] - e['first']))
        return G