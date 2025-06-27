# Route Hijack Challenge - Reverse Engineering Writeup

## Challenge Information

**Category:** Reverse Engineering  
**Author:** H04X  
**Difficulty:** Medium  

### Challenge Description
A top-secret aviation system has been compromised, and mission-critical flight data is encrypted using military-grade cipher protocols. Intelligence suggests the system generates a random security clearance code, but there might be a flaw in how the decryption process works.

## Initial Analysis

### File Examination
```bash
$ ls
chall

$ file chall
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, 
interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=67b34ccf2de717ae3a8af92422f15f96fb05a307, 
for GNU/Linux 3.2.0, stripped
```

**Key Observations:**
- Single ELF 64-bit executable
- Position Independent Executable (PIE)
- Stripped binary (no debug symbols)
- Dynamically linked

## Static Analysis

### Main Function Analysis

Using Ghidra for reverse engineering, the main function reveals the following logic:

```c
undefined8 FUN_00102aec(void)
{
  int iVar1;
  time_t tVar2;
  undefined8 uVar3;
  int local_1c;    // User input
  int local_18;    // Copy of user input
  int local_14;    // Random number (1-10000)
  int local_10;    // Loop counter
  int local_c;     // Loop counter
  
  FUN_0010290b();                    // Setup function
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);                // Seed RNG with current time
  iVar1 = rand();
  local_14 = iVar1 % 10000 + 1;     // Generate random number 1-10000
  
  printf(&DAT_00103ad0);             // Prompt for clearance code
  __isoc99_scanf(&DAT_00103afa, &local_1c);  // Read user input
  
  // Display processing messages
  puts(&DAT_00103b00);
  puts(&DAT_00103b28);
  for (local_c = 0; local_c < 3; local_c = local_c + 1) {
    putchar(0x2e);
    fflush(stdout);
  }
  putchar(10);
  
  local_18 = local_1c;
  
  if (local_14 == local_1c) {        // Check if user input matches random number
    FUN_00102a77();                  // Success message function
    
    // Decrypt and print flag
    for (local_10 = 0; local_10 < DAT_00106204; local_10 = local_10 + 1) {
      local_18 = (*(code *)(&PTR_FUN_00106220)[local_10])(local_14);
      putchar((int)(char)local_18);
    }
    
    // Display success messages
    puts("\n");
    puts(&DAT_00103b60);
    puts(&DAT_00103b88);
    puts(&DAT_00103bb0);
    uVar3 = 0;
  }
  else {
    FUN_001029f3();                  // Failure message function
    uVar3 = 1;
  }
  return uVar3;
}
```

### Key Findings

1. **Random Number Generation**: The program generates a random number between 1-10000 using the current time as seed
2. **User Authentication**: User must guess the exact random number to proceed
3. **Decryption Process**: If authenticated, the program calls functions from `PTR_FUN_00106220` array using the random number as a decryption key
4. **Vulnerability**: The decryption functions are deterministic - same key always produces same output

### Function Pointer Array Analysis

The `PTR_FUN_00106220` array contains addresses of multiple decryption functions:

```assembly
PTR_FUN_00106220:
00106220    addr    FUN_001021a9
00106228    addr    FUN_001021bb
00106230    addr    FUN_001021cd
... (continuing for ~100 functions)
```

**Analysis of Decryption Functions:**
- Each function performs XOR operations between encrypted data and some value
- Functions follow the same pattern: `encrypted_byte XOR some value = decrypted_byte`
- The key (random number) is passed to each function sequentially

## Vulnerability Analysis

### The Flaw
The main vulnerability lies in the predictable nature of the decryption process:

1. **Fixed Encrypted Data**: The encrypted flag data remains constant
2. **Limited Key Space**: Only 10,000 possible keys (1-10000)
3. **Deterministic Decryption**: Same key always produces same output
4. **No Rate Limiting**: Program can be executed multiple times

### Attack Vector
Since we cannot predict the random number, but we know:
- The key space is limited (1-10000)
- The decryption is deterministic
- We can control the key through binary patching

## Exploitation Strategy

### Approach 1: Binary Patching (Recommended)

