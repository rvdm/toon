#!/usr/bin/env python

import pprint
from Toon import Toon
import argparse

parser = argparse.ArgumentParser(description='Communicate with the Eneco Toon thermostat')
parser.add_argument('-t',help='return current temperature in Celsius',action='store_true')
parser.add_argument('-p',help='return current power usage in Watts',action='store_true')
parser.add_argument('-U','--username',help='the Toon username',required=True,dest='username')
parser.add_argument('-P','--password',help='the Toon password',required=True,dest='password')

args = parser.parse_args()

username = args.username
password = args.password

toon = Toon(username,password)
toon.login()

if args.t == True:
	thermostat = toon.getThermostatInfo()
	temp = float(thermostat["currentTemp"]) / 100
	print "current_temp:%.2f" % temp

if args.p == True:
	power = toon.getPowerUsage()
	print "current_powerusage:%d" % power["value"]

toon.logout()

