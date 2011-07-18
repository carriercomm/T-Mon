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

from django.db import models
from django.contrib.auth.models import User
from rjdj.tmon.server.utils.connection import connection
from django.db import transaction


from couchdb.mapping import ( Document, 
                              TextField, 
                              IntegerField, 
                              DateTimeField,
                              FloatField, 
                              ViewField, )

class WebService(models.Model):
    """ Represents any web service to be tracked """
    
    owner = models.ForeignKey(User)
    secret = models.CharField("Secret for web service authentication", max_length = 128, unique = True)
    name = models.CharField("Name of the Service", max_length = 40, unique = True)
    
    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        super(WebService, self).save(*args, **kwargs)
        connection.setup_db(self.name)
    
class TrackingData(Document):
    """ A class for saving trackable data """
    
    user_agent = TextField()
    url = TextField()
    timestamp = DateTimeField()
    country = TextField()
    latitude = FloatField()
    longitude = FloatField()
    username = TextField()
    city = TextField()
    
    
