"""Trajectory Network Stream

Implements the TrajectoryNetStream class, a subclass of BaseStream
that represents an iterator of Graph objects.

"""
import os, ijson
from networkx import Graph
from spatialnet.common.generic.iterators import BaseStream
from spatialnet.common.regions import Region


class TrajectoryNetStream(BaseStream):
    """An iterator over static graph snapshots.

    Provides methods for reading and saving streams of Graph
    objects to and from storage, as well as merging different streams.
    
    Params
    ------
    items : Iterator
        The Graph objects to be used for this stream.
    id : str or int
        The unique identifier for this SpatialSet.
        Randonly generated with UUID v4, if not provided.
    """


    def calculate_bounds(self):
        """Automatically calculate and set this Stream's bounds.

        By necessity, this has to run the full iterator, store its
        contents as a list, calculate bounds and finally recreate it.

        Returns
        -------
        Region
            The new bounds.
        """
        
        item_list = self.checkpoint()

        lower = [min(n[1][d] for G in item_list
            for n in G.nodes(data='pos')) for d in range(self.dimension)]
        upper = [max(n[1][d] for G in item_list
            for n in G.nodes(data='pos')) for d in range(self.dimension)]
        
        return Region.from_coords(lower=lower, upper=upper)


    @staticmethod
    def serialize_item(item):
        """Serialize a single Graph item in this stream.
        
        Params
        ------
        item : Graph
            Serializable Graph object

        Returns
        -------
        dict
            Serializable dictionary representation of Graph item
        """
        
        return {'time': item.time,
                'nodes': [{'id': n[0], **n[1]}
                    for n in item.nodes(data=True)],
                'edges': [{'from': e[0], 'to': e[1]}
                    for e in item.edges()]}


    @staticmethod
    def deserialize_item(item_dict):
        """Deserialize and add a Graph to the stream.
        
        Params
        ------
        item_dict : dict
            Deserialized Graph dict object

        Returns
        -------
        item
            Graph item for this stream
        """

        G = Graph()
        G.add_nodes_from((n['id'], {k:v for k,v in n.items() if k != 'id'})
            for n in item_dict['nodes'])
        G.add_edges_from((e['from'], e['to']) for e in item_dict['edges'])
        G.time = int(float(item_dict['time']))
        return G


    @classmethod
    def load(cls, file, cutoff=None):
        """Read a BaseStream from a file.

        Params
        ------
        file: file or str
            File path or file object to load stream from
        cutoff: int (optional, default: None)
            A cutoff time to stop.
            
        Returns
        -------
        TrajectoryNetStream
            The corresponding stream iterator
        """

        if isinstance(file, str) :
            file = open(file, 'r')


        def read_file(file, cutoff):
            for item in ijson.items(file, 'items.item'):
                G = cls.deserialize_item(item)
                yield G
                if cutoff is not None and int(G.time) >= cutoff:
                    break

        stream_id = os.path.splitext(os.path.basename(file.name))[0]
        return cls(id=stream_id, items=read_file(file, cutoff))