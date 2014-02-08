import re
import urllib2
import urllib
from cookielib import CookieJar
import json
import sys
import uuid
import pprint

""" The Toon module impersonates the Eneco Toon mobile app, and implements
similar functionality. """

class Toon:
	""" Log in to the Toon API, and do stuff. """
	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.debug = 0

	def login(self):
		""" Log in to the toon API, and set up a session. """
		# First we open the login page, to get the agreement
		# details.
		# Agreement details and user details are stored in the
		# sessiondata variable.
		self.cj = CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		formdata = { "username" : self.username, "password": self.password }
		data_encoded = urllib.urlencode(formdata)
		response = self.opener.open("https://toonopafstand.eneco.nl/toonMobileBackendWeb/client/login", data_encoded)
		self.sessiondata = json.loads(response.read())

		# Now re-use the agreement details to do the actual
		# authentication. This establishes a session, and allows
		# state to be retrieved.
		# TODO: check for variable existence / throw exception on
		# failure
		formdata = {	"clientId": self.sessiondata["clientId"],
				"clientIdChecksum": self.sessiondata["clientIdChecksum"],
				"agreementId": self.sessiondata["agreements"][0]["agreementId"],
				"agreementIdChecksum": self.sessiondata["agreements"][0]["agreementIdChecksum"],
				"random": uuid.uuid1() }
		data_encoded = urllib.urlencode(formdata)
		url = "https://toonopafstand.eneco.nl/toonMobileBackendWeb/client/auth/start?%s" % data_encoded
		response = self.opener.open(url)

	def logout(self):
		""" Log out of the API. 
		This is needed, as toon keeps a maximum amount of display clients - too many logins lead to 500 responses from the API. """
		formdata = {	"clientId": self.sessiondata["clientId"],
				"clientIdChecksum": self.sessiondata["clientIdChecksum"],
				"random": uuid.uuid1() }
		data_encoded = urllib.urlencode(formdata)
		url = "https://toonopafstand.eneco.nl/toonMobileBackendWeb/client/auth/logout?%s" % data_encoded
		response = self.opener.open(url)

	def retrieveToonState(self):
		formdata = { 	"clientId": self.sessiondata["clientId"],
				"clientIdChecksum": self.sessiondata["clientIdChecksum"],
				"random": uuid.uuid1() }
		data_encoded = urllib.urlencode(formdata)
		url = "https://toonopafstand.eneco.nl/toonMobileBackendWeb/client/auth/retrieveToonState?%s" % data_encoded
		response = self.opener.open(url)
		self.toonstate = json.loads(response.read()) # TODO: check for success

	def getGasUsage(self):
		if not hasattr(self, 'toonstate'):
			self.retrieveToonState()
		return self.toonstate["gasUsage"]

	def getPowerUsage(self):
		if not hasattr(self, 'toonstate'):
			self.retrieveToonState()
		return self.toonstate["powerUsage"]
		
	def getThermostatInfo(self):
		if not hasattr(self, 'toonstate'):
			self.retrieveToonState()
		return self.toonstate["thermostatInfo"]

	def getThermostatStates(self):
		if not hasattr(self, 'toonstate'):
			self.retrieveToonState()
		return self.toonstate["thermostatStates"]

