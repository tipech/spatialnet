
from pprint import pprint

from common.regions import Region
from common.regions import RegionStream

from generators.trajectories import TrajectoryGenerator
from common.trajectories import TrajectoryStream, TrajectoryNetStream
from visualizers import TrajectoryVisualizer, TrajectoryNetVisualizer

from generators.trajectories import TrajectoryNetConstructor, TrajectoryEdgeConverter
from algorithms import NaiveImportance


# pgenerator = TrajectoryGenerator(duration=500, initial=.05, speed=10, rnd_accel=True)
# tstream = pgenerator.get_trajectory_stream(300)
# tstream.store('data/test.json')


# tstream = TrajectoryStream.load('data/test.json')  
# tnetstream = TrajectoryNetConstructor().get_trajectorynet(tstream, 100)
# print(list(tstream))
# tstream.calculate_bounds()
# tnetstream.store('data/test2.json')

# tnetstream = TrajectoryNetStream.load('data/test2.json')
# tnedgestream = TrajectoryEdgeConverter().get_edge_stream(tnetstream)
# tnedgestream.store('data/test3.json')

tstream = TrajectoryNetStream.load('data/test2.json')  
ni = NaiveImportance()
importance = ni.get_importance(tstream)
pprint(importance[:10])

# viz = TrajectoryVisualizer(tstream)
# viz = TrajectoryNetVisualizer(tnetstream, interval=30)
# viz.show()