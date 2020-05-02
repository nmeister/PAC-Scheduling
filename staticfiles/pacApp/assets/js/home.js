function homeDisableSchdFootHead() {
	// checks location path and checks if we are on home page
	// if we are on home page, we want to disable the header and footers 
	var place = String(window.location.pathname);
	 if (place == "/" || place == "/homepage" || place != "/schedule") {
	 	console.log('Currently on home page, disable footer + header from schedule');
	 	$('#headerschedule').css('display','none');
	 	$('#footerschedule').css('display','none');
	 }

}