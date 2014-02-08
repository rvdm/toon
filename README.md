Toon
====

A simple python module to interface with the Eneco Toon 'intelligent' thermostat.

The Toon API and clients
====

The Toon device is a rebranded 'cuby' (http://quby.nl/) thermostat. It
interfaces with a few web services at Eneco, and gathers power, gas and
thermostat information.
When using the Toon along with the 'Toon op afstand' option, some of the
Toon information and settings can be accessed via a simple iPhone app.

Eneco's iPhone client for Toon is essentially a browser object, connecting
to the 'toon op afstand' web pages at https://toonopafstand.eneco.nl/ .
The toonopafstand web app consumes an API being served out of the same
domain.

Authentication
===
Authentication to the Toon API is a two-step process. No cookies or referer
settings are required.
1) 
Log in using the 'toonopafstand' username and password. The username and
password are the same as the ones you use for 'mijn eneco'.
The login response returns a JSON blob with some address and agreement
information:

```
{u'agreements': [{u'agreementId': u'SOMEINTEGER',
                  u'agreementIdChecksum': u'SOMECHECKSUM',
                  u'city': u'SOMECITY',
                  u'displayCommonName': u'eneco-xxx-yyyyyy',
                  u'displayHardwareVersion': u'qb2/ene/2.6.24',
                  u'displaySoftwareVersion': u'qb2/ene/2.6.24',
                  u'houseNumber': u'xx',
                  u'postalCode': u'xxxxAB',
                  u'street': u'SOMESTREET'}],
 u'clientId': u'SOMEUUID',
 u'clientIdChecksum': u'SOMECHECKSUM',
 u'passwordHash': u'SOMEHASH',
 u'sample': False,
 u'success': True}
```

2) 
Grab the JSON response from the login request, and extract the agreement
information. The agreement information is subsequently used to start a
session, and to allow retrieval of data. My guess is that the two-step
process might allow for a 'select your toon' feature in the future, assuming
people can have more of them.

The session start return simply returns 'success:true' on success.


Retrieving status
===

Retrieving status is a simple call, re-using the agreement information from
the second step of the authentication process. 
The status retrieval call accepts clientId, clientIdChecksum, agreementID
and agreementIdChecksum as parameters. The API expects an additional
parameter called random, containing a random UUID.

The return JSON looks like this:
```
{u'gasUsage': {u'avgDayValue': 25498.57,
               u'avgValue': 1062.44,
               u'dayCost': 0.0,
               u'dayUsage': 19380,
               u'isSmart': 0,
               u'meterReading': 4840000,
               u'value': 0},
 u'powerUsage': {u'avgValue': 477.99,
                 u'dayCost': 2.7,
                 u'dayCostProduced': u'0.00',
                 u'dayLowUsage': 7713,
                 u'dayUsage': 0,
                 u'isSmart': 0,
                 u'meterReading': 2521773,
                 u'meterReadingLow': 2431872,
                 u'value': 511,
                 u'valueProduced': u'0'},
 u'thermostatInfo': {u'activeState': 0,
                     u'burnerInfo': u'0',
                     u'currentModulationLevel': 16,
                     u'currentSetpoint': 1950,
                     u'currentTemp': 1959,
                     u'errorFound': 255,
                     u'haveOTBoiler': 0,
                     u'nextProgram': 1,
                     u'nextSetpoint': 1550,
                     u'nextState': 2,
                     u'nextTime': 1391900400,
                     u'otCommError': u'0',
                     u'programState': 1,
                     u'randomConfigId': 1804289383,
                     u'zwaveOthermConnected': 0},
 u'thermostatStates': {u'state': [{u'dhw': 1, u'id': 0, u'tempValue': 1950},
                                  {u'dhw': 1, u'id': 1, u'tempValue': 1850},
                                  {u'dhw': 1, u'id': 2, u'tempValue': 1550},
                                  {u'dhw': 1, u'id': 3, u'tempValue': 1200},
                                  {u'dhw': 0, u'id': 4, u'tempValue': 600},
                                  {u'dhw': 1, u'id': 5, u'tempValue': 600}]}}
```


Example
====

```python
from Toon import Toon

username = "YOURTOONUSERNAME"
password = "YOURTOONPASSWORD"

toon = Toon(username,password)
toon.login()

thermostat = toon.getThermostatInfo()
power = toon.getPowerUsage()
toon.logout()

temp = float(thermostat["currentTemp"]) / 100
print "Current temperature: %.2f degrees Celsius" % temp
print "Current power usage: %d Watt" % power["value"]
```
