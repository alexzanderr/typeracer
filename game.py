

import curses
from curses import textpad, wrapper
from screen import NCursesScreen
from threading import Thread
from time import time, sleep
from textwrap import wrap
from copy import copy

# core package
from core.numbers__ import fixed_set_precision_str

def wrap_lines(lines: list, width: int):
    wrapped_lines = []
    for line in lines:
        wrapped_lines.extend(
            wrap(
                text=line, # just the line
                width=width, # witdh
                expand_tabs=False, # doesnt destroy tabs
                replace_whitespace=False, # doesnt replace tabs ('\t') with whitespace
                drop_whitespace=False # doesnt destroy endlines ('\n')
            )
        )
    return wrapped_lines


class Game:
    def __init__(self, 
        ncurses_screen: "curses._CursesWindow",
        custom_text,
        minimalist: bool,
        save_stats: bool,
        ui_theme: str
    ) -> None:
        self.screen = NCursesScreen(ncurses_screen)
        self.text_wrap_width = self.screen.width - 3
        self.padding = 4
        self.custom_text = wrap_lines(
            custom_text,
            self.text_wrap_width - self.padding * 2 - 2
        )

        self.text_input_area = ""
        self.text_input_area_y = self.screen.height // 2 + 5

        self.stats_start_y = int(self.screen.height / 1.5) + 5
        self.stats_start_x = 5

        self.is_playing = 0
        self.is_playing_icon = "● "


        self.minimalist = minimalist
        self.save_stats = save_stats
        self.ui_theme = ui_theme
        #  curses.init_pair(1, 197, 52)
        self.start_x = 5
        self.start_y = 7
        self.border_space = 4
        self.wpm_score_start_x = 20



    #  def time_thread_incrementer(self):
    #      try:
    #          while self.time_thread_active:
    #              self.elapsed_time = time() - self.start_time
    #              self.elapsed_time = fixed_set_precision_str(self.elapsed_time, 2)

    #              # print live time
    #              self.print_text(
    #                  2, self.wpm_score_start_x * 2,
    #                  "Stopwatch: "
    #              )
    #              self.print_text(
    #                  2, self.wpm_score_start_x * 2 + len("Stopwatch: "),
    #                  self.elapsed_time,
    #                  self.yellow_foreground
    #              )
    #              sleep(0.1)

    #      except KeyboardInterrupt:
    #          self.time_thread_active = 0


    def calculate_wpm(self):
        self.wpm = (60 * len(self.total_correct_typed_chars) / 5) / (time() - self.start_time)
        return round(self.wpm)
 

    def draw_status_line(self):
        self.screen.draw_rectangle(1, 2, 3, self.screen.width - 3)
        self.screen.print_text(2, 5, "playing: ")
        if self.is_playing:
             self.screen.print_text(
                2, 
                5 + len("playing: "), 
                self.is_playing_icon,
                self.screen.green_foreground
            )
        else:
            self.screen.print_text(
                2, 
                5 + len("playing: "), 
                self.is_playing_icon
            )
           

        self.wpm = self.calculate_wpm()
        # print self.wpm
        self.screen.print_text(
            2,
            self.wpm_score_start_x,
            f"WPM: "
        )
        self.screen.print_text(
            2,
            self.wpm_score_start_x + len("WPM: "),
            str(self.wpm),
            self.screen.yellow_foreground
        )

        self.screen.print_text(
            2, self.wpm_score_start_x * 2,
            f"Elapsed: {fixed_set_precision_str(time() - self.start_time, 2)}"
        )

    
    def draw_text_input_area(self):
        self.screen.draw_rectangle(
            self.text_input_area_y, 2,
            self.text_input_area_y + 2,
            self.text_wrap_width
        )
        self.text_input_area_length = 60
        self.screen.print_text(self.text_input_area_y + 1, self.border_space, ">", self.screen.yellow_foreground)

        # print what i inputted
        self.screen.print_text(self.text_input_area_y + 1, self.border_space, "> ", self.screen.yellow_foreground)
        self.screen.print_text(self.text_input_area_y + 1, self.border_space + 2, self.text_input_area.ljust(self.text_input_area_length))


    def draw_stats_box(self):
        self.screen.draw_rectangle(
            self.stats_start_y - 1,
            2, self.stats_start_y + 3,
            self.screen.width - 3
        )
        if self.current_index == len(self.current_line):
            return
        
        self.screen.print_text( 
            self.stats_start_y, self.stats_start_x, f"current: {self.current_index} ( {repr(self.current_line[self.current_index])} )")
        self.screen.print_text( 
            self.stats_start_y + 1, self.stats_start_x, f"correct: {self.correct_index} ( {repr(self.current_line[self.correct_index])} )")
        self.screen.print_text( 
            self.stats_start_y + 2, self.stats_start_x, f"wrong: {self.wrong_index} ( {repr(self.current_line[self.wrong_index])} )")


    def draw_cursor(self):
       # display cursor accordingly
        if self.current_index == 0:
            self.screen.move_cursor(self.start_y + self.line_index, self.start_x)
        else:
            total_tabs_until_current = 0
            for i in range(self.current_index):
                if self.current_line[i] == "\t":
                    total_tabs_until_current += 1

            diff = self.current_index - total_tabs_until_current
            self.screen.move_cursor(
                self.start_y + self.line_index,
                self.start_x + 4 * total_tabs_until_current + diff
            )


    def print_game_lines(self):
        # print already completed lines to the line_index
        for i in range(self.line_index):
            self.print_completed_line_on_screen(
                self.start_y + i,
                self.start_x,
                self.custom_text[i]
            )

 
        #  # print colored the line
        #  # it will be updated correcly if you type right or wrong
        #  # pe line_index print current status
        self.print_colored_line_on_screen(
            self.start_y + self.line_index, self.start_x, self.current_line, self.current_index, self.correct_index, self.wrong_index)

        # from line_index + 1 print uncompleted lines
        self.screen.print_lines(
            self.start_y + self.line_index + 1,
            self.start_x,
            self.custom_text,
            self.line_index + 1
        )       
    
    def draw_game(self):
        self.draw_status_line()

        # the main rectangle where the text belongs
        self.screen.draw_rectangle(
            5, 2,
            self.screen.height // 2 + 3,
            self.screen.width - 3
        )

        self.draw_text_input_area()
        self.draw_stats_box()
        self.print_game_lines()
        self.draw_cursor()
        self.screen.reload()



    def play_typeracer(self) -> None:
        self.current_index = 0
        self.line_index = 0
        self.correct_index = 0
        self.wrong_index = 0
        self.wrong_index_limit = 15
        self.wpm = 0
        self.accuracy = 0
        self.total_correct_typed_chars = ""
        self.total_wrong_typed_chars = ""

        self.start_time = time()


        for line_index, line_to_match in \
            enumerate(self.custom_text):
            if line_to_match == "":
                continue

            self.current_index = 0
            self.correct_index = 0
            self.wrong_index = 0
            self.wrong_index_limit = 15
            self.current_line = line_to_match
            self.line_index = line_index
            while 1:
                self.draw_game()

                # get the inserted key
                key = self.screen.get_char()
                self.inputted_char = chr(key)

                if self.inputted_char == "KEY_RESIZE":
                    self.screen.resize()
                    self.screen.reload()
                    self.draw_game()
                    

                if not self.inputted_char.isascii():
                    continue

                self.is_playing = 1

                # backspace part
                if self.inputted_char in ('KEY_BACKSPACE', '\b', '\x7f'):
                    # you cannot backspace if there is no mistake
                    # its pointless and makes the game worse programmable
                    if self.wrong_index == 0:
                        continue
                    if self.current_index > 0:
                        self.current_index -= 1
                        if self.wrong_index == 0 and self.correct_index > 0:
                            self.correct_index -= 1
                        if self.current_index == 0:
                            self.correct_index = 0
                            self.wrong_index = 0

                    if self.wrong_index > 0:
                        self.wrong_index -= 1

                else:
                    # text input area
                    # not related to self.wpm
                    if self.inputted_char == "\t":
                        self.text_input_area += "\\t"
                    elif self.inputted_char == " ":
                        self.text_input_area = ""
                    elif self.inputted_char == "\n":
                        self.text_input_area = ""
                    else:
                        self.text_input_area += self.inputted_char

                    if len(self.text_input_area) > 50:
                        self.text_input_area = ""


                    # check if inserted self.inputted_char is correct
                    if self.inputted_char == line_to_match[self.current_index] and self.wrong_index == 0:
                        self.correct_index += 1
                        self.current_index += 1
                        self.total_correct_typed_chars += self.inputted_char  

                    else:
                        if self.wrong_index < self.wrong_index_limit and self.current_index < len(line_to_match) - 1:
                            self.wrong_index += 1
                            self.current_index += 1
                            self.total_wrong_typed_chars += self.inputted_char


                # meaning that the game is done and you successfully typed everything correct
                if self.correct_index == len(line_to_match):
                    break


        # print every completed line with green after game is over
        for i in range(len(self.custom_text)):
            self.print_completed_line_on_screen(self.start_y + i, self.start_x, self.custom_text[i])


        self.is_playing = 0
        self.time_thread_active = 0


        self.screen.reload()



        # await user input
        self.screen.await_input()




    def print_colored_line_on_screen(self, y: int, x: int, line: str, curr: int, corr: int, wrg: int) -> None:
        #  \tprint(\"hello world\")\n
        formatted_line = copy(line)
        #  '    print(\"hello world\")'

        if curr == 0 and corr == 0:
            self.screen.print_text(y, x, formatted_line.replace(
                "\t", "--->").replace("\n", "↵"))
            return

        green_part = formatted_line[:corr]
        red_part = formatted_line[corr: corr + wrg]
        white_part = formatted_line[corr + wrg:]
        if len(line) - 1 == curr and wrg > 0:
            red_part = formatted_line[corr: corr + wrg + 1]
            white_part = ""

        counter = 0
        for self.inputted_char in green_part:
            if self.inputted_char == "\t":
                self.screen.print_text(y, x + counter, "--->", self.screen.gray_background)
                counter += 3

            elif self.inputted_char == " ":
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.gray_background)
            elif self.inputted_char == "\n":
                self.screen.print_text(y, x + counter, '↵', self.screen.gray_background)  
            else:
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.gray_foreground)
            counter += 1

        for self.inputted_char in red_part:
            if self.inputted_char == "\t":
                self.screen.print_text(y, x + counter, "--->", self.screen.red_background)
                counter += 3
            elif self.inputted_char == " ":
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.red_background)
            elif self.inputted_char == "\n":
                self.screen.print_text(y, x + counter, '↵', self.screen.red_background)
            else:
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.red_foreground)
            counter += 1

        for self.inputted_char in white_part:
            if self.inputted_char == "\n":
                self.screen.print_text(y, x + counter, '↵', self.screen.white_foreground)
            elif self.inputted_char == "\t":
                self.screen.print_text(y, x + counter, "--->", self.screen.white_foreground)
                counter += 3
            else:
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.white_foreground)
            counter += 1


    def print_completed_line_on_screen(self, y, x, line):
        counter = 0
        for self.inputted_char in line:
            if self.inputted_char == "\t":
                self.screen.print_text(y, x + counter, "--->", self.screen.gray_background)
                counter += 3
            elif self.inputted_char == " ":
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.gray_background)
            elif self.inputted_char == "\n":
                self.screen.print_text(y, x + counter, '↵', self.screen.gray_background)  
            else:
                self.screen.print_text(y, x + counter, self.inputted_char, self.screen.gray_foreground)
            counter += 1

