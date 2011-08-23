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

from collections import defaultdict
from django.conf import settings
from django.dispatch import receiver
from rjdj.djangotornado.signals import tornado_exit
from rjdj.tmon.server.models import resolve
from rjdj.tmon.server.couchdbviews.couchdbkeys import CouchDBKeys
from rjdj.tmon.server.utils.connection import connection
from threading import Thread, Lock
import time



__all__ = ["bulkInsertManager"]

CACHE_TIME = 300 # 5 minutes

def bulkinsert(data, webservice):
    """ """
    
    database = connection.database(webservice.name)
    database.update(data)
    
class BulkInsertManager(object):
    """ """
    
    def __init__(self):
        """ """
        
        self.insertion_stacks = defaultdict(list)
        self.lock = Lock()
        
    def insert(self, document, webservice):
        """ Adds a document to an insertion queue which will be inserted after a certain number of  """

        ins = self.insertion_stacks
        wsid = webservice.id
        with self.lock:
            ins[wsid].append(document)
            if settings.DEBUG or len(ins[wsid]) > settings.MAX_BATCH_ENTRIES:
                insertion = Thread(target = bulkinsert, args = (ins[wsid], webservice))
                insertion.start()
                ins[wsid] = []
                if settings.DEBUG: insertion.join()
                
            
            
    def cache(self, data, ws):
        """ Temporarily save the request count to memcache """
        
        t = data[CouchDBKeys.TIMESTAMP]
        tstamp = int(time.mktime(t.timetuple()))
        key = "%d_%d" % (ws.id, tstamp)
        cache.set(key, cache.get(key, 0) + 1, CACHE_TIME)

    def flush(self):
        """ Inserts all remaining documents in the cache regardless of their number. """ 
        
        worker = lambda i: bulkinsert(i[1], resolve(i[0]))
        map(worker, self.insertion_stacks.iteritems())
        self.insertion_stacks = defaultdict(list)


bulkInsertManager = BulkInsertManager()

    
def on_tornado_exit(sender, **kwargs):
    """ When Tornado exits, write everything from the buffer to the database. """
    bulkInsertManager.flush()

tornado_exit.connect(on_tornado_exit)


