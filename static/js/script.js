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


$(document).ready(function(){
    $("#heart").click(function(){
      if($("#heart").hasClass("liked")){
        $("#heart").html('<i class="fa fa-heart-o" aria-hidden="true"></i>');
        $("#heart").removeClass("liked");
      }else{
        $("#heart").html('<i class="fa fa-heart" aria-hidden="true"></i>');
        $("#heart").addClass("liked");
      }
    });
  });

