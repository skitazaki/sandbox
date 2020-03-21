#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
A simple HTTP server with `twisted.web` to implement OAuth service provider.

If you are new to Twisted, read 'Twisted Web in 60 seconds' at first.
"""

# A secret of rpy script :P
cache()

from crypt import crypt
import logging
import os
import os.path
import time

import oauth.oauth as oauth
from twisted.cred.checkers import FilePasswordDB
# twisted.web.error.NoResource is deprecated since Twisted 9.0.
from twisted.web.resource import Resource, NoResource
from twisted.web.static import File

BASEDIR = os.path.abspath(os.path.dirname(__file__))
CALLBACK_URL = 'http://localhost/callback'


class MockOAuthDataStore(oauth.OAuthDataStore):
    """Import from example script.
    """

    def __init__(self):
        self.consumer = oauth.OAuthConsumer('ANONYMOUS', 'ANONYMOUS')
        self.request_token = oauth.OAuthToken('requestkey', 'requestsecret')
        self.access_token = oauth.OAuthToken('accesskey', 'accesssecret')
        self.nonce = 'nonce'

    def lookup_consumer(self, key):
        if key == self.consumer.key:
            return self.consumer
        return None

    def lookup_token(self, token_type, token):
        token_attrib = getattr(self, '%s_token' % token_type)
        if token == token_attrib.key:
            ## HACK
            token_attrib.set_callback(CALLBACK_URL)
            return token_attrib
        return None

    def lookup_nonce(self, oauth_consumer, oauth_token, nonce):
        if oauth_token and oauth_consumer.key == self.consumer.key and \
                (oauth_token.key == self.request_token.key or \
                    oauth_token.key == self.access_token.key) and \
                nonce == self.nonce:
            return self.nonce
        return None

    def fetch_request_token(self, oauth_consumer, oauth_callback):
        if oauth_consumer.key == self.consumer.key:
            if oauth_callback:
                # want to check here if callback is sensible
                # for mock store, we assume it is
                self.request_token.set_callback(oauth_callback)
            return self.request_token
        return None

    def fetch_access_token(self, oauth_consumer, oauth_token, oauth_verifier):
        if oauth_consumer.key == self.consumer.key and \
                oauth_token.key == self.request_token.key:
            # want to check here if token is authorized
            # for mock store, we assume it is
            return self.access_token
        return None

    def authorize_request_token(self, oauth_token, user):
        if oauth_token.key == self.request_token.key:
            # authorize the request token in the store
            # for mock store, do nothing
            return self.request_token
        return None

SERVER = oauth.OAuthServer(MockOAuthDataStore())
SERVER.add_signature_method(oauth.OAuthSignatureMethod_HMAC_SHA1())

CACHE = {}


class BaseOAuthResource(Resource):

    def getChild(self, name, request):
        return self

    def render_POST(self, request):
        uri = 'https://' if request.isSecure() else 'http://'
        uri += request.getHeader('host')
        uri += request.path
        logging.debug("Requested URI:", uri)
        c = None
        if request.getHeader('content-length'):
            c = request.content.read()
        # Be care to case-sensitiveness in OAuth library code.
        h = request.getHeader('authorization')
        headers = {'Authorization': h} if h else None
        oauth_request = oauth.OAuthRequest.from_request('POST', uri,
            headers=headers, parameters=None, query_string=c)
        if not oauth_request:
            request.setResponseCode(401)
            request.setHeader('Content-Type', 'text/plain')
            return 'invalid request'
        request.setHeader('Content-Type',
                'application/x-www-form-urlencoded')
        # TODO: rewrite to use `Deferred`.
        try:
            ret = self.handle(oauth_request)
            return ret
        except oauth.OAuthError, err:
            request.setResponseCode(401)
            header = oauth.build_authenticate_header(realm=uri)
            for k, v in header.iteritems():
                request.setHeader(k, v)
            return str(err.message)

    def handle(self, request, oauth_request):
        raise NotImplementedError()


class OAuthInitiator(BaseOAuthResource):
    """First step on OAuth 1.0a dance.
    """

    def handle(self, oauth_request):
        token = SERVER.fetch_request_token(oauth_request)
        if token:
            return token.to_string()
        raise oauth.OAuthError('simple oauth error on step1.')


class OAuthTokenIssuer(BaseOAuthResource):
    """Third step on OAuth 1.0a dance.
    """

    def handle(self, oauth_request):
        ck = oauth_request.get_parameter('oauth_consumer_key')
        tok = oauth_request.get_parameter('oauth_token')
        verifier = oauth_request.get_parameter('oauth_verifier')
        ret = CACHE.get(tok, None)
        if ret is None:
            raise oauth.OAuthError('unkown oauth_token.')
        v, user, t = ret
        if time.time() - t > 10000:
            raise oauth.OAuthError('expired oauth_token.')
        if v != verifier:
            raise oauth.OAuthError('invalid oauth_verifier.')
        access_token = SERVER.fetch_access_token(oauth_request)
        if access_token:
            del CACHE[tok]
            # TODO: Associate access token and user data.
            return access_token.to_string()
        raise oauth.OAuthError('simple oauth error on step3.')


class OAuthAuthorizer(Resource):
    """Second step on OAuth 1.0a dance.
    Show HTML page to have user filled account form.
    """

    TEMPLATE = os.path.join(BASEDIR, 'authorize.html')

    # "httpd.password" contains oauth/oauth user.
    DB = FilePasswordDB(os.path.join(BASEDIR, 'httpd.password'))

    def render_GET(self, request):
        tok = self._get(request, 'oauth_token')
        # TODO: Check token is available.
        if tok:
            return open(self.TEMPLATE).read()
        request.setResponseCode(401)
        request.setHeader('content-type', 'text/plain')
        return "Invalid request, no \"oauth_token\"."

    def render_POST(self, request):
        request.setHeader('content-type', 'text/plain')
        tok = self._get(request, 'oauth_token')
        username = self._get(request, 'username')
        password = self._get(request, 'password')
        if not (tok and username and password):
            request.setResponseCode(401)
            return "Invalid parameter."
        if not self._authenticate(username, password):
            request.setResponseCode(401)
            return "Failed to authorize you."
        user = None
        token = oauth.OAuthToken(tok, None)
        ret = SERVER.authorize_token(token, user)
        if ret:
            verifier = 'abc'
            CACHE[tok] = (verifier, user, time.time())
            cb = token.get_callback_url()
            if cb:
                url = (cb + '&') if '?' in cb else (cb + '?')
                return url + 'oauth_token=%s&oauth_verifer=%s' % (tok, verifier)
            return "Verifier code is \"%s\"." % (verifier,)
        request.setResponseCode(401)
        return "No token left for you, \"%s\"." % (tok,)

    def _get(self, request, key):
        """Get request parameter from given key.
        If given key is not found, return `None`.
        """
        if key in request.args:
            v = request.args[key]
            if type(v) == list:
                return v[0].strip()
            elif type(v) == str:
                return v.strip()
            return v
        return None

    def _authenticate(self, username, password):
        try:
            _, hashed = self.DB.getUser(username)
            # Check '.htpasswd' style crypt-ed string.
            return hashed == crypt(password, hashed[:2])
        except KeyError:
            pass
        return False


class OAuthServiceProvider(Resource):

    _children = {"initiate": OAuthInitiator,
                 "authorize": OAuthAuthorizer,
                 "token": OAuthTokenIssuer}

    def getChild(self, name, request):
        if name in self._children:
            return self._children[name]()
        return NoResource()

# Promised variable for `twistd` resource script.
resource = Resource()
resource.putChild('oauth', OAuthServiceProvider())

# Static resources, JavaScript and stylesheets.
for f in os.listdir(BASEDIR):
    _, suffix = os.path.splitext(f)
    if suffix in ('.js', '.css'):
        path = os.path.join(BASEDIR, f)
        resource.putChild(f, File(path))

# vim: set expandtab tabstop=4 shiftwidth=4 cindent :
