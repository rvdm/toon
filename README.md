Toon
====

A simple python module to interface with the Toon 'intelligent' thermostat.

Example
====

```
from Toon import Toon

toonurl = "https://toonopafstand.eneco.nl/"
username = "YOURTOONUSERNAME"
password = "YOURTOONPASSWORD"

toon = Toon(username,password)
toon.login()
toon.retrieveToonState()

thermostat = toon.getThermostatInfo()
power = toon.getPowerUsage()
toon.logout()

temp = float(thermostat["currentTemp"]) / 100
print "Current temperature: %.2f degrees Celsius" % temp
print "Current power usage: %d Watt" % power["value"]
```
