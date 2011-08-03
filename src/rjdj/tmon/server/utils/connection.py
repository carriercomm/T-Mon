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
from couchdb.http import ResourceNotFound, PreconditionFailed
from django.conf import settings
from threading import Lock

class DBConnection(object):
    """ """
    
    def __init__(self, protocol, host, port, user = None, password = None):
        """ """
        
        self.protocol = protocol
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        self.connections = 0
        self.lock = Lock()
        
    def get_db(self, name):
        """ """
        server = self.connect()
        try:        
            return server[name]
        except ResourceNotFound:
            raise InvalidWebService(name)

    def disconnect(self):
    
        self.lock.acquire()
        self.connections -= 1
        self.lock.release()

    def connect(self):
        """ """
        self.lock.acquire()
        if self.user and self.password:
            url =  "%s://%s:%s@%s:%d" % (self.protocol, 
                                         self.user, 
                                         self.password, 
                                         self.host, 
                                         self.port)
        else:
            url =  "%s://%s:%d" % (self.protocol, self.host, self.port)
            
        self.connections += 1
        self.lock.release()
        return Server(url)

    def setup_db(self, name):
        """ """
        server = self.connect()
        try:
            database = server.create(name)
            for q in all_queries:
                q.sync(database)
        except PreconditionFailed:
            database = self.get_db(name)
            
        return database
        
    def remove_db(self, name):
        """ """
        server = self.connect()
        if name in server:
            del server[name]
        

# the one and only connection to the CouchDB       
connection = DBConnection(**settings.TRACKING_DATABASE)
