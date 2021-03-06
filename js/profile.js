"use strict";

window.onload = function() {
  document.getElementById("star1").addEventListener("click", selectStars);
  document.getElementById("star2").addEventListener("click", selectStars);
  document.getElementById("star3").addEventListener("click", selectStars);
  document.getElementById("star4").addEventListener("click", selectStars);
  document.getElementById("star5").addEventListener("click", selectStars);
  document.getElementById("submit").addEventListener("click", doneRequest);
  enableAnnotation(); //calls from annotation.js

  // Gets the numberof stars selected and sends it to the backend.
  function selectStars() {
    var numStars = this.value;
    var xmlhttp = new XMLHttpRequest();
    var url = getUrl("setStars");
    var id = document.URL.split("=")[1];
    var params = { id:id, stars:numStars };
    xmlhttp.open("POST", url, true);
    xmlhttp.send(JSON.stringify(params));
  }

  // Changes page to the candidate search page.
  function doneRequest() {
    var url = getUrl("home");
    window.location = url;
  }

  // Helper function to determine if we're running on localhost or the
  // production web server
  function getUrl(nextPage) {
    var url = window.location.protocol + "//" + window.location.hostname;
    if (window.location.hostname == "localhost") {
      url += ":" + window.location.port;
    }
    url += "/" + nextPage;
    return url;
  }
}
