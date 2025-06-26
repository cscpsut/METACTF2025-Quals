#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

const char* flag_filename = "flag.txt";
void clear_to_takeoff(long a1, long a2, long a3, long a4, long a5, const char* filename) {

    if (a1 == 0x1 && a2 == 0x2 && a3 == 0x3 &&
        a4 == 0x4 && a5 == 0x5) {

        printf("\n\x1b[32m=== CLEARED TO TAKEOFF ===\n");


        FILE* flag_file = fopen(filename, "r");
        if (flag_file == NULL) {
            printf("Error: Could not open flag file\n");
            exit(1);
        }


        char flag[100];
        if (fgets(flag, sizeof(flag), flag_file) == NULL) {
            printf("Error: Could not read flag\n");
            fclose(flag_file);
            exit(1);
    }


    printf("Flag: %s\n", flag);


    fclose(flag_file);
}
 else {
        printf("\n\x1b[31m<<< INCORRECT CLEARANCE PARAMETERS! ABORTING! >>>\x1b[0m\n");
        exit(1);
    }
}


void gadget1(){

    __asm__ __volatile__ (
        "pop %rdi\n"

        "ret\n"
    );
}
void gadget2(){

    __asm__ __volatile__ (
        "pop %rsi\n"

        "ret\n"
    );
}

void gadget3(){

    __asm__ __volatile__ (
        "pop %rdx\n"

        "ret\n"
    );
}
void gadget4(){

    __asm__ __volatile__ (
        "pop %rcx\n"

        "ret\n"
    );
}
void gadget5(){

    __asm__ __volatile__ (
        "pop %r8\n"

        "ret\n"
    );
}
void gadget6(){

    __asm__ __volatile__ (
        "pop %r9\n"

        "ret\n"
    );
}

void approach_control() {
    char runway_buffer[128];
    char *position_ptr = runway_buffer;

    printf("Airport Approach Control System\n");





    printf("Vector byte: ");
    fflush(stdout);


    read(0, position_ptr, 256);




    position_ptr++;

}
setup(){

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);


}
int main() {
    setup();

    printf("\n=== WELCOME TO METACTF INTERNATIONAL AIRPORT ===\n");
    printf("Your flight: CTF-007\n");
    printf("Destination: METACTF-FINALS\n");
    printf("Objective: gain takeoff clearance\n\n");

    approach_control();

    printf("\n<<< TAKEOFF ABORTED >>> Return to holding pattern\n");
    return 0;
}