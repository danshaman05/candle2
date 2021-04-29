


class PlacedLesson:
    def __init__(self, lesson, column=0):
        self.lesson = lesson
        self.topPercent = self.minutes2percentage(lesson.start)  # position from top in %
        self.column = column
        self.bottomPercent = 100 - self.minutes2percentage(lesson.end + lesson.breaktime) # position from bottom in %. It corrensponds to the end of the lesson.

    def get_style(self):
        """Returns css style required for positioning of the lesson in the timetable."""
        return f"top: {self.topPercent}%; bottom: {self.bottomPercent}%; left: {self.get_left_margin() }%; z-index: {self.column}"


    def get_start(self):
        return self.lesson.start

    def get_end(self):
        return self.lesson.end

    def get_left_margin(self):
        return self.column * 20     # maximalne 5 columns mozu byt vedla seba

    @classmethod
    def minutes2percentage(cls, minutes):
        return int((minutes - 490) / 700 * 100)
