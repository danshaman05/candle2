// A $( document ).ready() block.
$( document ).ready(function() {
	$('#overlay').fadeOut();

	if ($(window).width() < 996) {
		$('#timetable__days').stick_in_parent({
			offset_top: 40
		});

		$('.timetable').scroll(function() {
			$('.timetable__days').css('left', $('.timetable').scrollLeft() * -1);
		});
	} else {
		$('#timetable__days').stick_in_parent();
	}

	$('.sidebar__element .fa-bars').on('click', function() {
		$('#overlay').fadeToggle();
		$('.sidebar__container').toggleClass('sidebar__container--expanded');
	});

	$('.sidebar__element .fa-arrow-right').on('click', function() {
		$('#overlay').fadeIn();
		$('.sidebar__container').addClass('sidebar__container--expanded');
		$('.sidebar__element .fa-arrow-right').fadeOut("slow", function() {
			$('.sidebar__element .fa-arrow-left').fadeIn();
		});
	});

	$('#sidebar__close, .sidebar__element .fa-arrow-left').on('click', function() {
		$('#overlay').fadeOut();
		$('.sidebar__container').removeClass('sidebar__container--expanded');
		$('.sidebar__element .fa-arrow-left').fadeOut("slow", function() {
			$('.sidebar__element .fa-arrow-right').fadeIn();
		});
	});

	$('.lecture_container').each(function () {
		let numberOfLectures = $(this).children().length;
		if (numberOfLectures > 1) {
			$(this).children().each(function (index) {
				$(this).addClass('lecture_container__lecture--absolute');
				$(this).css('right', 4 + (35 * index));
			});
		}
	});

	setTimeIndicator();

	setInterval(function() {
		setTimeIndicator();
	}, 120 * 1000);
});

function setTimeIndicator() {
	var minutes = getMinutes();
	minutes = minutes + (minutes / 51);

	if (minutes > 0) {
		$('.timetable__current_time').css('top', minutes);
	} else {
		$('.timetable__current_time').css('top', 0);
	}
}

function getMinutes() {
	var currentdate = new Date();
	return (currentdate.getHours() - 8) * 60 + currentdate.getMinutes() - 10;
}
