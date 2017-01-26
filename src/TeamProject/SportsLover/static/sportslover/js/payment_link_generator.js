// When the document is ready run this code
$( document ).ready(function() {

	// When the button is clicked run this code
	$("#generateLink").click(function(e) {

		// Prevent the form from reloading the page
		e.preventDefault();

		// Define the variables to generate the link
		var recipient = $("#recipient").val(),
			amount = $("#amount").val(),
			note = $("#note").val(),
            payOrrequest = $("#payOrrequest").val(),
			link = "https://venmo.com/?txn=" + payOrrequest + "&recipients="+recipient+"&amount="+amount+"&note="+note;

		// Add the link we generate to the result textarea
		$("#result").val(link);
        window.location.href = link;

	});

});