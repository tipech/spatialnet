"""Base Definition for IdObject

Defines a generic class and handling for objects that will have
a unique id.
"""

from uuid import uuid4

class IdObject(object):
    """Generic class for an object with (auto) assigned id.

    Params
    ------
    id : str or int (optional, default: '', i.e. generate a uuid)
        The id of the object.
    kwargs : dict
        Further keyword arguments, added for super() compatibility
    """

    def __init__(self, id='', **kwargs):
        """Initialize object with id, generate it if not provided.

        Params
        ------
        id : str or int (optional, default: '', i.e. generate a uuid)
            The id of the object.
        kwargs : dict
            Further keyword arguments, added for super() compatibility
        """

        if len(str(id)) == 0:
            id = str(uuid4())[:8]

        self.id = id
        
        super().__init__(**kwargs)


    ### Methods: Syntactic sugar

    def __hash__(self):
        """Return the hash value for this object.

        Two objects that compare equal must also have the same hash
        value, but the reverse is not necessarily true.

        Returns
        -------
        int
            The hash value for this object.
        """

        return hash(self.id)