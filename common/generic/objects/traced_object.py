"""Base Definition for TracedObject

Defines a generic class and handling for objects whose origins will be
traced.
"""

class TracedObject():
    """Generic class for an object with traced origins.

    These objects have been created from combinations of other objects,
    and the TracedObject class provides the functionality to track
    the chain of objects back to the original ones.

    Params
    ------
    ancestors : set, list or dict (optional, default: None - origin)
        Parents of these object, if they exist.
    kwargs : dict
        Further keyword arguments, added for super() compatibility
    """

    def __init__(self, ancestors=None, **kwargs):
        """Initialize traced object, if no ancestors set as original.

        Params
        ------
        ancestors : set, list or dict (optional, default: None-origin)
            Parents of this object, if they exist.        
        kwargs : dict
            Further keyword arguments, added for super() compatibility
        """

        super().__init__(**kwargs)
        
        if ancestors is None:
            self.ancestors = {self.id}

        # if given a set of traced objects
        elif all(hasattr(a, 'ancestors') for a in ancestors):
            self.ancestors = set(a for a.ancestors in ancestors)

        else:
            self.ancestors = set(ancestors)