

"""
    https://facebook.com
"""

import curses
from curses import textpad
import textwrap




class NCursesScreen:
    def __init__(self, screen: "curses._CursesWindow") -> None:
        self.__screen = screen

    def draw_rectangle(self, y1, x1, y2, x2):
        """
            this is a rectangle with specified coordinates:

            (y1, x1)            (y1, x1)
            |------------------|
            |                  |
            |                  |
            |                  |
            |------------------|
            (y2, x1)            (y2, x2)
        """
        textpad.rectangle(self.__screen, y1, x1, y2, x2)


    def func(self):
        self.text = "text"

    def print_text(self, y, x, item, color=None) -> None:
        if type(item) != str:
            item = str(item)
        if color:
            self.__screen.addstr(y, x, item, color)
        else:
            self.__screen.addstr(y, x, item)



def test_app(screen: "curses._CursesWindow") -> None:

    screen_height, screen_width = screen.getmaxyx()
    while 1:
        textpad.rectangle(screen, 1, 2, screen_height // 2, screen_width - 3)

        textpad.rectangle(screen, screen_height // 2 + 5, 2, screen_height // 2 + 7, screen_width - 3)
        screen.addstr(screen_height // 2 + 6, 3, "> ")
        screen.getch()




variable_renamed = 123


if __name__ == "__main__":
    try:
        curses.wrapper(test_app)
    except KeyboardInterrupt:
        print("done")
