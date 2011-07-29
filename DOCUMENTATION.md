RjDj T-Mon Realtime Traffic Monitoring Server
=============================================================================

## Features:
* Open Source under the GNU Public License v3
* Realtime monitoring of multiple web services from multiple users
* Platform independency
* Show the 500 latest requests on a map
* Ranking of the most active countries and cities (by request)
* and much more!

## Quick Setup:

1. Start the server as stated in README
2. Connect to `http://localhost:8000/admin` with your browser
3. Log in using the created administrator credentials
4. Create a new WebService with a __unique name__. An ID and a secret will be created automatically on save.
5. With the secret and the webservice's id, use the client package to add some data!

## Description

T-Mon aimes to be a realtime monitoring system for various web services and an addition to other monitoring systems like Google Analytics. It relies on [Apache's CouchDB](http://couchdb.apache.org/ "The Apache CouchDB Project"), [Python 2](http://python.org "Python"), [Django 1.3](http://www.djangoproject.com "The Django Project") and [Tornado](http://www.tornadoweb.org "Tornado Web Server") in order to assert flexibility, security, scalability and performance. 

The process of this monitoring system is simple:
1. Collect data
2. Filter data
3. Show data

All of these steps are taken care of with T-Mon. As explained later in more detail, the data collection process is language and platform independent and encrypted. The filtering process is done with CouchDB's views and showing is again taken care of by T-Mon. 

### Why T-Mon?

T-Mon is Open Source and aimes to fill the gap between JavaScript based website monitoring and pure hardware load monitoring, which leads to a collection process that is language- and platform independent and a simple web-based monitoring site to view the collected data. The server application itself is also lightweight and can easily be used for any kind of web service or website tracking. For security reasons the collected data has to be encrypted using a 256 bit [AES](http://en.wikipedia.org/Advanced_Encryption_Standard "Wikipedia: Advanced Encryption Standard") cipher. 

#### The Tracking Process

Data collection is very easy: The server offers a RESTful interface `/data/collect`, which accepts the (encrypted) monitoring data using HTTP POST (details see below). Per default this data is mainly the user agent, the URL and the IP of the request, but it can easily be enhanced, without the fuss of schemamigrations or similar database activities.

If a Python-based web service should be tracked, there is an additional library that makes tracking easier: [T-Mon Client API](https://github.com/celaus/T-Mon-Client-API "T-Mon Client API's GitHub repository").

### Dependencies

These dependencies are from a Debian-based Linux platform and when using Mac OS X or any other Linux distribution the package names may vary.

* python2.6 <
* python2.6-dev <
* bzip2 
* gcc 
* g++ 
* libxslt1.1 
* libxslt-dev 
* libpcre3-dev 
* autotools-dev 
* libpq5 
* libpq-dev 
* memcached 
* make 
* swig 
* psmisc 
* python-imaging 
* python-crypto

Many of those dependencies come from the fact that during the buildout process, Nginx is being compiled.

## Setup (the scientific approach)

First checkout the repository from my [Repository](https://github.com/celaus/T-Mon "T-Mon's GitHub repository") with 
    
    git clone git://github.com/celaus/T-Mon.git

T-Mon comes with the following folder structure:

    T-Mon/
        base.cfg                          # basic buildout conifguration file
        bootstrap.py                      # bootstrapping file, generates buildout script
        buildout.cfg                      # softlink to buildout.testing.cfg
        buildout.staging.cfg              # buildout config for staging environment
        buildout.testing.cfg              # buildout config for (local) testing environment
        buildout.production.cfg           # buildout config for production environment
        CHANGES.txt                       # the latest changes
        COPYING                           # a copy of the GPLv3 
        cron.cfg                          # buildout config for cronjobs
        DOCUMENTATION.md                  # this file
        mime.types                        # mime types for nginx
        nginx.cfg                         # buildout config for nginx
        nginx.conf                        # configuration file for nginx
        README                            # basic server setup file
        setup.py                          # setup.py for easy_install and distribute 
        src/                              # source code directory
            __init__.py
            rjdj/
                __init__.py  
                tmon/
                    __init__.py
                    server/               # files for the server
                        __init__.py
                        admin.py          
                        exceptions.py
                        models.py
                        urls.py           # url configuration for the server 
                        views.py
                        tests/            # contains (zope) tests for the server
                            ...
                        utils/            # application logic!
                            ... 
                        management/       # management commands for instance executable
                            ...
                    tools/                # additional tools for the server  
                        __init__.py
                        regenerate_views.py
            settings/                     # deployment settings
                __init__.py               # basic settings for django
                testing.py                # testing specific settings
                staging.py                # staging specific settings
                production.py             # production specific settings
            static/                       # everything that is statically served (pictures, JavaScript, ...)
                js/
                    dashboard.js
                    event.js
                    jquery-1.6.2.min.js
                    jquery-ui-1.8.14.custom.min.js
                    jquery.flot.min.js
                    jquery.flot.pie.min.js
                    utils.js
                ui-lightness/
                    ...
                dashboard.css
                loader.gif
                login.css
                map.html
            templates/                     # Django templates 
                dashboard.html
                dialogs.html               # modal dialogs
                index.html
                login.html

### Prerequisites

Before anything can happen, it has to be decided how the server should be deployed, as there are three stages:
* testing: Uses the file `testing.py` in `src/settings/` and should be used for local testing
* staging: When everything is quite clear and T-Mon should be deployed on a live environment (uses `staging.py`)
* production: Everything is sorted out and T-Mon should go live! (uses `production.py`)

Keep in mind that these settings are also Django's settings and they can as well be modified here. The basis for these settings can be found in the init module from `src/settings/`.

The stage specific settings can be configured in `src/settings/`. 

#### Important flag(s):

##### DEBUG

_Should be false on production systems or when expecting heavy load in staging._

__Effects:__ 

* Commits after every insert into couchdb (instead of bulk-inserting - CPU intense)
* Responds with the exception message to every /data/collect request

### Buildout

_Buildout is a Python-based build system for creating, assembling and deploying applications from multiple parts, some of which may be non-Python-based. It lets you create a buildout configuration and reproduce the same software later._
From [www.buildout.org](http://www.buildout.org/ "Buildout")

In order to set up T-Mon run (using Python 2.x)

    python bootstrap.py
    
This will then create a directory called `bin/` where the binaries can be found and the __buildout__ script. Call it with the desired settings to set T-Mon up.

    bin/buildout -vc buildout.xxxx.cfg 
    
The flags v (verbose) and c (config file) are not mandatory, especially when no config file is given, the file `buildout.cfg` will be used (which is actually a link to `buildout.testing.cfg`).

In case any errors occur, please see the dependencies section. Please note that on some systems they can be named differently.

The bootstrap and buildout process will add the following structure:
    
    T-Mon/
        bin/                               # contains the binaries (to run the server, install cronjobs, etc)
        parts/                             # additional resources like the GeoLite database 
        cron/                              # the cron jobs that will be appended to /etc/crontab when install_cronjobs is run
        develop-eggs/                      # temporary folders for the buildout process
        downloads/                         # temporary folders for the buildout process
        ... 

#### Customizing the Builout process

In order to customize the Buildout process, the `buildout.xxxx.cfg` files should be edited. If some parts should not be downloaded and set up, they can be either commented out (using a leading `#`) or removed. Please note that if a file is removed from `extends`, the parts from this file also have to be removed from `parts`. Everything in `parts` will actually be built and installed.

    [buildout]
    extends = cron.cfg
              base.cfg
              nginx.cfg
    parts = instance
            regenerate
            upstream_fair
            nginx
            nginx-ctl
            webservice
            GeoLiteCityDB
            crondir
            install_cronjobs
            regenerate_views

If no extensions are planned to be made or a local nginx/apache is running, it is not recommended to edit the builout configuration files.

## Web Pages

GET "/" HTTP1.1
-----------------------------------------------------------------------------
_Root/Index page._

Returns this page.

GET "/login" HTTP1.1
-----------------------------------------------------------------------------
_Log In page._

Lets a user log in, to monitor his web services.

GET "/logout" HTTP1.1
-----------------------------------------------------------------------------
_Logs the current user out and redirects to /login._

Lets a user log in, to monitor his web services.

GET "/view/dashboard/$wsid" HTTP1.1
-----------------------------------------------------------------------------
_Dashboard for server monitoring._

### Request
    wsid           : long [optional]

Shows the dashboard for the specified web service or a page to choose one web service from. If the $wsid is missing, the last web service of the user will be shown.

## RESTful Interfaces

### Request
POST data: [data=...&wsid=...]

    data      :  Base64 encoded and AES encrypted JSON string using the secret
    wsid      :  The id of the web service to be tracked

### Response
Mime-Type: application/json (gzipped)

#### Success
    {
	    "status_code": 200
    }

#### Error
    {
		"status_code": 400/405
    }

If an error occurs, the corresponding HTTP status code is also set.

### Authentication

Every web service requires to be authenticated with a valid user account (can be created in the Django Admin interface), except for the data collection web service, which relies on (256 bit) AES encryption with a generated shared secret.


POST "/data/collect" HTTP1.1
-----------------------------------------------------------------------------
_Collecting Data for T-Mon._

### Request
    url            : string
    ip             : string
    useragent      : string
    username       : string [optional] 

### Response
    status_code    : long
    
#### Example

POST /data/collect: data=ANENCRYPTEDBASE64STRING&wsid=1

    data: 
    {
        "ip": "72.32.231.8",
        "useragent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405", 
        "url": "/" 
    }

GET "/$wsid/data/users/country" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped by country for this web service._

### Request
    wsid           : long

### Response
    status_code    : long
    
GET "/$wsid/data/users/city" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped by city for this web service._

### Request
    wsid           : long

### Response
    status_code    : long

GET "/$wsid/data/users/locations/$ne_lat/$ne_lng/$sw_lat/$sw_lng" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped by latitude and longitude this web service._

### Request
    wsid           : long
    ne_lat         : float 
    ne_lng         : float
    sw_lat         : float
    sw_lng         : float

### Response
    status_code    : long
    
GET "/$wsid/data/users/os" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped by operating system for this web service._

### Request
    wsid           : long

### Response
    status_code    : long
    
GET "/$wsid/data/users/device" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped by device for this web service._

### Request
    wsid           : long

### Response
    status_code    : long
    
GET "/$wsid/data/requests/$resolution/$limit" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the number of requests in the specified resolution._

### Request
    wsid           : long
    resolution     : second|minute|hour|day
    limit          : long

### Response
    status_code    : long
