
"""
    docs: https://willpittman.net:8080/index.php?title=Python_curses
"""

import sys
import os
import curses
import traceback
from textwrap import wrap

# current project
from game import Game
from args import ParseProgramArguments

from core.aesthetics import asciify
from core.json__ import read_json_from_file, write_json_to_file, prettify, pretty_print


def run_control_sequence(sequence):
    os.write(sys.stdout.fileno(), bytes(sequence, 'utf-8'))

# TODO:
# add more templates for code
# add auto resize when user presses super + arrow


colors = {
    "author": ((240, 233), ""),
    "background": (int, 233, ""),
    "correct": ((240, 233), ""),
    "incorrect": ((197, 52), ""),
    "prompt": ((244, 233), ""),
    "quote": ((195, 233), ""),
    "score": ((230, 197), ""),
    "top_bar": ((51, 24), ""),
}


multiline_code_to_match = [

    # "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
    "string = \"andrew is here and he wants to tell you something\"",
    "\t\t\tx = 3\n",
    "\t\ty = 2\n",
    "\tprint()\n",
    "from core.json__ import *\n",
    "\tprint(\"hello world\")\n",
    "\n",
    "\n",
    "for i in range(100):\n",
    "\tx = 3\n",
    "\ty = 2\n",
    "\n",
    "print(\"something22222222\")\n",
    "",
    "",
]


multiline_code_to_match = []
multiline_code_to_match = [
    "string = andrew is here and he wants to tell you something22222222\n",
]

some_dictionary = {}


def TyperacerGame(ncurses_screen: "curses._CursesWindow"):
    # the game
    program_arguments = ParseProgramArguments()
    if program_arguments.code_from_json and program_arguments.code_from_txt:
        print("error: you cant load from a json file and a text file at the same time")
        exit(0)

    elif program_arguments.custom_quote and program_arguments.code_from_json:
        print("error: you cant load from a json file and a custom quote at the same time")
        exit(0)

    elif program_arguments.custom_quote and program_arguments.code_from_txt:
        print("error: you cant load from a text file and a custom quote at the same time")
        exit(0)

    if program_arguments.code_from_txt:
        # load custom code from text file
        custom_text = []

    if program_arguments.code_from_json:
        custom_text = []

    if program_arguments.custom_quote:
        custom_text = program_arguments.custom_quote

    game = Game(
        ncurses_screen=ncurses_screen,
        custom_text=multiline_code_to_match,
        minimalist=program_arguments.minimalist,
        save_stats=program_arguments.save_stats,
        ui_theme=program_arguments.ui_theme
    )
    game.play_typeracer()


def NCursesApplication():
    # Initialize curses
    ncurses_screen = curses.initscr()

    # Turn off echoing of keys, and enter cbreak mode,
    # where no buffering is performed on keyboard input
    curses.noecho()
    curses.cbreak()

    # In keypad mode, escape sequences for special keys
    # (like the cursor keys) will be interpreted and
    # a special value like curses.KEY_LEFT will be returned
    ncurses_screen.keypad(True)

    # Start color, too.  Harmless if the terminal doesn't have
    # color; user can test with has_color() later on.  The try/catch
    # works around a minor bit of over-conscientiousness in the curses
    # module -- the error return from C start_color() is ignorable.
    try:
        curses.start_color()
    except:
        pass

    block_cursor = "\x1b[\x32 q"
    beam_cursor = "\x1b[\x36 q"
    #  run_control_sequence(block_cursor)

    # setting up cursor
    (3, 3, 3, 3)
    curses.curs_set(1)
    try:
        TyperacerGame(ncurses_screen=ncurses_screen)
    except Exception as error:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error.with_traceback(exc_traceback)

        # Set everything back to normal
        ncurses_screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        print(error)
        print(type(error))
        print("game stopped")


def testing_just_a_function(self):
    self = 233
    for x in range(100):
        print("hello")


if __name__ == "__main__":
    NCursesApplication()
    #  ParseProgramArguments()
