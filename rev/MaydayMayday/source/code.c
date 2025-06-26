#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>
#include <math.h>

void typewriter_print(const char* text, int delay_ms) {
    for (int i = 0; text[i] != '\0'; i++) {
        printf("%c", text[i]);
        fflush(stdout);
        usleep(delay_ms * 1000);
    }
}

void animated_border() {
    const char* frames[] = {
        "✈️ ═══════════════════════════════════════════════════════════ ✈️",
        "🛩️ ═══════════════════════════════════════════════════════════ 🛩️",
        "🚁 ═══════════════════════════════════════════════════════════ 🚁",
        "✈️ ═══════════════════════════════════════════════════════════ ✈️"
    };
    
    for (int i = 0; i < 4; i++) {
        printf("\r%s", frames[i]);
        fflush(stdout);
        usleep(200000); // 200ms
    }
    printf("\n");
}

void spinning_radar(int spins) {
    const char* radar_frames[] = {"📡", "📡", "📡", "📡"};
    const char* directions[] = {"|", "/", "-", "\\"};
    
    for (int spin = 0; spin < spins; spin++) {
        for (int frame = 0; frame < 4; frame++) {
            printf("\r%s Radar scanning %s", radar_frames[frame], directions[frame]);
            fflush(stdout);
            usleep(150000); // 150ms
        }
    }
    printf("\n");
}

void animated_dots(const char* message, int dots_count) {
    printf("%s", message);
    fflush(stdout);
    for (int i = 0; i < dots_count; i++) {
        printf(".");
        fflush(stdout);
        usleep(300000); // 300ms
    }
    printf("\n");
}

void blinking_alert(const char* message, int blinks) {
    for (int i = 0; i < blinks; i++) {
        printf("\r🔴 %s", message);
        fflush(stdout);
        usleep(400000); // 400ms
        printf("\r   %*s", (int)strlen(message), ""); // Clear with spaces
        fflush(stdout);
        usleep(200000); // 200ms
    }
    printf("\r🔴 %s\n", message);
}

void progress_bar(const char* label, int duration_ms) {
    const int bar_width = 30;
    printf("%s [", label);
    
    for (int i = 0; i <= bar_width; i++) {
        printf("\r%s [", label);
        for (int j = 0; j < bar_width; j++) {
            if (j < i) printf("█");
            else if (j == i) printf("▓");
            else printf("░");
        }
        printf("] %d%%", (i * 100) / bar_width);
        fflush(stdout);
        usleep((duration_ms * 1000) / bar_width);
    }
    printf("\n");
}

// Anti-debugging: Radar detection system
int radar_sweep() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        return 1; // Enemy radar detected (debugger)
    }
    return 0;
}

// Anti-debugging: Flight time analysis
int check_flight_time() {
    clock_t takeoff = clock();
    volatile int altitude = 0;
    // Simulate flight calculations
    for (int i = 0; i < 1000000; i++) {
        altitude += i;
    }
    clock_t landing = clock();
    double flight_time = ((double)(landing - takeoff)) / CLOCKS_PER_SEC;
    
    // If flight is too slow, suspicious activity detected
    if (flight_time > 0.1) {
        return 1;
    }
    return 0;
}

// Decoy transponder signal
void fake_transponder() {
    char fake_callsign[] = "METACTF{fake_mayday_wrong_runway}";
    typewriter_print("📡 Emergency Transponder: ", 50);
    typewriter_print(fake_callsign, 30);
    printf("\n");
}

// Aviation encryption: Similar to aircraft communication encoding
void aviation_decrypt(char* data, int len, char frequency) {
    for (int i = 0; i < len; i++) {
        data[i] ^= frequency;
    }
}

// ICAO phonetic alphabet cipher
void phonetic_decode(char* str) {
    for (int i = 0; str[i]; i++) {
        if (str[i] >= 'a' && str[i] <= 'z') {
            str[i] = ((str[i] - 'a' + 13) % 26) + 'a';
        } else if (str[i] >= 'A' && str[i] <= 'Z') {
            str[i] = ((str[i] - 'A' + 13) % 26) + 'A';
        }
    }
}

