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

import operator

class WidgetDataAdapter(object):
    """ Base class for any DataAdapter for JavaScript widgets """
    
    def __init__(self, data_dicts):
    
        if not isinstance(data_dicts, list):
            raise ValueError("Data needs to be in a list")
            
        self.data = data_dicts
    
    def create(self, *args, **kwargs):
        """ Effectively executes data adaption. """
        
        raise NotImplementedError("Please use subclass")
    
class PieChart(WidgetDataAdapter):    
    """ A pie chart (list of dicts), with keys as "label" and values as "data" entry. """
    
    def create(self):
    
        results = []
        append = results.append
                
        for d in self.data:
            for k, v in d.iteritems():
                append({ "label": k, "data": v })
                
        return results


class MapPins(WidgetDataAdapter):
    """ Provides a list of dicts containing the keys "lat" "lng" and "count". """
    
    def create(self):
        
        results = []
        append = results.append
        
        for d in self.data:
            for k, v in d.iteritems():
                append({"lat": k[0], "lng": k[1], "count": v })
                
        return results


class SortedList(WidgetDataAdapter):
    """ Provides a list of dicts sorted by their values. """
    
    def create(self, reverse = True):
        
        combined = {}
        for d in self.data:
            for k, v in d.iteritems():
                combined[k] = v
         
        return [{k: v} for k, v in sorted(combined.iteritems(), key = operator.itemgetter(1), reverse = reverse)]
