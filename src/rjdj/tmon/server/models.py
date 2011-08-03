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
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from rjdj.tmon.server.utils.connection import connection
from django.db import transaction

# http://wiki.apache.org/couchdb/HTTP_database_API#Naming_and_Addressing
name_validator = RegexValidator(regex = r'^[a-z][a-z0-9\_\$()\+\-]*$', 
                                message = 'Name must be a valid CouchDB Database name (without a "/")')


class WebService(models.Model):
    """ Represents any web service to be tracked """
    
    owner = models.ForeignKey(User)
    secret = models.CharField("Secret for web service authentication", max_length = 128, unique = True)
    name = models.CharField("Name of the Service", max_length = 40, unique = True, validators = [name_validator])
    
    @transaction.commit_on_success
    def save(self, *args, **kwargs):
        super(WebService, self).save(*args, **kwargs)
        connection.setup_db(self.name)
    
    @transaction.commit_on_success
    def delete(*args, **kwargs):
        name = self.name
        super(WebService, self).save(*args, **kwargs)
        connection.remove_db(name)    
    
class TrackingDataKeys(object):
    """ A class for saving trackable data """
    
    USER_AGENT = "useragent"
    URL = "url"
    LATITUDE = "lat"
    LONGITUDE = "lng"
    TIMESTAMP = "timestamp"
    COUNTRY = "country"
    USERNAME = "username"
    IP = "ip"
    CITY = "city"
    
