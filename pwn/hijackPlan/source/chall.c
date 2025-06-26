#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <fcntl.h>
#include <dlfcn.h>


#define alert write(1, plane, strlen(plane));
#define alert_1 alert
#define alert_2 alert_1 alert
#define alert_3 alert_2 alert
#define alert_4 alert_3 alert
#define alert_5 alert_4 alert
#define alert_6 alert_5 alert
#define alert_7 alert_6 alert
#define alert_8 alert_7 alert
#define alert_9 alert_8 alert
#define alert_10 alert_9 alert
#define PLANE(N) alert_##N


const char *text_colors[] = {
    "\033[31m",      // RED
    "\033[33m",      // GOLD
    "\033[37m",      // WHITE
    "\033[34m",      // BLUE
};

const char *bg_colors[] = {
    "\033[41m",      // BG RED
    "\033[43m",      // BG GOLD
    "\033[47m",      // BG WHITE
    "\033[44m",      // BG BLUE
};

const char *text_styles[] = {
    "\033[4m",       // underline
    "\033[5m",       // blink
    "\033[1m",       // bold
};

void clear_buffer(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int random_choice(int max) {
    return rand() % max;
}


void menu() { 

    const char *seat="1⚪ View vault:\n";
    const char *change_ur_seat="2⚪Steal:";
    write(1,seat , strlen(seat));
    write(1,change_ur_seat,strlen(change_ur_seat));
}
int main() {
    clear_buffer();
    char c ;
    puts(" ⚠️ Warninig Flashing lights. Can induce seizures for people with epilepsy, only press Y to continue ⚠️ : ");
    scanf(" %c",&c);
    if (c != 'y' && c !='Y')
        exit(1);
    char plane[] = "              ##### | #####\n             # _ _ #|# _ _ #\n             #      |      #\n       |       ############\n                   # #\n|                  # #\n                  #   #\n       |     |    #   #      |        |\n|  |             #     #               |\n       | |   |   # .-. #         |\n                 #( O )#    |    |     |\n|  ################. .###############  |\n ##  _ _|____|     ###     |_ __| _  ##\n#  |                                |  #\n#  |    |    |    |   |    |    |   |  #\n ######################################\n                 #     #\n                  #####\n             OOOOOOO|OOOOOOO\n                    U\n\n\n\n";
    clear_buffer();
    srand(time(NULL));
    
    // Colorful alert effect
    for (int i = 0; i < 30; ++i) {
        size_t text_choices_n = sizeof text_colors / sizeof text_colors[0];
        size_t bg_choices_n = sizeof bg_colors / sizeof bg_colors[0];
        size_t style_choices_n = sizeof text_styles / sizeof text_styles[0];
        const char *text_color = text_colors[random_choice(text_choices_n)];
        const char *bg_color = bg_colors[random_choice(bg_choices_n)];
        const char *style = text_styles[random_choice(style_choices_n)];
        printf("%s%s%s", text_color, bg_color, style);
        PLANE(10);PLANE(10);PLANE(10);PLANE(10);PLANE(10);
        PLANE(10);PLANE(10);PLANE(10);PLANE(10);PLANE(10);
        PLANE(10);PLANE(10);PLANE(10);PLANE(10);PLANE(10);
        usleep(75000);
    }

    menu();

    printf("\n\n\n");
    puts("                                 __|__");
    puts("                          --o--o--(_)--o--o--");
    char vault_name[32];
    unsigned long balance, cash_money;
    int choice;
    
    for( int i = 0; i <2 ; i++){
        scanf("%2d", &choice);
        if (choice == 1) {
            scanf("%10s", vault_name);
            void *vault = dlsym(RTLD_DEFAULT, vault_name);
            printf("%p\n", vault);
        } else if (choice == 2) {
            scanf("%lu %lu", &balance, &cash_money);
            *(unsigned long*)balance = cash_money;
        }
        else{
            exit(1);
        }
    }
    
    puts("Your current balance is");
    puts("$0");
    puts("Please set down while the plane takes off");
    return 0;
}


// gcc chall.c -no-pie -O0 -o hijack
