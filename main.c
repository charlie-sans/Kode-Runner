#include <stdio.h>
// delay 
void delay(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < 100000; j++) {
        }
    }
}
int main() {
    // print the message character by character
    char message[] = "would you like to play a game?";
    for (int i = 0; message[i] != '\0'; i++) {
        printf("%c", message[i]);
        delay(500);
    }
    return 0;
}