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

from rjdj.tmon.server.exceptions import *
from rjdj.tmon.server.utils.queries import all_queries

from couchdb import Server
from django.conf import settings

class DBConnection(object):
    
    def __init__(self, protocol, host, port, user = None, password = None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.server = self.connect()
        self.database = None
        
    def switch_db(self, wsid):
        db_name = "_".join((settings.WEB_SERVICE_DB_PREFIX, str(wsid)))
        
        if db_name not in self.server:
            raise InvalidWebService(wsid)
        
        if not self.database or self.database.name != db_name:
            self.database = self.server[db_name]
        
        return self.database

    def connect(self):
        if self.user and self.password:
            url =  "%s://%s:%s@%s:%d" % (self.protocol, 
                                         self.user, 
                                         self.password, 
                                         self.host, 
                                         self.port)
        else:
            url =  "%s://%s:%d" % (self.protocol, self.host, self.port)
        return Server(url)

    def setup_db(self, wsid):
        db_name = "_".join((settings.WEB_SERVICE_DB_PREFIX, str(wsid)))
        
        if db_name not in self.server:
            self.database = self.server.create(db_name)
            for q in all_queries:
                q.sync(self.database)
        elif db_name in self.server:
            self.switch_db(wsid)
            
        return self.database
        
connection = DBConnection(**settings.TRACKING_DATABASE)
