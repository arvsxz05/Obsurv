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
$('.chips-placeholder').material_chip({
	secondaryPlaceholder: '+ Add Tags',
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

$(".response-form").submit(function (event) {
	event.preventDefault();
    // var response = $(this).find('input[name=response]').val();
    var allVals = [];
	$(this).find('input[name=response]:checked').each(function() {
		allVals.push($(this).val());
	});
    console.log(allVals);
    if(allVals.length == 0) {
    	$(this).find(".error").show();
        $(this).find(".error").text('Choose an answer to respond!');
    } else {
        $("#response-error").hide();

        $.ajax({
            url: $(this).attr('action'),
            data: {
                'response': allVals
            },
            dataType: 'json',
            success: function (data) {
            	suffix = data.question;
                if (!data.success) {
                    $("#response-error-"+suffix).show();
                    $("#response-error-"+suffix).text('Something went wrong...');
                } else {
                	console.log(data.no_respondents);
                    $("#response-error-"+suffix).show();
                    $("#response-error-"+suffix).text('Your response has been recorded.');
                    $("#card-"+suffix).attr("disabled", true);
                    $("#number-"+suffix).text(data.no_respondents);
                    var temp = $.parseHTML("<button class='waves-effect waves-light btn col l5 m4 s12 hoverable edit-button' id='edit-" + suffix + "' type='button' onclick='edit(this.id)'><i class='material-icons left'>edit</i>Edit</button>");
                    $("#submit-"+suffix).replaceWith(temp);
                }
            }
        });
    }
});
function edit(id) {
	var temp = "edit-";
	id_num = id.slice(temp.length);
	console.log(id);
	$("#"+id).replaceWith($.parseHTML("<button class='waves-effect waves-light btn col l5 m4 s12 hoverable' id='submit-" + id_num + "'><i class='material-icons left'>assessment</i>Respond</button>"));
	$("#card-" + id_num).attr("disabled", false);
	$("#response-error-"+id_num).text('');
}