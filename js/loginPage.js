window.onload = function() {
     document.getElementById("signIn").onclick = signIn;

    // Send users to the LinkedIn login page.
    function signIn() {
        var client_id = "75kh0yq5sa89ld";

        // Redirect URI can either be our app engine domain or localhost:8080.
        // Need special cases to accomodate both.
        var redirect_uri = window.location.protocol +  "//" +
        window.location.hostname;
        if (window.location.hostname == "localhost") {
          redirect_uri = redirect_uri + ":" + window.location.port;
        }
        redirect_uri += "/auth/linkedIn";

        var state = "ALS12sdij12989IDJSA0923u";
        var scope = "r_basicprofile";

        auth_url = "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id="
            + client_id + "&redirect_uri=" + encodeURIComponent(redirect_uri) +
            "&state=" + state + "&scope=" + scope;
        window.location = auth_url;
    }
}
