import xml.sax.handler

_formats = {
    "item_count": int,
    "item_count_total": int,
    "item_offset": int,
    "request_query_count": int,
    "request_process_time": float,
}
_dictionaries = {
    "asset": lambda handler: _setDictionary(handler._dictionaries[-1], key="asset"),
    "dublin_core": lambda handler: _setDictionary(
        handler._dictionaries[-1], key="dublin_core"
    ),
    "header": lambda handler: handler.headers,
    "item": lambda handler: _setDictionary(handler.items),
    "mediafile": lambda handler: _setDictionary(handler.items[-1]["mediafiles"]),
    "metadata": lambda handler: _setDictionary(
        handler._dictionaries[-1], key="metadata"
    ),
    "rdf:Description": lambda handler: _setDictionary(
        handler._dictionaries[-1], key="rdf"
    ),
    "qualified_dublin_core": lambda handler: _setDictionary(
        handler._dictionaries[-1], key="qualified_dublin_core"
    ),
    "still": lambda handler: _setDictionary(
        handler.items[-1]["mediafiles"][-1]["stills"]
    ),
}
for i in range(0, 1000):
    _dictionaries[f"app_{i}"] = lambda handler, i=i: _setDictionary(
        handler._dictionaries[-1], key=f"app_{i}"
    )
_lists = {
    "mediafiles": lambda handler: handler.items[-1].setdefault("mediafiles", []),
    "still": lambda handler: handler.items[-1]
    .setdefault("mediafiles", [{}])[-1]
    .setdefault("stills", []),
}
_ignore = [
    "items",
    "mediafiles",
    "response",
    "rdf",
]


def _setDictionary(container, key=None):
    """Set a dictionary."""
    dictionary = {}

    if type(container) == dict:
        container[key] = dictionary
    elif type(container) == list:
        container.append(dictionary)

    return dictionary


class MediaMosaResponseContentHandler(xml.sax.handler.ContentHandler):
    """Content-handler for responses from a MediaMosa-server."""

    def __init__(self):
        """Constructor."""
        self.headers = {}
        self.items = []

        self._elements = []
        self._dictionaries = []
        self._content = None

    def startElement(self, name, attributes):
        """Handle start-element."""
        if name in _lists:
            _lists[name](self)

        if name in _dictionaries:
            dict_ = _dictionaries[name](self)
            self._dictionaries.append(dict_)

        self._elements.append(name)
        self._content = ""

    def endElement(self, name):
        """Handle end-element."""
        try:
            if name in _ignore:
                pass
            elif name in _dictionaries:
                self._dictionaries.pop()
            elif self._elements[-2] in _dictionaries:
                format_ = _formats.get(name, None)
                if format_:
                    content = format_(self._content)
                else:
                    content = self._content

                if name in self._dictionaries[-1]:
                    if type(self._dictionaries[-1][name]) != list:
                        self._dictionaries[-1][name] = [self._dictionaries[-1][name]]
                    self._dictionaries[-1][name].append(content)
                else:
                    self._dictionaries[-1][name] = content
        except IndexError:
            pass

        self._elements.pop()
        self._content = None

    def characters(self, content):
        """Handle characters."""
        if self._elements:
            if self._content is not None:
                self._content += content
