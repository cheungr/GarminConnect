import requests
import re
import json

# garmin = GarminConnect('email', 'password')
# garmin.postWeight(138.21, '2018-01-16')

class GarminConnect:
	session = None
	username = None
	password = None
	ssoURL = 'https://sso.garmin.com/sso/login'
	postWeightURL = 'https://connect.garmin.com/modern/proxy/weight-service/user-weight'

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def _login(self):
		ssoticket = None

		if self.session is None:
			self.session = requests.Session()

		r = self.session.post(self.ssoURL, 
			params={'service':'https://connect.garmin.com/modern/', 'clientId':'GarminConnect', 'consumeServiceTicket':'false', 'mobile':'false'},
			data={'username':self.username, 'password':self.password, 'embed':'false'})

		ssoticketSearch = re.compile("ticket=([^']*)").search(r.text)
		if ssoticketSearch:
			ssoticket = ssoticketSearch.group(1)
		else:
			raise Exception('auth error. Can not find sso ticket.')

		r = self.session.get(self.ssoURL,
			params={'ticket':ssoticket})

		if r.status_code == 200:
			self.session.get('https://connect.garmin.com/modern/')
			return True
		else:
			raise Exception('auth error. Response was: %s' % r.text)

	def postWeight(self, weight, day):
		weightData = {"value":weight,"unitKey":"lbs","date":day}
		if self._login():
			headers = {'content-type':'application/json', 'origin':'https://connect.garmin.com', 'referer':'https://connect.garmin.com/modern/weight', 'nk': 'NT', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3318.0 Safari/537.36', 'x-requested-with':'XMLHttpRequest'}
			r = self.session.post(self.postWeightURL, headers=headers, data=json.dumps(weightData))
		else:
			raise Exception('Unable to send weight. Auth Error.')



