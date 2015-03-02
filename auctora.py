import os
import urllib
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

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
		logging.info("" + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('html/LoginPage.html')
		self.response.write(template.render())

# serve the root page for the Auctora slides
class SlidesLandingHandler(webapp2.RequestHandler):
	def get(self):
		requestedFile = self.request.url[1:]
		logging.info("" + requestedFile)
		template = JINJA_ENVIRONMENT.get_template('html/slides.html')
		self.response.write(template.render())

class LinkedInAuthHandler(webapp2.RequestHandler):
	def get(self):
		error = self.request.get("error", "no error")
		if error != "no error":
			self.response.write("<html><body>Authentication Error</body></html>")

		authCode = self.request.get("code")
		state = self.request.get("state")

		self.response.write("<html><body>Authentication code: " + authCode + "\nState: " + state + " </body></html>")


application = webapp2.WSGIApplication([
	# root path handler
	('/', LandingHandler),

	# auctora pitch slides handlers
	('/slides', SlidesLandingHandler),

	# LinkedIn auth handler
	('/auth/linkedIn', LinkedInAuthHandler),

], debug=True)
