"""Trajectory Generator class

Implements the TrajectoryGenerator class, a class that handles random
generation of particle objects.

"""

import random

from common.trajectories import Particle, ParticleStream, TrajectoryStream
from generators.common import Randoms, SpatialGenerator, TimeGenerator


class TrajectoryGenerator(SpatialGenerator,TimeGenerator):
    """Particle generator singleton class.

    Params
    ------
    bounds : Region (optional, default: None)
        A region with the outer bounds of the observation space
    dimension : int (optional, default: bounds or 1)
        The number of dimensions of all Particles generated
    posrng : method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing the position of Particles.
    duration : int (optional, default: 1000)
        The duration of the simulation/generation
    timerng : method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing Particle appearance times.
    initial : float (optional, default: 0)
        The fraction of objects to be pre-generated at t=0
    speed : int or float (optional, default: 1)
        The maximum initial speed of objects (before acceleration)
    rnd_accel : bool (optional, default: False - constant)
        Flag that controls whether the particle will move in a
        constant or a random pattern.
    """
    
    def __init__(self, bounds=None, dimension=None, posrng=Randoms.uniform(),
                 duration=1000, timerng=Randoms.uniform(), initial=0,
                 speed=10, rnd_accel=False):
        """Initialize the data generator with user-specified parameters.

        Params
        ------
        bounds : Region (optional, default: None)
            A region with the outer bounds of the observation space
        dimension : int (optional, default: bounds or 1)
            The number of dimensions of all Particles generated
        posrng : method or list of methods (optional,default: uniform)
            The random number generator or list of random number
            generator options for choosing the position of Particles.
        duration : int (optional, default: 1000)
            The duration of the simulation/generation
        timerng : method or list of methods (optional,default: uniform)
            The random number generator or list of random number
            generator options for choosing Particle appearance times.
        initial : float (optional, default: 0)
            The fraction of objects to be pre-generated at t=0
        speed : int or float (optional, default: 1)
            The maximum initial speed of objects (before acceleration)
        rnd_accel : bool (optional, default: False - constant)
            Flag that controls whether the particle will move in a
            constant or a random pattern.
        """

        super().__init__(bounds=bounds,dimension=dimension,posrng=posrng,
                         duration=duration, timerng=timerng, initial=initial)

        self.speed = speed
        self.rnd_accel = rnd_accel



    def generate_particle(self, at_edge = False):
        """Generate a single particle according to generator params.

        Params
        ------
        at_edge : boolean
            Flag that controls if the particle will be generated at
            the edge of space or not.

        Returns
        -------
        Particle
            The generated Particle object.
        """

        # select position, velocity
        point = self.get_point()
        lower = [-self.speed for d in range(self.dimension)]
        upper = [self.speed for d in range(self.dimension)]

        # select dimension and edge where the particle will be placed
        if at_edge:
            d = random.randrange(self.dimension)

            if random.randint(0,1) == 0: # lower edge picked
                point[d] = self.bounds.factors[d].lower
                lower[d] = 0
            else: # upper edge picked
                point[d] = self.bounds.factors[d].upper
                upper[d] = 0

        particle = Particle(position=point)
        particle.randomize_velocity(lower=lower, upper=upper)
        return particle


    def generate_particles(self, n, time):
        """Get a stream of particles for a single timestamp.
        
        Params
        ------
        n : int
            The number of geenrated objects.
        time : int
            The timestamp this corresponds to.
        
        Returns
        -------
        ParticleStream
            An iterator over newly generated particle objects
        """

        at_edge = (time != 0)

        return ParticleStream((self.generate_particle(at_edge)
            for i in range(n)))


    def simulate_particles(self, particles):
        """Simulate the movement of all objects for a single timestamp.

        Params
        ------
        particles : ParticleStream
            The iterator over all Particles in that timestamp

        Returns
        -------
        ParticleStream
            An iterator over updated particle objects for this timestep
        """

        for particle in particles:

            if self.rnd_accel:
                particle.randomize_acceleration()
            particle.move()

            if self.bounds.contains(particle.position):
                yield particle

        
    def get_particle_stream(self, time_counts):
        """Simulate the movement of all objects for a single timestamp.

        Params
        ------
        time_counts : dict
            The counts of objects to be generated every timestep.

        Returns
        -------
        ParticleStream
            An iterator over updated particle objects for this timestep
        """

        active = []
        for t in range(self.duration):

            # add newly generated particles and simulate timestamp
            active = list(self.simulate_particles(active))
            active += list(self.generate_particles(time_counts[t], t))

            yield ParticleStream(time=t, items=(a for a in active))
        


    def get_trajectory_stream(self, n):
        """Randomly generate N moving object trajectories.

        Generation happens according to generator parameters.

        Params
        ------
        n : int
            The number of trajectories the stream should contain.

        Returns
        -------
        TrajectoryStream
            The generated trajectories in a TrajectoryStream.
        """

        # how many objects will be generated every timestamp
        time_counts = { t:0 for t in range(self.duration) }
        time_counts[0] = int(n * self.initial)

        # determine generation times of remaining objects
        for i in range(n - int(n * self.initial)):
            time_counts[self.get_moment()] += 1

        return TrajectoryStream(self.get_particle_stream(time_counts))