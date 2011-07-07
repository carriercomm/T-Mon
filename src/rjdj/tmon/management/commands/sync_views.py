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

from django.core.management.base import BaseCommand
from rjdj.tmon.utils.queries import all_queries
from rjdj.tmon.models import WebService
from rjdj.tmon.utils import db

class Command(BaseCommand):

    help = """ Prepares the CouchDB for inserts! """
    
    def handle(self, *args, **kwargs):
        errors = 0
        for ws in WebService.objects.all():
            for q in all_queries:
                try:
                    db.sync(q, ws.id)
                except Exception as ex:
                    errors += 1
                    print "Error during sync: ", ex, "... ignoring"
                    
        print "done.", errors if errors else "no", "errors occured!"