// Aviation Base64 (modified for aircraft systems)
void decode_flight_data(char* input, char* output) {
    const char* aviation_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    int len = strlen(input);
    int j = 0;
    
    for (int i = 0; i < len; i += 4) {
        int navigation_data = 0;
        for (int k = 0; k < 4 && i + k < len; k++) {
            char signal = input[i + k];
            int bearing = 0;
            for (int l = 0; l < 64; l++) {
                if (aviation_alphabet[l] == signal) {
                    bearing = l;
                    break;
                }
            }
            navigation_data = (navigation_data << 6) | bearing;
        }
        
        output[j++] = (navigation_data >> 16) & 0xFF;
        output[j++] = (navigation_data >> 8) & 0xFF;
        output[j++] = navigation_data & 0xFF;
    }
    output[j] = '\0';
}

// Secure communication protocol check
int secure_comms_check(const char* callsign1, const char* callsign2) {
    int interference = 0;
    while (*callsign1 && *callsign2) {
        interference |= (*callsign1++ ^ *callsign2++);
    }
    return interference | (*callsign1 ^ *callsign2);
}

// Flight plan validation system
int validate_flight_plan(char* clearance_code) {
    if (strlen(clearance_code) != 32) {
        return 0;
    }
    
    // Flight Level 2: Character validation (aviation standard)
    for (int i = 0; i < 32; i++) {
        if (!((clearance_code[i] >= 'A' && clearance_code[i] <= 'Z') || 
              (clearance_code[i] >= 'a' && clearance_code[i] <= 'z') || 
              (clearance_code[i] >= '0' && clearance_code[i] <= '9') ||
              clearance_code[i] == '{' || clearance_code[i] == '}' || 
              clearance_code[i] == '_' || clearance_code[i] == '-')) {
            return 0;
        }
    }
    
    // Flight Level 3: Callsign format validation - now checking for METACTF{
    if (clearance_code[0] != 'M' || clearance_code[1] != 'E' || 
        clearance_code[2] != 'T' || clearance_code[3] != 'A' ||
        clearance_code[4] != 'C' || clearance_code[5] != 'T' ||
        clearance_code[6] != 'F' || clearance_code[7] != '{') {
        return 0;
    }
    
    if (clearance_code[31] != '}') {
        return 0;
    }
    
    // Flight Level 4: Navigation system validation
    char flight_path[24];
    for (int i = 0; i < 23; i++) {
        flight_path[i] = clearance_code[i+8];
    }
    flight_path[23] = '\0';
    
    // Apply ROT13 decoding first
    phonetic_decode(flight_path);
    
    // Then decrypt with radio frequency (XOR with 23 - aviation frequency)
    aviation_decrypt(flight_path, 23, 23);
    
    char authorized_route[] = {35,126,38,35,32,38,39,118,58,109,35,34,32,36,114,58,116,38,110,39,32,58,58};
    
    // Compare the processed flight path with authorized route
    for (int i = 0; i < 23; i++) {
        if (flight_path[i] != authorized_route[i]) {
            return 0;
        }
    }
    
    return 1;
}

// Air traffic control system
void atc_system() {
    char atc_data[] = {0x43, 0x6C, 0x65, 0x61, 0x72, 0x65, 0x64, 0x00};
    typewriter_print("🎮 ATC: ", 50);
    typewriter_print(atc_data, 30);
    typewriter_print(" for takeoff\n", 50);
}

// Calculate bearing (aviation math)
double calculate_bearing(double lat1, double lon1, double lat2, double lon2) {
    double dlon = lon2 - lon1;
    double y = sin(dlon) * cos(lat2);
    double x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon);
    double bearing = atan2(y, x);
    return bearing * 180.0 / M_PI;
}

