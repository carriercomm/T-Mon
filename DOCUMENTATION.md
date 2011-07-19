RjDj T-Mon Realtime Traffic Monitoring Server
=============================================================================

## Features:
* Realtime monitoring of multiple web services from multiple users
* Platform independency
* Show the 100 latest requests on a map
* Ranking of the 10 most active countries and cities
* and much more!

## Basic Setup:

1. Start the server as stated in README
2. Connect to __http://localhost:8000/admin__ with your browser
3. Log in using the created administrator credentials
4. Create a new WebService with a __unique name__. An ID and a secret will be created on save.
5. With the secret and the webservice's id, use the client package to add some data!

## Web Services and Web Pages by T-Mon

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

## Web Pages

GET "/" HTTP1.1
-----------------------------------------------------------------------------
_Root/Index page._

Returns this page.

GET "/login" HTTP1.1
-----------------------------------------------------------------------------
_Log In page._

Lets a user log in, to monitor his web services.

GET "/view/dashboard/$wsid" HTTP1.1
-----------------------------------------------------------------------------
_Dashboard for server monitoring._

### Request
    wsid           : long [optional]

Shows the dashboard for the specified web service or a page to choose one web service from. If the $wsid is missing, the first web service of the user will be shown.


## RESTful Interfaces

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
