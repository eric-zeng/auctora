window.onload = function() {
  document.getElementById("selectStudent").onclick = selectStudent;

  var xmlhttp = new XMLHttpRequest();
  var url = getUrl("nameRequest");
  xmlhttp.open("GET", url, true);
  xmlhttp.responseType = "JSON";
  xmlhttp.onload = function(e) {
    var arr = JSON.parse(xmlhttp.response);
    var students = document.getElementById("students");

    for (var i = 0; i < arr.length; i++) {
      for (var key in arr) {
        var node = document.createElement("option");
        node.value = arr[key]["fname"] + " " + arr[key]["lname"];
        node.id = arr[key]["id"];
        students.appendChild(node);
      }
    }
  }
  xmlhttp.send();

  function selectStudent() {
    var students = document.getElementById("students");
    var input = document.getElementById("input");
    var id;
    for (var i = 0; students.options.length; i++) {
      if (students.options[i].value == input.value) {
        id = students.options[i].id;
        break;
      }
    }

    url = getUrl("profile");
    url += "?id=" + id;
    window.location = url;
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

function navToList() {
  document.location.href = "/candidateList"
}
