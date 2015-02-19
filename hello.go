package hello

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

func init() {
	http.HandleFunc("/", handler)

	// Handlers for Auctora pitch slides.
	http.HandleFunc("/slides", slidesIndexHandler)
	http.HandleFunc("/slides/", slidesHandler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello, world!")
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
func slidesHandler(w http.ResponseWriter, r *http.Request) {
	requestedFile := strings.TrimPrefix(r.URL.Path, "/") // Remove the leading slash

	file, err := ioutil.ReadFile(requestedFile)
	if err != nil {
		fmt.Fprintf(w, "Couldn't read %s", requestedFile)
		return
	}
	w.Write(file)
}
