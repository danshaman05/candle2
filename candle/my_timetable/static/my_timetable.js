'use strict';


$(function(){
  $("#timetable_new_btn").on('click',function(){
    let name = prompt('Zadajte nazov noveho rozvrhu:');
    if (name == null){
        return;
    }
    $.post($SCRIPT_ROOT + Flask.url_for('my_timetable.new_timetable'),{"name": name})
        .done(function (data){
          window.location.replace(data);
        })
  });
});

$(function(){
  $("#timetable_delete_btn").on('click',function(event) {
      let rozvrh_tag = $("#rozvrh_taby li a.selected");
      let rozvrh_name = rozvrh_tag.text();
      if (confirm(`Naozaj chcete zmazať rozvrh s názvom "${rozvrh_name}"?`)) {
          // Zmazeme rozvrh
          $.ajax({
              url: window.location.href + '/delete',
              type: 'DELETE',
              success: function (data) {
                  window.location.replace(data['next_url']);
              }
          })
      } else {
          // Nothing to do.
      }
  });
});


$(function(){
  $("#timetable_duplicate_btn").on('click',function(event) {
      $.post(window.location.href + '/duplicate')
        .done(function (data) {
            window.location.href = data['next_url'];
      })
  });
});

$(function(){
  $("#timetable_rename_btn").on('click',function(){
    let old_name = $("#rozvrh_taby li a.selected").text();
    let name = prompt(`Zadajte nový názov pre rozrvh "${old_name}"`);
    if (name == null){
        return;
    }
    if (old_name === name){
        alert("Chyba: Zadali ste rovnaký názov!");
        return;
    }
    $.ajax(
        {
            url: window.location.href + '/rename',
            type: 'PUT',
            data: {"new_name": name}
        }
    ).done(function (data){
            const taby_selector = '#rozvrh_taby';
            const web_header_selector = '#web_header'

            document.title = data['title_html'];
            $(taby_selector).fadeOut(function (){
                $(taby_selector).html(data['tabs_html']).fadeIn();
            });
            $(web_header_selector).fadeOut(function (){
                $(web_header_selector).html(data['web_header_html']).fadeIn();
            });
    })
  });
});

function lesson_checkbox_handler(checkbox, subject_id) {
    // function is called from the HTML ("onclick" attribute)

    // CSS selector for subject's checkbox:
    let subject_cb_selector = `input[class='predmet_check'][value='${subject_id}']`;
    // CSS selector for all subject's lessons checkboxes:
    let lessons_cbs_selector = `input[name=${subject_id}]`;
    let lesson_id = checkbox.value;

    let action = "";
    if (checkbox.checked){
        action = "add"
        // if all lessons of this subject are checked:
        if ($(lessons_cbs_selector + ':checked').length === $(lessons_cbs_selector).length){
            // set subject's checkbox to "checked" also:
            $(subject_cb_selector).prop("checked", true) ;
        }
    } else {
       action = "remove"
        // uncheck subject's checkbox:
        $(subject_cb_selector).prop("checked", false) ;
    }
    $.ajax(
    {
        url: window.location.href + `/lesson/${lesson_id}/${action}`,
        type: 'POST'
    })
    .done(function (data) {
        if (data['success'] === false){
            $(checkbox).prop('checked', false);
            alert("Cannot add more neighbour lessons to one day!");
        } else {
            $('#rozvrh').html(data['layout_html']);
            $('#rozvrhList').html(data['list_html']);
        }
    })
}


function subject_checkbox_handler(checkbox) {
    // function is called from the HTML ("onclick" attribute)

    let subject_id = checkbox.value;
    // CSS selector for subject's lessons checkboxes:
    let lessons_cbs_selector = `input[name=${subject_id}]`;

    let action = "";
    if (checkbox.checked){
        action = "add"
        $(lessons_cbs_selector).prop("checked", true) ;
    } else {
       action = "remove";
       $(lessons_cbs_selector).prop("checked", false) ;
    }
    $.ajax({
        url: window.location.href + `/subject/${subject_id}/${action}`,
        type: 'POST'
    }).done(function (data){
        $('#rozvrh').html(data['layout_html']);
        $('#rozvrhList').html(data['list_html']);
    })
}