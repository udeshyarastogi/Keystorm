import curses
import time
import random

# Word list for random generation
WORDS = [
    "python", "keyboard", "function", "variable", "syntax", "debug", "program",
    "script", "string", "input", "output", "compile", "loop", "condition",
    "object", "class", "method", "exception", "typing", "test"
]

def get_random_words(count=30):
    return " ".join(random.choices(WORDS, k=count))

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Continuous Typing Test!\n", curses.color_pair(4))
    stdscr.addstr("Type as fast and accurately as you can.\n")
    stdscr.addstr("Press [Enter] to stop | Press [Shift] to restart anytime\n")
    stdscr.addstr("\nPress any key to begin...")
    stdscr.refresh()
    stdscr.getkey()

def draw_text(stdscr, target_text, user_input, wpm, errors):
    stdscr.clear()

    stdscr.addstr("Typing Speed Test\n", curses.color_pair(4))
    stdscr.addstr(f"WPM: {wpm}    Errors: {errors}\n\n", curses.color_pair(4))

    for i in range(len(target_text)):
        if i < len(user_input):
            if user_input[i] == target_text[i]:
                stdscr.addstr(target_text[i], curses.color_pair(1))  # correct
            else:
                stdscr.addstr(target_text[i], curses.color_pair(2))  # incorrect
        else:
            stdscr.addstr(target_text[i], curses.color_pair(3))      # not typed yet

    stdscr.refresh()

def typing_test(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # correct
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # incorrect
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # upcoming
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # UI

    while True:
        target_text = get_random_words()
        user_input = ""
        errors = 0
        start_time = time.time()
        stdscr.nodelay(True)

        while True:
            elapsed = max(time.time() - start_time, 1)
            wpm = round((len(user_input) / 5) / (elapsed / 60))

            draw_text(stdscr, target_text, user_input, wpm, errors)

            try:
                key = stdscr.get_wch()
            except:
                continue

            # Shift restarts
            if isinstance(key, str) and key.isupper():
                break

            # Enter ends test
            if key == '\n':
                stdscr.nodelay(False)
                stdscr.clear()
                stdscr.addstr(f"\nTest ended.\nFinal WPM: {wpm}\nTotal Errors: {errors}\n\n")
                stdscr.addstr("Press any key to exit...")
                stdscr.getkey()
                return

            # Handle backspace
            if key in ('\b', '\x7f', curses.KEY_BACKSPACE):
                if len(user_input) > 0:
                    user_input = user_input[:-1]
                continue

            # Add to input
            if len(user_input) < len(target_text) and isinstance(key, str):
                user_input += key
                if key != target_text[len(user_input) - 1]:
                    errors += 1

            # Refill text when done
            if len(user_input) >= len(target_text):
                target_text += " " + get_random_words(10)

def main():
    curses.wrapper(run_app)

def run_app(stdscr):
    start_screen(stdscr)
    typing_test(stdscr)

if __name__ == "__main__":
    main()