Instead of guessing the random number, we can patch the binary to:
1. Bypass the random number check
2. Use our input directly as the decryption key

#### Patch 1: Bypass Authentication Check
```assembly
# Original (fail if not equal):
00102bcb    JNZ    LAB_00102c65

# Patched (fail if equal):
00102bcb    JZ     LAB_00102c65
```

This inverts the condition, making the program succeed when our input doesn't match the random number.

#### Patch 2: Use Input as Decryption Key
```assembly
# Original (use random number):
00102bfc    MOV    EAX, dword ptr [RBP + local_14]

# Patched (use user input):
00102bfc    MOV    EAX, dword ptr [RBP + local_18]
```

This changes the decryption key source from the random number to our input.

### Approach 2: GDB Manipulation (Alternative)

Use GDB to:
1. Set breakpoint before random number generation
2. Manually set the random number to our desired value
3. Continue execution

However, this approach is slower for brute-forcing multiple keys.

## Solution Implementation

### Step 1: Apply Binary Patches

Using a hex editor or binary patching tool, apply the two patches mentioned above.

### Step 2: Brute Force Script

```python
#!/usr/bin/env python3
from pwn import *
import sys

def run_chall_with_number(number):
    try:
        p = process('./challPATCHED')
        p.sendline(str(number).encode())

        try:
            output = p.recvall(timeout=2).decode('utf-8', errors='ignore')
        except EOFError:
            output = p.recvall().decode('utf-8', errors='ignore')

        p.close()
        
        return output
    
    except Exception as e:
        log.error(f"Error running chall with {number}: {e}")
        return ""

def main():
    context.log_level = 'error'
    
    log.info("Starting search for METACTF in chall binary output...")
    log.info("Testing numbers from 1 to 10000...")
    
        
    for i in range(1, 10001):
        output = run_chall_with_number(i)
        
        if "METACTF" in output:
            log.success(f"Found METACTF with number: {i}")
            log.success(f"Full output:")
            print("-" * 50)
            print(output)
            print("-" * 50)
            return
    
    log.failure("Search completed. METACTF not found in any output from 1 to 10000 using either method.")

if __name__ == "__main__":
    main()
```

### Step 3: Execute Attack

```bash
$ python3 exploit.py
[*] Starting brute force attack on decryption key...
[*] Testing keys from 1 to 10000...
[*] Tested 1000/10000 keys...
[*] Tested 2000/10000 keys...
[+] Flag found with key: 2847
[+] Decrypted output:
------------------------------------------------------------
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🛩  CLASSIFIED FLIGHT CONTROL SYSTEM 🛩                    ║
║                          ✈  TOP SECRET CLEARANCE REQUIRED ✈                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  AUTHORIZATION CODE REQUIRED FOR FLIGHT MANIFEST DECRYPTION                 ║
║                                                                              ║
║  🎯 Mission Briefing:                                                        ║
║     A classified flight manifest has been encrypted using advanced          ║
║     aviation cipher protocols. Only authorized personnel with the           ║
║     correct security clearance code can decrypt the mission details.        ║
║                                                                              ║
║  📡 System Status: ACTIVE                                                    ║
║  🔐 Encryption: Multi-layer aircraft-specific XOR cipher                    ║
║  ⚠  Security Level: MAXIMUM                                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔑 Enter your security clearance code: 
🔍 Verifying authorization...
⏳ Checking against flight control database...
...

✅ ═══════════════════════════════════════════════════════════════════════════ ✅
                        🔓 AUTHORIZATION ACCEPTED 🔓
                      DECRYPTING FLIGHT MANIFEST...
✅ ═══════════════════════════════════════════════════════════════════════════ ✅

📋 CLASSIFIED MISSION DATA:
═══════════════════════════
Preflight complete. You're cleared for takeoff, Captain. 
destination: METACTF{cabin_flag_pressure_normal}

🎯 Mission decryption complete! 
🛩  All aircraft systems nominal
✈  Ready for takeoff, pilot!
------------------------------------------------------------
```

## Flag

**METACTF{cabin_flag_pressure_normal}**
