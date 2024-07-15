import curses


def get_x(stdscr, y):
    max_x = stdscr.getmaxyx()[1] - 1
    x = max_x
    while x > 0:
        char = stdscr.inch(y, x) & 0xFF
        if char not in (ord(' '), 0):
            break
        x -= 1
    return x + 1 if x > 0 else max_x + 1


def main(stdscr):
    stdscr.idcok(True)
    stdscr.clear()
    # curses.echo()
    stdscr.scrollok(True)
    stdscr.idlok(True)
    curses.curs_set(0)
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Black text on white background
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White text on black background
    while True:
        row, col = stdscr.getmaxyx()
        try:
            key = stdscr.getch()
            if key == ord('i'):  # Insert mode
                curr_row, curr_col = stdscr.getyx()
                input_window = curses.newwin(1, col, row - 1, 0)
                input_window.bkgd(' ', curses.color_pair(1))
                input_window.scrollok(True)
                input_window.idlok(True)
                input_window.keypad(True)
                curses.cbreak()
                curses.curs_set(1)
                s = ""
                while True:
                    stdscr.refresh()
                    input_window.refresh()
                    key = input_window.getch()
                    if key == 27:  # Escape key
                        input_window.clear()
                        input_window.refresh()
                        input_window.bkgd(' ', curses.color_pair(2))
                        input_window.refresh()
                        curses.curs_set(0)
                        del input_window
                        break
                    elif key == curses.KEY_BACKSPACE or key == 127:
                        y, x = input_window.getyx()
                        if x == 0:
                            if y == 0:
                                continue
                            input_window.move(y - 1, get_x(input_window, y - 1) - 1)
                            y, x = input_window.getyx()
                            x += 1
                        input_window.delch(y, x - 1)
                        if len(s): s = s[:-1] if s[-1] != "\n" else s[:-2]
                    elif key == curses.KEY_ENTER or key == 10:
                        input_window.clear()
                        input_window.refresh()
                        input_window.refresh()
                        if len(s):
                            stdscr.addstr(curr_row, 0, f"{s}\n")
                        #     for server side send this to server with some tags around it
                        curr_row, _ = stdscr.getyx()
                        s = ""
                        stdscr.refresh()
                    else:
                        input_window.addch(key)
                        s += chr(key)
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    curses.wrapper(main)
