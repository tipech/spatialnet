import functional
import geopandas as gpd

from ..classes import Frame,Trajectory

def frames_to_trajectories(frames):
    """Convert a list or sequence of frames into one of trajectories.

    Params
    ------
    frames : list, iterable or Sequence of Frame objects
        Input collection of Frame objects.

    Returns
    -------
    pyfunctional.Sequence if frames is Sequence, else list
        Collection of Trajectory objects, same type as frames
    """

    # determine if input was sequence, if not convert it and remember
    nonseq = False
    if not isinstance(frames, functional.pipeline.Sequence):
        nonseq = True
        frames = functional.seq(frames)

    # flatten, group by particle id and convert to Trajectory objects
    records = frames.flat_map(lambda f: ( (pID,(f.time,pos))
        for pID,pos in f.items()) )
    trajectories = records.group_by_key().sorted()\
        .map(lambda x: Trajectory(*x))

    if nonseq:
        return trajectories.to_list()
    return trajectories


def trajectories_to_frames(trajectories):
    """Convert a list or sequence of trajectories into one of frames.

    Params
    ------
    trajectories : list, iterable or Sequence of Trajectory objects
        Input collection of Trajectory objects.

    Returns
    -------
    pyfunctional.Sequence if trajectories is Sequence, else list
        Collection of Frame objects, same type as trajectories
    """

    # determine if input was sequence, if not convert it and remember
    nonseq = False
    if not isinstance(trajectories, functional.pipeline.Sequence):
        nonseq = True
        trajectories = functional.seq(trajectories)

    # flatten, group by particle id and convert to Trajectory objects
    records = trajectories.flat_map(lambda t: ( (time,(t.pID,pos))
        for time,pos in t.items()) )
    frames = records.group_by_key().sorted().map(lambda x: Frame(*x))

    if nonseq:
        return frames.to_list()
    return frames


def trajectories_to_gdf(trajectories):
    """Convert a list or sequence of trajectories into a GeoDataFrame.

    Params
    ------
    trajectories : list or iterable of Trajectory objects
        Input collection of Trajectory objects.

    Returns
    -------
    pandas.GeoDataFrame
        GeoDataFrame with columns 'pID' and 'geometry'
    """

    # convert to list if it isn't
    trajectories = list(trajectories)

    return gpd.GeoDataFrame({
        'pIDs': [t.pID for t in trajectories],
        'geometry': [t.get_geometry() for t in trajectories]})

