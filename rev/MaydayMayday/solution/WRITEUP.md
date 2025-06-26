## Challenge - Mayday Mayday [Rev]

### Description

```
An aircraft is requesting access to restricted airspace. The terminal only accepts a valid pilot clearance code. anything else triggers decoy responses and failsafes.
```

### Author:

```
H04X
```
---

### Checking the chall files

```
┌──(kali㉿kali)-[Mayday_Mayday]
└─$ ls
chall
                                                                                                                                                                                                                                            
┌──(kali㉿kali)-[Mayday_Mayday]
└─$ file chall                   
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=3c8e8f8b7c29db438dfc74bdc329dc28a994dca2, for GNU/Linux 3.2.0, not stripped
```

here we can see we have 1 file ```chall``` which is an ELF ```64-bit``` file and it is not stripped 

---

### Reversing the Binary 

#### Analyzing Main

```c

undefined8 main(void)

{
  int iVar1;
  size_t sVar2;
  char local_218 [512];
  undefined8 local_18;
  int local_10;
  int local_c;
  
  animated_border();
  typewriter_print(&DAT_00103330,0x1e);
  typewriter_print(&DAT_00103378,0x1e);
  typewriter_print(&DAT_001033c0,0x1e);
  typewriter_print(&DAT_00103408,0x1e);
  typewriter_print(&DAT_00103458,0x1e);
  animated_border();
  putchar(10);
  spinning_radar(3);
  animated_dots(&DAT_001034a0,3);
  iVar1 = radar_sweep();
  if (iVar1 != 0) {
    blinking_alert("MAYDAY! MAYDAY! Enemy radar lock detected!",3);
    typewriter_print(&DAT_001034f8,0x32);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  progress_bar(&DAT_00103528,0x5dc);
  iVar1 = check_flight_time();
  if (iVar1 == 0) {
    typewriter_print(&DAT_001035c0,0x28);
    fflush(stdout);
    fgets(local_218,0x200,stdin);
    sVar2 = strcspn(local_218,"\n");
    local_218[sVar2] = '\0';
    putchar(10);
    animated_dots(&DAT_001035e8,4);
    atc_system();
    animated_dots(&DAT_00103610,3);
    local_18 = calculate_bearing(0x40445b3d07c84b5e,0xc05280624dd2f1aa,0x4049c0f27bb2fec5,
                                 0xbfc05bc01a36e2eb);
    typewriter_print(&DAT_00103634,0x28);
    printf("%.2f degrees\n",local_18);
    progress_bar(&DAT_00103659,2000);
    iVar1 = validate_flight_plan(local_218);
    if (iVar1 == 0) {
      putchar(10);
      blinking_alert("ACCESS DENIED - INVALID CLEARANCE",2);
      puts(&DAT_001037c0);
      typewriter_print(&DAT_00103840,0x32);
      typewriter_print(&DAT_00103870,0x32);
      typewriter_print(&DAT_00103898,0x32);
      puts(&DAT_001037c0);
      putchar(10);
      animated_dots(&DAT_001038c8,3);
      fake_transponder();
    }
    else {
      putchar(10);
      for (local_c = 0; local_c < 3; local_c = local_c + 1) {
        puts(&DAT_00103678);
        usleep(100000);
      }
      typewriter_print(&DAT_001036f8,0x32);
      typewriter_print(&DAT_00103728,0x32);
      typewriter_print(&DAT_00103750,0x32);
      typewriter_print(&DAT_00103776,0x32);
      typewriter_print(local_218,0x1e);
      putchar(10);
      for (local_10 = 0; local_10 < 3; local_10 = local_10 + 1) {
        puts(&DAT_00103678);
        usleep(100000);
      }
    }
    return 0;
  }
  blinking_alert("ALTITUDE WARNING: Abnormal flight pattern detected!",3);
  typewriter_print(&DAT_00103588,0x32);
                    /* WARNING: Subroutine does not return */
  exit(1);
}

```

**Analysis:** The code simulates an aviation/air traffic control system with various security checks. First check is the ```radar_sweep()```, Then ```check_flight_time()```, and lastly the user input validation in the ``` validate_flight_plan()``` function.


#### Analyzing radar_sweep()

```c

bool radar_sweep(void)

{
  long lVar1;
  
  lVar1 = ptrace(PTRACE_TRACEME,0,1,0);
  return lVar1 == -1;
}
```

**Analysis:** This is a basic ptrace anti-debugger.


#### Analyzing check_flight_time()

```c

bool check_flight_time(void)

{
  clock_t cVar1;
  clock_t cVar2;
  int local_c;
  
  cVar1 = clock();
  for (local_c = 0; local_c < 1000000; local_c = local_c + 1) {
  }
  cVar2 = clock();
  return 0.1 < (double)(cVar2 - cVar1) / 1000000.0;
}

```

**Analysis:** This function detects execution slowdown, which might imply debugging or sandboxing so its essentinaly another anti-debugger.


#### Analyzing validate_flight_plan()

