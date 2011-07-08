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

from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *

from rjdj.tmon.server import views

admin.autodiscover()

ROOT_FILES = (
    'favicon.ico',
    'crossdomain.xml',
    'robots.txt',
    )

handler404 = views.not_found
handler500 = views.server_error

urlpatterns = patterns('',
#    (r'^$', views.default),
    (r'^admin/', include(admin.site.urls)),

    # JavaScript GET interfaces
    (r'^(?P<wsid>[\d]+)/data/users/country', views.users_per_country),
    (r'^(?P<wsid>[\d]+)/data/users/device', views.users_per_device),
    (r'^(?P<wsid>[\d]+)/data/users/os', views.users_per_os),
    (r'^(?P<wsid>[\d]+)/data/users/locations/(?P<ne_lat>[\d.-]+)/(?P<ne_lng>[\d.-]+)/(?P<sw_lat>[\d.-]+)/(?P<sw_lng>[\d.-]+)', views.users_locations),
    (r'^(?P<wsid>[\d]+)/data/requests/(?P<grouping>(second|minute|hour|day))/(?P<limit>[\d]+)', views.request_count),
    
    # HTML Pages
    (r'^view/dashboard/(?P<wsid>[\d]+)', views.dashboard),
    (r'^view/login', views.loginpage),

    # POST interfaces
    (r'^data/collect', views.data_collect),

   # static files
    (r'^(%s)$' % '|'.join(ROOT_FILES),
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
