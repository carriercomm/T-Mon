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

# Base Class
class TMonServerError(Exception):
    http_status_code = 400

# Parser Errors
class ParsingFailed(TMonServerError):
    http_status_code = 400
        
class FieldMissing(ParsingFailed):
    http_status_code = 400
    
class InvalidPostData(ParsingFailed):
    http_status_code = 400

class InvalidIPAdress(ParsingFailed):
    http_status_code = 400

# Decryption Errors
class DecryptionFailed(TMonServerError):
    http_status_code = 403
    

# Bad Requests
class InvalidRequest(TMonServerError):
    http_status_code = 405
    
class InvalidWebService(TMonServerError):
    http_status_code = 403
    
