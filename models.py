import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb

# Copied from a blog. This extends the default webapp2 User class so that
# it supports changing passwords.
class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    """Sets the password for the current user

    :param raw_password:
        The raw password which will be hashed and stored
    """
    self.password = security.generate_password_hash(raw_password, length=12)

  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    """Returns a user object based on a user ID and token.

    :param user_id:
        The user_id of the requesting user.
    :param token:
        The token string to be verified.
    :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
    """
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    # Use get_multi() to save a RPC call.
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
        timestamp = int(time.mktime(valid_token.created.timetuple()))
        return user, timestamp

    return None, None


class Candidate(ndb.Model):
	id = ndb.StringProperty()
	fname = ndb.StringProperty()
	lname = ndb.StringProperty()
	profilePicUrl = ndb.StringProperty()
	activeProfileId = ndb.StringProperty()

class Profile(ndb.Model):
	id = ndb.StringProperty()
	careerFairId = ndb.StringProperty()
	candidateId = ndb.StringProperty()
	resume = ndb.StringProperty()   # URL of resume stored in blobstore
	askAbout = ndb.StringProperty() # JSON array of strings
	school = ndb.StringProperty()
	degree = ndb.StringProperty()
	lookingFor = ndb.StringProperty()

class CareerFair(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty()
	startTime = ndb.DateTimeProperty()
	endTime = ndb.DateTimeProperty()

class Recruiter(ndb.Model):
	id = ndb.StringProperty()
	fname = ndb.StringProperty()
	lname = ndb.StringProperty()
	email = ndb.StringProperty()
	passwordHash = ndb.StringProperty()

class RecruiterAttendance(ndb.Model):
	recruiterId = ndb.StringProperty()
	careerFairId = ndb.StringProperty()

class Annotation(ndb.Model):
	recruiterId = ndb.StringProperty()
	profileId = ndb.StringProperty()
	rating = ndb.IntegerProperty()
	comments = ndb.StringProperty()

# Old model classes that should be deprecated!
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
