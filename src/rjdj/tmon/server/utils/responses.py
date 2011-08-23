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

from django.http import HttpResponse
import ujson as json

class GenericJSONResponse(object):
    """ A very basic JSON response containing nothing but a status code. """

    MIME = 'application/json'
    STATUS_CODE_KEY = "status"

    def __init__(self, status_code, data):
        self.status_code = status_code
        self.contents = {}
        self.data = data
            
    def update_contents(self):
        self.contents.update({ self.STATUS_CODE_KEY : self.status_code })
        self.contents.update(self.data)

    def create(self):
        self.update_contents()
        res = json.encode(self.contents)        
        return HttpResponse(res,
                            status = self.status_code,
                            mimetype = self.MIME,
                            content_type = '%s; charset=utf-8' % self.MIME)
