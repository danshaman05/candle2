
(function () {

var pendingRequests = 0;

function addSearch(url, input, target, error, useEditor) {
    if (!$(input)) return;

    var throbber = $('panel_throbber');
    var oldValue;
    var searchRequest = new Request.HTML({
        url: candleFrontendAbsoluteUrl+url,
        link: 'cancel',
        onSuccess: function(responseTree, responseElements,
            responseHTML, responseJavaScript) {
            pendingRequests--;
            if (pendingRequests == 0 && $chk(throbber)) {
                throbber.removeClass('active');
            }
            $(target).innerHTML = responseHTML;

            if (useEditor && $chk(document.timetableEditor)) {
                createEditorPanel(document.timetableEditor);
            }

        },
        onCancel: function() {
            pendingRequests--;
            if (pendingRequests == 0 && $chk(throbber)) {
                throbber.removeClass('active');
            }
        },
        onFailure: function() {
            pendingRequests--;
            if (pendingRequests == 0 && $chk(throbber)) {
                throbber.removeClass('active');
            }
            $(target).innerHTML = error;
        }
    });
    
    var searchTimer = null;


    $(input).addEvent('keyup', function() {
        if ($(input).value == oldValue) return;
        oldValue = $(input).value;
        
        if (searchTimer != null) {
            clearTimeout(searchTimer);
        }
        searchTimer = setTimeout(function() {
            var cas = new Date().getTime();
            if (pendingRequests == 0 && $chk(throbber)) {
                throbber.addClass('active');
            }
            pendingRequests++;

            var data = { 'cas': cas };
            data[input] = $(input).value;

            if (useEditor && $chk(document.candleTimetableEditor_timetableId)) {
                data.timetable_id = document.candleTimetableEditor_timetableId;
            }
            searchRequest.get(data);
        }, 500);
    });
}

// TODO: Zmenit routes:
window.addEvent('domready', function() {
    // addSearch('/panel/list-lessons', 'showLessons', 'list_lessons_box',
    //     'Nepodarilo sa načítať zoznam predmetov.', true);                // DG: toto ma nastaveny parameter UseEditor na true
    // addSearch('/panel/list-teachers', 'showTeachers', 'list_teachers_box',
    //     'Nepodarilo sa načítať zoznam učiteľov.');

    //DG: prvy parameter by mal byt nejak namapovany na funkciu, kt. vylistuje hladane miestnosti
    addSearch('/miestnosti/B', 'show_rooms', 'list_rooms_box',
        'Nepodarilo sa načítať zoznam miestností.');


    // addSearch('/panel/list-studentGroups', 'showStudentGroups', 'list_studentGroups_box',
    //     'Nepodarilo sa načítať zoznam krúžkov.');
});

})();

