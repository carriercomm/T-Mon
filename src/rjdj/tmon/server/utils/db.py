##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from couchdb.design import ViewDefinition
from rjdj.tmon.server.utils.connection import connection
from django.core.cache import cache
from rjdj.tmon.server.models import WebService
from rjdj.tmon.server.exceptions import *

# memcached's retention time
CACHE_TIME = 2629744 # seconds of 1 month

def get_webservice(wsid):
    """ Retrieves a WebService instance from Django's DB. """ 
    
    try:
        webservice = cache.get(wsid) or WebService.objects.get(id = wsid)
        cache.set(wsid, webservice, CACHE_TIME)
        return webservice   
        
    except WebService.DoesNotExist as ws: 
        raise InvalidWebService(ws)

def store(data, wsid):
    """ Writes the given data to the associated CouchDB. """
    ws_name = get_webservice(wsid).name
    
    if data:
        data.store(connection.switch_db(ws_name))

def execute(query, wsid, **options):
    """ Executes a query from utils.queries. """

    if isinstance(query, ViewDefinition):
    
        ws_name = get_webservice(wsid).name
        return query(connection.switch_db(ws_name), **options)

def sync(query, wsid):
    """ Syncs the given utils.query query with the associated CouchDB. """
    
    if isinstance(query, ViewDefinition):
        ws_name = get_webservice(wsid).name
        query.sync(connection.switch_db(ws_name))
