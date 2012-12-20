import datetime


class MediaMosaResource(object):

    class STATE(object):
        EMPTY = 0
        PARTIAL = 1
        FULL = 2

    def __init__(self, resource_id, api=None):
        """Initializes an empty resource.
        """
        self.id = resource_id
        self.data = {}
        self._meta = self._Meta()
        self._meta.api = api
        self._meta.state = self.STATE.EMPTY

    def __getattr__(self, attr):
        """Looks up an attribute in the data dictionary. It will query
        the api if there is no data available.
        """
        # return it if it already exists
        if attr in self.data:
            return self.handle(attr, self.data.get(attr))

        # do a lookup for partials and upgrade to full
        if not self._meta.state == self.STATE.FULL and self.is_connected():
            new_resource = self.fetch_resource_from_api(self.id)
            # add received data to resource and change is_empty state
            self.data = new_resource.data
            self._meta.state = self.STATE.FULL
            # retry lookup
            return self.__getattr__(attr)

    def handle(self, attr, value):
        """Will translate the API value to its python equivalent. This
        depends on the BOOLEANS and DATETIMES tuples defined in the
        concrete MediaMosa resource.
        """
        if attr in self.BOOLEANS:
            return value == u'TRUE'
        elif attr in self.DATETIMES:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            return value

    @classmethod
    def fromdict(cls, dct, api=None, full=False):
        """Creates an MediaMosaResource from a resource description
        received from the MediaMosaAPI."""
        res_id = dct.get(cls.RESOURCE_ID_KEY)
        resource = cls(res_id)
        resource.data = dct
        if full:
            resource._meta.state = cls.STATE.FULL
        else:
            resource._meta.state = cls.STATE.PARTIAL
        resource._meta.api = api
        return resource

    def is_connected(self):
        return self._meta.api is not None

    class _Meta(object):
        state = None
        api = None


class Mediafile(MediaMosaResource):
    RESOURCE_ID_KEY = 'mediafile_id'
    BOOLEANS = (
        'is_original_file', 'is_streamable', 'is_downloadable',
        'response_metafile_available', 'is_protected', 'is_inserted_md',
        'is_hinted', 'response_plain_available', 'response_object_available',
        'is_still',
    )
    DATETIMES = (
        'created', 'changed',
    )

    def fetch_resource_from_api(self, res_id):
        """Performs the api query necessary to retrieve the mediamosa resource.
        """
        return self._meta.api.mediafile(self.id)

    def __repr__(self):
        return "<mediamosa.resources.Mediafile (%s) %s>" % \
            (self.file_extension, self.id)


class Asset(MediaMosaResource):
    RESOURCE_ID_KEY = 'asset_id'
    BOOLEANS = (
        'is_unappropriate', 'is_favorite', 'has_streamable_mediafiles',
        'granted', 'is_empty_asset', 'asset_property_is_hidden',
        'isprivate', 'is_unappropiate', 'is_external', 'is_protected',
    )
    DATETIMES = (
        'videotimestampmodified', 'videotimestamp',
    )

    def fetch_resource_from_api(self, res_id):
        """Performs the api query necessary to retrieve the mediamosa resource.
        """
        return self._meta.api.asset(self.id)

    def list_mediafiles(self):
        """Returns a list of mediafiles associated with this asset
        """
        return [Mediafile.fromdict(dct,
            api=self._meta.api, full=False) for dct in self.mediafiles]

    def __repr__(self):
        return "<mediamosa.resources.Asset %s>" % self.id
