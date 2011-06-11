/**
 * @brief set color on your console.
 * @see /usr/share/terminfo for TERM environmental variable
 * $ g++ d60.cpp -lcurses && TERM=xterm-xfree86 a./out a b c
 */
#include <iostream>
#include <ctime>
#include <curses.h>

/**
 * Use constant values defined in "curses.h".
 */
void set_console_color(int color_code)
{
    if (color_code < 0 || color_code > COLORS)
        return;
    std::cout << "\e[3" << color_code << 'm';
}

inline void print_title(char* title)
{
    set_console_color(COLOR_RED);
    std::cout << "-- " << title << " --" << "\r\n";
    set_console_color(COLOR_BLACK);
}

int main(int argc, char **argv)
{
    WINDOW *win = initscr();
    if (!win) {
        std::cout << "initialization error!!" << "\r\n";
        return 1;
    }
    start_color();
    print_title("Compile information.");
    std::cout << "This file name is '" << __FILE__ << "'" << "\r\n";
    std::cout << "Build at " << __DATE__ << " " << __TIME__ << "\r\n";

    print_title("Running information.");
    time_t now;
    now = time(NULL);
    set_console_color(COLOR_BLUE);
    std::cout << "Now: " << ctime(&now) << "\r\n";

    print_title("ARGUMENTS");
    for(int i=0; i<argc; i++)
        std::cout << "argv[" << i << "] = " << argv[i] << "\r\n";

    set_console_color(COLOR_GREEN);
    std::cout << "Running time: " << clock() / CLOCKS_PER_SEC << "[sec]" << "\r\n";
    if (!isendwin())
        endwin();
    return 0;
}

