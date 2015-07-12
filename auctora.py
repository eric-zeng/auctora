import logging
import jinja2
import json
import os
import random
import urllib
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

from webapp2_extras import sessions

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
	stars = ndb.IntegerProperty()

class Annotation(ndb.Model):
	# id of BasicProfile that the annotation is associated with.
	id = ndb.StringProperty()
	 # Name of BasicProfile field that is annotated.
	field = ndb.StringProperty()
	 # Data-URL of the image.
	image = ndb.StringProperty()

class Position(ndb.Model):
	id = ndb.IntegerProperty()
	profileId = ndb.StringProperty() # Foreign key to BasicProfile
	title = ndb.StringProperty()
	description = ndb.StringProperty()
	company = ndb.StringProperty()

	startMonth = ndb.IntegerProperty()
	startYear = ndb.IntegerProperty()
	endMonth = ndb.IntegerProperty()
	endYear = ndb.IntegerProperty()
	isCurrent = ndb.BooleanProperty()

class BaseSessionHandler(webapp2.RequestHandler):
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)

		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)

	@webapp2.cached_property
	def session(self):
		# Returns a session using the default cookie key.
		return self.session_store.get_session()

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
class LinkedInAuthHandler(BaseSessionHandler):
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

class QuestionsHandler(BaseSessionHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('candidate/questions.html')
		self.response.write(template.render())

class CompaniesHandler(BaseSessionHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('candidate/companies.html')
		self.response.write(template.render())

class QuestionsFormHandler(BaseSessionHandler):
	def post(self):
		logging.info(self.request.body)

class RecruiterLoginHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('recruiter/recruiterLogin.html')
		self.response.write(template.render())
	def post(self):
		logging.info(self.request.body)

class SearchHandler(BaseSessionHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('recruiter/search.html')
		self.response.write(template.render())

class ProfileHandler(BaseSessionHandler):
	def get(self):
		profiles = BasicProfile.query(BasicProfile.id == self.request.get('id')).fetch()
		if len(profiles) == 0:
			self.response.write('<html><body>Could not find profile ' + \
								self.request.get('id') + '</body></html>')

		positions = Position.query(Position.profileId == self.request.get('id'))

		template = JINJA_ENVIRONMENT.get_template('recruiter/profile.html')
		template_values = {'profile': profiles[0], 'positions': positions}

		self.response.write(template.render(template_values))

class RecruiterHomeHandler(BaseSessionHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('recruiter/home.html')
		profiles = BasicProfile.query().order(-BasicProfile.stars).fetch()
		template_values = {"profiles": profiles}
		self.response.write(template.render(template_values))

# Update the number of stars in the profile.
class StarsHandler(BaseSessionHandler):
	def post(self):
		stars = json.loads(self.request.body)
		profiles = BasicProfile.query(BasicProfile.id == stars['id']).fetch()
		profiles[0].stars = int(stars['stars'])
		profiles[0].put()

# Handles requests for profile by id.
# Send GET http://tidy-nomad-842.appspot.com/profileRequest?id=<insert id here>
# to get a JSON string with all of the fields.
class ProfileRequestHandler(BaseSessionHandler):
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
			'profileUrl': profile.profileUrl,
			'stars':      profile.stars
		}, sort_keys=True)
		self.response.write(result)

# Handles requests for profiles by name.
# Send GET http://tidy-nomad-842.appspot.com/nameRequest?<insert name here>
# to get a JSON array containing JSON objects with first name, last name,
# picture, and id.
# Intended for use in autocomplete.
class NameRequestHandler(BaseSessionHandler):
	def get(self):
		prefix = self.request.get('startsWith').lower()
		query = BasicProfile.query().order(BasicProfile.fname)
		profiles = query.fetch(projection=[BasicProfile.fname,
											BasicProfile.lname,
											BasicProfile.pictureUrl,
											BasicProfile.id,
											BasicProfile.stars])
		output = list()
		for profile in profiles:
			# Skip returning a profile if it is unrated and the request only
			# wants rated profiles.
			if self.request.get('rated') == 'true' and profile.stars == 0:
				continue
			fname = profile.fname.lower()
			lname = profile.lname.lower()
			fullname = profile.fname.lower() + " " + profile.lname.lower()
			if fname.startswith(prefix) or lname.startswith(prefix) or fullname.startswith(prefix):
				output.append({
					"fname": profile.fname,
					"lname": profile.lname,
					"id": profile.id,
					"pictureUrl": profile.pictureUrl,
					"stars": profile.stars})

		self.response.write(json.dumps(output, sort_keys=True))

# Handles saving profile annotations.
# POST http://tidy-nomad-842.appspot.com/submitAnnotation
# With JSON body:
# {
#   id:    asdflkj
#   field: (fname|lname|headline|industry|location)
#   image: <the data-uri of the image>
# }
class AnnotationHandler(BaseSessionHandler):
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

class ProfileIdLookupHandler(BaseSessionHandler):
	def get(self):
		self.response.write('<html><body>')
		self.response.write('<h3>Profile IDs</h3>')
		profiles = BasicProfile.query().fetch()
		for profile in profiles:
			self.response.write(profile.fname + " " + profile.lname + ": ")
			self.response.write(profile.id + "<br>")
		self.response.write('</body></html>')

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
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
	('/recruiterLogin', RecruiterLoginHandler),
	('/search', SearchHandler),
	('/profile', ProfileHandler),
	('/home', RecruiterHomeHandler),
	('/setStars', StarsHandler),

	# Profile data request handlers
	('/profileRequest', ProfileRequestHandler),
	('/nameRequest', NameRequestHandler),

	# Handler for submitting an annotations image.
	('/submitAnnotation', AnnotationHandler),

	# Manual data entry for demos
	('/manualPosition', ManualPositionHandler),
	('/profileIdLookup', ProfileIdLookupHandler),

], config=config, debug=True)
