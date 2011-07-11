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

class BasicAdapter(object):

    def __init__(self, query_results, max_results = 0, converter = None):
        self.raw_results = query_results
        self.max_results = max_results
        self.converter = converter
        
    def process(self):
        return [{ self.key(res) : self.value(res) } for res in self.raw_results]
        
    def key(self, row): raise NotImplementedError()
    def value(self, row): raise NotImplementedError()
        
class DefaultDictAdapter(BasicAdapter):

    def key(self, row):
        return row["key"]
    
    def value(self, row):
        return row["value"]
    
class PieChartAdapter(BasicAdapter):    

    def process(self):
        return [{ "label": self.key(res), "data": self.value(res) } for res in self.raw_results]

    def key(self, row):
        return row["key"]
    
    def value(self, row):
        return row["value"]


class MapAdapter(BasicAdapter):

    def process(self):
        return [ self.key(res) for res in self.raw_results]
        
    def key(self, row): 
        return {"lat": row["key"][0], "lng" : row["key"][1]}
        
    def value(self, row): raise NotImplementedError()
    
class RequestResultAdapter(BasicAdapter):

    def process(self):
        if not self.converter: raise ValueError("a converter is required for this adapter")
        tmp = [0] * self.max_results
        results = []
        now = datetime.now()
        
        for row in self.raw_results:
            then = self.key(row)
            diff = self.converter.diff(now, then)
            
            if diff < self.max_results: 
                tmp[diff] = self.value(row)
        
        for i in xrange(self.max_results):
            results.append((-i, tmp[i]))
        
        return results
        
    def key(self, row):
        return datetime(*row["key"])
    
    def value(self, row):
        return row.value
    
