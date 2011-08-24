##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from couchdb import Server
from couchdb.http import ResourceNotFound, PreconditionFailed
from django.conf import settings
from rjdj.tmon.server.couchdbviews.couchdbviews import CouchDBViews
from rjdj.tmon.server.exceptions import *
from threading import Lock


class DBConnection(object):
    """ Represents a database connection. """
    
    def __init__(self, protocol, host, port, user = None, password = None):
        """ """
        
        self.protocol = protocol
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
        self.lock = Lock()
       
        
    def database(self, name):
        """ Return a specific database from the server. """
        
        server = self.create()
        try:        
            return server[name]
        except ResourceNotFound:
            raise InvalidWebService(name)


    def create(self):
        """ Creates a new Server object, representing a connection. """
        with self.lock:
            if self.user and self.password:
                url =  "%s://%s:%s@%s:%d" % (self.protocol, 
                                             self.user, 
                                             self.password, 
                                             self.host, 
                                             self.port)
            else:
                url =  "%s://%s:%d" % (self.protocol, self.host, self.port)
            
            return Server(url)
        
        
    def setup(self, name):
        """ Initial setup of the given database """

        server = self.create()
        
        try:
            database = server.create(name)
            CouchDBViews.sync(database)
        except PreconditionFailed:
            database = connection.database(name)
        return database
        
        
    def remove(self, name):
        """ Deletes the given Database """
        
        server = self.create()
        if name in server:
            del server[name]
        
        
connection = DBConnection(**settings.TRACKING_DATABASE)
