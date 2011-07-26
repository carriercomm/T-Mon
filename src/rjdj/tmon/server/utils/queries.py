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

from couchdb.design import ViewDefinition

users_per_country = ViewDefinition(
                        design = "geographic",
                        name = "users_per_country",
                        map_fun = """   function(doc) {
                                            if(doc["country"] != null && doc["country"] != "") {  
                                                var regexp = /(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z/;
                                                var matched = doc.timestamp.match(regexp);
                                                matched.shift();
                                                for(var i = 0; i < matched.length; i++) {
                                                    matched[i] = Number(matched[i]);
                                                }

                                                var timestamp = new Date(matched[0], 
                                                                         matched[1] - 1, 
                                                                         matched[2], 
                                                                         matched[3], 
                                                                         matched[4], 
                                                                         matched[5], 0);
                                                var now = new Date();
                                                var diff_date = now - timestamp;
                                                var num_minutes = Math.round(diff_date / 60000); 
                                                if(num_minutes < 10) {
                                                    emit(doc["country"], 1); 
                                                }
                                            }
                                        }""",
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True)
                        
                                        
users_per_city = ViewDefinition(
                        design = "geographic",
                        name = "users_per_city",
                        map_fun = """   function(doc) {
                                            if(doc["city"] != null && doc["city"] != "") {    
                                                var regexp = /(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z/;
                                                var matched = doc.timestamp.match(regexp);
                                                matched.shift();

                                                for(var i = 0; i < matched.length; i++) {
                                                    matched[i] = Number(matched[i]);
                                                }

                                                var timestamp = new Date(matched[0], 
                                                                         matched[1] - 1, 
                                                                         matched[2], 
                                                                         matched[3], 
                                                                         matched[4], 
                                                                         matched[5], 0);
                                                var now = new Date();
                                                var diff_date = now - timestamp;
                                                var num_minutes = Math.round(diff_date / 60000); 
                                                
                                                if(num_minutes < 10) {
                                                    emit(doc["city"] + " (" + doc["country"] + ")", 1); 
                                                }
                                            }
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True)


users_per_device = ViewDefinition(
                        design = "geographic",
                        name = "users_per_device",
                        map_fun = """   function(doc)  {
                                            var regexp = /([\w\s\/]+); (U; )?([\w\d\.\_\s]+)/;
                                            res = doc["user_agent"].match(regexp);
                                            if (res != null) {
                                                emit(res[1], 1);
                                            }
                                            else {
                                                emit("other", 1);
                                            }
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True,
                        limit = 500)


users_per_os = ViewDefinition(
                        design = "geographic",
                        name = "users_per_os",
                        map_fun = """   function(doc)  {
                                            var regexp = /([\w\s\/]+); (U; )?([\w\d\.\_\s]+)/;
                                            res = doc["user_agent"].match(regexp);
                                            if (res != null) {
                                                emit(res[res.length - 1], 1);
                                            } else {
                                                emit("other", 1);
                                            }
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True,
                        limit = 500)


request_count = ViewDefinition(
                        design = "requests",
                        name = "count",
                        map_fun = """   function(doc) {
                                            var regexp = /(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z/;
                                            var matched = doc.timestamp.match(regexp);
                                            matched.shift();
                                            for(var i = 0; i < matched.length; i++) {
                                                matched[i] = Number(matched[i]);
                                            }
                                            emit(matched, 1);
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True,
                        descending = True)
                        
                        
users_locations = ViewDefinition(
                        design = "geographic",
                        name = "users_locations",
                        map_fun = """   function(doc) {
                                            if(doc["latitude"] != null && doc["longitude"] != null) {
                                                var regexp = /(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z/;
                                                var matched = doc.timestamp.match(regexp);
                                                matched.shift();

                                                for(var i = 0; i < matched.length; i++) {
                                                    matched[i] = Number(matched[i]);
                                                }

                                                var timestamp = new Date(matched[0], 
                                                                         matched[1] - 1, 
                                                                         matched[2], 
                                                                         matched[3], 
                                                                         matched[4], 
                                                                         matched[5], 0);
                                                var now = new Date();
                                                var diff_date = (now - timestamp) / 1000;
                                                emit([ diff_date, doc["latitude"], doc["longitude"] ], 1);
                                            }
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True)


# hacky ... from http://www.java2s.com/Tutorial/JavaScript/0240__Date/Getyearmonthanddayfromdatedifference.htm
age_in_days = ViewDefinition(
                        design = "entries",
                        name = "age_in_days",
                        map_fun = """   function(doc) {
                                            var regexp = /(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z/;
                                            var matched = doc.timestamp.match(regexp);
                                            matched.shift();

                                            for(var i = 0; i < matched.length; i++) {
                                                matched[i] = Number(matched[i]);
                                            }

                                            var timestamp = new Date(matched[0], 
                                                                     matched[1] - 1, 
                                                                     matched[2], 
                                                                     matched[3], 
                                                                     matched[4], 
                                                                     matched[5], 0);
                                            var now = new Date();
                                            var diff_date = now - timestamp;
                                            var num_days = ((diff_date % 31536000000) % 2628000000) / 86400000; 
                                            emit(num_days, doc._id);
                                        } """,
                                        descending = True)
all_queries = (
        users_per_country,
        users_per_city,
        users_per_os,
        users_per_device,
        request_count,
        users_locations,
        age_in_days,
    )

def get_queries_as_dict():
    """ """
    
    queries_dict = {}
    for q in all_queries:
        if isinstance(queries_dict[q.design_doc], list):
            queries_dict[q.design_doc] = [q.name]  
        else:
            queries_dict[q.design_doc].append(q.name)
            
    return queries_dict
