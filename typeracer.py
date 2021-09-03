
import argparse
import curses
from curses import textpad
from time import sleep
from copy import copy
from textwrap import wrap


def wrap_multicode_lines(multiline_code, width):
    wrapped_array = []
    for line in multiline_code:
        wrapped_array.extend(wrap(text=line, width=width, expand_tabs=False, replace_whitespace=False, drop_whitespace=False))
    return wrapped_array


class Game:
    def __init__(self) -> None:
        #  curses.init_pair(1, 197, 52)
        self.start_x = 5
        self.start_y = 7
        self.border_space = 4
        self.game_status_icon = "● "
        pass


    def print_stats(self, y, string, current_index, correct_index, wrong_index):
        if current_index == len(string):
            return
        self.print_text_on_screen(
            y, 0, f"current: {current_index} ( {repr(string[current_index])} )")
        self.print_text_on_screen(
            y + 1, 0, f"correct: {correct_index} ( {repr(string[correct_index])} )")
        self.print_text_on_screen(
            y + 2, 0, f"wrong: {wrong_index} ( {repr(string[wrong_index])} )")


    def print_text_on_screen(self, y, x, text, color=None) -> None:
        if type(text) == int:
            text = str(text)
        if color:
            self.screen.addstr(y, x, text, color)
        else:
            self.screen.addstr(y, x, text)


    def play_typeracer(self, screen: "curses._CursesWindow", lines_array: list) -> None:
        self.screen = screen
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        multiline_code_to_match = wrap_multicode_lines(lines_array, self.screen_width - 3 - self.border_space * 2 - 2)
        
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

        curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.actual_green = curses.color_pair(8)


        # turn off cursor blinking
        curses.curs_set(1)
        self.is_playing = 0

        textpad.rectangle(screen, 1, 2, 3, self.screen_width - 3)
        self.print_text_on_screen(2, 5, "playing: ")
        self.print_text_on_screen(2, 5 + len("playing: "), self.game_status_icon)



        textpad.rectangle(screen, 5, 2, self.screen_height // 2 + 3, self.screen_width - 3)
        
        text_input_area_y = self.screen_height // 2 + 5
        textpad.rectangle(screen, text_input_area_y, 2, text_input_area_y + 2, self.screen_width - 3)
        self.text_input_area = ""
        self.text_input_area_length = 60
        self.print_text_on_screen(text_input_area_y + 1, self.border_space, ">", self.yellow_foreground)
        
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
                    self.print_completed_line_on_screen(self.start_y + i, self.start_x, multiline_code_to_match[i])

                #  # print colored the line
                #  # it will be updated correcly if you type right or wrong
                #  # pe line_index print current status
                self.print_colored_line_on_screen(
                    self.start_y + line_index, self.start_x, line_to_match, current_index, correct_index, wrong_index)

                # from line_index + 1 print uncompleted lines
                self.print_multi_lines_on_screen(
                    self.start_y + line_index + 1, self.start_x, multiline_code_to_match, line_index + 1)

                # print current index .. bla bla underneath
                #  print_stats(string_to_match, current_index, correct_index, wrong_index)
                    
                # this needs to be before the cursor because
                # if cursor is ON and you print something on the screen
                # then the cursor will be automatically moved after what you 
                # printed
                #  self.print_stats(20, line_to_match, current_index, correct_index, wrong_index)
                #  self.print_text_on_screen(25, 0, f"total y lines: {curses.LINES}", self.yellow_foreground)
                #  self.print_text_on_screen(30, 0, f"(x, y): {screen.getmaxyx()}", self.yellow_foreground)


                if current_index == 0:
                    screen.move(self.start_y + line_index, self.start_x)
                else:
                    total_tabs_until_current = 0
                    for i in range(current_index):
                        if line_to_match[i] == "\t":
                            total_tabs_until_current += 1
                    
                    diff = current_index - total_tabs_until_current
                    screen.move(self.start_y + line_index, 4 * total_tabs_until_current + diff + self.start_x)

                screen.refresh()


                # get the inserted key
                key = screen.getch()
                char = chr(key)
                self.is_playing = 1

                self.print_text_on_screen(2, 5, "playing: ")
                self.print_text_on_screen(2, 5 + len("playing: "), self.game_status_icon, self.actual_green)


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
                    if char == "\t":
                        self.text_input_area += "\\t"
                    elif char == " ":
                        self.text_input_area = ""
                    elif char == "\n":
                        self.text_input_area = ""
                    else:
                        self.text_input_area += char
                        
                    if len(self.text_input_area) > 50:
                        self.text_input_area = ""

                    # check if inserted char is correct
                    if char == line_to_match[current_index] and wrong_index == 0:
                        correct_index += 1
                        current_index += 1
                        correct_typed_chars += char

                    else:
                        if wrong_index < wrong_index_limit and current_index < len(line_to_match) - 1:
                            wrong_index += 1
                            current_index += 1
                
                self.print_text_on_screen(text_input_area_y + 1, self.border_space, "> ", self.yellow_foreground)
                self.print_text_on_screen(text_input_area_y + 1, self.border_space + 2, self.text_input_area.ljust(self.text_input_area_length))


                # meaning that the game is done and you successfully typed everything correct
                if correct_index == len(line_to_match):
                    break

   
                # update screen
                screen.refresh()


        # print every completed line with green after game is over
        for i in range(len(multiline_code_to_match)):
            self.print_completed_line_on_screen(self.start_y + i, self.start_x, multiline_code_to_match[i])
    

        self.is_playing = 0

        # print done message
        self.print_text_on_screen(13, 0, "done", self.yellow_foreground)
        screen.refresh()



        # await user input
        screen.getch()


    def print_multi_lines_on_screen(self, start_index: int, x: int,  multiline_array: list, from_index: int) -> None:
        for index, line in enumerate(multiline_array[from_index:], start=start_index):
            self.screen.addstr(index, x, line.replace(
                "\n", "↵").replace("\t", "--->"))


    def print_colored_line_on_screen(self, y: int, x: int, line: str, curr: int, corr: int, wrg: int) -> None:
        #  \tprint(\"hello world\")\n
        formatted_line = copy(line)
        #  '    print(\"hello world\")'

        if curr == 0 and corr == 0:
            self.print_text_on_screen(y, x, formatted_line.replace(
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
                self.print_text_on_screen(y, x + counter, "--->", self.green_background)
                counter += 3

            elif char == " ":
                self.print_text_on_screen(y, x + counter, char, self.green_background)
            elif char == "\n":
                self.print_text_on_screen(y, x + counter, '↵', self.green_background)
            else:
                self.print_text_on_screen(y, x + counter, char, self.green_foreground)
            counter += 1

        for char in red_part:
            if char == "\t":
                self.print_text_on_screen(y, x + counter, "--->", self.red_background)
                counter += 3
            elif char == " ":
                self.print_text_on_screen(y, x + counter, char, self.red_background)
            elif char == "\n":
                self.print_text_on_screen(y, x + counter, '↵', self.red_background)
            else:
                self.print_text_on_screen(y, x + counter, char, self.red_foreground)
            counter += 1

        for char in white_part:
            if char == "\n":
                self.print_text_on_screen(y, x + counter, '↵', self.white_foreground)
            elif char == "\t":
                self.print_text_on_screen(y, x + counter, "--->", self.white_foreground)
                counter += 3
            else:
                self.print_text_on_screen(y, x + counter, char, self.white_foreground)
            counter += 1


    def print_completed_line_on_screen(self, y, x, line):
        counter = 0
        for char in line:
            if char == "\t":
                self.print_text_on_screen(y, x + counter, "--->", self.green_background)
                counter += 3
            elif char == " ":
                self.print_text_on_screen(y, x + counter, char, self.green_background)
            elif char == "\n":
                self.print_text_on_screen(y, x + counter, '↵', self.green_background)
            else:
                self.print_text_on_screen(y, x + counter, char, self.green_foreground)
            counter += 1




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
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
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
    argument_parser = argparse.ArgumentParser(description="typeracer.py")

    argument_parser.add_argument("--code-from-txt", type=str,
                    help="load custom code/multiline text from text file (warning: format must be valid)",
                    default=None)

    argument_parser.add_argument("--code-from-json", type=str,
                    help="load custom code/multiline text from JSON file (warning: format must be valid)", default=None)

    argument_parser.add_argument(
        "--minimalist",
        type=bool,
        help="run the game without title and many details",
        default=False
    )

    argument_parser.add_argument(
        "--custom-quote",
        type=str,
        help="load custom single line text into the game",
        default=None
    )
        
    argument_parser.add_argument(
        "--save-stats",
        type=bool,
        help="if this is on, then you will get saved analytics of your matches; this requires a python simple web server which is by default shipped with the package",
        default=True
    )

    argument_parser.add_argument(
        "--ui-theme",
        type=str,
        help="gruvbox is the best",
        default="gruvbox"
    )

    program_arguments = argument_parser.parse_args()

    if program_arguments.code_from_json and program_arguments.code_from_txt:
        print("warning: you cant load from a json file and a text file at the same time")
        exit(0)
    #  print(program_arguments)

    try:
        game = Game()
        curses.wrapper(game.play_typeracer, multiline_code_to_match)
    except KeyboardInterrupt:
        print("done")

