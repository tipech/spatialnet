"""Base Definition for MovingObject

Defines a generic class for movement behavior.
"""

import random


class MovingObject():
    """Abstract class for moving objects.


    Params
    ------
    position : list of floats
        The position vector of the object
    velocity : list of floats (optional, default: 0)
        The velocity vector of the object
    acceleration : list of floats (optional, default: 0)
        The acceleration vector of the object
    kwargs:
        Further keyword arguments, added for super() compatibility
    """


    def __init__(self, position, velocity=None, acceleration=None, **kwargs):
        """Initialize a new generic moving object.

        Params
        ------
        position : list of floats
            The position vector of the object
        velocity : list of floats (optional, default: 0)
            The velocity vector of the object
        acceleration : list of floats (optional, default: 0)
            The acceleration vector of the object
        kwargs:
            Further keyword arguments, added for super() compatibility
        """

        super().__init__(**kwargs)

        self.dimension = len(position)

        # if no velocity/acceleration given initialize to 0 based on dimension
        if velocity is None:
            velocity = [0 for i in range(self.dimension)]
        if acceleration is None:
            acceleration = [0 for i in range(self.dimension)]

        self.position = [float(i) for i in position]
        self.velocity = [float(i) for i in velocity]
        self.acceleration = [float(i) for i in acceleration]


    def randomize_position(self, lower=-1000, upper=1000):
        """Assign random position value for every dimension, bounded.

        Params
        ------
        lower : float or list of floats
            The lower random bound (default: -1000)
        upper : float or list of floats
            The upper random bound (default: 1000)
        """
        if not isinstance(lower, list):
            lower = [lower for d in range(self.dimension)]
        if not isinstance(upper, list):
            upper = [upper for d in range(self.dimension)]

        for d in range(self.dimension):
            self.position[d] = random.uniform(lower[d], upper[d])


    def randomize_velocity(self, lower=-1, upper=1):
        """Assign random velocity value for every dimension, bounded.

        Params
        ------
        lower : float or list of floats
            The lower random bound (default: -1)
        upper : float or list of floats
            The upper random bound (default: 1)
        """

        if not isinstance(lower, list):
            lower = [lower for d in range(self.dimension)]
        if not isinstance(upper, list):
            upper = [upper for d in range(self.dimension)]

        for d in range(self.dimension):
            self.velocity[d] = random.uniform(lower[d], upper[d])


    def randomize_acceleration(self, lower=-1, upper=1):
        """Assign random acceleration value for every dimension, bounded.

        Params
        ------
        lower : float or list of floats
            The lower random bound (default: -1)
        upper : float or list of floats
            The upper random bound (default: 1)
        """

        if not isinstance(lower, list):
            lower = [lower for d in range(self.dimension)]
        if not isinstance(upper, list):
            upper = [upper for d in range(self.dimension)]

        for d in range(self.dimension):
            self.acceleration[d] = random.uniform(lower[d], upper[d])


    def move(self):
        """Perform a single movement step, apply acceleration and velocity."""

        for d in range(self.dimension):
            self.velocity[d] += self.acceleration[d]
            self.position[d] += self.velocity[d]