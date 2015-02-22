package hello

import (
	//"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"

	"appengine"
	"appengine/urlfetch"
)

func init() {

	// Handlers for Auctora pitch slides.
	http.HandleFunc("/slides", slidesIndexHandler)
	http.HandleFunc("/slides/", fileHandler)

	http.HandleFunc("/auth/linkedIn", authHandler)

	// Static file handlers
	http.HandleFunc("/css/", fileHandler)
	http.HandleFunc("/js/", fileHandler)
	http.HandleFunc("/fonts/", fileHandler)
	http.HandleFunc("/images/", fileHandler)

	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	landingHtml, err := ioutil.ReadFile("html/LoginPage.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(landingHtml)
}

// Serve the root page for the Auctora slides.
func slidesIndexHandler(w http.ResponseWriter, r *http.Request) {
	slidesHtml, err := ioutil.ReadFile("slides/auctora.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(slidesHtml)
}

// Serve files in the slides/ directory.
func fileHandler(w http.ResponseWriter, r *http.Request) {
	requestedFile := strings.TrimPrefix(r.URL.Path, "/") // Remove the leading slash

	file, err := ioutil.ReadFile(requestedFile)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(file)
}

func authHandler(w http.ResponseWriter, r *http.Request) {
	args := r.URL.Query()
	_, queryErr := args["error"]
	if queryErr {
		// TODO: Send back authentication error to client.
	}

	oauthToken := args["code"][0]
	// state := args["state"][0]

	v := url.Values{}
	v.Set("grant_type", "authorization_code")
	v.Set("code", oauthToken)
	v.Set("redirect_uri", "http://tidy-nomad-842.appspot.com/auth/linkedIn")
	v.Set("client_id", "75kh0yq5sa89ld")

	api_key, api_err := ioutil.ReadFile("API_Key.txt")
	if api_err != nil {
		http.Error(w, api_err.Error(), http.StatusInternalServerError)
		return
	}

	v.Set("client_secret", string(api_key))

	c := appengine.NewContext(r)
	client := urlfetch.Client(c)
	/*resp*/ _, err := client.PostForm("https://www.linkedin.com/uas/oauth2/accessToken", v)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	// fmt.Fprintf(w, "HTTP POST returned status %v", resp.Status)

	file, err := ioutil.ReadFile("html/questions.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
	w.Write(file)
}
