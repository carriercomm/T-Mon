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

from rjdj.tmon.exceptions import *
from rjdj.tmon.utils.queries import all_queries

from couchdb import Server
from couchdb.design import ViewDefinition
from django.conf import settings


server = None
database = None

def connect(protocol, host, port, user = None, password = None):
    global server
    
    if user and password:
        url =  "%s://%s:%s@%s:%d" % (protocol, user, password, host, port)
    else:
        url =  "%s://%s:%d" % (protocol, host, port)
    server = Server(url)

def setup(wsid, protocol, host, port, user = None, password = None):
    global database
    global server
    
    if not server: connect(protocol, host, port, user, password)
    
    db_name = "_".join((settings.WEB_SERVICE_DB_PREFIX, str(wsid)))
    
    if not database and db_name not in server:         
        database = server.create(db_name)
        for q in all_queries:
            q.sync(database)
    else:
        database = server[db_name]
        
def store(data, wsid):
    setup(wsid, **settings.TRACKING_DATABASE)
    data.store(database)

def execute(query, wsid, cls = None, **options):
    if not isinstance(query, ViewDefinition): return
    setup(wsid, **settings.TRACKING_DATABASE)
    return [{ r["key"] : r["value"] } for r in query(database, **options)]
    
