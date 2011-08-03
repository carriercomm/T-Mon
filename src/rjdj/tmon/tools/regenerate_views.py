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

from rjdj.tmon.server.utils.queries import all_queries
from rjdj.tmon.server.utils.connection import connection

from threading import Thread
import time

PAUSE = 5 # seconds

def refresh(view_name, server):

    for database in connection.server:
        if not database.startswith("_"):
            db = server[database]
            db.view(view_name, limit = 0).total_rows
        time.sleep(PAUSE)
        
        
def run(*args):

    server = connection.server  
    threads = []
    
    for query in all_queries:
        q_path = "/".join((query.design, query.name))
        t = Thread(target = refresh, args = (q_path, server))
        t.start()
        
    for thread in threads:
        thread.join()    
    
    
