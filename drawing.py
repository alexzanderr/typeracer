

import curses
from curses import textpad
import textwrap


def test_app(screen: "curses._CursesWindow"):

    screen_height, screen_width = screen.getmaxyx()
    while 1:
        textpad.rectangle(screen, 1, 2, screen_height // 2, screen_width - 3)

        textpad.rectangle(screen, screen_height // 2 + 5, 2, screen_height // 2 + 7, screen_width - 3)
        screen.addstr(screen_height // 2 + 6, 3, "> ")
        screen.getch()


if __name__ == "__main__":
    try:
        curses.wrapper(test_app)
    except KeyboardInterrupt:
        print("done")

