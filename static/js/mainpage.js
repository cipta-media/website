(function($) {
  "use strict"

  ///////////////////////////
  // Preloader
  $(window).on('load', function() {
    $("#preloader").delay(600).fadeOut();

    ///////////////////////////
    // Scrollspy
    $('body').scrollspy({
      target: '#nav',
      offset: $(window).height() / 2
    });

  });

  ///////////////////////////
  // Smooth scroll
  $("#nav .main-nav a[href^='#']").on('click', function(e) {
    e.preventDefault();
    var hash = this.hash;
    $('html, body').animate({
      scrollTop: $(this.hash).offset().top
    }, 600);
  });

  $('#back-to-top').on('click', function(){
    $('body,html').animate({
      scrollTop: 0
    }, 600);
  });

  ///////////////////////////
  // Btn nav collapse
  $('#nav .nav-collapse').on('click', function() {
    $('#nav').toggleClass('open');
  });

  ///////////////////////////
  // Mobile dropdown
  $('.has-dropdown a').on('click', function() {
    $(this).parent().toggleClass('open-drop');
  });

  ///////////////////////////
  // On Scroll
  $(window).on('scroll', function() {
    var wScroll = $(this).scrollTop();

    // Fixed nav
    wScroll > 1 ? $('#nav').addClass('fixed-nav') : $('#nav').removeClass('fixed-nav');

    // Back To Top Appear
    wScroll > 700 ? $('#back-to-top').fadeIn() : $('#back-to-top').fadeOut();
  });

})(jQuery);
