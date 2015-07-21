import logging
import json
import uuid

from google.appengine.ext import ndb

from webapp2_extras import sessions

from common import BaseHandler
from common import JINJA_ENVIRONMENT
from models import Recruiter
from models import BasicProfile

def RedirectRecruiterToHomeIfLoggedIn(session, response):
	if 'id' not in session:
		return False
	if len(Recruiter.query(Recruiter.id == session['id']).fetch()) == 1:
		response.location = "/home"
		response.status = 302
		return True
	return False

class RecruiterLoginHandler(BaseHandler):
	def get(self):
		if RedirectRecruiterToHomeIfLoggedIn(self.session, self.response):
			return
		template = JINJA_ENVIRONMENT.get_template('recruiter/recruiterLogin.html')
		self.response.write(template.render())

	def post(self):
		logging.info(self.request.body)

class RecruiterRegistrationHandler(BaseHandler):
	def get(self):
		if RedirectRecruiterToHomeIfLoggedIn(self.session, self.response):
			return
		template = JINJA_ENVIRONMENT.get_template('recruiter/recruiterRegistration.html')
		self.response.write(template.render())

	def post(self):
		logging.info(self.request.body)
		data = json.loads(self.request.body)
		# Parse the JSON form data representation into a dict
		formData = dict()
		for obj in data:
			logging.info(obj['name'])
			logging.info(obj['value'])

			formData[obj['name']] = obj['value']
		# Generate unique ID for the recruiter, try until unique id found
		while True:
			id = uuid.uuid4().hex
			existing = Recruiter.query(Recruiter.id == id).fetch()
			if len(existing) == 0:
				break
			logging.info('ID ' + id + ' already exists, trying again')

		pwhash = security.generate_password_hash(formData['password'])

		recruiter = Recruiter()
		recruiter.id = id
		recruiter.fname = formData['fname']
		recruiter.lname = formData['lname']
		recruiter.passwordHash = pwhash
		recruiter.put()

		self.session['userType'] = "recruiter"
		self.session['id'] = id

		self.response.write('{"redirect": "/home"}')

class SearchHandler(BaseHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('recruiter/search.html')
		self.response.write(template.render())

class ProfileHandler(BaseHandler):
	def get(self):
		profiles = BasicProfile.query(BasicProfile.id == self.request.get('id')).fetch()
		if len(profiles) == 0:
			self.response.write('<html><body>Could not find profile ' + \
								self.request.get('id') + '</body></html>')

		positions = Position.query(Position.profileId == self.request.get('id'))

		template = JINJA_ENVIRONMENT.get_template('recruiter/profile.html')
		template_values = {'profile': profiles[0], 'positions': positions}

		self.response.write(template.render(template_values))

class RecruiterHomeHandler(BaseHandler):
	def get(self):
		if 'id' not in self.session:
			self.response.status = 401
			self.response.write("<html><body><h1>401 Unauthorized</h1></body></html>")
			return

		sessionUserId = self.session['id']
		if len(Recruiter.query(Recruiter.id == sessionUserId).fetch()) != 1:
			self.response.write("<html><body><h1>No recruiter with id " + sessionUserId + "found!</h1></body></html>")
			return

		template = JINJA_ENVIRONMENT.get_template('recruiter/home.html')
		profiles = BasicProfile.query().order(-BasicProfile.stars).fetch()
		template_values = {"profiles": profiles}
		self.response.write(template.render(template_values))

# Update the number of stars in the profile.
class StarsHandler(BaseHandler):
	def post(self):
		stars = json.loads(self.request.body)
		profiles = BasicProfile.query(BasicProfile.id == stars['id']).fetch()
		profiles[0].stars = int(stars['stars'])
		profiles[0].put()

# Handles requests for profile by id.
# Send GET http://tidy-nomad-842.appspot.com/profileRequest?id=<insert id here>
# to get a JSON string with all of the fields.
class ProfileRequestHandler(BaseHandler):
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
class NameRequestHandler(BaseHandler):
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
class AnnotationHandler(BaseHandler):
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
