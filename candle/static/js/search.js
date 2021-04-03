function redirect( endpoint ) {
    window.location.href = $SCRIPT_ROOT + endpoint;
}

// TEACHERS
$( function() {
    $( "#showTeachers" ).autocomplete({     // The Autocomplete is a widget from the jQueryUI framework, see https://jqueryui.com/autocomplete/#remote
      source: $SCRIPT_ROOT + "/get_data/teachers",
      minLength: 2,
      select: function( event, ui ) {
          redirect('/ucitelia/' + ui.item.id);
      }
    });
});

// ROOMS
$( function() {
    $( "#showRooms" ).autocomplete({
      source: $SCRIPT_ROOT + "/get_data/rooms",
      minLength: 1,
      select: function( event, ui ) {
          redirect('/miestnosti/' + ui.item.id);
      }
    });
});

// STUDENT GROUPS
$( function() {
    $( "#showGroups" ).autocomplete({
      source: $SCRIPT_ROOT + "/get_data/groups",
      minLength: 1,
      select: function( event, ui ) {
          redirect('/kruzky/' + ui.item.id);
      }
    });
});