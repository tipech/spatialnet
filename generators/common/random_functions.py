"""Random Number Generators

Implements the Randoms class, a static class that provides factory
methods that each return Callable (lambdas), preconfigured to generate
random values based on a particular distribution or random number
generation function.

The only missing parameters in the lambda functions are the lower and
upper bounds of the values generated.

"""

from functools import partial

import random



class Randoms:
    """Static class providing random generation factory methods.

    Included factory methods return Callable (lambdas) that are
    preconfigured to generate random values based on a particular
    distribution or random number generation function.

    The only missing parameters are the lower and upper bounds
    of the values generated.
    """

    @classmethod
    def get(cls, name, **kwargs) :
        """Get a function that draws samples from a distribution.
         
        Passes given arguments as parameter for that factory method.

        Params
        ------
        name : str
            The name of random number generator for factory method
            that generated random number generators.
        kwargs : dict
            Arguments as parameter for that factory method.

        Returns
        -------
        Callable
            The factory method that generated random
            number generators, with params:

            lower:
                The lower bounding value of the range from
                which random values are to be generated.
            upper:
                The upper bounding value of the range from
                which random values are to be generated.
        """

        return getattr(cls, name)(**kwargs)


    @classmethod
    def list(cls):
        """ Lists available random number generators (distributions).

        Returns
        -------
        str
            The list of available random number
            generators (distributions).
        """
        excluded = ['get', 'list']
        israndng = lambda f: all([callable(getattr(cls, f)), f not in excluded,
                                                            not f.startswith('_')])

        return [f for f in dir(cls) if israndng(f)]

    ### Class Methods: Random Number Generators


    @classmethod
    def uniform(cls) :
        """Get a function drawing samples from a uniform distribution.

        Samples are uniformly distributed over the half-open interval
        [low, high) (includes low, but excludes high). In other words,
        any value within the given interval is equally likely to be
        drawn by uniform.

        Returns
        -------
        Callable
            A factory function that draws samples
            from a uniform distribution.
        """
        def uniform_rng(lower=0, upper=1):
            return random.uniform(lower, upper)

        return uniform_rng


    @classmethod
    def triangular(cls, mode=0.5) :
        """Get a function drawing samples from a triangular distribution.

        The triangular distribution is a continuous probability
        distribution with lower limit left, peak at mode, and
        upper limit right.

        Unlike the other distributions, these parameters directly
        define the shape of the probability distribution function (pdf).

        Params
        ------
        mode : float or list of floats (optional, default: 0.5)
            The peak value of the triangular distribution as
            a percentage of the total length, or a list of them for
            each dimension.

        Returns
        -------
        Callable
            A factory function that draws samples
            from a triangular distribution.
        """
        
        def triangular_rng(left=0, right=1, mode=mode):
            return random.triangular(left, right, (right - left)*mode + left)
        
        if isinstance(mode, list):
            return [partial(triangular_rng, mode=m) for m in mode]
        else:
            return triangular_rng


    @classmethod
    def gauss(cls, mean=0.5, sigma=0.2) :
        """Get a function drawing samples from a gaussian distribution.

        The gaussian distribution is a continuous probability
        distribution with lower limit left, mean at mean,
        standard deviation sigma and upper limit right.

        Params
        ------
        mean : float or list of floats (optional, default: 0.5)
            The mean value of the gaussian distribution as
            a percentage of the total length, or a list of them for
            each dimension.
        sigma : float or list of floats (optional, default: 0.2)
            The standard deviation of the gaussian distribution as
            a percentage of the total length, or a list of them for
            each dimension.

        Returns
        -------
        Callable
            A factory function that draws samples
            from a gaussian distribution.
        """

        def gauss_rng(left=0, right=1, mean=mean, sigma=sigma):
            return max(left, min(right,
                random.gauss((right - left)*mean + left, (right - left)*sigma)))

        if not isinstance(mean, list) and not isinstance(sigma, list):
            return gauss_rng
        
        if not isinstance(mean, list):
                mean = [mean for d in range(len(sigma))]
        if not isinstance(sigma, list):
                sigma = [sigma for d in range(len(mean))]

        return [partial(gauss_rng, mean=mean[d], sigma=sigma[d])
            for d in range(len(mean))]
    

    @classmethod
    def bimodal(cls, mean1=0.2, sigma1=0.1, mean2=0.8, sigma2=0.1) :
        """Get a function drawing samples from a bimodal gauss distribution.

        This distribution is a combination of two gaussian probability
        distributions with lower limit left, upper limit right, and\
        two respective mean and sigma vaules.

        Params
        ------
            mean1 : float or list of floats (optional, default: 0.2)
            mean2 : float or list of floats (optional, default: 0.8)
                The mean values of the gaussian
                distributions as a percentage of the
                total length.
            sigma1 : float or list of floats (optional, default: 0.1)
            sigma2 : float or list of floats (optional, default: 0.1)
                The standard deviations of the gaussian
                distributions as a percentage of the
                total length.

        Returns
        -------
        Callable
            A factory function that draws samples
            from a bimodal gaussian distribution.
        """

        def bimodal_rng(left=0, right=1, d=None):
            return max(left, min(right, random.choice(
                [random.gauss((right - left)*mean1 + left, (right - left)*sigma1),
                 random.gauss((right - left)*mean2 + left, (right - left)*sigma2)])
            ))

        return bimodal_rng
            

    @classmethod
    def hotspot(cls, dimension, n, min_mean=0, max_mean=1,
                min_sigma=0.05, max_sigma=0.2) :
        """Get a function drawing samples from a gauss hotspot distribution.

        This distribution is a combination of n gaussian probability
        distributions (hotspots) with lower limit left, upper limit
        right, and mean and sigma vaules between min and max.

        Params
        ------
        n : int
            Number of hotspots
        dimension : int
            The number of dimensions
        min_mean, max_mean : float (optional, default: 0, 1)
            Minimum and maximum mean values of the
            gaussian distributions as a percentage
            of the total length.
        min_sigma, min_sigma : float (optional, default: 0.05, 0.2)
            Minimum and maximum standard deviations
            of the gaussian distributions as a
            percentage of the total length.

        Returns
        -------
        Callable
            A factory function that draws samples
            from a hotspot distribution.
        """

        def hotspot_rng(left=0, right=1, mean=[], sigma=[]):
            
            mean = random.choice(mean)
            sigma = random.choice(sigma)

            return max(left, min(right, random.gauss(
                (right - left)*mean + left, (right - left)*sigma)))

        hotspots = []

        for d in range(dimension):
            mean = [random.uniform(min_mean, max_mean) for i in range(n)]
            sigma = [random.uniform(min_sigma, max_sigma) for i in range(n)]
        
            hotspots.append(partial(hotspot_rng, mean=mean, sigma=sigma))

        return hotspots
