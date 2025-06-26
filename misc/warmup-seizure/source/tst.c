#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
int main(){
    printf("Hello Passenger, Welcome on board!! ");
    fflush(stdout);
    
    srand(time(NULL));
    
    // Array of colors: {hex_bg, r, g, b}
    char colors[][4][10] = {
        {"#FFFFFF", "255", "255", "255"}, // White
        {"#FFD700", "255", "215", "0"},   // Gold
        {"#FF0000", "255", "0", "0"},     // Red
        {"#00FF00", "0", "255", "0"},     // Green
        {"#0000FF", "0", "0", "255"},     // Blue
        {"#FF00FF", "255", "0", "255"},   // Magenta
        {"#00FFFF", "0", "255", "255"},   // Cyan
        {"#FFA500", "255", "165", "0"},   // Orange
        {"#800080", "128", "0", "128"},   // Purple
        {"#8B4513", "139", "69", "19"}    // Brown
    };
    
    int flag_printed = 0;
    
    for(int i = 0; i < 10; i++) {
        // Change background color
        printf("\033]11;%s\007", colors[i][0]);
        
        if(flag_printed) {
            // Delete previous flag (backspace over it)
            for(int j = 0; j < 35; j++) printf("\b \b");
        }
        
        // Print flag in matching color (invisible)
        printf("\033[38;2;%s;%s;%smMETACTF{flaaaaaaaag_yes_this_a_flag}\033[0m", 
               colors[i][1], colors[i][2], colors[i][3]);
        
        flag_printed = 1;
        fflush(stdout);
        usleep(3000); // 300ms delay
        
        // Delete the flag after printing it
        for(int j = 0; j < 35; j++) printf("\b \b");
        fflush(stdout);
    }
    
    // Choose random final color
    int final_color = rand() % 10;
    printf("\033]11;%s\007", colors[final_color][0]);
    
    // Print final hidden flag and immediately delete it
    printf("\033[38;2;%s;%s;%smMETACTF{flaaaaaaaag_yes_this_a_flag}\033[0m", 
           colors[final_color][1], colors[final_color][2], colors[final_color][3]);
    fflush(stdout);
    
    // Delete the final flag
    for(int j = 0; j < 35; j++) printf("\b \b");
    
    // Clear everything with carriage return
    printf("\r");
    fflush(stdout);
    
    return 0;
}