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

import pygeoip
from django.conf import settings
from rjdj.tmon.server.exceptions import *

def resolve(ip):
    """ Resolves an IP (v4) address to a dict containing 3-letter country code and lat/lng.  """
    
    geoip = pygeoip.GeoIP(settings.GEOIP_DB_LOCATION)
    res = {}
    addr_rec = None
    try:    
        addr_rec = geoip.record_by_addr(ip)
    except pygeoip.GeoIPError: 
        pass
    
    if addr_rec:
        res["country"] = addr_rec["country_code3"]
        res["city"] = addr_rec.has_key("city") and addr_rec["city"].decode('latin-1') or None
        res["latitude"] = addr_rec["latitude"]
        res["longitude"] = addr_rec["longitude"]

    return res
