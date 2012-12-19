

class Mediafile(object):

    def __init__(self, item_dict):
        self.id = item_dict.get('mediafile_id')
        self.asset_id = item_dict.get('asset_id')
        self.file_extension = item_dict.get('file_extension')
        self.is_original = item_dict.get('is_original_file') == 'TRUE'

    def __repr__(self):
        return "<mediamosa.resources.Mediafile (%s) %s>" % \
            (self.file_extension, self.id)


class Asset(object):

    def __init__(self, item_dict):
        self.id = item_dict.get('asset_id')
        self.dublin_core = item_dict.get('dublin_core', {})

    def __repr__(self):
        return "<mediamosa.resources.Asset %s>" % self.id
