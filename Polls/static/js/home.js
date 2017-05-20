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

function blurFunction () {
	var choices_space = document.getElementById("choices_space");
	var list_items = choices_space.children;
	var li_value;
	var j=0;
	for (var i = 0; i < list_items.length; i++) {
		li_value = list_items[i].children[0].children[1].value;
		if((li_value == undefined || li_value.trim() == "") && i != list_items.length-1) {
			list_items[i].remove();
		} else {
			list_items[i].children[0].children[1].id = "id" + j;
			list_items[i].children[0].children[1].name = "id" + j;
			j++;
		}
	};
	if (li_value != undefined && li_value.trim() != "") {
		
		var cln = choices_space.children[list_items.length-1];
		// console.log("here");
		child = cln.cloneNode(true);
		child.children[0].children[1].value = "";
		choices_space.appendChild(child);
		j++;
	}
	
	document.getElementById("no_of_choices").value = j;
	if(document.getElementById("choices_space").lastChild.children[0].children[1].value.trim() == "") {
		document.getElementById("no_of_choices").value = j-1;
	}
	console.log(document.getElementById("no_of_choices").value);
}