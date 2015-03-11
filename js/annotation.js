"use strict";

alert("loaded");

function enableAnnotation() {
  alert("called");
  initializeAnnotationPane();
  $("h1, h2, h3, h4, h5, h6, p").each(addTriggersTo);
  document.getElementById("canvasDone").addEventListener("click", submitAnnotation);
  
  function addTriggersTo() {
    $(this).toggleClass("noNote");
    $(this).click(function() {
      if( this.classList.contains("annotated")) {
        //document.getElementById(this.id + "#").style.display("inline-block");
      } else {
        //alert("you clicked " + $(this).prop("tagName"));
        var noted = displayCanvas();
        if( noted ) {
          $(this).toggleClass("noNote");
          $(this).toggleClass("annotated");
        }

      }
    });

  }

  function initializeAnnotationPane() {
    var canvas = document.querySelector("canvas");
    var signaturePad = new SignaturePad(canvas);
    document.getElementById("canvasParent").style.display="none";
    document.getElementById("canvasParent").style.position="fixed";

    document.getElementById("canvasClear").addEventListener("click", function() {
      signaturePad.clear(); 
    });

    document.getElementById("canvasCancel").addEventListener("click", function() {
      document.getElementById("canvasParent").style.display="none";
    });

    document.
  }

  function submitAnnotation() {
    document.getElementById("canvasParent").style.display="none";
  }

  function displayCanvas() {
    document.getElementById("canvasParent").style.display="block";
    return true;
  }
}