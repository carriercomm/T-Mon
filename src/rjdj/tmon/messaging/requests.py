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

from rjdj.tmon.utils import *
from rjdj.tmon.utils import db
import json

class TrackingRequest(object):

    WSID_KEY = 'wsid'
    DATA_KEY = 'data'

    required_fields = (
        'ip',
        'useragent',
    )
    
    optional_fields = (
        'username',
    )
    
    @staticmethod
    def create_from_post_data(post_data):
        req = TrackingRequest()
        data = None
        try:
            wsid = post_data[TrackingRequest.WSID_KEY]
            req.webservice = db.get_webservice(wsid)
            secret = req.webservice.secret
            decrypted_data = decrypt_message(post_data[TrackingRequest.DATA_KEY], secret)
            data = json.loads(decrypted_data)
        except KeyError as ke:
            raise InvalidPostData(ke)
        except ValueError as ve:
            raise DecryptionFailed(ve)
        except InvalidWebService as ws:
            raise
            
        try:
            for key in TrackingRequest.required_fields:
                val = data[key]
                setattr(req, key, val)
                
        except KeyError as ke:
            raise FieldMissing(ke)

        for key in TrackingRequest.optional_fields:
            val = post_data.get(key)
            if val: setattr(req, key, val)
        
        return req
