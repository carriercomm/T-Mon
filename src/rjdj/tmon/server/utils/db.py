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

from couchdb.design import ViewDefinition
from rjdj.tmon.server.utils.connection import connection

def store(data, wsid):
    if data:
        data.store(connection.switch_db(wsid))

def execute(query, wsid, cls = None, **options):
    if isinstance(query, ViewDefinition):
        return query(connection.switch_db(wsid), **options)

def sync(query, wsid):
    if isinstance(query, ViewDefinition):
        query.sync(connection.switch_db(wsid))
