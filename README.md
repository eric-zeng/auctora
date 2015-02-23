# Auctora
*auctōrō, auctōrāre, auctōrāvī* - to hire one's self out for some service

We're trying to improve career fairs by making them less tedious for recruiters and students alike. Auctora is a web app for career fairs that gets rid of paper resumes and provides tools for students and recruiters to automate common tasks.

## Getting started with development
### Setting up the environment
1. Get the code from the repository.
`git clone https://github.com/eric-zeng/auctora.git`
2. Download and install the Google App Engine SDK for Go. https://cloud.google.com/appengine/downloads
3. Download the LinkedIn private API key file from the shared Google Drive (API_Key.txt) and put it in the main auctora directory. (Sorry, key is only available to the Auctora team.)

### Running the application
* There are two ways to run the code - either on the live production server, or a local App Engine server. We want to make sure that whatever is running on the production server is not broken, so if you are just testing your changes, please run a local instance of the server.
* Running local instances
  * Type in the command `goapp serve <auctora directory>`. <auctora directory> should be the folder that contains our app.yaml file.
  * The site will be hosted at `http://localhost:8080/`.
* Deploying to the production server
  * Run the command `goapp deploy <auctora directory>`. BE CAREFUL! Don't deploy bad code!

### Helpful resources
* Go resources
  * Go tutorial: http://tour.golang.org/welcome/1
  * Effective Go: http://golang.org/doc/effective_go.html (a good reference once you've picked up the basics)
  * Google App Engine for Go documentation: https://cloud.google.com/appengine/docs/go/
* Bootstrap docs: http://getbootstrap.com/getting-started/
* Mozilla Developer Network: https://developer.mozilla.org/en-US/ (general HTML/JS/CSS docs)
