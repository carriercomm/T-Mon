RjDj T-Mon Realtime Traffic Monitoring Server
=============================================================================

## Basic Setup:

1. Start the server as stated in README
2. Connect to __http://localhost:8000/admin__ with your browser
3. Log In using the created administrator credentials
4. Create a new WebService with a __unique name__ and a secret
5. With the secret and the webservice's id, use the client package to add some data!

## General

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

Every web service requires to be authenticated with a valid user account (can be created in the Django Admin interface), except for the data collection web service, which relies on AES encryption with a shared secret.

## Web Pages

GET "/" HTTP1.1
-----------------------------------------------------------------------------
_Root/Index page._

Returns this page.

GET "/view/dashboard/$wsid" HTTP1.1
-----------------------------------------------------------------------------
_Root/Index page._

### Request
    wsid           : long [optional]

Shows the dashboard for the specified web service or a page to choose one web service from.


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
_Retrieves the users grouped per country for this web service._

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
_Retrieves the users grouped per operating system for this web service._

### Request
    wsid           : long

### Response
    status_code    : long
    
GET "/$wsid/data/users/device" HTTP1.1
-----------------------------------------------------------------------------
_Retrieves the users grouped per device for this web service._

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
