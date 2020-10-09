"""Trajectory Visualizer class

Implements the TrajectoryVisualizer class, a class that provides common
behavior for all visualizers dealing with drawing object on screen.

"""

from matplotlib import pyplot as plt

from common.regions import Region, RegionStream
from visualizers import BaseVisualizer


class RegionVisualizer(BaseVisualizer):
    """Singleton class for region visualization.

    Params
    ------
    object_stream : RegionStream
        The input set of regions to visualize.
    dpi : int (optional, default: 100)
        The visualization resolution in dots/pixels per inch.
    width : float (optional, default: 7)
        The width of the visualization window in inches.
    height : float (optional, default: 6.5)
        The height of the visualization window in inches.
    region_color : str (optional, default: '0.75' - gray)
        The color of the drawn regions in matplotlib format.
    """

    def __init__(self, object_stream, dpi=100, width=7, height=6.5,
                 region_color='0.75'):
        """Initialize data visualization with user-specified parameters.

        Params
        ------
        object_stream : RegionStream
            The input set of regions to visualize.
        dpi : int (optional, default: 100)
            The visualization resolution in dots/pixels per inch.
        width : float (optional, default: 7)
            The width of the visualization window in inches.
        height : float (optional, default: 6.5)
            The height of the visualization window in inches.
        region_color : str (optional, default: '0.75' - gray)
            The color of the drawn regions in matplotlib format.
        """

        super().__init__(object_stream=object_stream, dpi=dpi, width=width,
                         height=height)

        self.region_color = region_color


        for region in object_stream:
            self.shapes[region.id] = plt.Rectangle(
                (region.factors[0].lower, region.factors[1].lower),
                region.lengths[0], region.lengths[1],
                fc=self.region_color, ec='black')

            self.ax.add_patch(self.shapes[region.id])


    def show(self):
        """Display the visualization window and run the animation."""

        super().show()