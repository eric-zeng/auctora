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

class RecruiterAttendance(ndb.Model):
	recruiterId = ndb.StringProperty()
	careerFairId = ndb.StringProperty()

class Annotation(ndb.Model):
	recruiterId = ndb.StringProperty()
	profileId = ndb.StringProperty()
	rating = ndb.IntegerProperty()
	comments = ndb.StringProperty()

