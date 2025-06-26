#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <signal.h>
#include "asci.h"
#include "plane_ascii.h"

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    fflush(stdout);
    
}


void asci(){
write(1, asci_txt, asci_txt_len);
}

void crash(){

  show_plane_crash(7);
}

void smooth(const char *str) {
    while (*str) {

        printf("\033[31m%c", *str);  
        fflush(stdout);  
        usleep(50000);  
        str++;
    }
    printf("\033[0m\n");  
}

int main(int argc, const char **argv, const char **envp)
{
  setup();
  signal(SIGALRM, crash);
  alarm(15<<6);

  
  fflush(stdout);

  

  
   pid_t pid = fork();

    if (pid== 0){
    asci();
    show_plane_flying(5);
    smooth("*click* *Click*Shhh-sh Tssh. La.. Lad... Ladies and gentlemen, this is your captain Yaseen speaking. "
           "We are experiencing a critical emergency. We’ve lost control and are going down. "
           "Please remain calm and brace for impact. Follow the instructions of the flight attendants immediately—"
           "this is not a drill. Secure your oxygen masks and assume the brace position.\n"
           "I want to thank you all for flying with us today. On behalf of the crew, I want to say that we are "
           "doing everything in our power to ensure the safest possible outcome. "
           "Hold on tight, and may we all find strength in this moment. Godspeed.*"
            "IF ANY OF THE PASSENGERS COULD HELP CAPTAIN YASEEN FIND A LANDING SPOT PLEASE HURRY UP TO THE CABIN!!"
            "WE Are limit in TIME............");
    
   };
  size_t v3; 
  size_t v4;
  size_t v5;
  size_t v6;
  
  char greeting[8] = "QUICK "; 
  
  char prompt[56] = "find a landing LOCATION for us "; 
  prompt[31] = 0;
  
  char country_prompt[64] = "THAT SHOULD HAVE BEEN engough, telll us what to do now NOW!! ";
  country_prompt[62] = 0;
  
  char user_input[32]; 
  
 
  void *stack_ptr = &greeting;
  

  v3 = strlen(prompt);
  write(1, prompt, v3);
  

  read(0, user_input, 320);

  v4 = strlen(greeting);
  write(1, greeting, v4);
  
  v5 = strlen(user_input);
  write(1, user_input, v5);
  

  v6 = strlen(country_prompt);
  write(1, country_prompt, v6);
 
  read(0, user_input, 320);
  show_plane_crash(7);
  puts("Captain and his crew didn't survi...");
 
  
  return 0;
}
