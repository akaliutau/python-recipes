About
======
This is a collection of recipes to create different web apps components on the basis of Python 3.9

Topics covered so far:

* RPA (web scraping)
* OAuth2 authorization
* Consuming public web APIs
* Asynchronous messaging in Python
* Microservices in Python
* Serverless apps in Python


Overview
=========

# Preliminary steps

1) First check the version - it should be 3.9.x (3.9.1 in our case)

```
python --version

Python 3.9.1
```

2) Create a virtual environment

```
python -m venv env
```
As a result a folder env with python libs will be created

3) Activate virtual env:

```
.\env\Scripts\activate
```
The promt will be changed to (env)

4) Install necessary dependencies into virtual environment:

```
pip install -r requirements.txt
```
As a result all extra dependencies will be added


# RPA (web scraping): Weather app

This is a simple web-scraping console application


1) One can perform testing in two ways - using standard browser with Chrome driver or the headless one. As for the latter, one can use PhantomJS (https://phantomjs.org/download.html)
in this project we are using PhantomJS. Download and install it in some directory, f.e. phantom

6) Execute the following command in console:

```
>python -m weatherapp -p WeatherComParser -u Celsius -a ae8230efd4bc57fdf721a02c7eb2b88c56aa6e71d73666328e33af3ea2039032132e24ae91b6a07862c5091a9d95a4b8 -td
```


The output should look like:

```
using sub type: _today_forecast
http://weather.com/weather/today/l/ae8230efd4bc57fdf721a02c7eb2b88c56aa6e71d73666328e33af3ea2039032132e24ae91b6a07862c5091a9d95a4b8
retrieved raw data 899273 bytes
{'location': ['London, England, United Kingdom Weather'], 'unit': ['°F'], 'temperature': ['51°'], 'phase': ['Partly Cloudy']}
```
Area codes for locations can be found at https://weather.com

# OAuth2 authorization

This is a simple app demonstrating the work with real OAuth2-secured services on the basis of Spotify
NOTE: it will need curses library to be installed, for Windows install it manually:

```
pip install windows-curses
```

1) Create an account on Spotify:
https://developer.spotify.com/dashboard
   
See screenshots 1 and 2
   
2) In a file called config.yaml in the spotify directory add client_id and client_secret are the keys that were created for us when we created the
Spotify application. These keys will be used to get an access token that we will have to
acquire every time we need to send a new request to Spotify's REST API.

```
client_id: '<your client ID>'
client_secret: '<your client secret>'
access_token_url: 'https://accounts.spotify.com/api/token'
auth_url: 'http://accounts.spotify.com/authorize'
api_version: 'v1'
api_url: 'https://api.spotify.com'
auth_method: 'AUTHORIZATION_CODE'
```
3) Run auth code to get a token

```
python -m spotify.spotify_auth
```
after successful authorization the server will catch the token and persist it into the file .jukebox in the current directory

4) Run main application to search information about artists and albums:

```
python -m spotify.app
```
# Consuming public API

# Exchange Rates, Currency Conversion Tool

This is a super simple project which is using foxit.io service to get currency exchange rates and MongoDB as 
the intermediate history persistent layer - basically it just plays the role of cache

1) This project requires the MongoDB instance, so the first step will be to create it using docker-compose file in root directory:

```
docker-compose -f docker-compose-min.yml up --build
```

2) Open account on fixer.io
This project is yet another example of consuming API. 
For this one the fixer API is used (https://github.com/fixerAPI/fixer#readme)
There is an option to get a free api token, see the details on https://fixer.io/

The screenshot on fixer_1.png shows how the page to open new account looks like

3) Run the app:

```
python -m forexapp --from EUR --to RUB --value 200 --token af65766c7c2403461e34867dc5142d44

converting 200.0 units from EUR->RUB
Fetching exchange rates from fixer.io [base currency: EUR]
200.0 EUR = 17866.24 RUB
```

4) One can query DB against collected rates to see the cached values:

```
db.rates.find({})
   .projection({})
   .sort({_id:-1})
   .limit(100)
```

The result will be similar to this one (rates field was truncated for brevity):

```
{
	"_id" : ObjectId("6065bae4716e1877db2e3c39"),
	"base" : "EUR",
	"date" : "2021-04-01",
	"rates" : {
		"AED" : 4.310488,
		"AFN" : 91.902225,
		"ALL" : 123.004027,
		"USD" : 1.173573,
		"UYU" : 52.083039,
		"UZS" : 12307.312892,
		"VEF" : 217051133237.23477,
		"ZMW" : 25.924749,
		"ZWL" : 377.891029
	},
	"success" : true,
	"timestamp" : 1617277386
}

```
Cache eviction rule is very simple:
<b> if the date of record in cache is too old (previous day or earlier) fresh data will be requested </b>



Requirements
=============

In order to execute the code the following toolkit is needed:

- Virtualenv
- Python 3.9
- pgAdmin
- Docker
