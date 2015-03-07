window.onload = function() {
  document.getElementById("star1").onclick = selectStars;
  document.getElementById("star2").onclick = selectStars;
  document.getElementById("star3").onclick = selectStars;
  document.getElementById("star4").onclick = selectStars;
  document.getElementById("star5").onclick = selectStars;
  document.getElementById("submit").onclick = doneRequest;

  function doneRequest() {
    var url = getUrl("studentSearch");
    window.location = url;
  }


  function selectStars() {
    var numStars = this.value;
    var xmlhttp = new XMLHttpRequest();
    var url = getUrl("setStars");
    var id = document.URL.split("=")[1];
    var params = { id:id, stars:numStars };
    xmlhttp.open("POST", url, true);
    xmlhttp.send(JSON.stringify(params));
  }

  function getUrl(nextPage) {
    var url = window.location.protocol + "//" + window.location.hostname;
    if (window.location.hostname == "localhost") {
      url += ":" + window.location.port;
    }
    url += "/" + nextPage;
    return url;
  }
} 