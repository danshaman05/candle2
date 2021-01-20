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
      if (confirm('Naozaj chcete zmazať tento rozvrh?')) {         // TODO nazov rozvrhu
          // Zmazeme rozvrh
          // console.log('Rozvrh bude zmazany.');
          $.post($SCRIPT_ROOT + "/delete_timetable", {"data": window.location.href})
            .done(function (data) {
                if (data['error']){
                    alert(data['error']);
                } else {
                  window.location.replace(data['next_url']);
                }
          })
      } else {
          // Nerobime nic
          console.log('Rozvrh nebude zmazany.');
      }
  });
});
