$(function(){
  $('#create').click(function(){
    $.ajax({
      url: '/days',
      type: 'POST',
      data: { count: 1000 },
      success: function(data, stat, xhr) {
        if (data.status) {
          console.info('Posted to days');
        }
        else {
          console.error('Bad response from days.');
        }
      },
      error: function() {
        console.error('Bad request to days.');
      }
    });
  });
  
  $('#purge').click(function(){
    $.ajax({
      url: '/days?_method=DELETE',
      type: 'POST',
      success: function(data, stat, xhr) {
        if (data.status) {
          console.info('Purged days');
        }
        else {
          console.error('Bad response from purging days.');
        }
      },
      error: function(){
        console.error('Bad request to purge days.');
      }
    });
  });
  
  var reload = function(){
    $('#main').empty('');
    var url = '/days';
    if (arguments.length > 0) {
      url += '?width=' + arguments[0];
    }
    if (arguments.length > 1) {
      url += '&height=' + arguments[1];
    }
    if (arguments.length > 2) {
      url += '&t1=' + arguments[2];
    }
    if (arguments.length > 3) {
      url += '&t2=' + arguments[3];
    }
    if (arguments.length > 4) {
      url += '&d1=' + arguments[4];
    }
    if (arguments.length > 5) {
      url += '&d2=' + arguments[5];
    }
    $.ajax({
      url: url,
      type: 'GET',
      success: function(data, stat, xhr){
        if (data.status) {
          var main = $('#main');
          $.each(data.days, function(i, day){
            var dayElem = $('<div class="day" id="' + day.label + '"><h2>' + day.label + '</h2><div class="clear">&nbsp;</div></div>');
            main.append(dayElem);
            
            $.each(day.images, function(j, image){
              dayElem.append('<div class="i" style="width:' + day.width + 
                'px;height:' + day.height + ';" id="' + image.stamp + '">' + 
                image.stamp + '</div>');
            });
            
            dayElem.append('<div class="clear">&nbsp;</div>');
          });
          console.info('Loaded day data.');
          
          $('.i').click(function(){
            var img = $(this),
                t1 = img.prev()[0].id,
                t2 = img.next()[0].id,
                parent = img.parent(),
                idx = $.inArray(this, parent.children()),
                d1 = parent[0].id,
                d2 = parent[0].id;
            if (t1 == '')
              t1 = img[0].id;
            if (t2 == '')
              t2 = img[0].id;
            if (parent.prev().length > 0)
              d1 = parent.prev()[0].id;
            if (parent.next().length > 0)
              d2 = parent.next()[0].id;
            reload(
              window.innerWidth, window.innerHeight, 
              t1, t2,
              d1, d2
            );
          });
        }
        else {
          console.error('Could not load day data.');
        }
      }
    });
  };
  $('#reload').click(function(){
    reload(window.innerWidth, window.innerHeight);
  });
  reload(window.innerWidth, window.innerHeight);
});