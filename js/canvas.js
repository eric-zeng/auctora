"use strict";

/*
Bryan Djunaedi
March 7, 2015
*/

// module-global format
(function() {						// anonymous function for window load event
	window.addEventListener("load", function() {
		$("#signature").jSignature()
		$("#done").onclick(submitAnnotation);
	});

	// for submitting the annotation
	function submitAnnotation() {
		$("#signature").jSignature("reset") // clears the canvas and rerenders the decor on it.
	}
})();