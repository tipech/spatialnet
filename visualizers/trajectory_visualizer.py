"""Trajectory Visualizer class

Implements the TrajectoryVisualizer class, a class that provides common
behavior for all visualizers dealing with drawing object on screen.

"""

from matplotlib import pyplot as plt
from matplotlib import animation

from common.regions import Region
from common.trajectories import TrajectoryStream
from visualizers import BaseVisualizer


class TrajectoryVisualizer(BaseVisualizer):
    """Singleton class for trajectory visualization.

    Params
    ------
    object_stream : TrajectorySet
        The input set of trajectories to visualize.
    dpi : int (optional, default: 100)
        The visualization resolution in dots/pixels per inch.
    width : float (optional, default: 7)
        The width of the visualization window in inches.
    height : float (optional, default: 6.5)
        The height of the visualization window in inches.
    interval : int (optional, default: 20)
        The delay between frames in milliseconds.
    blit : bool (optional, default: False)
        Controls whether blitting is used to optimize drawing.
        When using blitting any animated artists will be drawn
        according to their zorder.
    point_size : int (optional, default: 10)
        The size of the drawn points in pixels.
    point_color : str (optional, default: 'y' - yellow)
        The color of the drawn points in matplotlib format.
    """

    def __init__(self, object_stream, dpi=100, width=7, height=6.5,
                 interval=20, blit=False, point_size=10, point_color='b'):
        """Initialize data visualization with user-specified parameters.

        Params
        ------
        object_stream : TrajectorySet
            The input set of trajectories to visualize.
        dpi : int (optional, default: 100)
            The visualization resolution in dots/pixels per inch.
        width : float (optional, default: 7)
            The width of the visualization window in inches.
        height : float (optional, default: 6.5)
            The height of the visualization window in inches.
        interval : int (optional, default: 20)
            The delay between frames in milliseconds.
        blit : bool (optional, default: False)
            Controls whether blitting is used to optimize drawing.
            When using blitting any animated artists will be drawn
            according to their zorder.
        point_size : int (optional, default: 10)
            The size of the drawn points in pixels.
        point_color : str (optional, default: 'y' - yellow)
            The color of the drawn points in matplotlib format.
        """

        super().__init__(object_stream=object_stream, dpi=dpi, width=width,
                         height=height)

        self.interval = interval
        self.blit = blit
        self.point_size = point_size
        self.point_color = point_color

        self.timer = self.ax.text(2, -48, '0', fontsize=15)


    def animate(self, frame):
        """Perform one timestep of the animation.

        Params
        ------
        frame : ParticleStream
            The next frame from the trajectory set.

        Returns
        -------
        list
            A list of actors for this frame
        """

        self.timer.set_text(str(frame.time + 1))

        # determine new and old objects
        pos_dict = {p.id: p.position for p in frame}
        prev_items = set(self.shapes.keys())
        next_items = set(pos_dict.keys())

        # new nodes
        for n_id in next_items - prev_items:
            self.shapes[n_id] = plt.Circle(pos_dict[n_id],
                self.point_size, fc=self.point_color)
            self.ax.add_patch(self.shapes[n_id])

        # updated nodes
        for n_id in next_items.intersection(prev_items):
            self.shapes[n_id].center = pos_dict[n_id]

        # exited nodes
        for n_id in prev_items - next_items:
            self.shapes[n_id].remove()
            del self.shapes[n_id]

        return self.shapes.values()


    def show(self):
        """Display the visualization window and run the animation."""

        anim = animation.FuncAnimation(self.fig, self.animate,  
           frames=list(self.object_stream), repeat=False,
           interval=self.interval, blit=self.blit)

        super().show()