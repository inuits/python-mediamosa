import hashlib
import random
import requests
import xml.sax

from resources import Asset, Mediafile
from response import MediaMosaResponseContentHandler


class ApiException(Exception):
    pass


class MediaMosaAPI(object):

    class FORMATS(object):
        DOWNLOAD = 'download'
        METAFILE = 'metafile'
        OBJECT = 'object'
        STILL = 'still'
        PLAIN = 'plain'
        CUPERTINE = 'cupertino'
        RSTP = 'rstp'
        SILVERLIGHT = 'silverlight'

    def __init__(self, uri):
        self.uri = uri
        self.session = requests.session()

    ## API

    def authenticate(self, username, secret):
        """Authenticates with the server
        """
        self.username = username
        self.secret = secret

        # get challenge
        challenge = self._login_challenge()
        # send challenge response
        success = self._login_response(challenge)
        self.authenticated = success
        return success

    def assets(self):
        """Returns a list of Assets
        """
        headers, items = self._get('/asset')
        return [Asset(item_dict) for item_dict in items]

    def mediafiles(self, asset):
        """Returns a list of Mediafiles for an Asset
        """
        headers, items = self._get('/asset/%s' % asset.id)
        return [Mediafile(item_dict) \
            for item_dict in items[0].get('mediafiles')]

    def play(self, mediafile, user_id='pyUser', response=FORMATS.OBJECT):
        headers, items = self._get('/asset/%s/play' % mediafile.asset_id,
            {'user_id': user_id,
             'mediafile_id': mediafile.id,
             'response': response})
        return items[0]

    ## APPLICATION LAYER

    def _login_challenge(self):
        """Retrieves a login _login_challenge
        """
        headers, items = self._get('/login', {
            'dbus': 'AUTH DBUS_COOKIE_SHA1 %s' % self.username
        })

        if headers.get('request_result') != 'success':
            raise ApiException("Failed receiving challenge")

        return items[0].get('dbus').split(' ')[-1]

    def _login_response(self, challenge):
        """Performs a login response to a particular challenge
        """
        rand = hashlib.md5(str(random.random())).hexdigest()[:8]
        digest = hashlib.sha1('%s:%s:%s' % (challenge, rand, self.secret))\
                        .hexdigest()
        headers, items = self._post('/login',
            {'dbus': 'DATA %s %s' % (rand, digest)})

        # return true if already logged in
        if headers.get('request_result') != 'success':
            return 'already_identified' in \
                headers.get("request_result_description", [])

        return headers.get('request_result') == 'success'

    def _parse(self, response):
        """Parse a Mediamosa-response.
        """
        handler = MediaMosaResponseContentHandler()
        xml.sax.parseString(response, handler)

        return (handler.headers, handler.items)

    ## HTTP LAYER

    def _get_absolute_uri(self, relative_uri):
        return self.uri + relative_uri

    def _post(self, relative_uri, payload={}):
        """Performs a post call to the api
        """
        response = self.session.post(self._get_absolute_uri(relative_uri),
            data=payload)
        if response.status_code != 200:
            raise ApiException('API returned %s' % response.status_code)

        return self._parse(response.content)

    def _get(self, relative_uri, payload={}):
        """Performs a get call to the api.
        """
        response = self.session.get(self._get_absolute_uri(relative_uri),
            params=payload)

        if response.status_code != 200:
            raise ApiException('API returned %s' % response.status_code)

        return self._parse(response.content)
