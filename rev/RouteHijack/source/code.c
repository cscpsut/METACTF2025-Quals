#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Flight encryption keys - classified aviation data
int flight_keys[] = {1013,34,23,3,10,5,14,15,28,84,67,12,2,29,28,9,17,17,75,14,121,54,26,82,85,23,69,67,15,9,4,19,23,1,68,70,9,29,82,84,21,10,14,10,9,0,74,12,99,34,17,4,21,8,7,64,14,68,1,22,7,29,7,15,21,29,6,1,84,26,109,8,17,21,2,23,18,61,24,2,3,11,7,49,57,10,13,6,56,47,2,23,22,0,6,7,23,58,49,1,29,31,12,13,17};
int key_count = sizeof(flight_keys) / sizeof(flight_keys[0]);

// Aviation encryption functions - one for each aircraft type
int encrypt_cessna(int input) { return input ^ flight_keys[0]; }
int encrypt_piper(int input) { return input ^ flight_keys[1]; }
int encrypt_boeing737(int input) { return input ^ flight_keys[2]; }
int encrypt_airbus320(int input) { return input ^ flight_keys[3]; }
int encrypt_f16(int input) { return input ^ flight_keys[4]; }
int encrypt_f22(int input) { return input ^ flight_keys[5]; }
int encrypt_b52(int input) { return input ^ flight_keys[6]; }
int encrypt_c130(int input) { return input ^ flight_keys[7]; }
int encrypt_blackhawk(int input) { return input ^ flight_keys[8]; }
int encrypt_apache(int input) { return input ^ flight_keys[9]; }
int encrypt_chinook(int input) { return input ^ flight_keys[10]; }
int encrypt_osprey(int input) { return input ^ flight_keys[11]; }
int encrypt_sr71(int input) { return input ^ flight_keys[12]; }
int encrypt_u2(int input) { return input ^ flight_keys[13]; }
int encrypt_predator(int input) { return input ^ flight_keys[14]; }
int encrypt_reaper(int input) { return input ^ flight_keys[15]; }
int encrypt_global_hawk(int input) { return input ^ flight_keys[16]; }
int encrypt_stealth(int input) { return input ^ flight_keys[17]; }
int encrypt_phantom(int input) { return input ^ flight_keys[18]; }
int encrypt_tomcat(int input) { return input ^ flight_keys[19]; }
int encrypt_hornet(int input) { return input ^ flight_keys[20]; }
int encrypt_eagle(int input) { return input ^ flight_keys[21]; }
int encrypt_falcon(int input) { return input ^ flight_keys[22]; }
int encrypt_thunderbolt(int input) { return input ^ flight_keys[23]; }
int encrypt_warthog(int input) { return input ^ flight_keys[24]; }
int encrypt_lightning(int input) { return input ^ flight_keys[25]; }
int encrypt_raptor(int input) { return input ^ flight_keys[26]; }
int encrypt_viper(int input) { return input ^ flight_keys[27]; }
int encrypt_harrier(int input) { return input ^ flight_keys[28]; }
int encrypt_intruder(int input) { return input ^ flight_keys[29]; }
int encrypt_prowler(int input) { return input ^ flight_keys[30]; }
int encrypt_hawkeye(int input) { return input ^ flight_keys[31]; }
int encrypt_galaxy(int input) { return input ^ flight_keys[32]; }
int encrypt_starlifter(int input) { return input ^ flight_keys[33]; }
int encrypt_globemaster(int input) { return input ^ flight_keys[34]; }
int encrypt_stratofortress(int input) { return input ^ flight_keys[35]; }
int encrypt_stratofreighter(int input) { return input ^ flight_keys[36]; }
int encrypt_stratotanker(int input) { return input ^ flight_keys[37]; }
int encrypt_awacs(int input) { return input ^ flight_keys[38]; }
int encrypt_jstars(int input) { return input ^ flight_keys[39]; }
int encrypt_rivet_joint(int input) { return input ^ flight_keys[40]; }
int encrypt_compass_call(int input) { return input ^ flight_keys[41]; }
int encrypt_looking_glass(int input) { return input ^ flight_keys[42]; }
int encrypt_nightwatch(int input) { return input ^ flight_keys[43]; }
int encrypt_doomsday(int input) { return input ^ flight_keys[44]; }
int encrypt_air_force_one(int input) { return input ^ flight_keys[45]; }
int encrypt_marine_one(int input) { return input ^ flight_keys[46]; }
int encrypt_spirit(int input) { return input ^ flight_keys[47]; }
int encrypt_stealth_bomber(int input) { return input ^ flight_keys[48]; }
int encrypt_flying_wing(int input) { return input ^ flight_keys[49]; }
int encrypt_concorde(int input) { return input ^ flight_keys[50]; }
int encrypt_tu144(int input) { return input ^ flight_keys[51]; }
int encrypt_mig21(int input) { return input ^ flight_keys[52]; }
int encrypt_mig29(int input) { return input ^ flight_keys[53]; }
int encrypt_su27(int input) { return input ^ flight_keys[54]; }
int encrypt_su35(int input) { return input ^ flight_keys[55]; }
int encrypt_rafale(int input) { return input ^ flight_keys[56]; }
int encrypt_typhoon(int input) { return input ^ flight_keys[57]; }
int encrypt_gripen(int input) { return input ^ flight_keys[58]; }
int encrypt_mirage(int input) { return input ^ flight_keys[59]; }
int encrypt_tornado(int input) { return input ^ flight_keys[60]; }
int encrypt_jaguar(int input) { return input ^ flight_keys[61]; }
int encrypt_harrier_jump(int input) { return input ^ flight_keys[62]; }
int encrypt_sea_harrier(int input) { return input ^ flight_keys[63]; }
int encrypt_buccaneer(int input) { return input ^ flight_keys[64]; }
int encrypt_vulcan(int input) { return input ^ flight_keys[65]; }
int encrypt_victor(int input) { return input ^ flight_keys[66]; }
int encrypt_valiant(int input) { return input ^ flight_keys[67]; }
int encrypt_canberra(int input) { return input ^ flight_keys[68]; }
int encrypt_lightning_eng(int input) { return input ^ flight_keys[69]; }
int encrypt_hunter(int input) { return input ^ flight_keys[70]; }
int encrypt_hawk(int input) { return input ^ flight_keys[71]; }
int encrypt_red_arrow(int input) { return input ^ flight_keys[72]; }
int encrypt_blue_angel(int input) { return input ^ flight_keys[73]; }
int encrypt_thunderbird(int input) { return input ^ flight_keys[74]; }
int encrypt_snowbird(int input) { return input ^ flight_keys[75]; }
int encrypt_patrouille(int input) { return input ^ flight_keys[76]; }
int encrypt_frecce(int input) { return input ^ flight_keys[77]; }
int encrypt_aerobatic(int input) { return input ^ flight_keys[78]; }
int encrypt_demonstration(int input) { return input ^ flight_keys[79]; }
int encrypt_formation(int input) { return input ^ flight_keys[80]; }
int encrypt_squadron(int input) { return input ^ flight_keys[81]; }
int encrypt_wing(int input) { return input ^ flight_keys[82]; }
int encrypt_group(int input) { return input ^ flight_keys[83]; }
int encrypt_command(int input) { return input ^ flight_keys[84]; }
int encrypt_tactical(int input) { return input ^ flight_keys[85]; }
int encrypt_strategic(int input) { return input ^ flight_keys[86]; }
int encrypt_reconnaissance(int input) { return input ^ flight_keys[87]; }
int encrypt_surveillance(int input) { return input ^ flight_keys[88]; }
int encrypt_intelligence(int input) { return input ^ flight_keys[89]; }
int encrypt_electronic(int input) { return input ^ flight_keys[90]; }
int encrypt_warfare(int input) { return input ^ flight_keys[91]; }
int encrypt_combat(int input) { return input ^ flight_keys[92]; }
int encrypt_fighter(int input) { return input ^ flight_keys[93]; }
int encrypt_bomber(int input) { return input ^ flight_keys[94]; }
int encrypt_transport(int input) { return input ^ flight_keys[95]; }
int encrypt_cargo(int input) { return input ^ flight_keys[96]; }
int encrypt_refueling(int input) { return input ^ flight_keys[97]; }
int encrypt_tanker(int input) { return input ^ flight_keys[98]; }
int encrypt_trainer(int input) { return input ^ flight_keys[99]; }
int encrypt_experimental(int input) { return input ^ flight_keys[100]; }
int encrypt_prototype(int input) { return input ^ flight_keys[101]; }
int encrypt_classified(int input) { return input ^ flight_keys[102]; }
int encrypt_secret(int input) { return input ^ flight_keys[103]; }
int encrypt_top_secret(int input) { return input ^ flight_keys[104]; }

