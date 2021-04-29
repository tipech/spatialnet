

# from pprint import pprint

# from common.regions import Region
# from common.regions import RegionStream

# from generators.regions import RegionGenerator

# from generators.trajectories import TrajectoryGenerator
# from common.trajectories import TrajectoryStream, TrajectoryNetStream
# # from visualizers import TrajectoryVisualizer, TrajectoryNetVisualizer

# from generators.trajectories import TrajectoryNetConstructor, TrajectoryEdgeConverter
# from algorithms import NaiveImportance


# pgenerator = TrajectoryGenerator(duration=500, initial=.05, speed=10, rnd_accel=True)
# tstream = pgenerator.get_trajectory_stream(300)
# # tstream.fork().store(dir='data')

# # tstream = TrajectoryStream.load('data/test.json')  
# # tstream.calculate_bounds()
# # tnetstream = TrajectoryNetConstructor().get_trajectorynet(tstream, 100)
# # tnetstream.fork().store(dir='data')

# # # # # tnetstream = TrajectoryNetStream.load('data/test2.json')
# # tnedgestream = TrajectoryEdgeConverter().get_edge_stream(tnetstream)
# # tnedgestream.fork().store(dir='data')

# # tstream = TrajectoryNetStream.load('data/test2.json')  
# # ni = NaiveImportance()
# # importance = ni.get_importance(tstream)
# # pprint(importance[:10])

# viz = TrajectoryVisualizer(tstream)
# # viz = TrajectoryNetVisualizer(tnetstream, interval=30)
# # viz.show()