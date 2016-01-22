#!/usr/bin/env python

import pprint
from Toon import Toon
import argparse

parser = argparse.ArgumentParser(description='Communicate with the Eneco Toon thermostat')
parser.add_argument('-t', help='return current temperature in Celsius', action='store_true')
parser.add_argument('-p', help='return current power usage in Watts', action='store_true')
parser.add_argument('-c', help='return active program state', action='store_true')
parser.add_argument('-s', '--settemp', help='set target temperature', dest='targettemp', type=float)
parser.add_argument('-C', '--setstate', help='set target state', dest='targetstate')
parser.add_argument('-U', '--username', help='the Toon username', required=True, dest='username')
parser.add_argument('-P', '--password', help='the Toon password', required=True, dest='password')

args = parser.parse_args()

username = args.username
password = args.password

toon = Toon(username, password)
toon.set_maxretries(5)
toon.login()

if args.t:
        thermostat = toon.get_thermostat_info()
        temp = float(thermostat["currentTemp"]) / 100
        print "current_temp:%.2f" % temp

if args.p:
        power = toon.get_power_usage()
        print "current_powerusage:%d" % power["value"]

if args.c:
        state = toon.get_program_state()
        print "active_state:%d" % state

if args.targetstate is not None:
        print "set_state:%s" % args.targetstate
        toon.set_program_state(args.targetstate)

if args.targettemp is not None:
        print "set_temp:%s" % args.targettemp
        toon.set_thermostat(args.targettemp)

toon.logout()
