/**
 * @brief set color on your console.
 */
#include <iostream>
#include <ctime>

/**
 * @param color_code is from 0 to 7, which mean as folows.
 *      - 0: Black
 *      - 1: Red
 *      - 2: Green
 *      - 3: Yellow
 *      - 4: Blue
 *      - 5: Purple
 *      - 6: Light blue
 *      - 7: White
 */
void set_console_color(int color_code)
{
    if (color_code < 0 || color_code > 7)
        return;
    std::cout << "\33[3" << color_code << 'm';
}

inline void print_title(char* title)
{
    set_console_color(1);
    std::cout << "-- " << title << " --" << std::endl;
    set_console_color(0);
}

int main(int argc, char **argv)
{
    print_title("Compile information.");
    std::cout << "This file name is '" << __FILE__ << "'" << std::endl;
    std::cout << "Build at " << __DATE__ << " " << __TIME__ << std::endl;

    print_title("Running information.");
    time_t now;
    now = time(NULL);
    set_console_color(4);
    std::cout << "Now: " << ctime(&now) << std::endl;

    print_title("ARGUMENTS");
    for(int i=0; i<argc; i++)
        std::cout << "argv[" << i << "] = " << argv[i] << std::endl;

    set_console_color(2);
    std::cout << "Running time: " << clock() / CLOCKS_PER_SEC << "[sec]" << std::endl;
    return 0;
}

