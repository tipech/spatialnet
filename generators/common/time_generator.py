"""Time Generator class

Implements the TimeGenerator class, a generic class that provides common
behavior for all generators dealing with creating objects over time.

"""

import random

from spatialnet.generators.common import Randoms


class TimeGenerator():
    """Time generator singleton class.

    Random generation of temporal objects.

    Params
    ------
    duration : int (optional, default: 1000)
        The duration of the simulation/generation
    timerng: method or list of methods (optional, default: uniform)
        The random number generator or list of random number
        generator options for choosing object appearance times
    initial : float (optional, default: 0)
        The fraction of objects to be pre-generated at t=0
    """
    def __init__(self, duration=1000, timerng=Randoms.uniform(), initial=0,
                 **kwargs):
        """Initialize data generator with user-specified parameters.

        Params
        ------
        duration : int (optional, default: 1000)
            The duration of the simulation/generation
        timerng: method or list of methods (optional, default: uniform)
            The random number generator or list of random number
            generator options for choosing object appearance times
        initial : float (optional, default: 0)
            The fraction of objects to be pre-generated at t=0
        """
        
        super().__init__(**kwargs)

        self.duration = duration
        self.timerng = timerng
        self.initial = initial


    def get_moment(self):
        """Get random moment within the duration according to timerng.

        Returns
        -------
        int
            The randomly selected moment.
        """

        return int(self.timerng(0, self.duration))
