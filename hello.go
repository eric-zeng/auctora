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
	http.HandleFunc("/css/", fileHandler)
	http.HandleFunc("/js/", fileHandler)
	http.HandleFunc("/fonts/", fileHandler)
	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	landingHtml, err := ioutil.ReadFile("bootstrap.html")
	if err != nil {
		fmt.Fprintf(w, "Couldn't read bootstrap.html")
		return
	}
	w.Write(landingHtml)
	//fmt.Fprint(w, "Hello, world!")
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