int main() {
    // Animated startup sequence
    animated_border();
    typewriter_print("║                 AVIATION SECURITY SYSTEM                    ║\n", 30);
    typewriter_print("║              \"Flight Control Access Terminal\"              ║\n", 30);
    typewriter_print("║                                                             ║\n", 30);
    typewriter_print("║  🛩️  Unauthorized access to aircraft systems detected      ║\n", 30);
    typewriter_print("║  📡  Please provide valid pilot clearance code             ║\n", 30);
    animated_border();
    printf("\n");
    
    // Animated radar sweep for hostile aircraft (debuggers)
    spinning_radar(3);
    animated_dots("🔍 Scanning for hostile aircraft", 3);
    
    if (radar_sweep()) {
        blinking_alert("MAYDAY! MAYDAY! Enemy radar lock detected!", 3);
        typewriter_print("🚨 Activating emergency evasive maneuvers...\n", 50);
        exit(1);
    }
    
    // Animated flight time check
    progress_bar("⏱️  Analyzing flight patterns", 1500);
    
    if (check_flight_time()) {
        blinking_alert("ALTITUDE WARNING: Abnormal flight pattern detected!", 3);
        typewriter_print("🛑 Air traffic control ordering immediate landing...\n", 50);
        exit(1);
    }
    
    char pilot_input[512];
    typewriter_print("🎯 Enter pilot clearance code: ", 40);
    fflush(stdout);
    fgets(pilot_input, sizeof(pilot_input), stdin);
    
    // Remove newline
    pilot_input[strcspn(pilot_input, "\n")] = 0;
    
    // Animated processing
    printf("\n");
    animated_dots("🔄 Processing clearance request", 4);
    
    // Contact ATC with animation
    atc_system();
    
    // Navigation calculation with animation
    animated_dots("📡 Calculating navigation bearing", 3);
    double bearing = calculate_bearing(40.7128, -74.0060, 51.5074, -0.1278);
    typewriter_print("📍 Current bearing: ", 40);
    printf("%.2f degrees\n", bearing);
    
    // Animated validation process
    progress_bar("🔐 Validating flight plan", 2000);
    
    if (validate_flight_plan(pilot_input)) {
        printf("\n");
        // Success animation
        for (int i = 0; i < 3; i++) {
            printf("🎉 ═══════════════════════════════════════ 🎉\n");
            usleep(100000);
        }
        
        typewriter_print("   ✅ CLEARANCE GRANTED! WELCOME ABOARD!\n", 50);
        typewriter_print("   🛫 Flight systems now accessible\n", 50);
        typewriter_print("   🏆 Mission accomplished, pilot!\n", 50);
        typewriter_print("   📋 Your clearance code: ", 50);
        typewriter_print(pilot_input, 30);
        printf("\n");
        
        for (int i = 0; i < 3; i++) {
            printf("🎉 ═══════════════════════════════════════ 🎉\n");
            usleep(100000);
        }
    } else {
        printf("\n");
        // Failure animation
        blinking_alert("ACCESS DENIED - INVALID CLEARANCE", 2);
        
        printf("❌ ═══════════════════════════════════════ ❌\n");
        typewriter_print("   🚫 ACCESS DENIED - INVALID CLEARANCE\n", 50);
        typewriter_print("   ⛔ Aircraft systems remain locked\n", 50);
        typewriter_print("   🔒 Contact ground control for assistance\n", 50);
        printf("❌ ═══════════════════════════════════════ ❌\n");
        
        printf("\n");
        animated_dots("🚨 Activating emergency protocols", 3);
        
        // Trigger fake emergency transponder with animation
        fake_transponder();
    }
    
    return 0;
}

// Maintenance hangar functions (dead code)
void engine_diagnostics() {
    char engine_status[] = "All engines nominal";
    int fuel_level = 100;
    fuel_level = fuel_level * 0.95;
}

void weather_radar() {
    for (int i = 0; i < 360; i++) {
        double weather_data = sin(i * M_PI / 180.0);
    }
}

void navigation_backup() {
    typewriter_print("🧭 Backup navigation system online\n", 40);
}

// Autopilot system
typedef void (*autopilot_func)();
autopilot_func get_autopilot() {
    return &atc_system;
}

// Flight recorder backup
void backup_flight_data() {
    // Additional encoded data for misdirection
    char backup_data[] = "RkxJR0hUX0RBVEFfQkFDS1VQ"; // Base64 of "FLIGHT_DATA_BACKUP"
    char decoded_backup[50];
    decode_flight_data(backup_data, decoded_backup);
}