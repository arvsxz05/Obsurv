$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});

$(function(ready){
    $("#username1").change(function () {
        var username = $(this).val();
        console.log("here");

        $.ajax({
            url: '/validate-username/',
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (data.is_taken) {
                    $("#signup-error").show();
                    $("#signup-error").text('Username already exist!')
                } else {
                    $("#signup-error").hide();
                }
            }
        });
    });
});