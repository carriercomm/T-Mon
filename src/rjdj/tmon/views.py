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
from rjdj.tmon.utils import location, db

from rjdj.tmon.models import TrackingData

from datetime import datetime

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
        
    trackingreq = TrackingRequest.create_from_post_data(request.POST)
    
    user_location = location.resolve(trackingreq.ip)
    
    data = TrackingData(user_agent = trackingreq.useragent, 
                        timestamp = datetime.now(),
                        country = user_location["country"],
                        latitude = user_location["latitude"],
                        longitude = user_location["longitude"],
                        wsid = trackingreq.webservice.id)
    
    db.store(data)
 
@return_status          
def data_view(request):
    from rjdj.tmon.utils.queries import all_queries
    upc = all_queries["users_per_country"]
    import pdb; pdb.set_trace()

    
def login(request):
    pass
    
