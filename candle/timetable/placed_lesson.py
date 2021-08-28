'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

class PlacedLesson:
    """This class deals with how the lesson is positioned in the layout.
    PlacedLesson is positioned by CSS position:absolute property."""

    def __init__(self, timetable, lesson, column=0):
        self.timetable = timetable
        self.lesson = lesson
        self.column = column
        """Column in which the lesson is placed in."""

        self.left_neigs = set()
        self.right_neigs = set()
        """Each lesson can have neighbours - other lessons that run at the same time in other columns."""

        self.topPercent = self.minutes2percentage(lesson.start)
        """position from top in %"""

        self.bottomPercent = 100 - self.minutes2percentage(lesson.end + lesson.breaktime)
        """position from bottom in %"""

        self.leftPercent = None  # position from left in %
        self.rightPercent = None # position from right in %

    @property
    def get_css_style(self):
        """Returns css style required for positioning of the lesson in the timetable."""
        return f"top: calc({self.topPercent}% + 2px); bottom: {self.bottomPercent}%; left: {self.get_left_position()}%; right: {self.get_right_position()}%;"

    def get_start(self):
        return self.lesson.start

    def get_end(self):
        return self.lesson.end

    def get_left_position(self):
        return self.leftPercent

    def get_right_position(self):
        return self.rightPercent

    def set_horizontal_position(self, component_width=None):
        if component_width is None:
            raise Exception("component_width cannot be none!")
        self.leftPercent = 100 // component_width * self.column
        self.rightPercent = 100 // component_width * (component_width - self.column -1)

    def add_left_neig(self, placed_lesson):
        """add left neighbour lesson"""
        self.left_neigs.add(placed_lesson)

    def add_right_neig(self, placed_lesson):
        """add right neighbour lesson"""
        self.right_neigs.add(placed_lesson)

    def has_neigs(self):
        """Return True, if the lesson has any neighbour, else False."""
        return True if self.neigs else False

    def minutes2percentage(self, minutes):
        """Calculate time in minutes to percentage of the height of the column."""
        return (minutes - self.timetable.minimum_time) / self.timetable.teaching_duration * 100

    @property
    def neigs(self):
        """Return all lesson's neighbours."""
        return self.right_neigs.union(self.left_neigs)

    def print_info(self):
        """Only for debug purpose. Print info about placed lesson."""
        print()
        print("Placed-Lesson Info:")
        print(f"{self.lesson.subject.name} {self.lesson.room.name} {self.lesson.type.name} {self.lesson.subject.code}")
        print(f"column: {self.column}")