// Array of aircraft encryption functions
int (*aircraft_encrypt[])(int) = {
    encrypt_cessna, encrypt_piper, encrypt_boeing737, encrypt_airbus320, encrypt_f16,
    encrypt_f22, encrypt_b52, encrypt_c130, encrypt_blackhawk, encrypt_apache,
    encrypt_chinook, encrypt_osprey, encrypt_sr71, encrypt_u2, encrypt_predator,
    encrypt_reaper, encrypt_global_hawk, encrypt_stealth, encrypt_phantom, encrypt_tomcat,
    encrypt_hornet, encrypt_eagle, encrypt_falcon, encrypt_thunderbolt, encrypt_warthog,
    encrypt_lightning, encrypt_raptor, encrypt_viper, encrypt_harrier, encrypt_intruder,
    encrypt_prowler, encrypt_hawkeye, encrypt_galaxy, encrypt_starlifter, encrypt_globemaster,
    encrypt_stratofortress, encrypt_stratofreighter, encrypt_stratotanker, encrypt_awacs, encrypt_jstars,
    encrypt_rivet_joint, encrypt_compass_call, encrypt_looking_glass, encrypt_nightwatch, encrypt_doomsday,
    encrypt_air_force_one, encrypt_marine_one, encrypt_spirit, encrypt_stealth_bomber, encrypt_flying_wing,
    encrypt_concorde, encrypt_tu144, encrypt_mig21, encrypt_mig29, encrypt_su27,
    encrypt_su35, encrypt_rafale, encrypt_typhoon, encrypt_gripen, encrypt_mirage,
    encrypt_tornado, encrypt_jaguar, encrypt_harrier_jump, encrypt_sea_harrier, encrypt_buccaneer,
    encrypt_vulcan, encrypt_victor, encrypt_valiant, encrypt_canberra, encrypt_lightning_eng,
    encrypt_hunter, encrypt_hawk, encrypt_red_arrow, encrypt_blue_angel, encrypt_thunderbird,
    encrypt_snowbird, encrypt_patrouille, encrypt_frecce, encrypt_aerobatic, encrypt_demonstration,
    encrypt_formation, encrypt_squadron, encrypt_wing, encrypt_group, encrypt_command,
    encrypt_tactical, encrypt_strategic, encrypt_reconnaissance, encrypt_surveillance, encrypt_intelligence,
    encrypt_electronic, encrypt_warfare, encrypt_combat, encrypt_fighter, encrypt_bomber,
    encrypt_transport, encrypt_cargo, encrypt_refueling, encrypt_tanker, encrypt_trainer,
    encrypt_experimental, encrypt_prototype, encrypt_classified, encrypt_secret, encrypt_top_secret
};

void print_aviation_banner() {
    printf("╔══════════════════════════════════════════════════════════════════════════════╗\n");
    printf("║                    🛩️  CLASSIFIED FLIGHT CONTROL SYSTEM 🛩️                    ║\n");
    printf("║                          ✈️  TOP SECRET CLEARANCE REQUIRED ✈️                  ║\n");
    printf("╠══════════════════════════════════════════════════════════════════════════════╣\n");
    printf("║  AUTHORIZATION CODE REQUIRED FOR FLIGHT MANIFEST DECRYPTION                 ║\n");
    printf("║                                                                              ║\n");
    printf("║  🎯 Mission Briefing:                                                        ║\n");
    printf("║     A classified flight manifest has been encrypted using advanced          ║\n");
    printf("║     aviation cipher protocols. Only authorized personnel with the           ║\n");
    printf("║     correct security clearance code can decrypt the mission details.        ║\n");
    printf("║                                                                              ║\n");
    printf("║  📡 System Status: ACTIVE                                                    ║\n");
    printf("║  🔐 Encryption: Multi-layer aircraft-specific XOR cipher                    ║\n");
    printf("║  ⚠️  Security Level: MAXIMUM                                                 ║\n");
    printf("╚══════════════════════════════════════════════════════════════════════════════╝\n\n");
}

void print_access_denied() {
    printf("\n");
    printf("🚫 ═══════════════════════════════════════════════════════════════════════════ 🚫\n");
    printf("                            ❌ ACCESS DENIED ❌\n");
    printf("                     UNAUTHORIZED FLIGHT CODE DETECTED\n");
    printf("                          SECURITY BREACH LOGGED\n");
    printf("🚫 ═══════════════════════════════════════════════════════════════════════════ 🚫\n");
    printf("\n");
    printf("   📞 Contact Air Traffic Control for authorized access codes\n");
    printf("   🛡️  This incident has been reported to aviation security\n\n");
}

void print_decryption_header() {
    printf("\n");
    printf("✅ ═══════════════════════════════════════════════════════════════════════════ ✅\n");
    printf("                        🔓 AUTHORIZATION ACCEPTED 🔓\n");
    printf("                      DECRYPTING FLIGHT MANIFEST...\n");
    printf("✅ ═══════════════════════════════════════════════════════════════════════════ ✅\n");
    printf("\n");
    printf("📋 CLASSIFIED MISSION DATA:\n");
    printf("═══════════════════════════\n");
}

int main() {
    print_aviation_banner();
    
    srand(time(NULL));
    int security_clearance_code = (rand() % 10000) + 1;
    int user_code;
    
    printf("🔑 Enter your security clearance code: ");
    scanf("%d", &user_code);
    
    printf("\n🔍 Verifying authorization...\n");
    printf("⏳ Checking against flight control database...\n");
    
    for(int i = 0; i < 3; i++) {
        printf(".");
        fflush(stdout);
    }
    printf("\n");
    
    int decrypted_data = user_code;
    
    if (user_code == security_clearance_code) {
        print_decryption_header();
        
        for (int i = 0; i < key_count; i++) {
            decrypted_data = aircraft_encrypt[i](security_clearance_code);
            printf("%c", (char)(decrypted_data & 0xFF));
        }
        
        printf("\n\n");
        printf("🎯 Mission decryption complete! \n");
        printf("🛩️  All aircraft systems nominal\n");
        printf("✈️  Ready for takeoff, pilot!\n\n");
    }
    else {
        print_access_denied();
        return 1;
    }
    
    return 0;
}