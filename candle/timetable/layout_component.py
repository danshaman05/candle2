'''
Project: Candle (New Generation): Candle rewrite from PHP to Python.
Author: Daniel Grohol, FMFI UK
'''

class LayoutComponent:
    """LayoutComponent consists of PlacedLesson class objects.

    This class represents a component of PlacedLesson objects (PL). Each PL is linked to its
     sibling PLs in the same column (day)."""

    def __init__(self):
        self.placed_lessons = []
        self.width = None
        """width is the number of sub-columns needed for fitting the component into a day"""

    def add(self, placed_lesson):
        self.placed_lessons.append(placed_lesson)

    def set_width(self, width):
        self.width = width

    def set_lessons_width(self):
        if not self.placed_lessons:
            raise Exception("LayoutComponent needs to be filled with lessons!")
        if not self.width:
            raise Exception("Set the component's width first!")
        for pl in self.placed_lessons:
            pl.set_horizontal_position(self.width)
