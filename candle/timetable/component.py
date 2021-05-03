class Component:
    """Component consists of PlacedLesson class objects."""

    # TODO docstrings
    def __init__(self):
        self.placed_lessons = []
        self.width = None
        """width is the number of columns needed for fitting the component into a day"""

    def add(self, placed_lesson):
        self.placed_lessons.append(placed_lesson)

    def set_width(self, width):
        self.width = width

    def set_lessons_width(self):
        if not self.placed_lessons:
            raise Exception("Component needs to be filled with lessons first!")
        if not self.width:
            raise Exception("Set the component width first!")
        for pl in self.placed_lessons:
            pl.set_horizontal_position(self.width)
