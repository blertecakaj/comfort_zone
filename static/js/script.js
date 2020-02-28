$('.register_part').hide(function(){
$('#signUp').click(function(){
    $('.login_part').hide()
    $('.register_part').show()
    });
});

$('#register').click(function(){
        $('.register_part').hide()
        $('.login_part').show()
});


