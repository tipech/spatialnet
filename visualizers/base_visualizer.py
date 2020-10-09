"""Base Visualizer class

Implements the BaseVisualizer class, a generic class that provides common
behavior for all visualizers dealing with drawing object on screen.

"""

from matplotlib import pyplot as plt

from common.regions import Region


class BaseVisualizer():
    """Generic spatial visualization singleton class.

    Params
    ------
    object_stream : BaseStream
        The input iterator of spatial objects to visualize.
    dpi : int (optional, default: 100)
        The visualization resolution in dots/pixels per inch.
    width : float (optional, default: 7)
        The width of the visualization window in inches.
    height : float (optional, default: 6.5)
        The height of the visualization window in inches.
    """

    def __init__(self, object_stream, dpi=100, width=7, height=6.5):
        """Initialize data visualization with user-specified parameters.

        Params
        ------
        object_stream : BaseStream
            The input iterator of spatial objects to visualize.
        dpi : int (optional, default: 100)
            The visualization resolution in dots/pixels per inch.
        width : float (optional, default: 7)
            The width of the visualization window in inches.
        height : float (optional, default: 6.5)
            The height of the visualization window in inches.
        """


        self.fig = plt.figure()
        self.fig.set_dpi(dpi)
        self.fig.set_size_inches((width, height))

        self.object_stream = object_stream

        space = object_stream.calculate_bounds().factors
        self.ax = plt.axes(xlim=(space[0].lower, space[0].upper),
                           ylim=(space[1].lower, space[1].upper),
                           xticks=[], yticks=[])

        self.shapes = {}


    def show(self):
        """Display the visualization window."""

        plt.show()