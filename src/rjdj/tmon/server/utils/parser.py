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

import json
from rjdj.tmon.server.utils import decrypt_message, location
from rjdj.tmon.server.utils.resolution import CHART_RESOLUTIONS
from rjdj.tmon.server.models import TrackingData
from rjdj.tmon.server.exceptions import *
from datetime import datetime
from db import get_webservice

class TrackingRequestParser(object):
    """ 
        Parses a request containing trackable data from a client to a CouchDB document.
        
        Example:
        >>> post_data = { 
        ...     "data": "ABCDEFGHIJKLMNOPQRSTUVW", # AES encrypted payload, using the corresponding 
        ...                                        # secret of the web service's id
        ...     "wsid": 1 # the web service's id in T-Mon's environment
        ... }
        >>> TrackingRequestParser.create_document(post_data)
        (<WebService object at ...>, <TrackingData object at ...>)
    """

    WSID_KEY = 'wsid'
    DATA_KEY = 'data'

    IP_KEY = 'ip'
    UA_KEY = 'useragent'
    USER_KEY = 'username'
    URL_KEY = 'url'

    @staticmethod
    def create_document(post_data):
        """ 
            Creates a CouchDB-document from the given POST data and returns the 
            corresponding WebService object. 
        """
        if not isinstance(post_data, dict): 
            raise InvalidPostData(type(post_data))
            
        data = None
        webservice = None
        try:
            wsid = post_data[TrackingRequestParser.WSID_KEY]
            webservice = get_webservice(wsid)
            secret = webservice.secret
            decrypted_data = decrypt_message(post_data[TrackingRequestParser.DATA_KEY], secret)
            data = json.loads(decrypted_data)
            
        except KeyError as ke: raise InvalidPostData(ke)
        except ValueError as ve: raise DecryptionFailed(ve)

        try:
            ip = data[TrackingRequestParser.IP_KEY]
            useragent = data[TrackingRequestParser.UA_KEY]
            url = data[TrackingRequestParser.URL_KEY]
        except KeyError as ke:
            raise FieldMissing(ke)

        username = data.get(TrackingRequestParser.USER_KEY)
        user_location = location.resolve(ip)
        
        country = None
        city = None
        latitude = None
        longitude = None
        
        
        if user_location:
            # some (127.0.0.0, 10.0.0.0, 192.168.0.0 or other) IP addresses could result in None
            country = user_location["country"]
            city = user_location["city"]
            latitude = user_location["latitude"]
            longitude = user_location["longitude"]
           
        tracking_data = TrackingData(user_agent = useragent,
                                     timestamp = datetime.now(),
                                     country = country,
                                     city = city,
                                     latitude = latitude,
                                     longitude = longitude,
                                     username = username,
                                     url = url)
        
        return webservice, tracking_data


class ChartResolutionParser(object):
    """ """

    @staticmethod
    def get(name):
        """ """
        
        if not (isinstance(name, unicode) or isinstance(name, str)): 
            raise InvalidRequest(type(name))
        
        try:
            return CHART_RESOLUTIONS[name]()
        except KeyError as ke:
            raise InvalidRequest(ke)
