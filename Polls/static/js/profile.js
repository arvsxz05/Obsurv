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