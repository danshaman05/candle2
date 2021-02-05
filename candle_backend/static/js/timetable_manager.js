// CSRF-protection header
// source: https://stackoverflow.com/questions/31888316/how-to-use-flask-wtforms-csrf-protection-with-ajax
let csrf_token = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});
//// (end of) CSRF-protection header

$(function(){
  $("#novy_rozvrh").on('click',function(){
    let name = prompt('Zadajte nazov noveho rozvrhu:');
    if (name == null){
        return;
    }
    $.post($SCRIPT_ROOT + "/new_timetable",{"data": name})
        .done(function (data){
          window.location.replace(data);
        })
  });
});

$(function(){
  $("#zmazat_rozvrh").on('click',function(event) {
      // event.preventDefault();        // TODO treba?
      let rozvrh_tag = $("#rozvrh_taby li a.selected");
      let rozvrh_name = rozvrh_tag.text();
      if (confirm('Naozaj chcete zmazať rozvrh s názvom "' + rozvrh_name + '?"')) {
          // Zmazeme rozvrh
          let rozvrh_url = rozvrh_tag.attr("href");
          $.post($SCRIPT_ROOT + "/delete_timetable",
              {"data": rozvrh_url})
            .done(function (data) {
                // if (data['error']){      // Momentalne nemam ziaden error
                //     alert(data['error']);
                // } else {
                  window.location.replace(data['next_url']);
                // }
          })
      } else {
          // Nerobime nic - rozvrh nebude zmazany
      }
  });
});


$(function(){
  $("#duplikovat_rozvrh").on('click',function(event) {
      // event.preventDefault();
          let rozvrh_url = window.location.href;
          $.post($SCRIPT_ROOT + "/duplicate_timetable",
              {"data": rozvrh_url})
            .done(function (data) {
                window.location.href = data['next_url'];
                // TODO nakoniec by to chcelo zobrazit nejaku flask messages!
          })
  });
});