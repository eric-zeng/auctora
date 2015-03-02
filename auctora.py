import logging
import json
import os
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

# handler for URL with no path (just tidy-nomad-842.appspot.com)
# shows the Auctora login page
class LandingHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info('' + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('html/LoginPage.html')
		self.response.write(template.render())

# serve the root page for the Auctora slides
class SlidesLandingHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info('' + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('html/slides.html')
		self.response.write(template.render())

# Handle the redirect from the LinkedIn sign in page.
class LinkedInAuthHandler(webapp2.RequestHandler):
	def get(self):
		error = self.request.get('error', 'no error')
		if error != 'no error':
			self.response.write('<html><body>LinkedIn Authentication Error: ' +
				error + '</body></html>')
			return

		# Extract the URL queries.
		authCode = self.request.get('code')
		state = self.request.get('state')

		# Read the private API Key from the file.
		keyFile = open('API_Key.txt', 'r')
		privateKey = keyFile.read()

		# Create the POST request to obtain an access token.
		tokenRequest = {
		  'grant_type': 'authorization_code',
		  'code': authCode,
		  'redirect_uri': self.request.path_url,
		  'client_id': '75kh0yq5sa89ld',
		  'client_secret': privateKey
		}

		# Send the POST request.
		tokenRequestData = urllib.urlencode(tokenRequest)
		tokenResponse = urlfetch.fetch(
			url='https://www.linkedin.com/uas/oauth2/accessToken',
		    payload=tokenRequestData,
		    method=urlfetch.POST,
		    headers={'Content-Type': 'application/x-www-form-urlencoded'})

		if tokenResponse.status_code != 200:
			self.response.write('<html><body>Error ' +
				str(tokenResponse.status_code) +
				' while getting token</body></html>')
			return

		# Read the access token from the JSON response.
		token = json.loads(tokenResponse.content)
		accessToken = token["access_token"]
		expiresIn = token["expires_in"]

		# Use the access token to retrieve the basic profile.
		tokenHeader = 'Bearer ' + accessToken
		profileResponse = urlfetch.fetch(
			url='https://api.linkedin.com/v1/people/~?format=json',
			method=urlfetch.GET,
			headers={'Authorization': tokenHeader})

		if profileResponse.status_code != 200:
			self.response.write('<html><body>Error ' + str(profile.status_code)+
				' while retrieving profile</body></html>')
			return

		profile = json.loads(profileResponse.content)

		# TODO: Save candidate data in datastore.

		# Send the authentication->questions redirect page.
		template = JINJA_ENVIRONMENT.get_template('html/redirect.html')
		self.response.write(template.render())

class QuestionsHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('html/questions.html')
		self.response.write(template.render())

application = webapp2.WSGIApplication([
	# Home page handler
	('/', LandingHandler),

	# auctora pitch slides handler
	('/slides', SlidesLandingHandler),

	# LinkedIn auth handler
	('/auth/linkedIn', LinkedInAuthHandler),

	# Student questions handler
	('/questions', QuestionsHandler),

], debug=True)
