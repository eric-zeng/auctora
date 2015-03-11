"use strict";

/*
Bryan Djunaedi
March 7, 2015
*/

// module-global format
(function() {						// anonymous function for window load event
	window.addEventListener("load", function() {
		var canvas = document.querySelector("canvas");
   		var signaturePad = new SignaturePad(canvas);
   		document.getElementById("canvasParent").style.display="inline-block";
		document.getElementById("canvasClear").addEventListener("click", function() { submitAnnotation(signaturePad); });
	});

	// for submitting the annotation
	function submitAnnotation(signaturePad) {
		signaturePad.clear();
	}
})();