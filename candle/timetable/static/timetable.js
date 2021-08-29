'use strict';

// This function belongs to all timetables hence we placed it here.
$(function(){
  $("#exportovat_rozvrh").on('click',function(event) {
    event.preventDefault();
    window.open(window.location.href + '/export')
  });
});