import json, orjson # faster than stock json

def _default(self, obj):
    return getattr(obj.__class__, "to_dict", _default.default)(obj)

_default.default = json.JSONEncoder().default
json.JSONEncoder.default = _default



class JSONSerializable():
    """Provides JSON serialization/deserialization options.

    Requires self.to_dict() and cls.from_dict() to be defined.
    """


    def to_json(self, path_or_buf=None):
        """Convert the object to a JSON string.

        Params
        ------
        path_or_buf : str or file handle, optional
            File path or object. If not specified, returns a bytestring.
        """

        d = self.to_dict()

        if path_or_buf is None:
            return json.dumps(d)

        # filename given, open and save as binary
        elif isinstance(path_or_buf, str):
            with open(path_or_buf, 'wb') as file:
                file.write(orjson.dumps(d))

        # file object given in binary mode, save binary json
        elif 'b' in path_or_buf.mode:
            path_or_buf.write(orjson.dumps(d))
        
        # file object given in text mode, save string json
        elif not 'b' in path_or_buf.mode:
            path_or_buf.write(json.dumps(d))

    @classmethod
    def from_json(cls, source):
        """Get an object from a JSON path, buffer or string.

        Params
        ------
        source : str or file handle
            File path, object or JSON string.
        """

        # JSON string or bytestring, deserialize
        if isinstance(source, (str, bytes, bytearray)):
            try:
                d = orjson.loads(source)

            # file path, read
            except json.decoder.JSONDecodeError as e:
                with open(source) as file:
                    d = orjson.loads(file.read())
        else:
            d = orjson.loads(source.read())

        return cls(**d)


    @classmethod
    def from_file(cls, source):
        """Alias for cls.from_json."""

        return cls.from_json(source)