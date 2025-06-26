#include "plane_ascii.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <ncurses.h>
#include <signal.h>

#define PLANE_HEIGHT 6
#define PLANE_WIDTH 19
#define EXPLOSION_FRAMES 5
#define MAX_CLOUDS 8
#define CLOUD_TYPES 3

// Flag to track if we're in a clean state to exit
static int ncurses_initialized = 0;

// Signal handler to ensure clean exit
static void cleanup_handler(int sig) {
    if (ncurses_initialized) {
        endwin();
    }
    exit(1);
}

// Plane ASCII art frames for different directions
static char *plane_right[PLANE_HEIGHT] = {
    "         -=\\`\\     ",
    "     |\\ ____\\_\\__  ",
    "   -=\\c`\"\"\"\"\"\"\"\" \"`)  ",
    "      `~~~~~/ /~~`  ",
    "        -==/ /      ",
    "          '-'       "
};

static char *plane_left[PLANE_HEIGHT] = {
    "     /`/=-         ",
    "  __/_/______ /|   ",
    "  (`\" \"\"\"\"\"\"\"\"\"c/=-   ",
    "  `~~\\ \\~~~~~`      ",
    "      \\ \\==-        ",
    "       `-'          "
};

// Explosion frames
static char *explosion[EXPLOSION_FRAMES][5] = {
    {
        "  *  ",
        " * * ",
        "* * *",
        " * * ",
        "  *  "
    },
    {
        " *** ",
        "*****",
        "*****",
        "*****",
        " *** "
    },
    {
        " *@* ",
        "*@#@*",
        "@#*#@",
        "*@#@*",
        " *@* "
    },
    {
        " \\|/ ",
        "-*O*-",
        "/|\\  ",
        "     ",
        "     "
    },
    {
        "     ",
        " . . ",
        ".   .",
        " . . ",
        "     "
    }
};

// Cloud ASCII art
static char *cloud_types[CLOUD_TYPES][3] = {
    {
        "   .-~~~-.   ",
        " .-~      ~-.",
        "(            )"
    },
    {
        "  .---.  ",
        " '     ' ",
        "'       '"
    },
    {
        "   _  ",
        "-=( )=-",
        "   -   "
    }
};

// Cloud structure
typedef struct {
    int x;
    int y;
    int type;
    int speed;
    int active;
} Cloud;

// Function declarations
static void draw_plane(int y, int x, int direction);
static void draw_explosion(int y, int x, int frame);
static void draw_cloud(int y, int x, int type);
static void initialize_clouds(Cloud *clouds, int max_x, int max_y);
static void update_clouds(Cloud *clouds, int max_clouds, int max_x, int max_y);
static void draw_clouds(Cloud *clouds, int max_clouds);

// Safe initialization of ncurses
static int safe_init_ncurses() {
    // Set up signal handlers for clean exit
    signal(SIGSEGV, cleanup_handler);
    signal(SIGINT, cleanup_handler);
    signal(SIGTERM, cleanup_handler);
    
    // Initialize ncurses
    initscr();
    ncurses_initialized = 1;
    
    cbreak();
    noecho();
    curs_set(0); // Hide cursor
    nodelay(stdscr, TRUE); // Non-blocking input
    keypad(stdscr, TRUE); // Enable function keys
    
    return 0;
}

// Safe cleanup of ncurses
static void safe_endwin() {
    if (ncurses_initialized) {
        endwin();
        ncurses_initialized = 0;
    }
}

