
import argparse
import curses
from curses import textpad
from time import sleep
from copy import copy
from textwrap import wrap



def color_on(color_index):
    global_screen.attron(curses.color_pair(color_index))


def color_off(color_index):
    global_screen.attroff(curses.color_pair(color_index))




def get_color(color_index) -> int:
    return curses.color_pair(color_index)


def print_multi_lines_on_screen(start_index: int, multiline_array: list, from_index: int) -> None:
    for index, line in enumerate(multiline_array[from_index:], start=start_index):
        global_screen.addstr(index, 0, line.replace(
            "\n", "↵").replace("\t", "--->"))


def print_colored_line_on_screen(y: int, line: str, curr: int, corr: int, wrg: int) -> None:
    #  \tprint(\"hello world\")\n
    formatted_line = copy(line)
    #  '    print(\"hello world\")'

    if curr == 0 and corr == 0:
        print_text_on_screen(y, 0, formatted_line.replace(
            "\t", "--->").replace("\n", "↵"))
        return

    green_part = formatted_line[:corr]
    red_part = formatted_line[corr: corr + wrg]
    white_part = formatted_line[corr + wrg:]
    if len(line) - 1 == curr and wrg > 0:
        red_part = formatted_line[corr: corr + wrg + 1]
        white_part = ""

    counter = 0
    for char in green_part:
        if char == "\t":
            print_text_on_screen(y, counter, "--->", green_background)
            counter += 3

        elif char == " ":
            print_text_on_screen(y, counter, char, green_background)
        elif char == "\n":
            print_text_on_screen(y, counter, '↵', green_background)
        else:
            print_text_on_screen(y, counter, char, green_foreground)
        counter += 1

    for char in red_part:
        if char == "\t":
            print_text_on_screen(y, counter, "--->", red_background)
            counter += 3
        elif char == " ":
            print_text_on_screen(y, counter, char, red_background)
        elif char == "\n":
            print_text_on_screen(y, counter, '↵', red_background)
        else:
            print_text_on_screen(y, counter, char, red_foreground)
        counter += 1

    for char in white_part:
        if char == "\n":
            print_text_on_screen(y, counter, '↵', white_foreground)
        elif char == "\t":
            print_text_on_screen(y, counter, "--->", white_foreground)
            counter += 3
        else:
            print_text_on_screen(y, counter, char, white_foreground)
        counter += 1


def print_completed_line_on_screen(y, line):
    counter = 0
    for char in line:
        if char == "\t":
            print_text_on_screen(y, counter, "--->", green_background)
            counter += 3
        elif char == " ":
            print_text_on_screen(y, counter, char, green_background)
        elif char == "\n":
            print_text_on_screen(y, counter, '↵', green_background)
        else:
            print_text_on_screen(y, counter, char, green_foreground)
        counter += 1


def print_stats(y, string, current_index, correct_index, wrong_index):
    if current_index == len(string):
        return
    print_text_on_screen(
        y, 0, f"current: {current_index} ( {repr(string[current_index])} )")
    print_text_on_screen(
        y + 1, 0, f"correct: {correct_index} ( {repr(string[correct_index])} )")
    print_text_on_screen(
        y + 2, 0, f"wrong: {wrong_index} ( {repr(string[wrong_index])} )")


def wrap_multicode_lines(multiline_code, width):
    wrapped_array = []
    for line in multiline_code:
        wrapped_array.extend(wrap(text=line, width=width, expand_tabs=False, replace_whitespace=False, drop_whitespace=False))
    return wrapped_array


class Game:
    def __init__(self) -> None:
        #  curses.init_pair(1, 197, 52)

        # red
        red_fore = 0
        red_back = curses.COLOR_RED
        curses.init_pair(1, red_fore, red_back)
        self.red_foreground = curses.color_pair(1)
        
        # blue
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.blue_foreground = curses.color_pair(2)

        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.yellow_foreground = curses.color_pair(3)

        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.white_foreground = curses.color_pair(4)

        #  curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, 240, 233)
        self.green_foreground = curses.color_pair(5)

        curses.init_pair(6, 240, 233)
        self.green_background = curses.color_pair(6) | curses.A_BOLD

        #  curses.init_pair(6, 197, 52)
        curses.init_pair(7, red_fore, red_back)
        self.red_background = curses.color_pair(7) | curses.A_BOLD



    def play_typeracer(self, screen: "curses._CursesWindow", lines_array: list) -> None:
        self.screen = screen
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        wrapped_array = wrap_multicode_lines(multiline_code_to_match, self.screen_width - 3)




    def print_text_on_screen(self, y, x, text, color=None) -> None:
        if type(text) == int:
            text = str(text)
        if color:
            self.screen.addstr(y, x, text, color)
        else:
            self.screen.addstr(y, x, text)


