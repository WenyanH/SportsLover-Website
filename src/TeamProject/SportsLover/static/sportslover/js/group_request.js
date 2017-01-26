window.onbeforeunload=function() {
	window.opener.location.reload();
}