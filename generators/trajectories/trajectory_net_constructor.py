"""Trajectory Network Constructor class

Implements the TrajectoryNetConstructor class, a class that handles
construction of trajectory networks from inital trajectory data.

"""

from networkx import Graph
import numpy as np
from itertools import combinations
from scipy.spatial.distance import pdist


from common.trajectories import Particle, ParticleStream, TrajectoryStream
from common.trajectories import TrajectoryNetStream


class TrajectoryNetConstructor():
    """Trajectory network constructor singleton class."""


    def get_proximitynet(self, stream, distance, save_position=False):
        """Get the proximity network for a single timestamp.
        
        Params
        ------
        stream : ParticleStream
            The iterator over Particles in that timestep
        distance : int or float
            The distance threshold within which objects are considered
            connected.
        save_position : boolean (optional, default: False)
            Whether to save particle positions as data in nodes.
        
        Returns
        -------
        networkx.Graph
            The proximity network for that timestamp.
        """

        print("Constructing trajectory network for time: {}"
            .format(stream.time), end="\r")
        G = Graph()
        particles = list(stream)
        if save_position:
            G.add_nodes_from((p.id, {'pos': p.position}) for p in particles)
        else:
            G.add_nodes_from(p.id for p in particles)

        pos = np.array([p.position for p in particles])

        if len(pos) > 1:
            all_distances = pdist(np.array(pos))
            valid_pairs = (np.array(list(combinations(range(len(pos)), 2)))
                [all_distances < distance])

            for node_from, node_to in valid_pairs:
                if node_from != node_to:
                    G.add_edge(particles[node_from].id, particles[node_to].id)

        G.time = int(float(stream.time))
        return G


    def get_trajectorynet(self, stream, distance=50):
        """Get a trajectory network from the provided trajectories.

        Params
        ------
        stream : TrajectoryStream
            An iterator over ParticleStream objects.
        distance : int or float (optional, default: 50)
            The distance threshold within which objects are considered
            connected.

        Returns
        -------
        TrajectoryNetStream
            The generated regions in a TrajectoryNetStream.
        """

        id = stream.id
        id = id.replace("trajectories", "trajectory_network")
        iterator = (self.get_proximitynet(ps, distance)
                for ps in stream)

        return TrajectoryNetStream(items=iterator, id=id,
            dimension=stream.dimension)
