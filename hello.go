package hello

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"

	"appengine"
	"appengine/datastore"
	"appengine/urlfetch"
	"appengine/user"
)

type Candidate struct {
	Id          string
	AccessToken string
	ExpiresIn   float64
}

func init() {
	// Handlers for Auctora pitch slides.
	http.HandleFunc("/slides", slidesLandingHandler)
	http.HandleFunc("/slides/", fileHandler)

	// LinkedIn authentication handler.
	http.HandleFunc("/auth/linkedIn", authHandler)

	// Static file handlers
	http.HandleFunc("/css/", fileHandler)
	http.HandleFunc("/js/", fileHandler)
	http.HandleFunc("/fonts/", fileHandler)
	http.HandleFunc("/images/", fileHandler)
	http.HandleFunc("/html/", fileHandler)

	// Form handler
	http.HandleFunc("html/companies", formHandler)

	// Root path handler.
	http.HandleFunc("/", landingHandler)
}

// Handler for URL with no path (just tidy-nomad842.appspot.com). Shows the
// Auctora login page.
func landingHandler(w http.ResponseWriter, r *http.Request) {
	landingHtml, err := ioutil.ReadFile("html/LoginPage.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(landingHtml)
}

// Serve the root page for the Auctora slides.
func slidesLandingHandler(w http.ResponseWriter, r *http.Request) {
	slidesHtml, err := ioutil.ReadFile("slides/auctora.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(slidesHtml)
}

// Serve any file referenced with an explicit path in the URL.
func fileHandler(w http.ResponseWriter, r *http.Request) {
	// Remove the leading slash
	requestedFile := strings.TrimPrefix(r.URL.Path, "/")

	file, err := ioutil.ReadFile(requestedFile)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(file)
}

// Handler for LinkedIn Authentication. At this point, the user has signed in
// with LinkedIn, and the browser redirected them to /auth/linkedIn.
// We need to exchange the authorization code for an access token for the user.
func authHandler(w http.ResponseWriter, r *http.Request) {
	args := r.URL.Query()

	// If "error" was in the URL query, then something went wrong.
	_, queryErr := args["error"]
	if queryErr {
		// TODO: Send back authentication error to client.
	}

	authCode := args["code"][0]
	// state := args["state"][0] // TODO: use value to to test for CSRF attacks.

	c := appengine.NewContext(r)

	// Form the POST request to get a Request Token from LinkedIn.
	v := url.Values{}
	v.Set("grant_type", "authorization_code")
	v.Set("code", authCode)

	// If we are running a local instance of the server, the port needs to be
	// included in the redirect URI.
	port := ""
	if appengine.DefaultVersionHostname(c) == "localhost" {
		port = ":8080"
	}

	url := fmt.Sprintf("http://%s%s/auth/linkedIn", appengine.DefaultVersionHostname(c), port)
	v.Set("redirect_uri", url)
	v.Set("client_id", "75kh0yq5sa89ld")

	// We can't hardcode our private API key, it's kept in a file separate from
	// the git repository. Read the file in to get it.
	api_key, api_err := ioutil.ReadFile("API_Key.txt")
	if api_err != nil {
		http.Error(w, api_err.Error(), http.StatusInternalServerError)
		return
	}
	v.Set("client_secret", string(api_key))

	// Send the POST request to the server.
	client := urlfetch.Client(c)
	/*resp*/ _, err := client.PostForm("https://www.linkedin.com/uas/oauth2/accessToken", v)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// TODO: parse the response to get the access token and store it in the
	// student database.

	// Serve the next page in the student flow.
	file, err := ioutil.ReadFile("html/redirect.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
	w.Write(file)
}

func formHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	year := r.PostFormValue("grade")
	gpa  := r.PostFormValue("gpa")
	//intl := r.PostFormValue("intl")
	goal := r.PostFormValue("lookingfor")

	/*fairHtml, err := ioutil.ReadFile("html/companies.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return		
	}
	w.Write(fairHtml)*/

	fmt.Fprintf(w, "I am a %s with a %s looking for a %s.", year, gpa, goal)
}

// Inserts a candidate into the datastore. Returns any errors that occurred.
func addCandidate(linkedInId string, accessToken string, tokenExpiration float64, c appengine.Context) error {
	candidate := Candidate{linkedInId, accessToken, tokenExpiration}
	key := datastore.NewIncompleteKey(c, "Candidate", nil)
	_, err := datastore.Put(c, key, &candidate)
	return err
}

// Updates a candidate in the datastore.
func updateCandidate(linkedInId string, accessToken string, tokenExpiration float64) {
	
}
