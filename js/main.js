function scrollTo(div) {
	document.getElementById(div).scrollIntoView(true);

	// now account for fixed header
	var scrolledY = window.scrollY;
	if (scrolledY) {
	  window.scroll(0, scrolledY - 50);
	}

	document.getElementById('navbarToggle').click();
}
