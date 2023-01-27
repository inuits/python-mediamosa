import unittest

from minimock import Mock, mock, TraceTracker

from mediamosa.resources import Mediafile, MediaMosaResource
from mediamosa.api import MediaMosaAPI, ApiException


class TestMediafileResource(unittest.TestCase):
    def setUp(self):
        self.api = MediaMosaAPI("http://video.example.com")
        self.tt = TraceTracker()
        mock("self.api.session", tracker=self.tt)
        self.response = Mock("requests.Response")
        self.response.status_code = 200
        self.api.session.get.mock_returns = self.response

        self.item_dict = {
            "is_original_file": "FALSE",
            "is_streamable": "FALSE",
            "is_downloadable": "FALSE",
            "app_id": "2",
            "transcode_inherits_acl": "TRUE",
            "tag": "",
            "response_metafile_available": "TRUE",
            "mediafile_id_source": "u2ilZNiHdl7iNUdexL7BcFMY",
            "asset_id": "g1QkoSmSeHdWfGkMKlOlldLn",
            "mediafile_id": "Md2RgaUEVFhfJMeUIbwPOMei",
            "transcode_profile_id": "17",
            "filename": "Sintel_Trailer1.1080p.DivX_Plus_HD.mp4",
            "is_protected": "FALSE",
            "ega_stream_url": "",
            "file_extension": "mp4",
            "metadata": {
                "is_inserted_md": "FALSE",
                "fps": "24",
                "bpp": "0.31",
                "file_duration": "00:00:52.20",
                "colorspace": "yuv420p",
                "container_type": "mov;mp4;m4a;3gp;3g2;mj2",
                "height": "478",
                "channels": "stereo",
                "width": "852",
                "sample_rate": "44100",
                "filesize": "20543936",
                "audio_codec": "aac",
                "video_codec": "h264",
                "is_hinted": "TRUE",
                "bitrate": "3012",
                "mime_type": "video/mp4",
            },
            "ega_download_url": "",
            "ega_play_url": "",
            "tool": "ffmpeg",
            "response_plain_available": "TRUE",
            "owner_id": "krkeppen",
            "response_object_available": "TRUE",
            "created": "2012-07-05 11:38:14",
            "changed": "2012-07-05 11:38:14",
            "uri": "",
            "is_still": "FALSE",
            "command": "audiocodec:libfaac;audiobitrate:128000;audiosamplingrate:44100;audiochannels:2;videocodec:libx264;videopreset_quality:slow;videopreset_profile:baseline;2_pass_h264_encoding:2;videobitrate:800000;qmax:17;size:852x480;maintain_aspect_ratio:yes",
            "group_id": "",
        }

    def test_getting_full_mediafile(self):
        """Test fetching a full mediafile from the api"""
        # setup
        self.response.content = open("tests/data/get_mediafile_id_response.xml").read()
        # test
        mediafile = self.api.mediafile("g1QkoSmSeHdWfGkMKlOlldLn")
        # validate
        self.assertIsInstance(mediafile, Mediafile)
        self.assertEqual(mediafile._mmmeta.state, MediaMosaResource.STATE.FULL)

    def test_getting_unexisting_mediafile(self):
        """Test fetching an non-existing mediafile"""
        # setup
        self.response.content = open("tests/data/invalid_mediafile_request.xml").read()
        # validate
        self.assertRaises(
            ApiException, self.api.mediafile, ("g1QkoSmSeHdWfGkMKlOlldLn")
        )
