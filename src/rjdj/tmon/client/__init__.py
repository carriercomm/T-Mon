##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of TMon.
#
# TMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-tornado. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import urllib2
import urllib
import json
from sys import stderr
from rjdj.tmon.client import config
from rjdj.tmon.client.exceptions import * 
from rjdj.tmon.client.utils import *


REMOTE_URL = "data/collect"

IP_KEY = 'ip'
UA_KEY = 'useragent'
USER_KEY = 'username'
URL_KEY = 'url'

#
# { data: {ip: ..., useragent: ..., username: ...} wsid: ... }
#         |   <-- encrypted payload -->          |  
#

def track(url, user_agent, remote_ip, username = ""):
    if not (config.SERVER_URL and config.WEBSERVICE_ID and config.WEBSERVICE_SECRET):
        raise NotConfigured()
    
    server = ""
    if config.SERVER_URL.endswith("/"):
        server = "".join((config.SERVER_URL, REMOTE_URL))
    else:
        server = "/".join((config.SERVER_URL, REMOTE_URL))
    
    data = { IP_KEY : remote_ip,
             UA_KEY : user_agent,
             URL_KEY: url }
    if username:
        data.update({ USER_KEY: username })
    wsid = int(config.WEBSERVICE_ID)
    encrypted_data = encrypt_message(json.dumps(data), config.WEBSERVICE_SECRET)
    try:
        urllib2.urlopen(server, urllib.urlencode({"data": encrypted_data, "wsid": wsid })).read()
    except Exception as ex: 
        stderr.write("Error while tracking the webservice: %s" % (ex)) 
