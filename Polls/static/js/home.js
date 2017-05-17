$( document ).ready(function(){
	$(".button-collapse").sideNav();
});

$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    min: true
});
$('.timepicker').pickatime({
    default: 'now',
    twelvehour: true, // change to 12 hour AM/PM clock from 24 hour
    donetext: 'OK',
	autoclose: false,
	vibrate: true // vibrate the device when dragging clock hand
});