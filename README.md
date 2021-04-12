About
======
This is a collection of recipes to create different web apps components on the basis of Python 3.9

Topics covered so far:

* RPA (web scraping)
* OAuth2 authorization
* Consuming public web APIs
* Microservices in Python
* Asynchronous messaging in Python (TBA)
* Serverless apps in Python (TBA)


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


1) One can perform testing in two ways - using standard browser with Chrome driver or the headless one. As for the latter, one can use PhantomJS (https://phantomjs.org/download.html).

In this project we are using PhantomJS. Download and install it into some directory, f.e. phantom

6) Execute the following command in console:

```
python -m weatherapp -p WeatherComParser -u Celsius -a ae8230efd4bc57fdf721a02c7eb2b88c56aa6e71d73666328e33af3ea2039032132e24ae91b6a07862c5091a9d95a4b8 -td
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
3) Run auth code to get a token (note way the module is executed - the FQN path must be specified)

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
python -m forexapp --from EUR --to RUB --value 200 --token <your token>

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

# Microservices


The module soa.microservices contains the simple implementation of Order microservice with the following endpoints:

```

```
Official Django documentation on microservices can the found here https://docs.djangoproject.com/en/3.2/intro/tutorial01/


Note the typical Django structure for project:
```
order/

    main/
       migrations/
           __init__
           <microservice implementation>
      
    order/
       __init__
       settings.py
       urls.py
       wsgi.py
      
    manage.py

```

In order to create all tables and add the initial auth records to internal db use the step 0:

0) Preliminary step: generate all necessary code using the commands:

create a package migrations inside your app directory (main in this case)

create a migration tasks
```
python -m soa.microservices.order.manage makemigrations
```
perform migrations
```
python -m soa.microservices.order.manage migrate
```
The result should look like this one:

```
current directory D:\repos-research\python-recipes
system paths ['D:\\repos-research\\python-recipes', 'C:\\ProgramData\\python391\\python39.zip', 'C:\\ProgramData\\python391\\DLLs', 'C:\\ProgramData\\python391\\lib', 'C:\\ProgramData\\python391', 'C:\\ProgramData\\python391\\lib\\site
-packages', 'D:\\repos-research\\python-recipes', 'D:\\repos-research\\python-recipes\\soa\\microservices\\order']
Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, main, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying authtoken.0001_initial... OK
  Applying authtoken.0002_auto_20160226_1747... OK
  Applying main.0001_initial... OK
  Applying sessions.0001_initial... OK

```
1) Create an initial user (admin):


```
python -m soa.microservices.order.manage createsuperuser

Username (leave blank to use 'akaliutau'): admin
Email address: test@test.org
Password:
Password (again):

Superuser created successfully.

```

2) To start the service with the following command (by some reason it does not start as a module):

```
python .\soa\microservices\order\manage.py runserver

cur directory D:\repos-research\python-recipes
Performing system checks...

System check identified no issues (0 silenced).

April 09, 2021 - 10:01:19
Django version 3.2, using settings 'soa.microservices.order.order.settings'
Starting development server at http://127.0.0.1:8000/

```
The first run will create a db.sqlite3 database with necessary tables.

If the system log contains the output like this one:
```
You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, authtoken, contenttypes, main, sessions.
Run 'python manage.py migrate' to apply them.
```
then perform migration in accordance with step 0 and step 1



3) Point browser to https://localhost:8000/admin, login.

Then click on Add and create a user with the username test_api. 

When the user is created, create an APi token using AUTH TOKEN section.
Assign this token to a newly created user: select the test_api in the drop-down menu and click SAVE. 

4) Finally one can test built microservice using the simple test app in test_order.py:

```
python -m soa.microservices.order.test_order   --token 83622fab3429404dccd8da65ba97468a0306551e

```
On log server one can observe the server has responded with 201 status:

```
created Order object (2)
[09/Apr/2021 17:01:35] "POST /api/order/add/ HTTP/1.1" 201 14

```

Requirements
=============

In order to execute the code the following toolkit is needed:

- Virtualenv
- Python 3.9
- pgAdmin
- Docker
