#include <stdio.h>
#include <unistd.h> // for usleep function
#include <stdlib.h> // for rand and srand functions
#include <time.h>   // for time function

// ANSI color escape codes
#define ANSI_COLOR_RED     "[31m"
#define ANSI_COLOR_GREEN   "[32m"
#define ANSI_COLOR_YELLOW  "[33m"
#define ANSI_COLOR_BLUE    "[34m"
#define ANSI_COLOR_MAGENTA "[35m"
#define ANSI_COLOR_CYAN    "[36m"
#define ANSI_COLOR_RESET   "[0m"

int main() {
    char *message = "Hello, World! this is from resonite so that i know it works";
    int i;

    // Seed the random number generator
    srand(time(NULL));

    for (i = 0; message[i] != '\0'; i++) {
        // Generate a random number from 0 to 5 for color selection
        int color_code = rand() % 6;
        const char *color;

        // Select color based on random number
        switch (color_code) {
            case 0: color = ANSI_COLOR_RED; break;
            case 1: color = ANSI_COLOR_GREEN; break;
            case 2: color = ANSI_COLOR_YELLOW; break;
            case 3: color = ANSI_COLOR_BLUE; break;
            case 4: color = ANSI_COLOR_MAGENTA; break;
            case 5: color = ANSI_COLOR_CYAN; break;
            default: color = ANSI_COLOR_RESET; break;
        }

        // Print the character in the selected color
        printf("%s \n %c", color, message[i]);
        fflush(stdout); // Ensure the character is printed immediately

        // Pause for 0.5 seconds (500000 microseconds)
        usleep(5000); // usleep is in microseconds, 500000 microseconds = 0.5 seconds
    }

    // this should print the contents to the console correctly with the color

return 0;
}
