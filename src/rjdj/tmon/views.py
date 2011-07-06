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

from rjdj.tmon.exceptions import *

from rjdj.tmon.utils.parser import TrackingRequestParser

from rjdj.tmon.utils.result_adapter import (DefaultDictAdapter,
                                            RequestResultAdapter, 
                                            PieChartAdapter,
                                            )

from rjdj.tmon.utils.decorators import return_json
from rjdj.tmon.utils import location, db

from rjdj.tmon.utils import queries

from datetime import datetime

from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         )
                         
from django.template.response import SimpleTemplateResponse

def not_found(request):
    return HttpResponseNotFound()

def server_error(request):
    return HttpResponseServerError()

@return_json
def data_collect(request):

    if request.method != "POST":
        raise InvalidRequest("GET is not allowed")

    webservice, data = TrackingRequestParser.create_document(request.POST)
    db.store(data, webservice.id)


@return_json
def users_per_country(request, wsid):
    query = queries.users_per_country
    return DefaultDictAdapter(db.execute(query, wsid)).process()

@return_json
def users_per_device(request, wsid):
    query = queries.users_per_device
    return PieChartAdapter(db.execute(query, wsid)).process()

matching_dict = {
    "second": 6,
    "minute": 5,
    "hour": 4,
    "day": 3,
}

@return_json
def request_count(request, wsid, grouping, limit):
    query = queries.request_count
    group_level = matching_dict[grouping]
    
    resp = RequestResultAdapter(db.execute(query, wsid, group_level = group_level, descending = True, limit = limit), int(limit))
    return resp.process()

@return_json
def users_per_os(request, wsid):
    query = queries.users_per_os
    return PieChartAdapter(db.execute(query, wsid)).process()

def login(request):
    pass
    
def dashboard(request, wsid):
    from rjdj.tmon.models import WebService
    try:
        ctx = { "webservice" : WebService.objects.get(id = wsid) }
    except WebService.DoesNotExist:
        raise InvalidWebService()
        
    return SimpleTemplateResponse("dashboard.html", 
                                       context = ctx)

