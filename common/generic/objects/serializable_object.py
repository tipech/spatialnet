"""Base Definition for SerializableObject

Defines a generic class objects (de)serialization.

Generic Classes:
- SerializableObject
"""

from jsonpickle import Pickler


class SerializableObject(object):
    """Generic class for a (de)serializable object."""


    def to_dict(self):
        """Get a dictionary representation of this object.

        Recursively serialize objects in attributes, if any.

        Returns
        -------
        dict
            A dict representation of this object.
        """

        # if object is iterator
        if(hasattr(self,'__iter__')):
            result = dict(vars(self).items())
            result['items'] = [obj.to_dict() for obj in self]
            return result

        else:
            return Pickler(unpicklable=False).flatten(self)


    @classmethod
    def from_dict(cls, dictObject):
        """Restore an object using a dict representation.

        Params
        ------
        dictObject : dict
            A dictionary representation of an object.
            
        Returns
        -------
        SerializableObject
            The corresponding serialized object
        """

        raise NotImplementedError('from_dict() in %s' % cls.__name__)
