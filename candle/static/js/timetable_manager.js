
$(function(){
  $("#novy_rozvrh").on('click',function(){
    let name = prompt('Zadajte nazov noveho rozvrhu:');
    if (name == null){
        return;
    }
    $.post($SCRIPT_ROOT + "/new_timetable",{"name": name})
        .done(function (data){
          window.location.replace(data);
        })
  });
});

$(function(){
  $("#zmazat_rozvrh").on('click',function(event) {
      let rozvrh_tag = $("#rozvrh_taby li a.selected");
      let rozvrh_name = rozvrh_tag.text();
      if (confirm(`Naozaj chcete zmazať rozvrh s názvom "${rozvrh_name}"?`)) {
          // Zmazeme rozvrh
          let rozvrh_url = rozvrh_tag.attr("href");
          $.post($SCRIPT_ROOT + "/delete_timetable",
              {"url": rozvrh_url})
            .done(function (data) {
                // if (data['error']){      // TODO implement errors
                //     alert(data['error']);
                // } else {
                  window.location.replace(data['next_url']);
                // }
          })
      } else {
          // Nothing to do.
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
                // TODO show flask-message, or some informative pop-up
          })
  });
});

$(function(){
  $("#premenovat_rozvrh").on('click',function(){
    let old_name = $("#rozvrh_taby li a.selected").text();
    let name = prompt(`Zadajte nový názov pre rozrvh "${old_name}"`);
    if (name == null){
        return;
    }
    if (old_name == name){
        alert("Chyba: Zadali ste rovnaký názov!");
        return;
    }
    $.post($SCRIPT_ROOT + "/rename_timetable",
        {"url": document.URL, "new_name": name}
        )
        .done(function (data){
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

