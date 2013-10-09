# Copyright 2012, 2013 GRNET S.A. All rights reserved.
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

try:
    from django.core.servers.basehttp import is_hop_by_hop
except ImportError:
    # Removed in Django 1.4
    _hop_headers = {
        'connection': 1, 'keep-alive': 1, 'proxy-authenticate': 1,
        'proxy-authorization': 1, 'te': 1, 'trailers': 1,
        'transfer-encoding': 1, 'upgrade': 1
    }

    def is_hop_by_hop(header_name):
        """Return true if 'header_name' is an HTTP/1.1 "Hop-by-Hop" header"""
        return header_name.lower() in _hop_headers


def fix_header(k, v):
    prefix = 'HTTP_'
    if k.startswith(prefix):
        k = k[len(prefix):].title().replace('_', '-')
    return k, v


def forward_header(k):
    return k.upper() not in ['HOST', 'CONTENT_LENGTH', 'CONTENT_TYPE'] and \
        not is_hop_by_hop(k) and not '.' in k
