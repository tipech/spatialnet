"""Trajectory Network EdgeStream Converter class

Implements the TrajectoryEdgeConverter class, a class that handles
conversion of trajectory networks to edge stream format.

"""

import random, heapq
from networkx import Graph
from common.trajectories import TrajectoryNetStream, TrajectoryEdgeStream

from pprint import pprint


class TrajectoryEdgeConverter():
    """Trajectory network constructor singleton class.

    Params
    ------
    sorted : boolean (optional, default: True)
        Whether to sort the output by start time or not.
    """

    def __init__(self, sort=True):
        """Initialize the converter with user-specified parameters.

        Params
        ------
        sorted : boolean (optional, default: True)
            Whether to sort the output by start time or not.
        """
        self.sort = sort


    def get_edge(self, stream):
        """Iteratively get single edges from a trajectory network.

        Items are sorted by end time or simply unsorted.

        Params
        ------
        stream : TrajectoryNetStream
            An iterator over Graphs (trajectory network snapshots).

        Returns
        -------
        Iterator : dict
            An unsorted iterator over single trajectory network edges.
        """
        
        active = {}
        next_edges = set()

        for G in stream:
            print("Converting graph for time: {}".format(G.time), end="\r")

            # get edges in this timestamp, guarantee unique ids
            prev_edges = next_edges
            next_edges = set(tuple(sorted(edge)) for edge in G.edges)

            # new edges, store start time and add to heap
            for edge in next_edges - prev_edges:
                active[edge] = (G.time, None)

            # update finished edges
            for edge in prev_edges - next_edges:
                active[edge] = (active[edge][0], G.time - 1)
                edge_dict = {'from': edge[0], 'to': edge[1],
                    'first': active[edge][0], 'last': active[edge][1]}
                del active[edge]
                yield edge_dict

        print("")


    def get_edge_sorted(self, stream):
        """Iteratively get single edges from a trajectory network.

        Uses a heap to make sure edges are sorted by start time.

        Params
        ------
        stream : TrajectoryNetStream
            An iterator over Graphs (trajectory network snapshots).

        Returns
        -------
        Iterator : dict
            A sorted iterator over single trajectory network edges.

        """
        
        active = {}
        heap = []
        next_edges = set()

        for G in stream:
            print("Converting graph for time: {}".format(G.time), end="\r")

            # get edges in this timestamp, guarantee unique ids
            prev_edges = next_edges
            next_edges = set(tuple(sorted(edge)) for edge in G.edges)

            # new edges, store start time and add to heap
            for edge in next_edges - prev_edges:
                heapq.heappush(heap, (G.time, edge))

                # add entry to dict as a list in case of multiple contacts
                active[edge] = active.get(edge, []) + [(G.time,None)]

            # update finished edges (always the last contact in the list)
            for edge in prev_edges - next_edges:
                active[edge][len(active[edge])-1] = (active[edge][0][0],
                                                     G.time-1)

            # check top of heap for finished edges
            while(len(heap) > 0 and active[heap[0][1]][0][1] is not None):
                edge = heapq.heappop(heap)[1]
                contact = active[edge].pop(0)
                edge_dict = {'from': edge[0], 'to': edge[1],
                    'first': contact[0], 'last': contact[1]}

                # if no more multiple contacts left, delete pair
                if len(active[edge]) == 0:
                    del active[edge]

                yield edge_dict

        print("")


    def get_edge_stream(self, stream):
        """Convert given network to an edge stream format.

        Params
        ------
        stream : TrajectoryNetStream
            An iterator over Graphs (trajectory network snapshots).

        Returns
        -------
        TrajectoryEdgeStream
            The generated trajectory network as a TrajectoryEdgeStream.
        """

        if self.sort:
            iterator = self.get_edge_sorted(stream)

        else:
            iterator = self.get_edge(stream)

        id = str(stream.id)
        id = id.replace("trajectory_networks", "trajectory_edges")

        return TrajectoryEdgeStream(items=iterator, id=id)
            
