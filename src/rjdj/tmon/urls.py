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

import settings
from django.contrib import admin
from django.conf.urls.defaults import *

from rjdj.tmon import views

from rjdj.djangotornado.handlers import (DjangoHandler,
                                         SynchronousDjangoHandler,
                                         )

from os import path

admin.autodiscover()

ROOT_FILES = (
    'favicon.ico',
    'crossdomain.xml',
    'robots.txt',
    )

handler404 = views.not_found
handler500 = views.server_error

urlpatterns = patterns( '',
#                        (r'^$', views.default),
                        (r'^admin/', include(admin.site.urls)),
                        
                        # JavaScript GET interfaces
                        (r'^(\d+)/data/users/country', views.users_per_country),
                        (r'^(\d+)/data/users/device', views.users_per_device),
                        (r'^(\d+)/data/users/os', views.users_per_os),
                        
                        # POST interfaces
                        (r'^data/collect', views.data_collect),

                        # static files
                        (r'^(%s)$' % '|'.join(ROOT_FILES),
                         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        (r'^static/(.*)$',
                         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                        )

# test view with the tornado web framework
tornado_urls = (
#    (r'/context/info', DjangoHandler, dict(django_view = views.get_geoinfo)),
    )