// Function to show plane flying freely with clouds
int show_plane_flying(int duration_seconds) {
    // Default duration if not specified
    if (duration_seconds <= 0) duration_seconds = 10;
    
    // Initialize ncurses safely
    if (safe_init_ncurses() != 0) {
        fprintf(stderr, "Failed to initialize ncurses\n");
        return -1;
    }
    
    // Setup colors if available
    int has_color = 0;
    if (has_colors()) {
        start_color();
        init_pair(1, COLOR_BLUE, COLOR_BLACK);   // For clouds
        init_pair(2, COLOR_YELLOW, COLOR_BLACK); // For plane
        has_color = 1;
    }
    
    // Get screen dimensions
    int max_y, max_x;
    getmaxyx(stdscr, max_y, max_x);
    
    // Seed random number generator
    srand(time(NULL));
    
    // Setup clouds
    Cloud *clouds = malloc(sizeof(Cloud) * MAX_CLOUDS);
    if (!clouds) {
        safe_endwin();
        return -1;
    }
    initialize_clouds(clouds, max_x, max_y);
    
    // Setup plane
    int plane_y = rand() % (max_y - PLANE_HEIGHT - 10) + 5;
    int plane_x = 0;
    int plane_dir = 0; // 0: right, 1: left
    int dx = 1, dy = 0;
    int frame_count = 0;
    
    // Animation timing
    time_t start_time, current_time;
    time(&start_time);
    int fps = 15; // Default frames per second
    
    // Main animation loop
    int result = 0;
    while (1) {
        // Clear the screen
        clear();
        
        // Update frame counter
        frame_count++;
        
        // Get current time
        time(&current_time);
        double elapsed_seconds = difftime(current_time, start_time);
        
        // Check if duration has elapsed
        if (elapsed_seconds >= duration_seconds) {
            break;
        }
        
        // Change direction randomly every 20 frames
        if (frame_count % 20 == 0) {
            int new_dir = rand() % 2;  // Only 0 (right) or 1 (left)
            plane_dir = new_dir;
            
            // Set velocity based on direction
            switch(plane_dir) {
                case 0: dx = 1; break;  // right
                case 1: dx = -1; break; // left
            }
            
            // Random vertical movement
            dy = (rand() % 3) - 1;  // -1, 0, or 1
        }
        
        // Update plane position
        plane_x += dx;
        plane_y += dy;
        
        // Screen boundaries check
        if (plane_x < 0) {
            plane_x = 0;
            dx = -dx;  // Bounce off left edge
            plane_dir = 0;
        }
        if (plane_y < 0) {
            plane_y = 0;
            dy = -dy;  // Bounce off top edge
        }
        if (plane_x > max_x - PLANE_WIDTH) {
            plane_x = max_x - PLANE_WIDTH;
            dx = -dx;  // Bounce off right edge
            plane_dir = 1;
        }
        if (plane_y > max_y - PLANE_HEIGHT) {
            plane_y = max_y - PLANE_HEIGHT;
            dy = -dy;  // Bounce off bottom edge
        }
        
        // Update and draw clouds
        update_clouds(clouds, MAX_CLOUDS, max_x, max_y);
        
        if (has_color) attron(COLOR_PAIR(1));
        draw_clouds(clouds, MAX_CLOUDS);
        if (has_color) attroff(COLOR_PAIR(1));
        
        // Draw plane with color if available
        if (has_color) attron(COLOR_PAIR(2));
        draw_plane(plane_y, plane_x, plane_dir);
        if (has_color) attroff(COLOR_PAIR(2));
        
        // Display info
        mvprintw(0, 0, "Position: (%d, %d) Time: %.1f/%.1fs", 
                plane_x, plane_y, elapsed_seconds, (double)duration_seconds);
        mvprintw(1, 0, "Press 'q' to quit");
        
        // Refresh the screen
        refresh();
        
        // Check for quit key
        int ch = getch();
        if (ch == 'q' || ch == 'Q') {
            result = 1; // User interrupted
            break;
        }
        
        // Animation speed
        usleep(1000000 / fps); // Convert fps to microseconds
    }
    
    // Cleanup
    free(clouds);
    safe_endwin();
    return result;
}

