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

from rjdj.tmon.server.models import WebService, resolve

from rjdj.tmon.server.exceptions import *

from rjdj.tmon.server.utils.widgetdataadapter import PieChart, MapPins
from rjdj.tmon.server.utils.decorators import return_json, print_request_time
from rjdj.tmon.server.utils import decrypt_message
from rjdj.tmon.server.models import TrackingData
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
            webservice = resolve(post_data[WSID_KEY])

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
    
    results = TrackingData.views.requests_by_country(resolve(wsid).name)

    return results


@return_json
def users_per_city(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_city(resolve(wsid).name)

    return results

@return_json
def users_per_device(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_device(resolve(wsid).name)
    
    return PieChart(results).create()

@return_json
def users_per_url(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_url(resolve(wsid).name)
    
    return PieChart(results).create()

@return_json
def users_per_os(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_os(resolve(wsid).name)
    
    return PieChart(results).create()

@return_json
def request_count(request, wsid, grouping, limit):
    """ """
    limit = int(limit)
    tmp = [0] * limit
    
    for p in TrackingData.views.request_count(resolve(wsid).name, grouping, limit):
        for k, v in p.iteritems():
            tmp[k] = v
            
    return tmp

@return_json
def users_locations(request, wsid, ne_lat, ne_lng, sw_lat, sw_lng):
    """ """
    
    results = TrackingData.views.requests_by_os(resolve(wsid).name, grouping, limit)
    return MapPins(results)


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
        context = { "webservice" : resolve(wsid), 
                    "webservices" : db.all_webservices(request.user) }
    except InvalidWebService:
        return not_found(request)

    return SimpleTemplateResponse("dashboard.html",
                                   context = context)

@login_required()
def dashboard_redirect(request):
    """ Redirects to the dashboard of the user's last web service. """
    
    try:
        webservices = db.all_webservices(request.user) 
    except InvalidWebService:
        return not_found(request)

    return redirect('/view/dashboard/%d' % webservices[0].id)

def overview(request):
    """ Shows the documentation text. """
    
    return SimpleTemplateResponse("index.html")
