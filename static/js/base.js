
/* ### PERSONA LOGIN CODE ### */

var user_email = null;
var login_clicked = false;

$(document).ready(function() {
	user_email = document.getElementById("user-email").value;
	var signinLink = document.getElementById('login');
	if (signinLink) {
		signinLink.onclick = function() { 
			login_clicked = true;
			navigator.id.request();
		};
	}
});

navigator.id.watch({
	loggedInUser: user_email,
	onlogin: function(assertion) {
		// A user has logged in! Here you need to:
		// 1. Send the assertion to your backend for verification and to create a session.
		// 2. Update your UI.
		if (login_clicked == true) {
			if  (assertion) {
				window.location = '/login/'+assertion
			} else {
				alert("Assertion not received! Sorry! Try logging in again?");
			}
		}
	},
	onlogout: function() {
		// A user has logged out! Here you need to:
		// Tear down the user's session by redirecting the user or making a call to your backend.
		// Also, make that loggedInUser will get set to null on the next page load.
		// (That's a literal JavaScript null. Not false, 0, or undefined. null.)
		$.ajax({
			type: 'POST',
			url: '/auth/logout', // This is a URL on your website.
			success: function(res, status, xhr) { window.location.reload(); },
			error: function(res, status, xhr) { alert("logout failure" + res); }
		});
	}
});


// ------------------------------------------------------------------------------------------------

/* ### MAKE SURE PRICE IS ALWAYS A NUMBER ### */
function isNumberKey(evt)
       {
          var charCode = (evt.which) ? evt.which : event.keyCode;
          if (charCode != 46 && charCode > 31 
            && (charCode < 48 || charCode > 57))
             return false;

          return true;
       }

/* ### FORM VALIDATION ### */
function notEmpty(elem){
	if(elem.value.length == 0){
		event.preventDefault();
		elem.focus(); // set the focus to this input
		$(elem).parent().parent().addClass("error");
		return false;
	}
	return true;
}

$(document).ready(function() {
	var validateElems = $(".validate");
	$("#submit").click(function(event) {
    	for (var i=0; i<validateElems.length; i++) {
			notEmpty(validateElems[i]);
		}
  	});
});