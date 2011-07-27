#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rjdj.tmon.server.utils.queries import all_queries
from rjdj.tmon.server.utils.connection import connection

from threading import Thread
import time

PAUSE = 5 # seconds

def refresh(view_name, server):

    for database in connection.server:
        if not database.startswith("_"):
            db = server[database]
            db.view(view_name, limit = 0)
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
    
    
