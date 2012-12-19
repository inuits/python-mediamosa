import xml.sax
import xml.sax.handler

_formats = {
    "item_count": int,
    "item_count_total": int,
    "item_offset": int,
    "output": lambda buffer: buffer.replace("\r\n", "\n")}


class MediaMosaResponseContentHandler(xml.sax.handler.ContentHandler):
    """Content-handler for Mediamosa-responses.
    """

    def __init__(self):
        """Constructor.
        """
        self.container = None
        self.element = None

        self.headers = {}
        self.items = []

        self.buffer = None

    def startElement(self, name, attributes):
        """Handle start-element.
        """
        if name == "header":
            self.container = "header"

        elif name == "item":
            self.container = "item"
            self.items.append({})

        elif name in ("dublin_core", "qualified_dublin_core"):
            self.container = name
            self.items[-1][name] = {}

        elif name == "mediafiles":
            pass

        elif name == "mediafile":
            if "mediafiles" not in self.items[-1]:
                self.items[-1]["mediafiles"] = []

            self.container = "mediafile"
            self.items[-1]["mediafiles"].append({})

        elif name == "metadata":
            self.container = "metadata"
            self.items[-1]["mediafiles"][-1]["metadata"] = {}

        elif name == "still":
            if "stills" not in self.items[-1]["mediafiles"][-1]:
                self.items[-1]["mediafiles"][-1]["stills"] = []

            self.container = "still"
            self.items[-1]["mediafiles"][-1]["stills"].append({})

        elif self.container:
            self.element = name
            self.buffer = ""

    def endElement(self, name):
        """Handle end-element.
        """
        if name in ("header", "item"):
            self.container = None

        elif name in ("dublin_core", "qualified_dublin_core", "mediafile"):
            self.container = "item"

        elif name == "mediafiles":
            pass

        elif name == "metadata":
            self.container = "mediafile"

        elif name == "still":
            self.container = "mediafile"

        else:
            format = _formats.get(self.element)
            if format:
                self.buffer = format(self.buffer)

            if self.container == "header":
                self.headers[self.element] = self.buffer

            elif self.container == "item":
                self.items[-1][self.element] = self.buffer

            elif self.container in ("dublin_core", "qualified_dublin_core"):
                self.items[-1][self.container][self.element] = self.buffer

            elif self.container == "mediafile":
                self.items[-1]["mediafiles"][-1][self.element] = self.buffer

            elif self.container == "metadata":
                self.items[-1]["mediafiles"][-1]["metadata"][self.element] = self.buffer

            elif self.container == "still":
                self.items[-1]["mediafiles"][-1]["stills"][-1][self.element] = self.buffer

            self.element = None
            self.buffer = None

    def characters(self, content):
        """Handle characters.
        """
        if self.element:
            self.buffer += content

