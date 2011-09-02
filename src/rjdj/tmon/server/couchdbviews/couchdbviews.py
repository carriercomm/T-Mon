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

from couchdb.design import ViewDefinition
from rjdj.tmon.server.couchdbviews.couchdbkeys import CouchDBKeys as Keys

# using the _sum Erlang function as a reduce function.
# from:
# http://wiki.apache.org/couchdb/Performance#View_generation

class CouchDBViews:
    """ """
    
    @staticmethod
    def sync(database):
        """ """
        for v in CouchDBViews.all():
            v.sync(database)
        
    
    @staticmethod
    def all():
        """ Returns all Views for the TrackingData class """
            
        return [view for name, view in CouchDBViews.__dict__.iteritems() if isinstance(view, ViewDefinition)]
        
    requests_by_location = ViewDefinition(
                            design = "geographic",
                            name = "requests_by_location",
                            map_fun = """   function(doc) {{
                                                if(doc.{country} == undefined || doc.{country} == null || doc.{country} == "") 
                                                    return;
                                                timestamp = new Date(doc.{timestamp});
                                                time_in_minutes = Math.round(timestamp.getTime() / 60000)
                                                var city = doc.{city} == undefined? null: doc.{city};
                                                emit([ time_in_minutes, doc.{country}, city ], 1);
                                            }}""".format(country = Keys.COUNTRY, 
                                                         timestamp = Keys.TIMESTAMP, 
                                                         city = Keys.CITY),
                            reduce_fun = """_sum""",
                            group = True)
                            
                                            
    requests_by_device = ViewDefinition(
                            design = "devices",
                            name = "requests_by_device",
                            map_fun = """   function(doc)  {{
                                                var regexp = /([\w\s\/]+); (U; )?([\w\d\.\_\s]+)/;
                                                res = doc.{user_agent}.match(regexp);
                                                if (res != null)
                                                    emit(res[1], 1);
                                                else
                                                    emit("other", 1);
                                            }}""".format(user_agent = Keys.USER_AGENT),
                            reduce_fun = """_sum""",
                            group = True,
                            limit = 500)


    requests_by_os = ViewDefinition(
                            design = "devices",
                            name = "requests_by_os",
                            map_fun = """   function(doc)  {{
                                                var regexp = /([\w\s\/]+); (U; )?([\w\d\.\_\s]+)/;
                                                res = doc.{user_agent}.match(regexp);
                                                if (res != null) 
                                                    emit(res[res.length - 1], 1);
                                                else 
                                                    emit("other", 1);
                                                
                                            }}""".format(user_agent = Keys.USER_AGENT),
                            reduce_fun = """_sum""",
                            group = True,
                            limit = 500)


    requests_by_url = ViewDefinition(
                            design = "devices",
                            name = "requests_by_url",
                            map_fun = """   function(doc) {{
                                                if(doc.{url} == undefined || doc.{url} == null && doc.{url} == "") 
                                                    return;  
                                                emit(doc.{url}.toLowerCase().replace(" ", ""), 1);
                                            }}""".format(url = Keys.URL),
                            reduce_fun = """_sum""",
                            group = True)


    request_count = ViewDefinition(
                            design = "requests",
                            name = "count",
                            map_fun = """   function(doc) {{
                                                timestamp = new Date();
                                                timestamp.setTime(doc.{timestamp});
                                                emit([ timestamp.getFullYear(), 
                                                       timestamp.getMonth() + 1, 
                                                       timestamp.getDate(), 
                                                       timestamp.getHours(), 
                                                       timestamp.getMinutes(), 
                                                       timestamp.getSeconds() ], 1);
                                            }} """.format(timestamp = Keys.TIMESTAMP),
                            reduce_fun = """_sum""",
                            group = True,
                            descending = True)
                            
                            
    requests_locations = ViewDefinition(
                            design = "geographic",
                            name = "requests_locations",
                            map_fun = """   function(doc) {{
                                                if(doc.{lat} == undefined || doc.{lng} == undefined ||
                                                   doc.{lat} == null || doc.{lng} == null) 
                                                    return;
                                                    
                                                emit([ timestamp, doc.{lat}, doc.{lng} ], 1);
                                            }}""".format(lat = Keys.LATITUDE, 
                                                         lng = Keys.LONGITUDE, 
                                                         timestamp = Keys.TIMESTAMP),
                            reduce_fun = """_sum""",
                            group = True,
                            descending = True)  


    age_in_days = ViewDefinition(
                            design = "entries",
                            name = "age_in_days",
                            map_fun = """   function(doc) {{
                                                timestamp = new Date(doc.{timestamp});
                                                time_in_minutes = Math.round(timestamp.getTime() / 60000)
                                                emit(time_in_minutes, doc._id);
                                            }}""".format(timestamp = Keys.TIMESTAMP),
                                            descending = True)
