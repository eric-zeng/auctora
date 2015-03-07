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

class BasicProfile(ndb.Model):
	id = ndb.StringProperty()
	fname = ndb.StringProperty()
	lname = ndb.StringProperty()
	headline = ndb.StringProperty()
	industry = ndb.StringProperty()
	location = ndb.StringProperty()
	pictureUrl = ndb.StringProperty()
	profileUrl = ndb.StringProperty()

class Annotation(ndb.Model):
	# id of BasicProfile that the annotation is associated with.
	id = ndb.StringProperty()
	 # Name of BasicProfile field that is annotated.
	field = ndb.StringProperty()
	 # Data-URL of the image.
	image = ndb.StringProperty()


# handler for URL with no path (just tidy-nomad-842.appspot.com)
# shows the Auctora login page
class LandingHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info('' + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('html/LoginPage-chip.html')
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
			profileEntity = BasicProfile(
				id         = profile['id'],
				fname      = profile['firstName'],
				lname      = profile['lastName'],
				headline   = None,
				industry   = None,
				location   = None,
				pictureUrl = None,
				profileUrl = profile['publicProfileUrl']
			)
			aData = profile.keys()
			if 'headline' in aData:
				profileEntity.headline = profile['headline']
			if 'industry' in aData:
				profileEntity.industry = profile['industry']
			if 'location' in aData and 'name' in aData:
				profileEntity.location = profile['location']['name']
			if 'pictureUrl' in aData:
				profileEntity.pictureUrl = profile['pictureUrl']
			profileEntity.put()
		else:
			logging.info(profile['id'] + " already in db, skipping.")

		# Send the authentication-to-questions redirect page.
		template = JINJA_ENVIRONMENT.get_template('html/authredirect.html')
		self.response.write(template.render())

class QuestionsHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('html/questions-chip.html')
		self.response.write(template.render())

class CompaniesHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('html/companies-chip.html')
		self.response.write(template.render())

class QuestionsFormHandler(webapp2.RequestHandler):
	def post(self):
		logging.info(self.request.body)

class StudentSearchHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('html/studentsearch.html')
		self.response.write(template.render())

class StudentProfileHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('html/studentprofile.html')
		self.response.write(template.render())

# Handles requests for profile by id.
# Send GET http://tidy-nomad-842.appspot.com/profileRequest?id=<insert id here>
# to get a JSON string with all of the fields.
class ProfileRequestHandler(webapp2.RequestHandler):
	def get(self):
		profiles = BasicProfile.query(BasicProfile.id == self.request.get('id')).fetch()
		if len(profiles) < 1:
			self.response.write('{"error": "no profile with id "' +
				self.request.get('id') + '}' )

		profile = profiles[0]
		logging.info(profile)
		result = json.dumps({
			'id':         profile.id,
			'fname':      profile.fname,
			'lname':      profile.lname,
			'headline':   profile.headline,
			'industry':   profile.industry,
			'location':   profile.location,
			'pictureUrl': profile.pictureUrl,
			'profileUrl': profile.profileUrl
		}, sort_keys=True)
		self.response.write(result)

# Handles requests for profiles by name.
# Send GET http://tidy-nomad-842.appspot.com/nameRequest?<insert name here>
# to get a JSON array containing JSON objects with first name, last name,
# picture, and id.
# Intended for use in autocomplete.
class NameRequestHandler(webapp2.RequestHandler):
	def get(self):
		prefix = self.request.get('startsWith').lower()
		query = BasicProfile.query().order(BasicProfile.fname)
		profiles = query.fetch(projection=[BasicProfile.fname,
											BasicProfile.lname,
											BasicProfile.pictureUrl,
											BasicProfile.id])
		output = list()
		for profile in profiles:
			fname = profile.fname.lower()
			lname = profile.lname.lower()
			fullname = profile.fname.lower() + " " + profile.lname.lower()
			if fname.startswith(prefix) or lname.startswith(prefix) or fullname.startswith(prefix):
				output.append({"fname": profile.fname,
					"lname": profile.lname,
					"id": profile.id,
					"pictureUrl": profile.pictureUrl})

		self.response.write(json.dumps(output, sort_keys=True))

# Handles saving profile annotations.
# POST http://tidy-nomad-842.appspot.com/submitAnnotation
# With JSON body:
# {
#   id:    asdflkj
#   field: (fname|lname|headline|industry|location)
#   image: <the data-uri of the image>
# }
class AnnotationHandler(webapp2.RequestHandler):
	def post(self):
		annotation = json.loads(self.request.body)
		annotationEntity = Annotation(id=annotation['id'],
									  field=annotation['field'],
									  image=annotation['image'])
		annotationEntity.put()

	# GET handler for testing. We'll might want to generate the annotation
	# in the profile page when it is loaded.
	def get(self):
		results = Annotation.query(
				Annotation.id == self.request.get['id'],
				Annotation.field == self.request.get['field']).fetch()
		if len(results) == 0:
			self.response.write("{}")

		# Assume one annotation per id+field
		a = results[0]
		output = {
			"id": a.id,
			"field": a.field,
			"image": a.image}
		self.response.write(json.dumps(output, sort_keys=True))

application = webapp2.WSGIApplication([
	# Home page handler
	('/', LandingHandler),

	# auctora pitch slides handler
	('/slides', SlidesLandingHandler),

	# LinkedIn auth handler
	('/auth/linkedIn', LinkedInAuthHandler),

	# Student UI Handlers
	('/questions', QuestionsHandler),
	('/companies', CompaniesHandler),

	# Student questions form response handler
	('/submitQuestions', QuestionsFormHandler),

	# Recruiter UI Handlers
	('/studentSearch', StudentSearchHandler),
	('/studentProfile', StudentProfileHandler),

	# Profile data request handlers
	('/profileRequest', ProfileRequestHandler),
	('/nameRequest', NameRequestHandler),

	# Handler for submitting an annotations image.
	('/submitAnnotation', AnnotationHandler)

], debug=True)
