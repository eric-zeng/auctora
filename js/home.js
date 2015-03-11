

function getUrl(nextPage) {
    var url = window.location.protocol + "//" + window.location.hostname;
    if (window.location.hostname == "localhost") {
        url += ":" + window.location.port;
    }
    url += "/" + nextPage;
    return url;
}

var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substrRegex;

    // an array that will be populated with substring matches
    matches = [];

    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');

    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push({ value: str });
      }
    });

    cb(matches);
  };
};

$(document).ready(function() {
    var nameToId = {}

    $('.typeahead').typeahead('val');

    var xmlhttp = new XMLHttpRequest();
    var url = getUrl("nameRequest");
    xmlhttp.open("GET", url, true);
    xmlhttp.responseType = "JSON";
    xmlhttp.onload = function(e) {
        var arr = JSON.parse(xmlhttp.response);

        for (var i = 0; i < arr.length; i++) {
            for (var key in arr) {
                nameToId[arr[key]["fname"] + " " + arr[key]["lname"]] = arr[key]["id"];
            }
        }

        $('.typeahead.input-sm').siblings('input.tt-hint').addClass('hint-small');
        $('.typeahead.input-lg').siblings('input.tt-hint').addClass('hint-large');

        $('#searchbox .typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'names',
            displayKey: 'value',
            source: substringMatcher(Object.keys(nameToId))
        }).bind("typeahead:selected", function(obj, datum, name) {
            var id = nameToId[datum['value']];
            document.location.href = "/profile?id=" + id
        });
    }
    xmlhttp.send();

});

function navToSearch() {
    document.location.href = "/search"
}
