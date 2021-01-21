var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})


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
      // event.preventDefault();
      let rozvrh_tag = $("#rozvrh_taby .selected");
      let rozvrh_name = rozvrh_tag.text();
      if (confirm('Naozaj chcete zmazať rozvrh s názvom "' + rozvrh_name + '?"')) {
          // Zmazeme rozvrh
          let rozvrh_url = rozvrh_tag.attr("href");
          console.log("HREF_URL:" + rozvrh_url);
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
