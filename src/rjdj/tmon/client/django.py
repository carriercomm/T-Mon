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

from rjdj.tmon import client

USER_AGENT_KEY = "HTTP_USER_AGENT"

def track(view_func, url = ""):

    def view(request, *args, **kwargs):
    
        if not url: url = request.path
        user_agent = request.META[USER_AGENT_KEY] if request.META.has_key(USER_AGENT_KEY) else ""
        remote_ip = request.META[REMOTE_ADDR] if request.META.has_key(REMOTE_ADDR) else ""
        client.track(url = url, 
                     user_agent = user_agent,
                     remote_ip = remote_ip,
                     username = request.user.name)
        
        return view_func(request, *args, **kwargs)
        
    return view_func