/// Function to show plane crash animation with improved compatibility
int show_plane_crash(int duration_seconds) {
    // Default duration if not specified
    if (duration_seconds <= 0) duration_seconds = 10;
    
    // Initialize ncurses safely
    if (safe_init_ncurses() != 0) {
        fprintf(stderr, "Failed to initialize ncurses\n");
        return -1;
    }
    
    // Setup colors if available
    int has_color = 0;
    if (has_colors()) {
        start_color();
        init_pair(1, COLOR_BLUE, COLOR_BLACK);   // For clouds
        init_pair(2, COLOR_YELLOW, COLOR_BLACK); // For plane
        init_pair(3, COLOR_RED, COLOR_BLACK);    // For explosion
        init_pair(4, COLOR_GREEN, COLOR_BLACK);  // For ground
        has_color = 1;
    }
    
    // Get screen dimensions
    int max_y, max_x;
    getmaxyx(stdscr, max_y, max_x);
    
    // Seed random number generator
    srand(time(NULL));
    
    // Setup clouds - use full MAX_CLOUDS like in the flying function
    Cloud *clouds = malloc(sizeof(Cloud) * MAX_CLOUDS);
    if (!clouds) {
        safe_endwin();
        return -1;
    }
    initialize_clouds(clouds, max_x, max_y);
    
    // Draw ground (limit to screen width)
    int ground_y = max_y - 3;
    char *ground_line = malloc(max_x + 1);
    if (!ground_line) {
        free(clouds);
        safe_endwin();
        return -1;
    }
    memset(ground_line, '_', max_x);
    ground_line[max_x] = '\0';
    
    // Setup plane - start from top left
    int plane_y = 5;
    int plane_x = 10;
    int plane_dir = 0; // Right direction
    int dx = 3;        // Moving right
    int dy = 1;        // Moving down diagonally
    
    // Collision tracking
    int collision = 0;
    int explosion_frame = 0;
    int fps = 15;
    int frame_count = 0;
    
    // Animation timing
    time_t start_time, current_time;
    time(&start_time);
    
    // Main animation loop
    int result = 0;
    while (1) {
        // Clear the screen
        clear();
        
        // Update frame counter
        frame_count++;
        
        // Get current time
        time(&current_time);
        double elapsed_seconds = difftime(current_time, start_time);
        
        // Check if duration has elapsed (only if not in explosion animation)
        if (!collision && elapsed_seconds >= duration_seconds) {
            // Force collision to start explosion sequence
            collision = 1;
            plane_y = ground_y - PLANE_HEIGHT + 1;
        }
        
        // Update plane position if not collided
        if (!collision) {
            plane_x += dx;
            plane_y += dy;
            
            // Screen boundaries check (similar to flying function)
            if (plane_x < 0) {
                plane_x = 0;
                dx = -dx;  // Bounce off left edge
                plane_dir = 0;
            }
            if (plane_y < 0) {
                plane_y = 0;
                dy = -dy;  // Bounce off top edge
            }
            if (plane_x > max_x - PLANE_WIDTH) {
                plane_x = max_x - PLANE_WIDTH;
                dx = -dx;  // Bounce off right edge
                plane_dir = 1;
            }
            
            // Check for collision with ground
            if (plane_y + PLANE_HEIGHT >= ground_y) {
                collision = 1;
                plane_y = ground_y - PLANE_HEIGHT + 1; // Position plane just above ground
            }
        } else {
            // Show explosion animation
            if (explosion_frame < EXPLOSION_FRAMES) {
                if (has_color) attron(COLOR_PAIR(3));
                draw_explosion(plane_y + PLANE_HEIGHT/2, plane_x + PLANE_WIDTH/2, explosion_frame);
                if (has_color) attroff(COLOR_PAIR(3));
                
                explosion_frame++;
                usleep(200000); // Slightly faster explosion animation
            } else {
                // End the animation after explosion
                break;
            }
        }
        
        // Update and draw clouds (like in flying function)
        update_clouds(clouds, MAX_CLOUDS, max_x, max_y);
        
        if (has_color) attron(COLOR_PAIR(1));
        draw_clouds(clouds, MAX_CLOUDS);
        if (has_color) attroff(COLOR_PAIR(1));
        
        // Draw ground
        if (has_color) attron(COLOR_PAIR(4));
        mvprintw(ground_y, 0, "%s", ground_line);
        // Add some ground details (limit based on screen width)
        for (int i = 0; i < max_x; i += 15) {
            if (i + 5 < max_x) {
                mvprintw(ground_y+1, i, "/\\/\\/\\");
            }
        }
        if (has_color) attroff(COLOR_PAIR(4));
        
        // Draw plane if not exploded
        if (!collision || explosion_frame == 0) {
            if (has_color) attron(COLOR_PAIR(2));
            draw_plane(plane_y, plane_x, plane_dir);
            if (has_color) attroff(COLOR_PAIR(2));
        }
        
        // Display info
        mvprintw(0, 0, "Position: (%d, %d) %s Time: %.1f/%.1fs", 
                plane_x, plane_y,
                collision ? "CRASH!" : "Descending...",
                elapsed_seconds, (double)duration_seconds);
        mvprintw(1, 0, "Press 'q' to quit");
        
        // Refresh the screen
        refresh();
        
        // Check for quit key
        int ch = getch();
        if (ch == 'q' || ch == 'Q') {
            result = 1; // User interrupted
            break;
        }
        
        // Animation speed
        usleep(1000000 / fps);
    }
    
    // Add a small delay at the end to show final frame
    usleep(500000);
    
    // Cleanup resources
    free(clouds);
    free(ground_line);
    safe_endwin();
    return result;
}

