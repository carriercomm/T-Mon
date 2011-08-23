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

from django.conf import settings
from collections import deque
from multiprocessing.pool import ThreadPool
from rjdj.djangotornado.signals import tornado_exit


class Scheduler(object):
    """ """
    
    def __init__(self):
        """ """
        
        self.pool = ThreadPool()
        self.threads = deque()
    
    def process(self, worker, *args, **kwargs):
        """ """
        
        t = self.pool.apply_async(worker, args, kwargs)
        self.threads.append(t)
        
    def join(self):
        """ Joins the underlying ThreadPool """
        p = self.pool
        p.close()
        p.join()
        
scheduler = Scheduler()

def on_tornado_exit(sender, **kwargs):
    """ When Tornado exits, finish all threads. """
    
    scheduler.join()

tornado_exit.connect(on_tornado_exit)

