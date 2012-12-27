# Copyright 2011-2012 GRNET S.A. All rights reserved.
#
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
#
#   1. Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY GRNET S.A. ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL GRNET S.A OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and
# documentation are those of the authors and should not be
# interpreted as representing official policies, either expressed
# or implied, of GRNET S.A.

import logging

from time import time, mktime
from urlparse import urlparse, urlsplit, urlunsplit
from urllib import quote, unquote

from django.conf import settings
from django.utils import simplejson as json
from django.utils.http import urlencode

from synnefo.lib.pool.http import get_http_connection

logger = logging.getLogger(__name__)

def retry(howmany):
    def execute(func):
        def f(*args, **kwargs):
            attempts = 0
            while attempts < howmany:
                try:
                    return func(*args, **kwargs)
                except Exception, e:
                    if e.args:
                        status = e.args[-1]
                        # In case of Unauthorized response or Not Found return directly
                        if status == 401 or status == 404:
                            raise e
                    attempts += 1
        return f
    return execute

def call(token, url, headers={}):
    p = urlparse(url)

    kwargs = {}
    kwargs['headers'] = headers
    kwargs['headers']['X-Auth-Token'] = token
    kwargs['headers']['Content-Length'] = 0

    conn = get_http_connection(p.netloc, p.scheme)
    try:
        conn.request('GET', p.path, **kwargs)
        response = conn.getresponse()
        headers = response.getheaders()
        headers = dict((unquote(h), unquote(v)) for h,v in headers)
        length = response.getheader('content-length', None)
        data = response.read(length)
        status = int(response.status)
    finally:
        conn.close()

    if status < 200 or status >= 300:
        raise Exception(data, status)

    return json.loads(data)


def authenticate(token, authentication_url='http://127.0.0.1:8000/im/authenticate'):
    return call(token, authentication_url)

@retry(3)
def get_username(token, uuid, url='http://127.0.0.1:8000/im/service/api/v2.0/users'):
    try:
        data = call(token, url, {'X-User-Uuid': uuid})
    except Exception, e:
        raise e
    else:
        return data.get('username')


@retry(3)
def get_user_uuid(token, username, url='http://127.0.0.1:8000/im/service/api/v2.0/users'):
    try:
        data = call(token, url, {'X-User-Username': username})
    except Exception, e:
        raise e
    else:
        return data.get('uuid')


def user_for_token(token, authentication_url, override_users):
    if not token:
        return None

    if override_users:
        try:
            return {'uniq': override_users[token].decode('utf8')}
        except:
            return None

    try:
        return authenticate(token, authentication_url)
    except Exception, e:
        # In case of Unauthorized response return None
        if e.args and e.args[-1] == 401:
            return None
        raise e

def get_user(request, authentication_url='http://127.0.0.1:8000/im/authenticate', override_users={}, fallback_token=None):
    request.user = None
    request.user_uniq = None

    # Try to find token in a parameter or in a request header.
    user = user_for_token(request.GET.get('X-Auth-Token'), authentication_url, override_users)
    if not user:
        user = user_for_token(request.META.get('HTTP_X_AUTH_TOKEN'), authentication_url, override_users)
    if not user:
        user = user_for_token(fallback_token, authentication_url, override_users)
    if not user:
        logger.warning("Cannot retrieve user details from %s",
                       authentication_url)
        return

    # use user uuid, instead of email, keep email/username reference to user_id
    request.user_uniq = user['uuid']
    request.user = user
    request.user_id = user['username']
    return user


def get_token_from_cookie(request, cookiename):
    """
    Extract token from the cookie name provided. Cookie should be in the same
    form as astakos service sets its cookie contents::

        <user_uniq>|<user_token>
    """
    try:
        cookie_content = unquote(request.COOKIES.get(cookiename, None))
        return cookie_content.split("|")[1]
    except AttributeError:
        pass

    return None