// Function to draw plane based on direction
static void draw_plane(int y, int x, int direction) {
    char **plane;
    
    // Select the plane art based on direction
    switch(direction) {
        case 0: plane = plane_right; break;
        case 1: plane = plane_left; break;
        default: plane = plane_right;
    }
    
    // Draw the plane
    for (int i = 0; i < PLANE_HEIGHT; i++) {
        mvprintw(y + i, x, "%s", plane[i]);
    }
}

// Function to draw explosion
static void draw_explosion(int y, int x, int frame) {
    for (int i = 0; i < 5; i++) {
        mvprintw(y + i - 2, x, "%s", explosion[frame][i]);
    }
}

// Function to draw a cloud
static void draw_cloud(int y, int x, int type) {
    for (int i = 0; i < 3; i++) {
        mvprintw(y + i, x, "%s", cloud_types[type][i]);
    }
}

// Initialize clouds
static void initialize_clouds(Cloud *clouds, int max_x, int max_y) {
    for (int i = 0; i < MAX_CLOUDS; i++) {
        clouds[i].x = rand() % max_x;
        clouds[i].y = rand() % (max_y / 3); // Keep clouds in upper third of screen
        clouds[i].type = rand() % CLOUD_TYPES;
        clouds[i].speed = (rand() % 2) + 1; // 1-2 pixels per frame
        clouds[i].active = (rand() % 2) ? 1 : 0; // 50% chance of being active initially
    }
}

// Update cloud positions
static void update_clouds(Cloud *clouds, int max_clouds, int max_x, int max_y) {
    for (int i = 0; i < max_clouds; i++) {
        if (clouds[i].active) {
            clouds[i].x -= clouds[i].speed;
            
            // If cloud moves off screen, reposition it
            if (clouds[i].x < -15) {
                clouds[i].x = max_x;
                clouds[i].y = rand() % (max_y / 3);
                clouds[i].type = rand() % CLOUD_TYPES;
                clouds[i].speed = (rand() % 2) + 1;
                
                // Small chance to deactivate cloud
                if (rand() % 10 == 0) {
                    clouds[i].active = 0;
                }
            }
        } else {
            // Small chance to activate an inactive cloud
            if (rand() % 30 == 0) {
                clouds[i].active = 1;
                clouds[i].x = max_x;
                clouds[i].y = rand() % (max_y / 3);
                clouds[i].type = rand() % CLOUD_TYPES;
                clouds[i].speed = (rand() % 2) + 1;
            }
        }
    }
}

// Draw all active clouds
static void draw_clouds(Cloud *clouds, int max_clouds) {
    for (int i = 0; i < max_clouds; i++) {
        if (clouds[i].active) {
            draw_cloud(clouds[i].y, clouds[i].x, clouds[i].type);
        }
    }
}