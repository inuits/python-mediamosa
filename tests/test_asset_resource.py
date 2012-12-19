import unittest

from mediamosa.resources import Asset, Mediafile


class TestAssetResource(unittest.TestCase):

    def test_create_empty_asset(self):
        Asset({})

    def test_create_asset(self):
        item_dict = {
            u'provider_id': '', u'is_unappropriate': u'FALSE',
            u'videotimestampmodified': u'2012-07-05 11:34:35',
            u'app_id': u'2', u'is_favorite': u'FALSE',
            u'has_streamable_mediafiles': u'TRUE', u'viewed': u'4',
            u'asset_id': u'g1QkoSmSeHdWfGkMKlOlldLn',
            u'ega_still_url': '', u'granted': u'TRUE', u'played': u'1',
            u'mediafile_duration': u'00:00:52.20',
            u'videotimestamp': u'2012-07-05 11:34:01',
            u'vpx_still_url': u'http://filvideod.ugent.be/media/17/Z/Z14cWALWKmfTRjTUKhhQQLv2.jpeg',
            u'owner_id': u'krkeppen', u'is_empty_asset': u'FALSE',
            u'play_restriction_end': '', u'asset_property_is_hidden': u'FALSE',
            u'dublin_core': {u'publisher': u'Kristof Keppens',
            u'rights': u'Kristof Keppens', u'description': u'test',
            u'language': u'nl', u'creator': u'Kristof Keppens',
            u'format': u'streaming video', u'coverage_spatial': '',
            u'date': '', u'relation': '', u'source': u'ugent',
            u'contributor': u', ', u'title': u'test sintel 2',
            u'identifier': '', u'type': u'video', u'coverage_temporal': '',
            u'subject': u'test'}, u'reference_id': '', u'isprivate': u'TRUE',
            u'qualified_dublin_core': {u'isformatof': '',
            u'description_abstract': '', u'license': '', u'created': '',
            u'issued': '', u'rightsholder': '', u'hasformat': '',
            u'title_alternative': '', u'format_medium': '',
            u'format_extent': '', u'isreferencedby': ''},
            u'mediafile_container_type': u'matroska;webm',
            u'is_unappropiate': u'FALSE', u'is_external': u'FALSE',
            u'is_protected': u'FALSE', u'play_restriction_start': '',
            u'group_id': ''}
        a = Asset(item_dict)
        self.assertEqual(a.id, 'g1QkoSmSeHdWfGkMKlOlldLn')
        self.assertEqual(a.dublin_core, item_dict.get('dublin_core'))