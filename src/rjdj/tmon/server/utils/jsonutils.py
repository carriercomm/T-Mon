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

from json import dumps, loads
from json.encoder import JSONEncoder
from time import mktime

class ExtendedJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, "timetuple"):
            return int(mktime(o.timetuple()))
        elif hasattr(o, "__dict__"):
            return {'__class__':o.__class__.__name__,
                    'o': o.__dict__,
                    }
        else:
            return str(o)

def json_encode(obj):
    return dumps(obj, cls=ExtendedJSONEncoder)

def json_decode(json):
    return loads(json)
