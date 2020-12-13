"""Particle Class

Implements the Particle class, a data class that defines a single
particle, with a number of dimensions and respective coords.

"""

from math import sqrt

from spatialnet.common.generic.objects import IdObject, MovingObject, SerializableObject


class Particle(IdObject,MovingObject,SerializableObject):
    """A representation of a particle in multidimensional space.
   
    Params
    ------
    position : list
        List of coordinates for each dimension.
    velocity : list of floats
        The velocity vector of the object
    acceleration:
        The acceleration vector of the object
    id : str or int
        The unique identifier for this Region
        Randonly generated with UUID v4, if not provided.
    """

    def __init__(self, position, velocity=None, acceleration=None, id=''):
        """Construct a new Particle from the given list of coordinates.

        Params
        ------
        position : list
            List of coordinates for each dimension.
        velocity : list of floats
            The velocity vector of the object
        acceleration:
            The acceleration vector of the object
        id : str or int
            The unique identifier for this Region
            Randonly generated with UUID v4, if not provided.
        """

        super().__init__(position=position, velocity=velocity,
                         acceleration=acceleration, id=id)


    ### Methods: Queries

    def __eq__(self, other):
        """Determine if the given Particle equals to this Particle.

        The two Particles are equal if have the same position
        (same coords for all dimensions), otherwise they are not.

        Return True if the two Regions are equal, otherwise False.

        Is syntactic sugar for:
            self == other

        Params
        ------
        other : Particle
            The other Particle to test if it has the
            same coordinates for all dimensions.

        Returns
        -------
        bool
            True:     If the two Particles are equal.
            False:    Otherwise.
        """
        return (isinstance(other, Particle) and 
                self.dimension == other.dimension and 
                all([f == other.position[i] 
                    for i, f in enumerate(self.position)]))


    def get_distance_to(self, other: 'Particle'):
        """Determine the Eucledean distance to the given Particle.

        Params
        ------
        other : Particle
            The other Particle.

        Returns
        -------
        float
            The distance between the two particles
        """
        return sqrt(sum((f - other.position[i])**2
            for i, f in enumerate(self.position)))


    ### Methods: Representations

    def __repr__(self):
        """Get a human-readable string representation of an object.

        Returns
        -------
        str
            String representation of an object.
        """
        dictobj = {
            'id': self.id[0:8] if len(self.id) > 8 else self.id,
            'd': self.dimension,
            'position': self.position,
            'velocity': self.velocity,
            'accel': self.acceleration
        }

        kvpairs = ', '.join('{}={}'.format(k,v) for k,v in dictobj.items())
        return '{}({})'.format(self.__class__.__name__,kvpairs)


    ### Methods: Deserialization

    @classmethod
    def from_dict(cls, dictObject):
        """Restore a Particle object using a dict representation.

        Params
        ------
        dictObject : dict
            A dictionary representation of an object.
            
        Returns
        -------
        Particle
            The corresponding serialized object
        """

        del dictObject['dimension']

        return Particle(**dictObject)