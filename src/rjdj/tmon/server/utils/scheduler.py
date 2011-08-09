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
from threading import Thread, Lock

class Scheduler(object):
    """ """
    
    def __init__(self):
        """ """
    
        self.lock = Lock()
        self.running_threads = 0
        self.queue = deque()
    
    def process(self, worker, *args, **kwargs):
        """ """
    
        self.lock.acquire()
        self.__process(worker, *args, **kwargs)
        self.lock.release()
    
    
    def callback(self, fn):
        """ """
        
        def wrapped(*args, **kwargs):
            """ """
            try:
                return fn(*args, **kwargs)
            except: raise
            finally: self.__on_finished()
            
        return wrapped
        
    def __process(self, worker, *args, **kwargs):
        """ """
    
        if self.running_threads <= settings.MAX_THREADS:
            t = Thread(target = self.callback(worker), 
                       args = args, 
                       kwargs = kwargs)
            t.start()
            self.running_threads += 1
    
    def __on_finished(self):
        """ """
        
        self.lock.acquire()
        self.running_threads -= 1
        self.lock.release()
        
scheduler = Scheduler()
