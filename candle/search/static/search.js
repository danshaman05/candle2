'use strict';

function redirect( endpoint ) {
    window.location.href = $SCRIPT_ROOT + endpoint;
}

// TEACHERS
$( function() {
    $( "#showTeachers" ).autocomplete({     // The Autocomplete is a widget from the jQueryUI framework, see https://jqueryui.com/autocomplete/#remote
      source: $SCRIPT_ROOT + Flask.url_for('api.get_teachers'),
      minLength: 2,
      select: function( event, ui ) {
          redirect('/ucitelia/' + ui.item.id);
      }
    });
});

// ROOMS
$( function() {
    $( "#showRooms" ).autocomplete({
      source: $SCRIPT_ROOT + Flask.url_for('api.get_rooms'),
      minLength: 1,
      select: function( event, ui ) {
          redirect('/miestnosti/' + ui.item.id);
      }
    });
});

// STUDENT GROUPS
$( function() {
    $( "#showGroups" ).autocomplete({
      source: $SCRIPT_ROOT + Flask.url_for('api.get_groups'),
      minLength: 1,
      select: function( event, ui ) {
          redirect('/kruzky/' + ui.item.id);
      }
    });
});

function showLessonsBoxList(item_id, item_category){
    const selector = "#list_lessons_box";
    let data = {
        'pathname': window.location.pathname,
        'item-id': item_id,
        'item-category': item_category
    }
    $(selector).load($SCRIPT_ROOT + Flask.url_for('search.lessons_list'), data).hide().fadeIn();
}

// SUBJECT LESSONS
// This code is from the JqueryUI Autocomplete: Categories example,
// see: https://jqueryui.com/autocomplete/#categories
$( function() {
    $.widget( "custom.catcomplete", $.ui.autocomplete, {
          _create: function() {
            this._super();
            this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
          },
          _renderMenu: function( ul, items ) {
            var that = this,
              currentCategory = "";
            $.each( items, function( index, item ) {
              var li;
              if ( item.category != currentCategory ) {
                ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
                currentCategory = item.category;
              }
              li = that._renderItemData( ul, item );
              if ( item.category ) {
                li.attr( "aria-label", item.category + " : " + item.label );
              }
            });
          }
        });

    $( "#showLessons" ).catcomplete({
        source: $SCRIPT_ROOT + Flask.url_for('search.subject_search_handler'),
        delay: 400,     // in miliseconds
        minLength: 1,
        select: function( event, ui ) {
            showLessonsBoxList(ui.item.id, ui.item.category);
      }
    });
});
