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

import time
import hashlib

from django.contrib import admin
from rjdj.tmon.server.models import *


class WebServiceAdmin(admin.ModelAdmin):
    
    readonly_fields = ('id', 'secret')
    fieldsets = (
        (None, {
            'fields': (('id','owner'),'name', 'secret')
        }),
    )
    
    list_display = ('id', 'name', 'owner')
    list_display_links = ('id', 'name', 'owner')
    search_fields = ('name', )
    list_filter = ('owner__username', )
    
    def save_model(self, request, obj, form, change):
        """ Generates the secret and saves the model. """
        
        if not change:
            obj.secret = hashlib.md5(obj.name + str(time.time())).hexdigest()
        obj.save()    

admin.site.register(WebService, WebServiceAdmin)


