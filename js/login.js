"use strict";

// this functionality may actually already be built in to app engine
(function() {						// anonymous function for window load event
	window.addEventListener("load", function() {
		
	});

	function set_cookie(username, valid_domain) {
	  var domain_string = valid_domain ? ("; domain=" + valid_domain) : '' ;
	  document.cookie = "username=" + username + "; path=/" + domain_string;
	}
})();