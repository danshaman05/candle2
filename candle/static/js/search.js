function redirect( endpoint ) {
    // redirect to a timetable
    window.location.href = $SCRIPT_ROOT + endpoint;
}

    ////////////////////// TODO: Refactor (three same functions below)
$( function() {
    $( "#showTeachers" ).autocomplete({     // The Autocomplete is a widget from the jQueryUI framework, see https://jqueryui.com/autocomplete/#remote
      source: $SCRIPT_ROOT + "/get_data/teachers",
      minLength: 2,
      select: function( event, ui ) {
          redirect('/ucitelia/' + ui.item.id);
      }
    });
});


$( function() {
    $( "#showRooms" ).autocomplete({
      source: $SCRIPT_ROOT + "/get_data/rooms",
      minLength: 1,
      select: function( event, ui ) {
          redirect('/miestnosti/' + ui.item.id);
      }
    });
});


// TODO showGroups: