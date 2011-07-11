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


from rjdj.tmon.client import config
from rjdj.tmon import client
from multiprocessing import Process
import time
import random

URLS = (
    "/",
    "/login",
    "/register",
    "/get/data",
    )

IPS = (
    "192.168.0.1",
    "231.71.58.1",
    "91.48.8.7",
    "8.8.8.8",
    "9.9.9.9",
    "123.45.8.91",
    )
    
UAS = (
    "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405", 
    "Mozilla/5.0 (Linux; U; Android 2.2.1; fr-ch; A43 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
    "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
    )
    
USER = (
    "claus",
    "martin",
    "christian", 
    "dom", 
    "joe", 
    "", "", # double the chances 
    "rob", 
    "michael",
    )
    
def send_request():
    url = URLS[random.randint(0, len(URLS) - 1)]
    ip = IPS[random.randint(0, len(IPS) - 1)]
    ua = UAS[random.randint(0, len(UAS) - 1)]
    user = USER[random.randint(0, len(USER) - 1)]
    client.track(url, ua, ip, user)

def run(duration, num_of_req):
    delay = num_of_req / 60 # minutes
    
    threads = []
    for minute in xrange(duration):
        for num in xrange(num_of_req):
            t = Process(target = send_request)
            t.start()
            threads.append(t)
           # time.sleep(delay)
