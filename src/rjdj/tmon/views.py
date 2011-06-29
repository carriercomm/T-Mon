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

from rjdj.tmon.exceptions import *
from rjdj.tmon.messaging.requests import TrackingRequest
from rjdj.tmon.utils.decorators import return_status

from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         )


def not_found(request):
    return HttpResponseNotFound()

def server_error(request):
    return HttpResponseServerError()

@return_status
def data_collect(request):
    if request.method != "POST":
        raise InvalidRequest("GET is not allowed")
        
    trackingreq = None
    trackingreq = TrackingRequest.create_from_post_data(request.POST)
    
            
def data_view(request):
    pass
    
def login(request):
    pass
    
