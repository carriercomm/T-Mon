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

def total_seconds(td):
    """ Returns the total seconds of a timedelta object. """
    
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6;

class ChartResolution(object):
    """ """
    
    def __call__(self, *args):
        """ """
        return self.diff(*args)
    
    def diff(self, dtA, dtB):
        """ """
        
        raise NotImplementedError()

class SecondsResolution(ChartResolution):
    """ """
    
    group_level = 6
    friendly_name = "second"
    
    def diff(self, dtA, dtB):
        return int(total_seconds(dtA - dtB)) 

class MinutesResolution(ChartResolution):
    """ """
    
    group_level = 5
    friendly_name = "minute"    
    
    def diff(self, dtA, dtB):
        return int(total_seconds(dtA - dtB) / 60) 

class HoursResolution(ChartResolution):
    """ """
    
    group_level = 4
    friendly_name = "hour"
        
    def diff(self, dtA, dtB):
        return int(total_seconds(dtA - dtB) / 3600) # 60 * 60
        
class DaysResolution(ChartResolution):
    """ """
    
    group_level = 3
    friendly_name = "day"
        
    def diff(self, dtA, dtB):
        return int((dtA - dtB).days) 

# A collection of all the possible Resolutions mapped to their friendly names

CHART_RESOLUTIONS = {
    SecondsResolution.friendly_name: SecondsResolution,
    MinutesResolution.friendly_name: MinutesResolution,
    HoursResolution.friendly_name: HoursResolution,
    DaysResolution.friendly_name: DaysResolution,
}
