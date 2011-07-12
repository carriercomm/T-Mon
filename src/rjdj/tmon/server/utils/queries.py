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
                        map_fun = """function(doc) { emit(doc["country"], 1); }""",
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
                        group = True)

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
                        group = True)

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
                                            emit([doc["latitude"], doc["longitude"]], 1)
                                        } """,
                        reduce_fun = """function(keys, values) { return sum(values); }""",
                        group = True)

all_queries = (
        users_per_country,
        users_per_os,
        users_per_device,
        request_count,
        users_locations,
    )
