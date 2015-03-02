window.onload = function() {
    document.getElementById("prevButton").addEventListener("click", function() {
      prevSlide();
    });

    document.getElementById("nextButton").addEventListener("click", function() {
      nextSlide();
    });

    nextSlide();
}

function keyEvent(event) {
    if (event.keyCode == 37) {
        prevSlide();
    } else if (event.keyCode == 39) {
        nextSlide();
    }
}

function nextSlide() {
  var current = document.getElementById("current");
  var prev = document.getElementById("previous");
  var next = document.getElementById("next");

  var n = next.firstChild;
  while (n.nodeType !== 1) {
    n = n.nextSibling;
  }

  if (n != null) {
    if (current.firstChild != null) {
      var oldSlide = current.removeChild(current.firstChild);
      prev.insertBefore(oldSlide, prev.firstChild);
    }
    var newSlide = next.removeChild(n);
    current.appendChild(newSlide);
  }
}

function prevSlide() {
  var current = document.getElementById("current");
  var prev = document.getElementById("previous");
  var next = document.getElementById("next");

  var p = prev.firstChild;
  while (p.nodeType !== 1) {
    p = p.nextSibling;
  }

  if (p != null) {
    if (current.firstChild != null) {
      var oldSlide = current.removeChild(current.firstChild);
      next.insertBefore(oldSlide, next.firstChild);
    }
    var newSlide = prev.removeChild(p);
    current.appendChild(newSlide);
  }
}
