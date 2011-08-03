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

import logging
import json

from rjdj.tmon.server.models import WebService

from rjdj.tmon.server.exceptions import *

from rjdj.tmon.server.utils.parser import ChartResolutionParser
from rjdj.tmon.server.utils.result_adapter import (DefaultDictAdapter,
                                                   GeoRequestAdapter,
                                                   RequestResultAdapter, 
                                                   PieChartAdapter,
                                                   MapAdapter,
                                                    )
from rjdj.tmon.server.utils.decorators import return_json, print_request_time
from rjdj.tmon.server.utils import db
from rjdj.tmon.server.utils import decrypt_message
from rjdj.tmon.server.utils import queries
from rjdj.tmon.server.utils.bulkinsert_manager import bulkInsertManager
from rjdj.tmon.server.utils.processors import process

from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         )
from django.template.response import SimpleTemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import QueryDict
from django.conf import settings

from datetime import datetime, timedelta

from threading import Thread
from tornado.web import RequestHandler

logger = logging.getLogger("debug")

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

WSID_KEY = "wsid"
DATA_KEY = "data"
#
# Tornado views
#
def data_collect(webservice, post_data):
    """ """
    
    decrypted_data = decrypt_message(post_data[DATA_KEY], webservice.secret)
    data = json.loads(decrypted_data)
    
    parsed_data = process(data)
    bulkInsertManager.insert(parsed_data, webservice)

class CollectionHandler(RequestHandler):
    """ """
    @print_request_time
    def post(self, *args, **kwargs):
        """ """
        
        try:
            post_data = QueryDict(self.request.body)
            webservice = db.get_webservice(post_data[WSID_KEY])

            t = Thread(target = data_collect, args = (webservice, post_data, ))
            t.start()
            if settings.DEBUG: t.join()
        except Exception as ex:
            logger.error("%s: %s" % (type(ex), ex))
        self.finish()   
        
#
# Django views
# 
@return_json
def users_per_country(request, wsid):
    """ """

    query = queries.users_per_location
    limit = datetime.now() - timedelta(minutes = 10)
    return GeoRequestAdapter(db.execute(query, wsid, group_level = 6)[[limit.year, limit.month, limit.day, limit.hour, limit.minute]:]).process()[:5]


@return_json
def users_per_city(request, wsid):
    """ """
 
    query = queries.users_per_location
    
    limit = datetime.now() - timedelta(minutes = 10)
    return GeoRequestAdapter(db.execute(query, wsid)[[limit.year, limit.month, limit.day, limit.hour, limit.minute]:]).process()[:5]


@return_json
def users_per_device(request, wsid):
    """ """

    query = queries.users_per_device
    return PieChartAdapter(db.execute(query, wsid)).process()

@return_json
def users_per_url(request, wsid):
    """ """

    query = queries.users_per_url
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
    
    limit = datetime.now() - timedelta(minutes = 10)
    result = db.execute(query, wsid, limit = 500)[:[limit.year, limit.month, limit.day, limit.hour, limit.minute]]

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

@login_required()
def logout_user(request):
    """ Logs the user out and redirects to the login page. """
    
    logout(request)
    
    return redirect('/login')

@login_required()
def dashboard(request, wsid):
    """ Shows the corresponding dashboard of this web service monitoring. """
    
    try:
        context = { "webservice" : db.get_webservice(wsid), 
                    "webservices" : db.get_webservices(request.user) }
    except InvalidWebService:
        return not_found(request)

    return SimpleTemplateResponse("dashboard.html",
                                   context = context)

@login_required()
def dashboard_redirect(request):
    """ Redirects to the dashboard of the user's last web service. """
    
    try:
        webservices = db.get_webservices(request.user) 
    except InvalidWebService:
        return not_found(request)

    return redirect('/view/dashboard/%d' % webservices[0].id)

def overview(request):
    """ Shows the documentation text. """
    
    return SimpleTemplateResponse("index.html")
