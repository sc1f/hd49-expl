$(document).ready(function(){
	$('hr.mini').hide();
	var w = window.innerWidth;
	if (w < 992){
		$('hr.mini').show();
	} else {
		//do nothing
	}
})