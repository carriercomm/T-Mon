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

from rjdj.tmon.server.models import WebService

from rjdj.tmon.server.exceptions import *

from rjdj.tmon.server.utils.parser import TrackingRequestParser, ChartResolutionParser
from rjdj.tmon.server.utils.result_adapter import (DefaultDictAdapter,
                                            RequestResultAdapter, 
                                            PieChartAdapter,
                                            MapAdapter,
                                            )
from rjdj.tmon.server.utils.decorators import return_json
from rjdj.tmon.server.utils import db
from rjdj.tmon.server.utils import queries

from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         )
from django.template.response import SimpleTemplateResponse
from django.contrib.auth.decorators import login_required

#
# Error pages
#

def not_found(request):
    """ HTTP Error Code 404. """
    return HttpResponseNotFound()

def server_error(request):
    """ HTTP Error Code 500. """ 
    return HttpResponseServerError()


#
# RESTful web services 
#

@return_json
def data_collect(request):
    """ """
    
    if request.method != "POST": raise InvalidRequest("GET is not allowed")
    
    webservice, data = TrackingRequestParser.create_document(request.POST)
    db.store(data, webservice.id)


@return_json
def users_per_country(request, wsid):
    """ """

    query = queries.users_per_country
    return DefaultDictAdapter(db.execute(query, wsid)).process()

@return_json
def users_per_device(request, wsid):
    """ """

    query = queries.users_per_device
    return PieChartAdapter(db.execute(query, wsid)).process()

@return_json
def request_count(request, wsid, grouping, limit):
    """ """
    
    res = ChartResolutionParser.get(grouping)
    query = queries.request_count
    resp = RequestResultAdapter(
                                db.execute(query, 
                                           wsid, 
                                           group_level = res.group_level, 
                                           limit = limit), 
                                int(limit),
                                res)
    return resp.process()

@return_json
def users_locations(request, wsid, ne_lat, ne_lng, sw_lat, sw_lng):
    """ """
    
    query = queries.users_locations
    result = db.execute(query, wsid, limit = 100)
    
    resp = MapAdapter(result)
    return resp.process()

@return_json
def users_per_os(request, wsid):
    """ """
    query = queries.users_per_os
    return PieChartAdapter(db.execute(query, wsid)).process()


#
# HTML Page(s)
#

@login_required(login_url='/admin/')
def dashboard(request, wsid):
    """ """
    try:
        context = { "webservice" : db.get_webservice(wsid), 
                    "webservices" : [ db.get_webservice(wsid) ] }
    except InvalidWebService:
        return not_found(request)

    return SimpleTemplateResponse("dashboard.html",
                                   context = context)

def overview(request):
    return SimpleTemplateResponse("index.html")
