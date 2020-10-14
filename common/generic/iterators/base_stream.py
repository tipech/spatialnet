"""Items Stream

Implements the BaseStream class, a generic class for handling spatial and
temporal object in a streaming way.

Provides various helper methods.

"""

import os, json, ijson, collections
from copy import copy
from common.generic.objects import SerializableObject, IdObject


class BaseStream(collections.Iterator, SerializableObject, IdObject):
    """Iterator for a streamed collection of objects.

    Params
    ------
    items : Iterator
        The data source to be used for this stream.
    dimension : int
        The number of dimensions of items in this stream
    id : str
        The id for this stream
    """

    def __init__(self, items, dimension=2, id=''):
        """Initialize a new objects collection iterator from a source.

        Optionally provide an id.

        Params
        ------
        items : Iterator
            The data source to be used for this stream.
        dimension : int
            The number of dimensions of items in this stream
        id : str
            The id for this stream
        """

        self.items = items
        self.dimension = dimension

        super().__init__(id=id)


    def __next__(self):
        """Get a single object from the stream."""

        return next(self.items)


    def checkpoint(self, recursive=False):
        """Run the full iterator, and save to a list.

        Returns
        -------
        tuple : list, iterator
            A list and iterator of this object's contents.
        recursive : boolean
            Flag to recursively checkpoint items and return iterator
        """

        # store regions to list and reset iterator
        item_list = list(self.items)
        if len(item_list) == 0:
            raise StopIteration

        # if this is a stream of streams, checkpoint its items recursively.
        if BaseStream.is_stream(item_list[0]):
            stream_list = [stream.checkpoint(True) for stream in item_list]
            item_list, iterators = zip(*stream_list)
            item_list = list(item_list)

            self.items = iter(iterators)
        else:
            self.items = iter(item_list)

        if recursive:
            return item_list, self
        else:
            return item_list


    def fork(self, recursive=False):
        """Checkpoint the iterator, and return a copy.

        Returns
        -------
        tuple : list, iterator
            A list and iterator of this object's contents.
        recursive : boolean
            Flag to recursively fork items and return both
        """

        # store regions to list and reset iterator
        item_list = list(self.items)
        fork = copy(self)
        if len(item_list) == 0:
            raise StopIteration

        # if this is a stream of streams, checkpoint its items recursively.
        if BaseStream.is_stream(item_list[0]):
            stream_list = [stream.fork(True) for stream in item_list]
            item_1, item_2 = zip(*stream_list)
            self.items = iter(item_1)
            fork.items = iter(item_2)
        else:
            self.items = iter(item_list)
            fork.items = iter(item_list)

        if recursive:
            return fork, self
        else:
            return fork



    def merge(self, other):
        """Merge this BaseStream with another BaseStream.

        Params
        ------
        other: BaseStream
            The stream to be merged with.

        Returns
        -------
        BaseStream
            The merged BaseStream.
        """
        
        if not (isinstance(other, BaseStream)
            or issubclass(type(other), BaseStream)):
            raise TypeError("Attempting to merge invalid streams")

        return chain(self, other)


    def store(self, file=None, dir=None):
        """Store a JSON representation of this graph stream.

        Recursively serialize graph snapshots.

        Params
        ------
        file: file or str (optional, default: None)
            file path or file object to store stream to
        dir: str (optional, default: None)
            file path or file object to store stream to
        """


        # if no filename given, use id
        if file is None or len(file) == 0:
            file = self.id + ".json"

        # open file if filename (and/or dir) was given
        if isinstance(file, str):
            if dir is not None and len(dir) > 0 :
                file = dir.rstrip('/').rstrip('\\') + '/' + file
            file = open(file, 'w')

        try:
            file.write('{"items":[\n')
            item = next(self)
            file.write(json.dumps(self.serialize_item(item),
                sort_keys=True, indent=4))

            for item in self:
                file.write(',\n')
                file.write(json.dumps(self.serialize_item(item),
                    sort_keys=True, indent=4))

            file.write(']}')
        finally:
            file.close()

    @classmethod
    def load(cls, file):
        """Read a BaseStream from a file.

        Params
        ------
        file: file or str
            File path or file object to load stream from
            
        Returns
        -------
        TrajectoryNetStream
            The corresponding stream iterator
        """

        if isinstance(file, str) :
            file = open(file, 'r')


        def read_file(file):
            for i, item in enumerate(ijson.items(file, 'items.item')):
                yield cls.deserialize_item(item)

        stream_id = os.path.splitext(os.path.basename(file.name))[0]
        return cls(id=stream_id, items=read_file(file))


    @staticmethod
    def serialize_item(item):
        """Serialize a single item in this stream.
        
        Params
        ------
        item : arbitrary object
            Serializable object

        Returns
        -------
        dict
            Serializable dictionary representation of item
        """
        
        if hasattr(item, "to_dict"):
            return item.to_dict()
        else:
            return item


    @classmethod
    def deserialize_item(cls, item_dict):
        """Deserialize and add a single item to the stream.
        
        Params
        ------
        item_dict : dict
            Deserialized dict object

        Returns
        -------
        item
            Arbitrary object for this stream
        """
        
        return item_dict


    @staticmethod
    def is_stream(target):
        """Determine whether an object is a stream.

        Parameters
        ----------
        target : object
            The object to examine

        Returns
        -------
        boolean
            True if target is a BaseStream or subclass, False otherwise
        """

        return (isinstance(target, BaseStream)
            or issubclass(type(target), BaseStream))