from google.appengine.ext import ndb

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
