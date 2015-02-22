package hello

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
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

	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	landingHtml, err := ioutil.ReadFile("LoginPage.html")
	if err != nil {
		fmt.Fprintf(w, "Couldn't read LoginPage.html")
		return
	}
	w.Write(landingHtml)
}

// Serve the root page for the Auctora slides.
func slidesIndexHandler(w http.ResponseWriter, r *http.Request) {
	slidesHtml, err := ioutil.ReadFile("slides/auctora.html")
	if err != nil {
		fmt.Fprintf(w, "Couldn't read slides/auctora.html")
		return
	}
	w.Write(slidesHtml)
}

// Serve files in the slides/ directory.
func fileHandler(w http.ResponseWriter, r *http.Request) {
	requestedFile := strings.TrimPrefix(r.URL.Path, "/") // Remove the leading slash

	file, err := ioutil.ReadFile(requestedFile)
	if err != nil {
		fmt.Fprintf(w, "Couldn't read %s", requestedFile)
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

	oauthToken := args["code"]
	state := args["state"]

	fmt.Fprintf(w, "OAuth token: %s, State: %s", oauthToken, state)

	// TODO: Finish LinkedIn oauth steps.

	// TODO: serve the questions page
	// file, err := ioutil.ReadFile("questions.html")
	// if err != nil {
	// 	fmt.Fprintf(w, "Couldn't read questions.html")
	// }
	// w.Write(file)
}
