$('#calendar').calendar({
  dataSource: dataSource,
  startYear: startYear,
  enableContextMenu: true,
  clickDay: function(e) {
    if(e.events.length > 0) {
      var content = '';
      for(var i in e.events) {
        content += '<div class="event-tooltip-content">'
                    + '<a href="' + e.events[i].url + '"><div class="event-name" style="color:' + e.events[i].color + '"><h4>' + e.events[i].name + '</h4></div>'
                    + '<div class="event-location"><h5>' + e.events[i].location + '</h5></div></a>'
                    + '<hr>'
                    + '</div>';
      }
      
      var popover = $(e.element).popover({
        trigger: 'manual',
        container: 'body',
        html:true,
        content: content,
        placement: 'bottom'
      });
      var popover = $(e.element).data('bs.popover').tip();
      var alreadyVisible = false;
      $('div.popover:visible').each(function() {
        if($(this).get(0) == popover.get(0)) {
          alreadyVisible = true;
        }
        else {
          $(this).hide();
        }
      });
      if(!alreadyVisible) {
        $(e.element).popover('show');
      }
    }
  },

});

$('[data-toggle="popover"],[data-original-title]').popover();
$(document).on('click', function(e) {
  $('[data-toggle="popover"],[data-original-title]').each(function() {
    if (!$(this).is(e.element) && $(this).has(e.element).length === 0 && $('.popover').has(e.events).length === 0) {
      $(this).popover('hide').data('bs.popover').inState.click = false
    }
  });
});
