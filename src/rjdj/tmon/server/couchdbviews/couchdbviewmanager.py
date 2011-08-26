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

from datetime import datetime
import logging
import operator
from rjdj.tmon.server.couchdbviews.couchdbviews import CouchDBViews
from rjdj.tmon.server.utils.connection import connection
from rjdj.tmon.server.utils import utc_timestamp_milliseconds

logger = logging.getLogger('debug')


MAX_AGE_MINUTES = 10

def total_seconds(td):
    """ Returns the total seconds of a timedelta object. """
    
    return (td.microseconds + (td.seconds + td.days * 86400) * 1000000) / 1000000.0 ;


def get(resolution):
    """ """
    
    if resolution == "second":
        return 6, lambda dtA, dtB: int(total_seconds(dtA - dtB))
    elif resolution == "minute":
        return 5, lambda dtA, dtB: int(total_seconds(dtA - dtB) / 60)
    elif resolution == "hour":
        return 4, lambda dtA, dtB: int(total_seconds(dtA - dtB) / 3600)
    elif resolution == "day": 
        return 3, lambda dtA, dtB: int((dtA - dtB).days)
    else: 
        raise ValueError("Unkown Resolution")
    

class CouchDBViewManager(object):
    
    @staticmethod
    def requests_by_country(db_name):
        """ """
        
        database = connection.database(db_name)
        limit = utc_timestamp_milliseconds(-(MAX_AGE_MINUTES * 60))
        raw_results = CouchDBViews.requests_by_location(database, group_level = 2)[:[limit]]
        results = {}
        
        for row in raw_results:
            key = row.key[-1]
            value = row.value
            
            if results.has_key(key):
                results[key] += value
            else:
                results[key] = value
                
        return [{k: v} for k, v in sorted(results.iteritems(), key = operator.itemgetter(1), reverse = True)]
    
    @staticmethod
    def requests_by_city(db_name):
        """ """
        
        database = connection.database(db_name)        
        limit = utc_timestamp_milliseconds(-(MAX_AGE_MINUTES * 60))
        raw_results = CouchDBViews.requests_by_location(database)[:[limit]]
        
        results = {}
        
        for row in raw_results:
            key = u"{city} ({country})".format(city = row.key[-1], country = row.key[-2])
            value = row.value
            
            if results.has_key(key):
                results[key] += value
            else:
                results[key] = value
                
        return [{k: v} for k, v in sorted(results.iteritems(), key = operator.itemgetter(1), reverse = True)]
                
    @staticmethod
    def requests_locations(db_name):
        """ """ 

        database = connection.database(db_name)
        limit = utc_timestamp_milliseconds(-(MAX_AGE_MINUTES * 60))
        raw_results = CouchDBViews.requests_locations(database, limit = 500)[:[limit]]
        sources = {}
        
        for row in raw_results:
            lat, lng = (row.key[-2], row.key[-1])
            value = row.value
            
            if sources.has_key((lat, lng)):
                sources[(lat, lng)] += value
            else:
                sources[(lat, lng)] = value
            
        return [{k: v} for k, v in sources.iteritems()]    
        
    @staticmethod
    def requests_by_url(db_name):
        """ """
        
        database = connection.database(db_name)
        raw_results = CouchDBViews.requests_by_url(database)
        
        results = {}
        for row in raw_results:
            key = row.key
            value = row.value
            
            if results.has_key(key):
                results[key] += value
            else:
                results[key] = value
                
        return [{k: v} for k, v in results.iteritems()]
    
    @staticmethod
    def requests_by_device(db_name):
        """ """
        
        database = connection.database(db_name)
        raw_results = CouchDBViews.requests_by_device(database)
        
        results = {}
        for row in raw_results:
            key = row.key
            value = row.value
            
            if results.has_key(key):
                results[key] += value
            else:
                results[key] = value
                
        return [{k: v} for k, v in results.iteritems()]

    @staticmethod
    def requests_by_os(db_name):
        """ """
        
        database = connection.database(db_name)
        raw_results = CouchDBViews.requests_by_os(database)
        
        results = {}
        for row in raw_results:
            key = row.key
            value = row.value
            
            if results.has_key(key):
                results[key] += value
            else:
                results[key] = value
                
        return [{k: v} for k, v in results.iteritems()]

    @staticmethod
    def request_count(db_name, resolution, scope):
        """ """
        
        database = connection.database(db_name)
        group_lvl, converter = get(resolution)
        raw_results = CouchDBViews.request_count(database, group_level = group_lvl, limit = scope + 1)
        
        results = []
        
        now = datetime.utcnow()
        
        for row in raw_results:
            tmp = {}
            then = datetime(*row.key)
            diff = converter(now, then)
            
            if diff < scope and diff >= 0: 
                tmp[diff] = row.value
                results.append(tmp)
        
        return results
        
    @staticmethod
    def age_in_days(db_name):
        """ """
        
        database = connection.database(db_name)
        raw_results = CouchDBViewManager.execute(CouchDBViews.age_in_days, database)  
        
        return [{ row.key: row.value } for row in raw_results]

    
