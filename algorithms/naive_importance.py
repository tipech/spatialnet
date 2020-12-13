import networkx as nx

from spatialnet.common.trajectories import TrajectoryStream
from pprint import pprint

class NaiveImportance():
    """Naive algorithm for node importance calculation."""

    def get_degree_profile(self, stream):
        """Construct node profiles.

        Params
        ------
        stream : TrajectoryStream
            The input data stream of ParticleStream objects
        """

        degree = {}

        for G in stream:
            # calculate degree of the current snapshot
            G_degrees = nx.degree(G)

            # store metric for every node
            for node, value in G_degrees:

                # new node, create value dict and add value with duration 1
                if node not in degree:
                    degree[node] = {value: 1}

                # this node existed, add or increment duration for this value
                else:
                    degree[node][value] = degree[node].get(value, 0) + 1

        return degree


    def get_importance(self, stream):
        """Calculate node importance metrics for input data.

        Params
        ------
        stream : TrajectoryStream
            The input data stream of ParticleStream objects
        """

        degrees = self.get_degree_profile(stream)

        results = {node:sum(value*duration for value, duration in values.items())
            for node, values in degrees.items()}

        return sorted(results.items(), key=lambda x: x[1], reverse=True)