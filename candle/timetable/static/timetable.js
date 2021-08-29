'use strict';

// This function belongs to all timetables hence we placed it here.
$(function(){
  $("#timetable_export_btn").on('click',function(event) {
    event.preventDefault();
    window.open(window.location.href + '/export')
  });
});

// Move 'Zmazat' (Delete) button to the right side:
$('ul#rozvrh_akcie').find('li#delete_timetable').appendTo('ul#rozvrh_akcie');
