##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# This file is part of T-Mon.
#
# TMon is free software: you can redistribute it and/or modify
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

import calendar
from Crypto.Cipher import AES
from datetime import datetime
import hashlib
import hmac

JS_TIMESTAMP_MULTIPLIER = 1000

def utc_timestamp_milliseconds(offset_seconds = 0):
    """ Creates a UTC UNIX timestamp in milliseconds. Offset can be positive or negative. """

    return (calendar.timegm(datetime.now().utctimetuple()) + offset_seconds) * JS_TIMESTAMP_MULTIPLIER

def decrypt_message(msg, secret):
    """ Decrypts a Base64 encoded message with the given secret (AES) """
    
    cipher = AES.new(secret, AES.MODE_CFB)
    return cipher.decrypt(msg)
    
def validate(msg, secret, signature):
    """ Validates a message by comparing hmac-based hash values. """

    actual_sig = hmac.new(str(secret), msg, hashlib.sha1).hexdigest()
    return signature == actual_sig
    
