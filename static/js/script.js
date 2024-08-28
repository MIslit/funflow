$(function() {
  /* Rounded Dots Dark */
  $("#content-1").mCustomScrollbar({
    theme: "rounded-dots-dark"
  });
});

window.setTimeout(function() {
  $(".alert").fadeTo(500, 0).slideUp(500, function(){
      $(this).remove(); 
  });
}, 4000);