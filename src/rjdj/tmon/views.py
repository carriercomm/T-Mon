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

from rjdj.tmon.utils.parser import TrackingRequestParser

from rjdj.tmon.utils.decorators import return_json
from rjdj.tmon.utils import location, db

from rjdj.tmon.utils import queries

from datetime import datetime

from django.http import  (
                         HttpResponseNotFound,
                         HttpResponseServerError,
                         )


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
    return db.execute(query, wsid)

@return_json
def users_per_device(request, wsid):
    query = queries.users_per_device
    return db.execute(query, wsid)

@return_json
def users_per_os(request, wsid):
    query = queries.users_per_os
    return db.execute(query, wsid)

def login(request):
    pass

