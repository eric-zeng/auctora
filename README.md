# Auctora
*auctōrō, auctōrāre, auctōrāvī* - to hire one's self out for some service

We're trying to improve career fairs by making them less tedious for recruiters and students alike. Auctora is a web app for career fairs that gets rid of paper resumes and provides tools for students and recruiters to automate common tasks.

## Getting started with development
### Setting up the environment
1. Get the code from the repository.
`git clone https://github.com/eric-zeng/auctora.git`
2. Download and install the Google App Engine SDK for Python. https://cloud.google.com/appengine/downloads
3. Install node.js: https://nodejs.org/
4. Once node is installed, install bower by running the command `npm install -g bower`.
5. Download the LinkedIn private API key file from the shared Google Drive (API_Key.txt) and put it in the main auctora directory. (Sorry, key is only available to the Auctora team.)

### Running the application
* There are two ways to run the code - either on the live production server, or a local App Engine server. We want to make sure that whatever is running on the production server is not broken, so if you are just testing your changes, please run a local instance of the server.
* Running local instances
  * Run the command `gcloud preview app run app.yaml` while in the auctora directory.
  * The site will be hosted at `http://localhost:8080/`.
* Deploying to the production server
  * Run the command `gcloud preview app deploy app.yaml` to deploy a new remote instance.
  * To replace the default instance at www.auctora.co, you need to run `gcloud preview app deploy app.yaml --set-default`.
  * To view all running instances, run `gcloud preview app modules list`. This will show the name and version number of each instance.
  * To delete a running instance, run `gcloud preview app modules delete default --version <version number>`.
  * To deploy to the production server, you need access to the App Engine project. Contact the repository owner if you can't deploy but should be able to.

### Updating Assets
Some front-end assets (Bootstrap, jQuery, and Typeahead) can be updated using Bower. To update them to the latest version, run `python scripts/update-assets.py`. This will run `bower install` to fetch the latest version of those packages, and then copy them over to the directory.

If you want to add new packages from Bower, add the package in bower.json, and then modify scripts/update-assets.py so that the new package's files are copied over to the lib folder.

### Helpful resources
* Google App Engine for Python documentation: https://cloud.google.com/appengine/docs/python/
* webapp2 docs: https://webapp-improved.appspot.com/
    - Sessions: https://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
    - Authentication: http://webapp-improved.appspot.com/api/webapp2_extras/auth.html
* WebOb docs (the request/response objects): http://docs.webob.org/en/latest/
* Bootstrap docs: http://getbootstrap.com/getting-started/
* Mozilla Developer Network: https://developer.mozilla.org/en-US/ (general HTML/JS/CSS docs)
