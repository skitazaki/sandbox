#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TODO: setup logger instead of root level.
#

"""\\
Wrapper script of `oauth` module.
This implemetantion uses referencial OAuth library and ``urllib2``.

:Author: KITAZAKI Shigeru
:Version: 0.4
"""

import logging
import sys
import urllib
import urllib2
import webbrowser

import oauth.oauth as oauth


class SimpleOAuthClient(oauth.OAuthClient):
    """Example client using urllib2.
    """

    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

    def _send_request(self, url_request):
        """Send HTTP request acutually using ``urllib2`` module.

        :param urllib2.Request url_request: request object to send
        :rtype: urllib2.Response
        """
        try:
            res = urllib2.urlopen(url_request)
            headers = res.info()
            logging.debug('Got resource: %s' % (headers['Content-Type'],))
            return res
        except urllib2.HTTPError, e:
            raise IOError(e.read())

    def fetch_request_token(self, oauth_request):
        """Fetch request token.

        :param oauth.OAuthRequest oauth_request: request object
            which contains credentials and was set http_method and http_url.
        :rtype: oauth.OAuthToken
        """
        oauth_request.sign_request(self.signature_method, self.consumer, None)
        req = urllib2.Request(oauth_request.http_url, [],
                oauth_request.to_header())
        r = self._send_request(req)
        self.request_token = oauth.OAuthToken.from_string(r.read())
        return self.request_token

    def fetch_access_token(self, oauth_request):
        """Fetch access token.

        :param oauth.OAuthRequest oauth_request: request object
            which contains credentials and was set http_method and http_url.
        :rtype: oauth.OAuthToken
        """
        oauth_request.sign_request(self.signature_method,
                self.consumer, self.request_token)
        req = urllib2.Request(oauth_request.http_url,
                urllib.urlencode(oauth_request.get_nonoauth_parameters()),
                oauth_request.to_header())
        r = self._send_request(req)
        return oauth.OAuthToken.from_string(r.read())

    def access_resource(self, oauth_request, data=None):
        """Access resources with authorized request and some data.

        :param oauth.OAuthRequest oauth_request: request object
            which contains credentials.
        :param data: data lists to POST
        :rtype: urllib2.Response
        """
        oauth_request.sign_request(self.signature_method,
                self.consumer, self.token)
        headers = oauth_request.to_header()
        req = urllib2.Request(oauth_request.http_url, headers=headers)
        if oauth_request.http_method == "POST":
            if data:
                logging.debug(":data %s" % (data,))
                req.add_header('Content-Type', 'application/atom+xml')
                req.add_data(data)
            else:
                req.add_header('Content-Type',
                        'application/x-www-form-urlencoded')
                req.add_data(urllib.urlencode(
                            oauth_request.get_nonoauth_parameters()))
        return self._send_request(req)

    def access(self, url, params=None, data=None):
        """Thin wrapper of `access_resource()`.
        Use this from API to avoid using `OAuthRequest`.

        :param string url: url to access resource
        :param params: parameters to set query string
        :param data: data lists to POST
        :type params: dict or None
        :type data: list or None
        :rtype: urllib2.Response
        """
        logging.debug("Access protected resources: %s" % (url,))
        if params:
            url += "?" + "&".join(["%s=%s" % (k, v)
                    for k, v in params.iteritems()])
            logging.debug("Added parameters: %s" % (url,))
        request = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                    token=self.token,
                    http_url=url, parameters=params)
        if data:
            request.http_method = "POST"
        return self.access_resource(request, data)

    def initialize(self, endpoints):
        """Initialize client instance, in short, fetch access token.

        :param endpoints tuple: list of endpoint to work with OAuth-dance.
        :rtype: tuple composed of key/secret pair.
        """
        if len(endpoints) == 1:
            oauth_token = initialize_direct(self, endpoints)
        elif len(endpoints) == 3:
            oauth_token = initialize_dance(self, endpoints)
        else:
            raise Error("Invalid parameters.")
        if oauth_token is None:
            raise Error("Fail to initialize your account.")
        return (str(oauth_token.key), str(oauth_token.secret))


def initialize_dance(client, endpoints):
    """Start 3-way dance for OAuth negotiation.

    :param SimpleOAuthClient client: client instance
    :param tuple endpoints: sequence of urls.
    :rtype: oauth.OAuthToken
    """
    assert len(endpoints) == 3
    request = oauth.OAuthRequest.from_consumer_and_token(client.consumer)
    request.http_method = "POST"
    request.http_url = endpoints[0]
    request_token = client.fetch_request_token(request)
    logging.debug('''Obtained request token:
key                : %s
secret             : %s
callback confirmed : %s
''' % (request_token.key,
        request_token.secret,
        request_token.callback_confirmed))
    logging.info("Get verifier code on your web browser.")
    url = "%s?oauth_token=%s" % (endpoints[1], request_token.key)
    webbrowser.open_new_tab(url)
    try:
        verifier = raw_input("verifier >")
    except KeyboardInterrupt:
        logging.info("Bye!")
        sys.exit(1)
    if not verifier:
        raise IOError("No verifier code.")
    request = oauth.OAuthRequest.from_consumer_and_token(
            client.consumer, token=request_token, verifier=verifier)
    request.http_method = "POST"
    request.http_url = endpoints[2]
    access_token = client.fetch_access_token(request)
    return access_token


def initialize_direct(client, endpoints):
    """Do xAuth authorization.

    :param SimpleOAuthClient client: client instance
    :param tuple endpoints: sequence of urls.
    :rtype: oauth.OAuthToken
    """
    assert len(endpoints) == 1
    print "Let's begin xAuth. Please input your usename and password."
    print "-" * 60
    import getpass
    username = raw_input("username >")
    password = getpass.getpass("password >")
    params = {'x_auth_mode': "client_auth",
              'x_auth_username': username,
              'x_auth_password': password}
    request = oauth.OAuthRequest.from_consumer_and_token(client.consumer,
                parameters=params)
    request.http_method = "POST"
    request.http_url = endpoints[0]
    client.request_token = None
    access_token = client.fetch_access_token(request)
    return access_token


def create(consumer_token, access_token=None):
    """Creates client object.

    Args:
    :param consumer_token: consumer token composed from 2-item tuple.
    :param access_token: access token composed from 2-item tuple.
    :rtype: SimpleOAuthClient
    """
    assert len(consumer_token) == 2
    consumer = oauth.OAuthConsumer(consumer_token[0], consumer_token[1])
    if access_token:
        assert len(access_token) == 2
        token = oauth.OAuthToken(access_token[0], access_token[1])
        client = SimpleOAuthClient(consumer, token)
    else:
        client = SimpleOAuthClient(consumer, None)
    return client


def test():
    # any tests will be welcomed :D
    consumer_token = ('ANONYMOUS', 'ANONYMOUS')
    access_token = ('SAMPLE', 'SAMPLE')
    client = create(consumer_token)
    assert client.consumer
    assert client.token is None
    client = create(consumer_token, access_token)
    assert client.consumer
    assert client.token

if __name__ == '__main__':
    test()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
