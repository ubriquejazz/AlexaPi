import time, json
import logging
import requests
from exceptions import ConfigurationException

logger = logging.getLogger(__name__)

class Token(object):

	_token = ''
	_timestamp = None
	_validity = 3570

	def __init__(self, aconfig):
		self._aconfig = aconfig
		if not self._aconfig.get('refresh_token'):
			logger.critical("AVS refresh_token not found in the configuration file. "
					"Run the setup again to fix your installation (see project wiki for installation instructions).")
			raise ConfigurationException

		self.renew()

	def __str__(self):

		if (not self._timestamp) or (time.time() - self._timestamp > self._validity):
			logger.debug("AVS token: Expired")
			self.renew()

		return self._token

	def renew(self):

		logger.info("AVS token: Requesting a new one")
		payload = {
			"client_id": self._aconfig['Client_ID'],
			"client_secret": self._aconfig['Client_Secret'],
			"refresh_token": self._aconfig['refresh_token'],
			"grant_type": "refresh_token"
		}

		url = "https://api.amazon.com/auth/o2/token"
		try:
			response = requests.post(url, data=payload)
			resp = json.loads(response.text)

			self._token = resp['access_token']
			self._timestamp = time.time()

			logger.info("AVS token: Obtained successfully")
		except requests.exceptions.RequestException as exp:
			logger.critical("AVS token: Failed to obtain a token: " + str(exp))

