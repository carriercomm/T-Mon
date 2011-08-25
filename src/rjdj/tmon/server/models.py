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

import time
from couchdb.http import PreconditionFailed
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import transaction, models
from rjdj.tmon.server.couchdbviews.couchdbviewmanager import CouchDBViewManager
from rjdj.tmon.server.couchdbviews.couchdbkeys import CouchDBKeys
from rjdj.tmon.server.exceptions import *
from rjdj.tmon.server.utils import utc_timestamp_milliseconds
from rjdj.tmon.server.utils.connection import connection     
from threading import Lock
from rjdj.tmon.server.utils.decorators import synced
import ujson
from couchdb import json 

# memcached's retention time
CACHE_TIME = 2629744 # seconds of 1 month

# set python-couchdb's json encoder/decoder
json.use(encode = ujson.encode, decode = ujson.decode)

# http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
name_validator = RegexValidator(regex = r'^[a-z][a-z0-9\_\$()\+\-]*$', 
                                message = 'Name must be a valid CouchDB Database name (without a "/")')

# Resolver lock
lock = Lock()

class WebService(models.Model):
    """ Represents any web service to be tracked """
    
    owner = models.ForeignKey(User)
    secret = models.CharField("Secret for web service authentication", max_length = 128, unique = True)
    name = models.CharField("Name of the Service", max_length = 40, unique = True, validators = [name_validator])
    
    
    @transaction.commit_on_success
    def save(self, *args, **kwargs):
    
        super(WebService, self).save(*args, **kwargs)
        connection.setup(self.name)
        
    
    @transaction.commit_on_success
    def delete(*args, **kwargs):
    
        name = self.name
        super(WebService, self).save(*args, **kwargs)
        connection.remove(name)   
        

class TrackingData(object):
    """ A class for saving trackable data """
    
    views = CouchDBViewManager
    
    keys = CouchDBKeys
    
    @staticmethod
    def now():
        """ Returns a unified UTC timestamp """
        
        return utc_timestamp_milliseconds()
        
@synced(lock)        
def resolve(wsid):
    """ Retrieves a WebService instance from Django's DB. """ 

    if isinstance(wsid, WebService):
        return wsid
    
    try:
        webservice = cache.get(wsid) or WebService.objects.get(id = wsid)
        cache.set(wsid, webservice, CACHE_TIME)
        return webservice   
        
    except WebService.DoesNotExist as ws: 
        raise InvalidWebService(ws)
