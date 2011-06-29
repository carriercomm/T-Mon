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

from rjdj.tmon.messaging.responses import BasicJSONResponse
from rjdj.tmon.exceptions import *
from django.conf import settings

def return_status(view):
    """ A decorator, so the view returns proper messages. """
    def restful_view(request):
        status = 200
        msg = ""
        
        try:
            view(request)
        except TMonError as ex: # could as well be more diverse
            status = ex.http_status_code 
            if settings.DEBUG: msg = str(ex)
        except Exception as ex:
            status = 500
            if settings.DEBUG: msg = str(ex)
        response = BasicJSONResponse(status)
        if settings.DEBUG: response.message = msg
        
        return response.create()
        
    return restful_view

