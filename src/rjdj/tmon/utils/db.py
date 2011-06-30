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

from rjdj.tmon.models import WebService
from rjdj.tmon.exceptions import *

from couchdb import Server
from django.conf import settings

server = None
database = None

def connect():
    global server
    global database
    
    protocol = settings.TRACKING_DATABASE['protocol']
    host = settings.TRACKING_DATABASE['url']
    port = settings.TRACKING_DATABASE['port']
    user = settings.TRACKING_DATABASE.get('user')
    pswd = settings.TRACKING_DATABASE.get('password')
    if user and pswd:
        url =  "%s://%s:%s@%s:%d" % (protocol, user, pswd, host, port)
    else:
        url =  "%s://%s:%d" % (protocol, host, port)
    server = Server(url)
    database = server[settings.TRACKING_DATABASE['name']]

def get_ws_secret(wsid):
    try:
        ws = WebService.objects.get(id = wsid)
    except WebService.DoesNotExist:
        raise InvalidWebService(wsid)
        
    return ws.secret
    
def get_webservice(wsid):
    try:
        return WebService.objects.get(id = wsid)
    except WebService.DoesNotExist:
        raise InvalidWebService(wsid)
        
def store(data):
    if not server: connect()
    data.store(database)

def get_db():
    if not server: connect()
    return database
