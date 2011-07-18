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

insertion_stacks = {}

__all__ = ["BulkInsertManager"]

class BulkInsertManager(object):
    """ """
    
    @staticmethod
    def insert(document, wsid):
        """ Adds a document to an insertion queue which will be inserted after a certain number of  """
        
        if not insertion_stacks.has_key(wsid):
            insertion_stacks[wsid] = [document]
        else:
            insertion_stacks[wsid].append(document)
        
                    
        if settings.DEBUG or len(insertion_stacks[wsid]) > settings.MAX_BATCH_ENTRIES:
            db.bulkinsert(insertion_stacks[wsid], wsid)
            insertion_stacks[wsid] = []        
            
    @staticmethod
    def insert_all():
        """ Inserts all remaining documents in the cache regardless of their number. """ 
        
        for wsid, stack in insertion_stacks.items():
            db.bulkinsert(stack, wsid)
            
        insertion_stacks = {}
        
def on_tornado_exit(sender, **kwargs):
    """ When Tornado exits, write everything from the buffer to the database. """
    BulkInsertManager.insert_all()

tornado_exit.connect(on_tornado_exit)
