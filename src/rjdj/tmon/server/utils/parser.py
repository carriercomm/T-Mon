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

from rjdj.tmon.server.utils import *
from rjdj.tmon.server.utils.resolution import class_dict
from rjdj.tmon.server.utils import location
from rjdj.tmon.server.models import TrackingData
from rjdj.tmon.server.exceptions import *
from datetime import datetime
import json
from db import get_webservice

class TrackingRequestParser(object):

    WSID_KEY = 'wsid'
    DATA_KEY = 'data'

    IP_KEY = 'ip'
    UA_KEY = 'useragent'
    USER_KEY = 'username'
    URL_KEY = 'url'

    @staticmethod
    def create_document(post_data):
        data = None
        webservice = None
        try:
            wsid = post_data[TrackingRequestParser.WSID_KEY]
            webservice = get_webservice(wsid)
            secret = webservice.secret
            decrypted_data = decrypt_message(post_data[TrackingRequestParser.DATA_KEY], secret)
            data = json.loads(decrypted_data)
        except KeyError as ke:
            raise InvalidPostData(ke)
        except ValueError as ve:
            raise DecryptionFailed(ve)
        except WebService.DoesNotExist as ws:
            raise InvalidWebService(ws)

        try:
            ip = data[TrackingRequestParser.IP_KEY]
            useragent = data[TrackingRequestParser.UA_KEY]
            url = data[TrackingRequestParser.URL_KEY]
        except KeyError as ke:
            raise FieldMissing(ke)

        username = data.get(TrackingRequestParser.USER_KEY)
        user_location = location.resolve(ip)
        
        country = None
        latitude = None
        longitude = None
        
        if user_location:
            country = user_location["country"]
            latitude = user_location["latitude"]
            longitude = user_location["longitude"]
           
        tracking_data = TrackingData(user_agent = useragent,
                                     timestamp = datetime.now(),
                                     country = country,
                                     latitude = latitude,
                                     longitude = longitude,
                                     username = username,
                                     url = url)
        
        return webservice, tracking_data


class ChartResolutionParser(object):

    @staticmethod
    def get(name):
        return class_dict[name]()
