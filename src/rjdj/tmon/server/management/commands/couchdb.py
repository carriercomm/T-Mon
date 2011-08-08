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

from django.core.management.base import BaseCommand
from rjdj.tmon.server.models import WebService
from rjdj.tmon.server.utils import db, queries
from rjdj.tmon.server.models.couchdbviews import CouchDBViews
from rjdj.tmon.server.utils.connection import connection
from pprint import pprint

DOCUMENTS_PER_ROUND = 5

class Command(BaseCommand):
    """ """
    
    def sync():
        """ """
    
        for ws in WebService.objects.all():
            CouchDBViews.sync(ws.name)
                    
    def flush():
        """ """
        user_input = raw_input("Delete all databases (yes/no)? ")
        really_delete = bool(user_input.lower() == "yes")
        
        if really_delete:
            dbs = 0
            print "Flushing CouchDB ..."
            server = connection.connect()
            for database in server:
                if not database.startswith("_"):
                    del server[database]
                    dbs += 1 
                    
            print dbs if dbs else "No", "databases deleted."
    
    def list_all():
        """ """
        
        print "Listing all databases ..."
        dbs = 0
        server = connection.connect()
        for database in server:
            try:
                if not database.startswith("_"): 
                    print " " * 4, database
                    dbs += 1
            except Exception as ex:
                print "Error during list: ", ex, "... ignoring"
        
        print dbs if dbs else "No", "databases found."

    def detail(name):
        """ """
        
        server = connection.connect()
        if name in server:
            database = server[name]
            print "Listing details about", name, " ..."
            
            for key, value in database.info().items():
                print " " * 4, key, ":", value
                
    
    def delete(name):
        """ """
        
        server = connection.connect()
        if not name.startswith("_") and name in server: 
            user_input = raw_input("Delete %s (yes/no)? " % name)
            really_delete = bool(user_input.lower() == "yes")
            if really_delete:
                print "Deleting", name, "..."
                del server[name]
        else:
            print name, "not found or it is a system database (leading '_')"
    
    
    def iterate(name):
        """ """
        
        server = connection.connect()
        if name in server:
            database = server[name]
            print "Iterating through", name, "with", DOCUMENTS_PER_ROUND, "Documents per round ..."
            
            rounds = 1
            for doc in database:
                d = database[doc]
                if not d["_id"].startswith("_"):
                    for k, v in d.iteritems():
                        print " " * 4, k, ":", v
                    print " " * 4, "-" * 10, "\n"
                    
                    if rounds % DOCUMENTS_PER_ROUND == 0:
                        user_input = raw_input("Another %d Documents? (n/q) " % DOCUMENTS_PER_ROUND)
                        if user_input.lower() != 'n': return

                    rounds += 1
    
    def cleanup(name, age):
        """ """
        
        server = connection.connect()
        if name in server:
            rows = 0
        
            database = server[name]
            query = queries.age_in_days
            results = query(database)
            age = int(age)
            for row in results[:age]:
                del database[row.id]
                rows += 1
            
            print "Deleted", rows, "entries from", name
        

    available_commands = { 
        "flush": flush,
        "list": list_all,
        "sync": sync,
        
        "detail": detail,
        "delete": delete,
        "iter": iterate,
        "cleanup": cleanup,
    }
    
    commands_text = "\n  -" + "\n  -".join(available_commands.keys())
    
    help_text = """Welcome to T-Mon's CouchDB interface, available commands are:"""
    help = "".join((help_text, commands_text))
    
    def handle(self, *args, **kwargs):
        """ """
        server = connection.connect()
        self.errors = 0
        cmd = "abc"
        if args:
            cmd = args[0]
            cmd_args = args[1:]
        print "\n" * 3
        print "T-Mon's CouchDB interface!"
        print "-" * 60
        print "Connected to", server.resource.url, "version", server.version(), "\n"
        try:
            self.available_commands[cmd](*cmd_args)
            print "done."
        except KeyError:
            print "Command not found!"
            print self.help
        except Exception as ex:
            print "ERROR:", ex
            print "Command not completed!"
        finally:
            print ""
    