```c
undefined8 validate_flight_plan(char *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  char local_58 [32];
  char local_38 [23];
  undefined1 local_21;
  int local_14;
  int local_10;
  int local_c;
  
  sVar1 = strlen(param_1);
  if (sVar1 == 0x20) {
    for (local_c = 0; local_c < 0x20; local_c = local_c + 1) {
      if (((((param_1[local_c] < 'A') || ('Z' < param_1[local_c])) &&
           ((param_1[local_c] < 'a' || ('z' < param_1[local_c])))) &&
          (((param_1[local_c] < '0' || ('9' < param_1[local_c])) && (param_1[local_c] != '{')))) &&
         (((param_1[local_c] != '}' && (param_1[local_c] != '_')) && (param_1[local_c] != '-')))) {
        return 0;
      }
    }
    if (((*param_1 == 'M') && (param_1[1] == 'E')) &&
       ((param_1[2] == 'T' &&
        ((((param_1[3] == 'A' && (param_1[4] == 'C')) && (param_1[5] == 'T')) &&
         ((param_1[6] == 'F' && (param_1[7] == '{')))))))) {
      if (param_1[0x1f] == '}') {
        for (local_10 = 0; local_10 < 0x17; local_10 = local_10 + 1) {
          local_38[local_10] = param_1[(long)local_10 + 8];
        }
        local_21 = 0;
        phonetic_decode(local_38);
        aviation_decrypt(local_38,0x17,0x17);
        builtin_strncpy(local_58,"#~&# &\'v:m#\" $r:t&n\' ::",0x17);
        for (local_14 = 0; local_14 < 0x17; local_14 = local_14 + 1) {
          if (local_38[local_14] != local_58[local_14]) {
            return 0;
          }
        }
        uVar2 = 1;
      }
      else {
        uVar2 = 0;
      }
    }
    else {
      uVar2 = 0;
    }
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}
```

**Analysis:** This function validates the user input through multiple steps:
First, the user input must be ```32 chars``` long and contains only ```Uppercase and lowercase letters, digits, and { } _ -``` then the user input must start with ```METACTF{``` and ends in ```}``` then the characters in the middle (without the flag format) will be passed into 2 functions. ```phonetic_decode()``` and ```aviation_decrypt()```.
lastly, the output of these 2 function will be comapred to this string ```#~&# &\'v:m#\" $r:t&n\' ::``` if they match the input is validated.


#### Analyzing phonetic_decode()

```c

void phonetic_decode(long param_1)

{
  int iVar1;
  undefined4 local_c;
  
  for (local_c = 0; *(char *)(param_1 + local_c) != '\0'; local_c = local_c + 1) {
    if ((*(char *)(param_1 + local_c) < 'a') || ('z' < *(char *)(param_1 + local_c))) {
      if (('@' < *(char *)(param_1 + local_c)) && (*(char *)(param_1 + local_c) < '[')) {
        iVar1 = *(char *)(param_1 + local_c) + -0x34;
        *(char *)(param_1 + local_c) = (char)iVar1 + (char)(iVar1 / 0x1a) * -0x1a + 'A';
      }
    }
    else {
      iVar1 = *(char *)(param_1 + local_c) + -0x54;
      *(char *)(param_1 + local_c) = (char)iVar1 + (char)(iVar1 / 0x1a) * -0x1a + 'a';
    }
  }
  return;
}

```

**Analysis:** This function just do a rot13 encoding.


#### Analyzing phonetic_decode()

```c

void aviation_decrypt(long param_1,int param_2,byte param_3)

{
  undefined4 local_c;
  
  for (local_c = 0; local_c < param_2; local_c = local_c + 1) {
    *(byte *)(param_1 + local_c) = *(byte *)(param_1 + local_c) ^ param_3;
  }
  return;
}

```

**Analysis:** This function xor the user input with param3 ```aviation_decrypt(local_38,0x17,0x17)``` from this we can see the key is ```0x17```.

---

### Solution 

After understanding the code i know what i should do to get the flag 
because we already have the result of our input ```#~&# &\'v:m#\" $r:t&n\' ::``` all we need to do is reverse the operation orders to get the correct flag.
first we xor this string with 0x17 then we reverse the rot13 operation

```py
def phonetic_decode(s):
    # Reverse ROT13 (same as forward ROT13)
    result = []
    for ch in s:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


def aviation_decrypt(data, frequency):
    return ''.join(chr(ord(c) ^ frequency) for c in data)


def main():
    # #~&# &\'v:m#\" $r:t&n\' ::
    authorized_route = [35,126,38,35,32,38,39,118,58,109,35,34,32,36,114,58,116,38,110,39,32,58,58]

    print("Original bytes:")
    print(" ".join(chr(b) for b in authorized_route))

    # Step 1: Reverse XOR with 23 (0x17)
    xor_reversed = ''.join(chr(b ^ 23) for b in authorized_route)
    print("\nAfter XOR reversal:")
    print(" ".join(f"{ord(c)}('{c}')" for c in xor_reversed))

    # Step 2: Reverse ROT13
    rot13_reversed = phonetic_decode(xor_reversed)
    print("\nAfter ROT13 reversal:")
    print(" ".join(f"{ord(c)}('{c}')" for c in rot13_reversed))

    print(f"\nDecoded middle part: '{rot13_reversed}'")
    print(f"Full flag: METACTF{{{rot13_reversed}}}")

if __name__ == "__main__":
    main()
```

```
┌──(kali㉿kali)-[Mayday_Mayday]
└─$ python sol.py
Original bytes:
# ~ & #   & ' v : m # "   $ r : t & n '   : :

After XOR reversal:
52('4') 105('i') 49('1') 52('4') 55('7') 49('1') 48('0') 97('a') 45('-') 122('z') 52('4') 53('5') 55('7') 51('3') 101('e') 45('-') 99('c') 49('1') 121('y') 48('0') 55('7') 45('-') 45('-')

After ROT13 reversal:
52('4') 118('v') 49('1') 52('4') 55('7') 49('1') 48('0') 110('n') 45('-') 109('m') 52('4') 53('5') 55('7') 51('3') 114('r') 45('-') 112('p') 49('1') 108('l') 48('0') 55('7') 45('-') 45('-')

Decoded middle part: '4v14710n-m4573r-p1l07--'
Full flag: METACTF{4v14710n-m4573r-p1l07--}
```

FLAG: ```METACTF{4v14710n-m4573r-p1l07--}```