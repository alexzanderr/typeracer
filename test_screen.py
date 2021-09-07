
from threading import main_thread
from screen import NCursesScreen
import curses




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

    # setting up curso
    curses.curs_set(1)

    try:
        screen = NCursesScreen(ncurses_screen)
        screen.print_text(0, 0, "jkstasd")
        screen.await_input()

    except Exception as error:
        # Set everything back to normal
        ncurses_screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

        print(error)
        print(type(error))
        print("game stopped")


if __name__ == "__main__":
    NCursesApplication()
