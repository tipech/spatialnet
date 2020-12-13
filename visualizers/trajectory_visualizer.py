"""Trajectory Visualizer class

Implements the TrajectoryVisualizer class, a class that provides common
behavior for all visualizers dealing with drawing object on screen.

"""

from matplotlib import pyplot as plt
from matplotlib import animation

from spatialnet.common.regions import Region
from spatialnet.common.trajectories import TrajectoryStream
from spatialnet.visualizers import BaseVisualizer


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
                 point_size=1, point_color='b', show_labels=True, radius=0,
                 interval=20, blit=False):
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
        point_size : int (optional, default: 10)
            The size of the drawn points in pixels.
        point_color : str (optional, default: 'y' - yellow)
            The color of the drawn points in matplotlib format.
        show_labels : boolean (optional, default: True)
            Whether to show text labels of object ids.
        radius : float or dict (optional, default: 0 - none)
            The radius to use when drawing proximity threshold circle.
            If 0 is given, then no circle is drawn.
            If a dict is provided, circle is drawn only for ids present
            in dict, with the respective radius.
        interval : int (optional, default: 20)
            The delay between frames in milliseconds.
        blit : bool (optional, default: False)
            Controls whether blitting is used to optimize drawing.
            When using blitting any animated artists will be drawn
            according to their zorder.
        """

        super().__init__(object_stream=object_stream, dpi=dpi, width=width,
                         height=height)
        
        # adjust for axis size
        scale = self.ax.get_ylim()[1] - self.ax.get_ylim()[0]
        self.point_size = point_size * scale / 100
        self.point_color = point_color

        self.timer = self.ax.text(0.02, 0.5, '0', fontsize=15,
            transform=plt.gcf().transFigure)

        self.show_labels = show_labels
        if (isinstance(radius,int) or isinstance(radius,float)) and radius>0:
            self.radius = radius * scale / 100
        else:
            self.radius = {v_id:r * scale / 100 for v_id, r in radius.items()}

        self.interval = interval
        self.blit = blit


    def add_object(self, n_id, position):
        """Add a single point object to the plot.

        If specified, add text label and/or proximity threshold circle.

        Params
        ------
        n_id : str or int
            The id of the object ot be added. 
        position : tuple (x, y)
            The xy position of the object ot be added. 
        """

        # draw point
        shapes = [plt.Circle(position, self.point_size, fc=self.point_color)]

        # draw proximity threshold circle if needed
        if ((isinstance(self.radius, int) or isinstance(self.radius, float))
            and self.radius > 0):
            shapes.append(plt.Circle(position, self.point_size + self.radius, fill=None, ec="red"))

        elif isinstance(self.radius, dict) and n_id in self.radius:
            shapes.append(plt.Circle(position, self.point_size + self.radius[n_id], fill=None, ec="red"))

        # add shapes to drawing
        self.shapes[n_id] = shapes
        for patch in shapes:
            self.ax.add_patch(patch)

        # add text
        if self.show_labels:
            self.labels[n_id] = [plt.text(*position, n_id)]


    def move_object(self, n_id, position):
        """Move a single point object in the plot.

        If specified, move text label and/or proximity circle.

        Params
        ------
        n_id : str or int
            The id of the object ot be moved. 
        position : tuple (x, y)
            The xy position of the object ot be moved. 
        """

        # move shapes
        for patch in self.shapes[n_id]:
            patch.center = position

        # move text label
        if self.show_labels:
            for text in self.labels[n_id]:
                text.set_position(position)


    def remove_object(self, n_id):
        """Remove a single point object in the plot.

        If specified, remove text label and/or proximity circle.

        Params
        ------
        n_id : str or int
            The id of the object ot be removed. 
        """

        # remove shapes
        for patch in self.shapes[n_id]:
            patch.remove()
        del self.shapes[n_id]

        # remove text
        if self.show_labels:
            for text in self.labels[n_id]:
                text.remove()
            del self.labels[n_id]


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
            self.add_object(n_id, pos_dict[n_id])

        # updated nodes
        for n_id in next_items.intersection(prev_items):
            self.move_object(n_id, pos_dict[n_id])

        # exited nodes
        for n_id in prev_items - next_items:
            self.remove_object(n_id)

        return ([patch for e in self.shapes.values() for patch in e])


    def show(self):
        """Display the visualization window and run the animation."""

        anim = animation.FuncAnimation(self.fig, self.animate,  
           frames=list(self.object_stream), repeat=False,
           interval=self.interval, blit=self.blit)

        super().show()