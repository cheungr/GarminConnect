GarminConnect
========

Python library to log my weight to Garmin Connect, because i broke up with fitbit - which btw supports IFTT and has open APIs for you to play with (Garmin does not.) - and now want my weight logged on Garmin Connect where the rest of my data is instead.

Installation
------------

Requires: 

* [Request](http://docs.python-requests.org/en/master/) `sudo pip install requests`

Usage
------------

```python
from GarminConnect import GarminConnect

garminUsername = 'you@provider.com'
garminPassword = 'C0nn3cTpw'

garmin = GarminConnect(garminUsername, garminPassword)
garmin.postWeight(138.21, '2018-01-16') # weight lbs & date, you can use time.strftime('%Y-%m-%d') for today's date.
```
