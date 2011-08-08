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

class WidgetDataAdapter(object):
    """ """
    
    def __init__(self, data_dicts):
        self.data = data_dicts
    
    
class PieChart(WidgetDataAdapter):    
    """ """
    
    def create(self):
        """ """
        
        results = []
        for d in self.data:
            for k, v in d.iteritems():
                results.append({ "label": k, "data": v })
                
        return results


class MapPins(WidgetDataAdapter):
    """ """
    
    def create(self):
        """ """
        
        results = []
        for d in self.data:
            for k, v in d.iteritems():
                results.append({"lat": k[0], "lng": k[1], "count": v })
                
        return results


class SortedList(WidgetDataAdapter):
    """ """
    
    def create(self, reverse = True):
        """ """
        
        combined = {}
        
        for d in self.data:
            for k, v in d.iteritems():
                combined[k] = v
                
        return [{k: v} for k, v in sorted(combined.iteritems(), key = operator.itemgetter(1), reverse = reverse)]
