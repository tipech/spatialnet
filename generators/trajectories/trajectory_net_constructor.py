"""Trajectory Network Constructor class

Implements the TrajectoryNetConstructor class, a class that handles
construction of trajectory networks from inital trajectory data.

"""

import random
from networkx import Graph
from common.trajectories import Particle, ParticleStream, TrajectoryStream
from common.trajectories import TrajectoryNetStream


class TrajectoryNetConstructor():
    """Trajectory network constructor singleton class."""


    def get_proximitynet(self, stream, distance):
        """Get the proximity network for a single timestamp.
        
        Params
        ------
        stream : ParticleStream
            The iterator over Particles in that timestep
        distance : int or float
            The distance threshold within which objects are considered
            connected.
        
        Returns
        -------
        networkx.Graph
            The proximity network for that timestamp.
        """
        G = Graph()
        particles = list(stream)
        G.add_nodes_from((p.id, {'pos': p.position}) for p in particles)

        for i in range(len(particles)):
            for j in range(i):
                if particles[i].get_distance_to(particles[j]) < distance:
                    G.add_edge(particles[i].id, particles[j].id)
                   
        G.time = stream.time 
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
        id = id.replace("trajectories", "trajectory_networks")
        iterator = (self.get_proximitynet(ps, distance)
                for ps in stream)

        return TrajectoryNetStream(items=iterator, id=id,
            dimension=stream.dimension)
