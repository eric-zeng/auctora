import logging
import json
import random
import urllib
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from webapp2_extras import security
from webapp2_extras import sessions

import recruiter
from common import BaseHandler
from common import JINJA_ENVIRONMENT
from models import Annotation
from models import BasicProfile
from models import Position

# handler for URL with no path (just tidy-nomad-842.appspot.com)
# shows the Auctora login page
class LandingHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('landing/main.html')
		self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info('' + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('candidate/loginPage.html')
		self.response.write(template.render())

# serve the root page for the Auctora slides
class SlidesLandingHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info('' + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('slides.html')
		self.response.write(template.render())

# Handle the redirect from the LinkedIn sign in page.
class LinkedInAuthHandler(BaseHandler):
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
		accessToken = token['access_token']
		expiresIn = token['expires_in']

		# Use the access token to retrieve the basic profile.
		tokenHeader = 'Bearer ' + accessToken
		profileFields = 'id,first-name,last-name,headline,location,' + \
			'industry,summary,specialties,positions,picture-url,' + \
			'public-profile-url,site-standard-profile-request'
		profileResponse = urlfetch.fetch(
			url='https://api.linkedin.com/v1/people/~:(' + profileFields + \
				')?format=json',
			method=urlfetch.GET,
			headers={'Authorization': tokenHeader})

		if profileResponse.status_code != 200:
			self.response.write('<html><body>Error ' + str(profile.status_code)+
				' while retrieving profile</body></html>')
			return

		profile = json.loads(profileResponse.content)

		# Save candidate data in datastore.
		logging.info(profileResponse.content)

		profiles = BasicProfile.query(BasicProfile.id == profile['id']).fetch()

		if len(profiles) == 0:
			# If this is the first login, create a new entity for their profile.
			profileEntity = BasicProfile()
		else:
			# Otherwise get the old profile and update it with newest version of
			# their LinkedIn profile.
			profileEntity = profiles[0]

		profileEntity.id = profile['id']
		profileEntity.fname = profile['firstName']
		profileEntity.lname = profile['lastName']
		profileEntity.profileUrl = profile['publicProfileUrl']
		profileEntity.stars = 0

		# These are optional fields, so run a check on each to see if they
		# exist.
		aData = profile.keys()
		if 'headline' in aData:
			profileEntity.headline = profile['headline']
		else:
			profileEntity.headline = None
		if 'industry' in aData:
			profileEntity.industry = profile['industry']
		else:
			profileEntity.industry = None
		if 'location' in aData and 'name' in profile['location']:
			profileEntity.location = profile['location']['name']
		else:
			profileEntity.location = None
		if 'pictureUrl' in aData:
			profileEntity.pictureUrl = profile['pictureUrl']
		else:
			profileEntity.pictureUrl = '/images/profile-pic.png'
		profileEntity.put()

		# Parse the position objects if they exist and put them in the datastore
		if 'positions' in aData and profile['positions']['_total'] > 0:
			total = profile['positions']['_total']
			for i in range(0, total):
				pos = profile['positions']['values'][i]

				# Check if this position already exists, if yes update, if not
				# create a new one.
				posQuery = Position.query(Position.id == pos['id']).fetch()
				if len(posQuery) == 0:
					posEntity = Position()
				else:
					posEntity = posQuery[0]

				posEntity.id = pos['id']
				posEntity.profileId = profile['id']
				posEntity.isCurrent = pos['isCurrent']

				if 'title' in pos:
					posEntity.title = pos['title']
				else:
					posEntity.title = None

				if 'summary' in pos:
					posEntity.description = pos['summary']
				else:
					posEntity.description = None

				if 'company' in pos:
					posEntity.company = pos['company']['name']
				else:
					posEntity.company = None

				if 'startDate' in pos:
					posEntity.startMonth = pos['startDate']['month']
					posEntity.startYear = pos['startDate']['year']
				else:
					posEntity.startMonth = None
					posEntity.startYear = None

				if 'endDate' in pos:
					posEntity.endMonth = pos['endDate']['month']
					posEntity.endYear = pos['endDate']['year']
				else:
					posEntity.endMonth = None
					posEntity.endYear = None

				posEntity.put()

		self.session['profileId'] = profile['id']
		self.session['userType'] = "candidate"

		# Send the authentication-to-questions redirect page.
		template = JINJA_ENVIRONMENT.get_template('candidate/authredirect.html')
		self.response.write(template.render())

class QuestionsHandler(BaseHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('candidate/questions.html')
		self.response.write(template.render())

class CompaniesHandler(BaseHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('candidate/companies.html')
		self.response.write(template.render())

class QuestionsFormHandler(BaseHandler):
	def post(self):
		logging.info(self.request.body)

class ManualPositionHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/manualData.html')
		self.response.write(template.render())
	def post(self):
		form = json.loads(self.request.body)
		position = Position()
		for obj in form:
			if obj['name'] == 'profileId':
				position.profileId = obj['value']
			if obj['name'] == 'title':
				position.title = obj['value']
			if obj['name'] == 'description':
				position.description = obj['value']
			if obj['name'] == 'company':
				position.company = obj['value']
			if obj['name'] == 'startMonth':
				position.startMonth = int(obj['value'])
			if obj['name'] == 'startYear':
				position.startYear = int(obj['value'])
			if obj['name'] == 'endMonth':
				position.endMonth = int(obj['value'])
			if obj['name'] == 'endYear':
				position.endYear = int(obj['value'])
			if obj['name'] == 'isCurrent':
				position.isCurrent = True
		position.id = random.randint(1, 1000000)
		position.put()

class ProfileIdLookupHandler(BaseHandler):
	def get(self):
		self.response.write('<html><body>')
		self.response.write('<h3>Profile IDs</h3>')
		profiles = BasicProfile.query().fetch()
		for profile in profiles:
			self.response.write(profile.fname + " " + profile.lname + ": ")
			self.response.write(profile.id + "<br>")
		self.response.write('</body></html>')

config = {
	'webapp2_extras.sessions': {
		'secret_key': 'my-super-secret-key',
	},
	'webapp2_extras.auth': {
		'user_model': 'models.User',
		'user_attributes': ['name']
	}
}

application = webapp2.WSGIApplication([
	# Home page handler
	('/', LandingHandler),

	# auctora pitch slides handler
	('/slides', SlidesLandingHandler),

	# LinkedIn auth handler
	('/auth/linkedIn', LinkedInAuthHandler),

	# Student UI Handlers
	('/login', LoginHandler),
	('/questions', QuestionsHandler),
	('/companies', CompaniesHandler),

	# Student questions form response handler
	('/submitQuestions', QuestionsFormHandler),

	# Recruiter UI Handlers
	('/recruiterLogin', recruiter.RecruiterLoginHandler),
	('/recruiterRegistration', recruiter.RecruiterRegistrationHandler),
	('/search', recruiter.SearchHandler),
	('/profile', recruiter.ProfileHandler),
	('/home', recruiter.RecruiterHomeHandler),
	('/setStars', recruiter.StarsHandler),

	# Profile data request handlers
	('/profileRequest', recruiter.ProfileRequestHandler),
	('/nameRequest', recruiter.NameRequestHandler),

	# Handler for submitting an annotations image.
	('/submitAnnotation', recruiter.AnnotationHandler),

	# Manual data entry for demos
	('/manualPosition', ManualPositionHandler),
	('/profileIdLookup', ProfileIdLookupHandler),

], config=config, debug=True)
