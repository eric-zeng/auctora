function scrollTo(div) {
	document.getElementById(div).scrollIntoView(true);

	// now account for fixed header
	var scrolledY = window.scrollY;
	if (scrolledY) {
	  window.scroll(0, scrolledY - 50);
	}
}

// Collapse the navbar dropdown if on mobile
$(document).on('click','.navbar-collapse.in',function(e) {
    if( $(e.target).is('a') && $(e.target).attr('class') != 'dropdown-toggle' ) {
        $(this).collapse('hide');
    }
});
