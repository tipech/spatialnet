"""Items Stream

Implements the BaseStream class, a generic class for handling spatial and
temporal object in a streaming way.

Provides various helper methods.

"""

import os, json, ijson, collections
from common.generic.objects import SerializableObject


class BaseStream(collections.Iterator, SerializableObject):
    """Iterator for a streamed collection of objects.

    Params
    ------
    items : Iterator
        The data source to be used for this stream.
    """

    def __init__(self, items, dimension = 2, **kwargs):
        """Initialize a new objects collection iterator from a source.

        Optionally provide an id.

        Params
        ------
        items : Iterator
            The data source to be used for this stream.
        """

        self.items = items
        self.dimension = dimension

        super().__init__(**kwargs)


    def __next__(self):
        """Get a single object from the stream."""

        return next(self.items)


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
        
        if not (isinstance(other, 'BaseStream')
            or issubclass(type(other), 'BaseStream')):
            raise TypeError("Attempting to merge invalid streams")

        return chain(self, other)


    def store(self, file):
        """Store a JSON representation of this graph stream.

        Recursively serialize graph snapshots.

        Params
        ------
        file: file or str
            file path or file object to store stream to
        """
        
        if isinstance(file, str) :
            file = open(file, 'w')

        try:
            file.write('{' + '"id":"{}", "items":[\n'.format(str(self.id)))
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
        """Read a TrajectoryNetStream from a file.

        Params
        ------
        file: file or str
            file path or file object to load stream from
            
        Returns
        -------
        TrajectoryNetStream
            The corresponding stream iterator
        """

        if isinstance(file, str) :
            file = open(file, 'r')

        stream_id = os.path.splitext(os.path.basename(file.name))[0]
        return cls(id=stream_id, items=(cls.deserialize_item(i)
            for i in ijson.items(file, 'items.item')))


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
