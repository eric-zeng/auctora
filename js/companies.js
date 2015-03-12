// Hardcoded company preference data.
var companyToGPA = [
    {
        "name": "amazon",
        "minGPA": 3.3,
        "visa": true,
        "fulltime": true,
        "internship": true,
        "freshmen": false,
        "sophomores": true,
        "juniors": true,
        "senior": true
     },
    {
        "name": "cisco",
        "minGPA": 3,
        "visa": false,
        "fulltime": true,
        "internship": false,
        "freshmen": false,
        "sophomores": false,
        "juniors": true,
        "senior": true
    },
    {
        "name": "dropbox",
        "minGPA": 3.8,
        "visa": true,
        "fulltime": true,
        "internship": false,
        "freshmen": false,
        "sophomores": true,
        "juniors": true,
        "senior": true
    },
    {
        "name": "facebook",
        "minGPA": 3.6,
        "visa": true,
        "fulltime": true,
        "internship": true,
        "freshmen": true,
        "sophomores": true,
        "juniors": true,
        "senior": true
    },
    {
        "name": "microsoft",
        "minGPA": 3.5,
        "visa": true,
        "fulltime": true,
        "internship": true,
        "freshmen": true,
        "sophomores": true,
        "juniors": true,
        "senior": true
    }
];

function customAlert(msg,duration) {
    var styler = document.createElement("div");
    styler.setAttribute("style","width:auto; height:auto; background-color: lightgreen; color: #353a43; position: absolute; top: 0%; left: 30%");
    styler.innerHTML = "<h3>"+msg+"</h3>";
    setTimeout(function() { styler.parentNode.removeChild(styler);},duration);
    document.getElementById("header").appendChild(styler);
}

function caller() {
    customAlert("Successfully uploaded resume","1500");
}

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}

function getUrlVars(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
        console.log(hash[0] + " " + hash[1]);
    }
    return vars;
}

function setBackgrounds () {
    var urlParams = getUrlVars();
    for (var i = companyToGPA.length - 1; i >= 0; i--) {
        var isValid = true;
        console.log(companyToGPA[i]);
        if(companyToGPA[i].minGPA > urlParams["gpa"]){
            isValid = false;
            document.getElementById(companyToGPA[i].name + "Info").innerHTML =
                "We only accept students with GPA >= " + companyToGPA[i].minGPA + "\n";
            document.getElementById(companyToGPA[i].name + "Info").innerHTML;
        }

        if(!companyToGPA[i].visa && urlParams["checkbox1"] == "on") {
            isValid = false;
            document.getElementById(companyToGPA[i].name + "Info").innerHTML =
                "Sorry, we do not sponsor international student visas";
            // company does not sponsor visa and student is international
        }

        if(urlParams["lookingfor"] == "internship" && !companyToGPA[i].internship){
            isValid = false;
            document.getElementById(companyToGPA[i].name + "Info").innerHTML =
                "Sorry, we are not looking for interns";
        }

        if(urlParams["lookingfor"] == "fulltime" && !companyToGPA[i].fulltime){
            document.getElementById(companyToGPA[i].name + "Info").innerHTML =
                "Sorry, we aren't looking for fulltime students";
            isValid = false;
        }

        var educationLevel = urlParams["grade"];
        if(!companyToGPA[i][educationLevel]){
            var grade = ""
            if (urlParams["grade"] == "freshman") {
                grade = "freshmen"
            } else {
                grade = urlParams["grade"] + "s"
            }
            document.getElementById(companyToGPA[i].name + "Info").innerHTML =
                "Sorry, we aren't looking for " + grade;
            isValid = false;
        }

        if(!isValid){
            document.getElementById(companyToGPA[i].name).style.backgroundColor = "#FFCCCC";
        }
    };
}

window.onload = function() {
    caller();
    setBackgrounds();
    document.getElementById("amazon").onclick = displayInfo;
    document.getElementById("cisco").onclick = displayInfo;
    document.getElementById("dropbox").onclick = displayInfo;
    document.getElementById("facebook").onclick = displayInfo;
    document.getElementById("microsoft").onclick = displayInfo;

    function displayInfo() {
        console.log(this.id);
        var curElement = document.getElementById(this.id +"Info");
        var result = $("#"+ this.id + "Info").css('height');
        result = result.substring(0, 3);

        // element is not visible
        if(curElement.style.display == "none") {
            curElement.style.display = "block";
            if(this.id == "microsoft") {
                var y = $(window).scrollTop();  // your current y position on the page
                var result = $("#microsoftInfo").css('height');
                result = result.substring(0, 3);
                var answer = (y * 1.0 + (1.0) * result) * 1.0;
                $("html, body").animate({scrollTop: answer}, '200', "swing");
            } else if (this.id == "cisco") {
                //curElement.style.display = "none";
            }
        } else {
            if(this.id == "microsoft") {
                var y = $(window).scrollTop();  // your current y position on the page
                var result = $("#microsoftInfo").css('height');
                result = result.substring(0, 3);
                $("html, body").animate({scrollTop: y-result}, '200', "swing");
            } else if (this.id == "cisco") {
                if(curElement.style.display == "block") {
                    curElement.style.display = "none";
                }
            }
            curElement.style.display = "none";
        }
    }
}
