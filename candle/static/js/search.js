function load_teacher( teacher_slug ) {
    // funkcia, presmeruje na rozvrh
    // console.log($SCRIPT_ROOT + '/ucitelia/' + teacher_slug);
    window.location.href = $SCRIPT_ROOT + '/ucitelia/' + teacher_slug
    }

$( function() {
    $( "#showTeachers" ).autocomplete({
      source: $SCRIPT_ROOT + "/get_teachers_list",   // odtial nacita zoznam vsetkych ucitelov
      minLength: 2,
      select: function( event, ui ) {
          load_teacher(ui.item.id);
      }
    });
});