import datetime
import unittest

from minimock import Mock, mock, TraceTracker

from mediamosa.resources import Asset, MediaMosaResource
from mediamosa.api import MediaMosaAPI


class TestMediaMosaResource(unittest.TestCase):
    """Tests the generic functionality of a MediaMosaResource. This is
    done using the Asset object as concrete implementation.
    """

    def setUp(self):
        self.api = MediaMosaAPI("http://video.example.com")
        self.tt = TraceTracker()
        mock("self.api.session", tracker=self.tt)
        self.response = Mock("requests.Response")
        self.response.status_code = 200
        self.api.session.get.mock_returns = self.response

        self.item_dict = {
            "provider_id": "",
            "is_unappropriate": "FALSE",
            "videotimestampmodified": "2012-07-05 11:34:35",
            "app_id": "2",
            "is_favorite": "FALSE",
            "has_streamable_mediafiles": "TRUE",
            "viewed": "4",
            "asset_id": "g1QkoSmSeHdWfGkMKlOlldLn",
            "ega_still_url": "",
            "granted": "TRUE",
            "played": "1",
            "mediafile_duration": "00:00:52.20",
            # u'videotimestamp': u'2012-07-05 11:34:01', # cleared it for partial
            "vpx_still_url": "http://filvideod.ugent.be/media/17/Z/Z14cWALWKmfTRjTUKhhQQLv2.jpeg",
            "owner_id": "krkeppen",
            "is_empty_asset": "FALSE",
            "play_restriction_end": "",
            "asset_property_is_hidden": "FALSE",
            "dublin_core": {
                "publisher": "Kristof Keppens",
                "rights": "Kristof Keppens",
                "description": "test",
                "language": "nl",
                "creator": "Kristof Keppens",
                "format": "streaming video",
                "coverage_spatial": "",
                "date": "",
                "relation": "",
                "source": "ugent",
                "contributor": ", ",
                "title": "test sintel 2",
                "identifier": "",
                "type": "video",
                "coverage_temporal": "",
                "subject": "test",
            },
            "reference_id": "",
            "isprivate": "TRUE",
            "qualified_dublin_core": {
                "isformatof": "",
                "description_abstract": "",
                "license": "",
                "created": "",
                "issued": "",
                "rightsholder": "",
                "hasformat": "",
                "title_alternative": "",
                "format_medium": "",
                "format_extent": "",
                "isreferencedby": "",
            },
            "mediafile_container_type": "matroska;webm",
            "is_unappropiate": "FALSE",
            "is_external": "FALSE",
            "is_protected": "FALSE",
            "play_restriction_start": "",
            "group_id": "",
        }

    # _mmmeta.state

    def test_create_empty_asset(self):
        """Tests if an empty asset can be created"""
        a = Asset("g1QkoSmSeHdWfGkMKlOlldLn")
        self.assertEqual(a._mmmeta.state, MediaMosaResource.STATE.EMPTY)

    def test_create_partial_asset(self):
        """Tests if a partially pre-filled asset can be created"""
        a = Asset.fromdict(self.item_dict)
        self.assertEqual(a._mmmeta.state, MediaMosaResource.STATE.PARTIAL)

    def test_create_full_asset(self):
        """Tests if an fully pre-filled asset can be created"""
        a = Asset.fromdict(self.item_dict, full=True)
        self.assertEqual(a._mmmeta.state, MediaMosaResource.STATE.FULL)

    # _mmmeta.api

    def test_create_connected_asset(self):
        """Tests if a connected asset can be created"""
        a = Asset("g1QkoSmSeHdWfGkMKlOlldLn", api=self.api)
        self.assertTrue(a.is_connected())

    def test_create_unconnected_asset(self):
        """Tests if an unconnected asset can be created"""
        a = Asset("g1QkoSmSeHdWfGkMKlOlldLn")
        self.assertFalse(a.is_connected())

    # accessing supplied data

    def test_can_access_asset_data(self):
        """Tests if pre-filled data can be accessed"""
        a = Asset.fromdict(self.item_dict)
        self.assertEquals(a.asset_id, "g1QkoSmSeHdWfGkMKlOlldLn")
        self.assertIsInstance(a.is_favorite, bool)
        self.assertIsInstance(a.videotimestampmodified, datetime.datetime)
        self.assertRaises(Exception, a.some_unexisting_attribute)
        self.assertEqual(a._mmmeta.state, MediaMosaResource.STATE.PARTIAL)

    # accessing unsupplied data

    def test_accessing_empty_asset(self):
        """Tests if an empty asset will automatically fill itself if
        queried"""
        # setup
        self.response.content = open("tests/data/get_asset_id_response.xml").read()
        # test
        asset = Asset("g1QkoSmSeHdWfGkMKlOlldLn", api=self.api)
        # validate
        self.assertIsInstance(asset.is_favorite, bool)
        self.assertNotEquals(self.tt.dump(), "")
        self.tt.clear()
        self.assertIsInstance(asset.videotimestamp, datetime.datetime)
        self.assertEquals(self.tt.dump(), "")
        self.assertRaises(Exception, asset.some_unexisting_attribute)
        self.assertEqual(asset._mmmeta.state, MediaMosaResource.STATE.FULL)

    def test_accessing_partial_asset(self):
        """Tests if a partial asset will automatically fill itself if
        queried"""
        # setup
        self.response.content = open("tests/data/get_asset_id_response.xml").read()
        # test
        asset = Asset.fromdict(self.item_dict, api=self.api, full=False)
        # validate
        self.assertIsInstance(asset.is_favorite, bool)
        self.assertEquals(self.tt.dump(), "")
        self.assertIsInstance(asset.videotimestamp, datetime.datetime)
        self.assertNotEquals(self.tt.dump(), "")
        self.assertRaises(Exception, asset.some_unexisting_attribute)
        self.assertEqual(asset._mmmeta.state, MediaMosaResource.STATE.FULL)