def play_typeracer(screen: 'curses._CursesWindow'):


    #  textpad.rectangle(screen, 1, 0, 5, 5)
    # foreground, background







    # turn off cursor blinking
    curses.curs_set(1)

    correct_typed_chars = ""
    for line_index, line_to_match in enumerate(multiline_code_to_match):
        if line_to_match == "":
            continue

        current_index = 0
        correct_index = 0
        wrong_index = 0
        wrong_index_limit = 15
        while 1:
            # print already completed lines to the line_index
            for i in range(line_index):
                print_completed_line_on_screen(i, multiline_code_to_match[i])

            # print colored the line
            # it will be updated correcly if you type right or wrong
            # pe line_index print current status
            print_colored_line_on_screen(
                line_index, line_to_match, current_index, correct_index, wrong_index)

            # from line_index + 1 print uncompleted lines
            print_multi_lines_on_screen(
                line_index + 1, multiline_code_to_match, line_index + 1)

            # print current index .. bla bla underneath
            #  print_stats(string_to_match, current_index, correct_index, wrong_index)
                
            # this needs to be before the cursor because
            # if cursor is ON and you print something on the screen
            # then the cursor will be automatically moved after what you 
            # printed
            print_stats(20, line_to_match, current_index, correct_index, wrong_index)
            print_text_on_screen(25, 0, f"total y lines: {curses.LINES}", yellow_foreground)
            print_text_on_screen(30, 0, f"(x, y): {screen.getmaxyx()}", yellow_foreground)


            if current_index == 0:
                screen.move(line_index, 0)
            else:
                total_tabs_until_current = 0
                for i in range(current_index):
                    if line_to_match[i] == "\t":
                        total_tabs_until_current += 1
                
                diff = current_index - total_tabs_until_current
                screen.move(line_index, 4 * total_tabs_until_current + diff)

            screen.refresh()


            # get the inserted key
            key = screen.getch()
            char = chr(key)


            # good for debugging
            #  print_text_on_screen(3, 0, f"                                ")
            #  print_text_on_screen(3, 0, f"> {char.__repr__()} -> {key}")

            # if its not ascii char we dont play
            # we dont take into consideration super keys and arrows keys
            # and anything that is outside the scope of alphabet and punctuation
            if not char.isascii():
                continue

            # backspace part
            if char in ('KEY_BACKSPACE', '\b', '\x7f'):
                if current_index > 0:
                    current_index -= 1
                    if wrong_index == 0 and correct_index > 0:
                        correct_index -= 1
                    if current_index == 0:
                        correct_index = 0
                        wrong_index = 0

                if wrong_index > 0:
                    wrong_index -= 1

            else:

                # check if inserted char is correct
                if char == line_to_match[current_index] and wrong_index == 0:
                    correct_index += 1
                    current_index += 1
                    correct_typed_chars += char

                else:
                    if wrong_index < wrong_index_limit and current_index < len(line_to_match) - 1:
                        wrong_index += 1
                        current_index += 1

            # meaning that the game is done and you successfully typed everything correct
            if correct_index == len(line_to_match):
                break

            # update screen
            screen.refresh()

    # print every completed line with green
    for i in range(len(multiline_code_to_match)):
        print_completed_line_on_screen(i, multiline_code_to_match[i])
    
    # print done message
    print_text_on_screen(13, 0, "done", yellow_foreground)
    screen.refresh()



    # await user input
    screen.getch()


# TODO:
# add wpm ofc (import formula from last project)
# add status bar
# add more templates for code




colors = {
    "author": ( (240, 233), ""),
    "background": (int, 233, ""),
    "correct": ( (240, 233), ""),
    "incorrect": ( (197, 52), ""),
    "prompt": ( (244, 233), ""),
    "quote": ( (195, 233), ""),
    "score": ( (230, 197), ""),
    "top_bar": ( (51, 24), ""),
}

multiline_code_to_match = [
    "\tx = \"asdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"\n",
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
    "print(\"something\")\n",
    "",
    "",
]

if __name__ == "__main__":
    try:
        game = Game()
        curses.wrapper(game.play_typeracer)
    except KeyboardInterrupt:
        print("done")

