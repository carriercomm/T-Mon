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

from datetime import datetime
import operator

class BasicAdapter(object):
    """ """

    def __init__(self, query_results, max_results = 0, converter = None):
        """ """
        
        self.raw_results = query_results
        self.max_results = max_results
        self.converter = converter
        
    def process(self):
        """ 
        Uses the key() and value() methods to extract information from all rows.
        Returns a list of dicts { key(): value() } per default, should be overwritten when necessary.
        """
        return [{ self.key(res) : self.value(res) } for res in self.raw_results]
        
    def key(self, row): raise NotImplementedError()
    def value(self, row): raise NotImplementedError()
        
        
class DefaultDictAdapter(BasicAdapter):
    """ """
    
    def key(self, row):
        return row["key"]
    
    def value(self, row):
        return row["value"]
        
        
class GeoRequestAdapter(BasicAdapter):
    """ """
    
    def process(self):
        results = {}
        for res in self.raw_results:
            key = self.key(res)
            if results.has_key(key):
                results[key] += self.value(res)
            else:
                results[key] = self.value(res)
            
        return [{k: v} for k, v in sorted(results.iteritems(), key = operator.itemgetter(1), reverse = True)]
    
    def key(self, row):
        return row["key"][-1]
    
    def value(self, row):
        return row["value"]
    
    
class PieChartAdapter(BasicAdapter):    
    """ """
    
    def process(self):
        return [{ "label": self.key(res), "data": self.value(res) } for res in self.raw_results]

    def key(self, row):
        return row["key"]
    
    def value(self, row):
        return row["value"]


class MapAdapter(BasicAdapter):
    """ """
    
    def process(self):
        sources = {}
        
        for res in self.raw_results:
            lat, lng = self.key(res)
            if sources.has_key((lat, lng)):
                sources[(lat, lng)] += self.value(res)
            else:
                sources[(lat, lng)] = self.value(res)
            
            
        return [ {"lat": k[0], "lng": k[1], "count": v } for k, v in sources.iteritems() ]
        
    def key(self, row): 
        return (row["key"][-2], row["key"][-1])
        
    def value(self, row): 
        return row["value"]
    
    
class RequestResultAdapter(BasicAdapter):
    """ """
    
    def process(self):
        if not self.converter: raise ValueError("a converter is required for this adapter")
        tmp = [0] * self.max_results
        results = []
        now = datetime.now()
        
        for row in self.raw_results:
            then = self.key(row)
            diff = self.converter(now, then)
            
            if diff < self.max_results: 
                tmp[diff] = self.value(row)
        
        for i in xrange(self.max_results):
            results.append((-i, tmp[i]))
        
        return results
        
    def key(self, row):
        return datetime(*row["key"])
    
    def value(self, row):
        return row.value
    
