"use strict";

window.onload = function() {
  document.getElementById("star1").addEventListener("click", selectStars);
  document.getElementById("star2").addEventListener("click", selectStars);
  document.getElementById("star3").addEventListener("click", selectStars);
  document.getElementById("star4").addEventListener("click", selectStars);
  document.getElementById("star5").addEventListener("click", selectStars);
  document.getElementById("submit").addEventListener("click", doneRequest);
  document.getElementById("canvasParent").style.display="none";
  $("h1, h2, h3, h4, h5, h6, p").each(addTriggersTo);
  $("#canvas").jSignature()
  document.getElementById("canvasDone").addEventListener("click", submitAnnotation);
  
  function addTriggersTo() {
    $(this).click(function() {
      if( this.classList.contains("annotated")) {
        //document.getElementById(this.id + "#").style.display("inline-block");
      } else {
        //alert("you clicked " + $(this).prop("tagName"));
        var noted = displayCanvas();
        if( noted ) {
          $(this).toggleClass("annotated");
          $(this).hover(changeHighlight, changeHighlight);
        }

      }
    });

  }

  function submitAnnotation() {
    document.getElementById("canvasParent").style.display="none";
  }

  function displayCanvas() {
    document.getElementById("canvasParent").style.display="block";
    return true;
  }

  function changeHighlight() {
    $(this).toggleClass("active");
  }

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
    var url = getUrl("candidateList");
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
