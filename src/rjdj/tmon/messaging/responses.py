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

from django.http import HttpResponse
from rjdj.tmon.utils.json import ExtendedJSONEncoder
import json

class BasicJSONResponse(object):
    """ A very basic JSON response containing nothing but a status code. """

    MIME = 'application/json'
    STATUS_CODE_KEY = "status"
    MESSAGE_KEY = "message"

    def __init__(self, status_code, message = None):
        self.status_code = status_code
        self.contents = {}
        self.message = message
    
    def update_contents(self):
        if self.message:
            self.contents.update({ 
                                   self.STATUS_CODE_KEY : self.status_code,
                                   self.MESSAGE_KEY : self.message
                                 })
        else:
            self.contents.update({ self.STATUS_CODE_KEY : self.status_code })

    def create(self):
        self.update_contents()
        res = json.dumps(self.contents, 
                         cls = ExtendedJSONEncoder,  
                         indent = 4)        
        
        return HttpResponse(res,
                             status = self.status_code,
                             mimetype = self.MIME,
                             content_type = '%s; charset=utf-8' % self.MIME)
