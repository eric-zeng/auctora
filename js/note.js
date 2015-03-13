"use strict";

var signaturePad;
var lastClick = null;
var noteMap = {};

function enableAnnotation() {
  addIds();
  initializeAnnotationPane();
  $("h1, h2, h3, h4, h5, h6, p").each(addTriggersTo);
}

function addIds() {
  var counter = 0;
  $("h1, h2, h3, h4, h5, h6, p").each(function() {
    $(this).attr("id", $(this).prop("tagName") + "_" + counter);
    counter++;
  })
}

function initializeAnnotationPane() {
  var canvas = document.querySelector("canvas");
  signaturePad = new SignaturePad(canvas);
  document.getElementById("canvasParent").style.display="none";
  document.getElementById("canvasParent").style.position="fixed";
  document.getElementById("canvasClear").addEventListener("click", function() {
    signaturePad.clear();
  });
}

function addTriggersTo() {
  $(this).toggleClass("noNote");
  $(this).click(function() {
    displayCanvas( this )
  });
}

function displayCanvas(element) {
  var cPar = document.getElementById("canvasParent");
  if( !element.classList.contains("active") ) {
    $(element).toggleClass("active");
    signaturePad.clear();
    if( lastClick != element ) {
      $(lastClick).removeClass("active"); 
    }
    var noNote = element.classList.contains("noNote");
    
    var cCan = document.getElementById("canvasCancel");
    var cDon = document.getElementById("canvasDone");
    cPar.style.display="block";
    if( noNote ) {
      cCan.addEventListener("click", function() {
        // don't modify classList of element
        $(element).toggleClass("active");
        cPar.style.display="none";
        deaf();
      });
      cDon.addEventListener("click", function() {
        if( !signaturePad.isEmpty() ) {
          // modify classList
          $(element).toggleClass("noNote");
          $(element).toggleClass("annotated");

          // save the annotation
          noteMap[$(element).attr('id')] = signaturePad.toDataURL();
        }
        $(element).toggleClass("active");
        cPar.style.display="none";
        deaf();
      });
    } else {
      signaturePad.fromDataURL(noteMap[$(element).attr("id")]);

      cCan.addEventListener("click", function() {
        $(element).toggleClass("active");
        cPar.style.display="none";
        signaturePad.clear();
        deaf();
      });
      cDon.addEventListener("click", function() {
        if( !signaturePad.isEmpty() ) {
          // save the annotation
          noteMap[$(element).attr('id')] = signaturePad.toDataURL();
        } else {       
          // modify classList
          $(element).toggleClass("noNote");
          $(element).toggleClass("annotated");

          // delete stored annotation
          noteMap[$(element).attr('id')] = null;
        }
        $(element).toggleClass("active");
        cPar.style.display="none";
        deaf();
      });
    }
    lastClick = element;
  } else {
    cPar.style.display="none";
    setTimeout( function() { cPar.style.display="block" }, 50 );
  }
}

function deaf() {
  var cancel = document.getElementById("canvasCancel");
    var cancelClone = cancel.cloneNode(true);
  cancel.parentNode.replaceChild(cancelClone, cancel);
  var done = document.getElementById("canvasDone");
    var doneClone = done.cloneNode(true);
  done.parentNode.replaceChild(doneClone, done);     
}