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

from rjdj.tmon.server.utils.responses import GenericJSONResponse
from rjdj.tmon.server.exceptions import *
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger("debug")

def return_json(view):
    """ A decorator, so the view returns proper messages. """
    
    def restful_view(request, *args, **kwargs):
        """ """
        status = 200
        msg = ""
        data = {}
        try:
            data = view(request, *args, **kwargs) or {}
            if data: data = { "results" : data }
            
        except TMonServerError as ex: # could as well be more diverse
            status = ex.http_status_code 
            if settings.DEBUG: msg = str(ex)
            logger.error("status code %d: %s" % (status, ex))
            
        except Exception as ex:
            status = 500
            
            if settings.DEBUG: msg = str(ex)
            logger.error("status code %d: %s" % (status, ex))
            
        if msg and settings.DEBUG: data.update({ "message": msg })
        return GenericJSONResponse(status, data).create()
        
    return restful_view


def print_request_time(func):
    """ Writes the duration of a request to logging.info. """
    
    def funct(*args, **kwargs):
        """ """
        
        start = datetime.now()
        try:
            return func(*args, **kwargs)
        finally:
            logger.info("request took %s" % (datetime.now() - start))

    return funct
