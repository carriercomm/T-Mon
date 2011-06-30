##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of TMon.
#
# TMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-tornado. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import pygeoip
from django.conf import settings
from rjdj.tmon.exceptions import *

def resolve(ip):
    """ Resolves an IP (v4) address to a dict containing 3-letter country code and lat/lng.  """
    geoip = pygeoip.GeoIP(settings.GEOIP_DB_LOCATION)
    
    addr_rec = geoip.record_by_addr(ip)
    res = {}
    if addr_rec:
        res["country"] = addr_rec["country_code3"]
        res["latitude"] = addr_rec["latitude"]
        res["longitude"] = addr_rec["longitude"]
    else:
        raise InvalidIPAdress(ip)
    
    return res
