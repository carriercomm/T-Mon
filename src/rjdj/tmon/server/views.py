##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# T-Mon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# T-Mon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with T-Mon. If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import base64

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         QueryDict,
                         )
from django.shortcuts import redirect
from django.template.response import SimpleTemplateResponse

import logging

from rjdj.tmon.server.exceptions import *

from rjdj.tmon.server.models import WebService, TrackingData, resolve
from rjdj.tmon.server.couchdbviews.couchdbkeys import CouchDBKeys as Keys
from rjdj.tmon.server.utils import validate
from rjdj.tmon.server.utils.bulkinsert_manager import bulkInsertManager
from rjdj.tmon.server.utils.decorators import return_json, print_request_time
from rjdj.tmon.server.utils.processors import process
from rjdj.tmon.server.utils.scheduler import scheduler
from rjdj.tmon.server.utils.widgetdataadapter import PieChart, MapPins

import ujson

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
SIGNATURE_KEY = "signature"

#
# Tornado views
#
def data_collect(post_data, timestamp):
    """ """
    webservice = resolve(post_data[WSID_KEY])
    decrypted_data = base64.b64decode(post_data[DATA_KEY])
    if not validate(decrypted_data, webservice.secret, post_data[SIGNATURE_KEY]):
        return
    try:        
        data = ujson.decode(decrypted_data)
        data.update({ Keys.TIMESTAMP : timestamp })
        parsed_data = process(data)
    except Exception as ex:
        logger.error(u"%s: %s" % (ex, ex))
        return

    bulkInsertManager.insert(parsed_data, webservice)


class CollectionHandler(RequestHandler):
    """ Handles the Data Collection interface """
    
    def post(self, *args, **kwargs):
        """ """
        post_data = QueryDict(self.request.body)
        scheduler.process(data_collect, post_data, TrackingData.now())
#        data_collect(post_data)
        
        self.finish()   
        
#
# Django views
# 
@return_json
def users_per_country(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_country(resolve(wsid).name)

    return results[:5]


@return_json
def users_per_city(request, wsid):
    """ """
    
    results = TrackingData.views.requests_by_city(resolve(wsid).name)

    return results[:5]

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
            
    return [(-i, tmp[i]) for i in xrange(len(tmp))]

@return_json
def users_locations(request, wsid, ne_lat, ne_lng, sw_lat, sw_lng):
    """ """
    
    results = TrackingData.views.requests_locations(resolve(wsid).name)
    return MapPins(results).create()


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
                    "webservices" : request.user.webservice_set.all() }
    except InvalidWebService:
        return not_found(request)

    return SimpleTemplateResponse("dashboard.html",
                                   context = context)

@login_required()
def dashboard_redirect(request):
    """ Redirects to the dashboard of the user's last web service. """
    
    try:
        webservices = request.user.webservice_set.all()
    except InvalidWebService:
        return not_found(request)

    return redirect('/view/dashboard/%d' % webservices[0].id)

def overview(request):
    """ Shows the documentation text. """
    
    return SimpleTemplateResponse("index.html")
