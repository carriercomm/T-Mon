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

from rjdj.tmon.server.utils import db
from rjdj.djangotornado.signals import tornado_exit

from django.conf import settings
from django.dispatch import receiver

__all__ = ["bulkInsertManager"]

class BulkInsertManager(object):
    """ """
    
    def __init__(self):
        """ """
        
        self.insertion_stacks = {}

    
    def insert(self, document, webservice):
        """ Adds a document to an insertion queue which will be inserted after a certain number of  """
        
        wsid = webservice.id
        
        if not self.insertion_stacks.has_key(wsid):
            self.insertion_stacks[wsid] = [document]
        else:
            self.insertion_stacks[wsid].append(document)
        
                    
        if settings.DEBUG or len(self.insertion_stacks[wsid]) > settings.MAX_BATCH_ENTRIES:
            db.bulkinsert(self.insertion_stacks[wsid], webservice)
            self.insertion_stacks[wsid] = []        

    def insert_all(self):
        """ Inserts all remaining documents in the cache regardless of their number. """ 
        
        for wsid, stack in self.insertion_stacks.items():
            db.bulkinsert(stack, wsid)
            
        self.insertion_stacks = {}

bulkInsertManager = BulkInsertManager()
    
def on_tornado_exit(sender, **kwargs):
    """ When Tornado exits, write everything from the buffer to the database. """
    bulkInsertManager.insert_all()

tornado_exit.connect(on_tornado_exit)


