from GridMaze import GridMaze
import random
import os
import time

def banner():
    data = r"""
    88888888888888888888888888888888888888888888888888888888888888888888888
    88.._|      | `-.  | `.  -_-_ _-_  _-  _- -_ -  .'|   |.'|     |  _..88
    88   `-.._  |    |`!  |`.  -_ -__ -_ _- _-_-  .'  |.;'   |   _.!-'|  88
    88      | `-!._  |  `;!  ;. _______________ ,'| .-' |   _!.i'     |  88
    88..__  |     |`-!._ | `.| |_______________||."'|  _!.;'   |     _|..88
    88   |``"..__ |    |`";.| i|_|MMMMMMMMMMM|_|'| _!-|   |   _|..-|'    88
    88   |      |``--..|_ | `;!|l|MMoMMMMoMMM|1|.'j   |_..!-'|     |     88
    88   |      |    |   |`-,!_|_|MMMMP'YMMMM|_||.!-;'  |    |     |     88
    88___|______|____!.,.!,.!,!|d|MMMo * loMM|p|,!,.!.,.!..__|_____|_____88
    88      |     |    |  |  | |_|MMMMb,dMMMM|_|| |   |   |    |      |  88
    88      |     |    |..!-;'i|r|MPYMoMMMMoM|r| |`-..|   |    |      |  88
    88      |    _!.-j'  | _!,"|_|M<>MMMMoMMM|_||!._|  `i-!.._ |      |  88
    88     _!.-'|    | _."|  !;|1|MbdMMoMMMMM|l|`.| `-._|    |``-.._  |  88
    88..-i'     |  _.''|  !-| !|_|MMMoMMMMoMM|_|.|`-. | ``._ |     |``"..88
    88   |      |.|    |.|  !| |u|MoMMMMoMMMM|n||`. |`!   | `".    |     88
    88   |  _.-'  |  .'  |.' |/|_|MMMMoMMMMoM|_|! |`!  `,.|    |-._|     88
    88  _!"'|     !.'|  .'| .'|[@]MMMMMMMMMMM[@] \|  `. | `._  |   `-._  88
    88-'    |   .'   |.|  |/| /                 \|`.  |`!    |.|      |`-88
    88      |_.'|   .' | .' |/                   \  \ |  `.  | `._-   |  88
    88     .'   | .'   |/|  /                     \ |`!   |`.|    `.  |  88
    88  _.'     !'|   .' | /                       \|  `  |  `.    |`.|  88
    8888888888888888888888888888888888888888888888888888888888888-AvA-88888"""

    data += r'''
    Hello stranger!
    Your goal here is to get out of this maze. but it is not that simple!
    You have limited resources that can only last you though the shortest path to get the key and then get out.
    Path formate is RDDLUR...
    Pleas play the game to know how the movement work!
    1- Play game (for testing)
    2- Get the flag
    > '''
    return data


def play_game():
    print("--- Welcome to the Maze Game! ---")
    
    
    n = random.choice([7, 9, 11]) 
    maze = GridMaze(n, n)
    maze.generate_maze() 

    player_position = (0, 0)
    has_key = False
    
    start_point = (0, 0)
    end_point = (maze.height - 1, maze.width - 1)

    while True:
        print("MAZE PUZZLE")
        print("S = Start  |  $ = Exit  |  & = Key  |  P = Player")
        print(f"Key Collected: {'Yes' if has_key else 'No'}")

        raw_maze_str_original = maze.get_raw_maze()
        maze_str_lines = raw_maze_str_original.split('\n')
        

        player_line_idx = 2 * player_position[0] + 1
        player_char_idx = 2 * player_position[1] + 1


        if player_line_idx < len(maze_str_lines) and player_char_idx < len(maze_str_lines[player_line_idx]):
            current_line_chars = list(maze_str_lines[player_line_idx])
            

            if player_position == maze.key_position:
                if not has_key: 
                    current_line_chars[player_char_idx] = 'P' 
                else: 
                    current_line_chars[player_char_idx] = ' ' 
            elif player_position == start_point:
                current_line_chars[player_char_idx] = 'S'
            elif player_position == end_point:
                current_line_chars[player_char_idx] = '$'
            else:
                 current_line_chars[player_char_idx] = 'P'
            
            maze_str_lines[player_line_idx] = "".join(current_line_chars)
        

        for i, line in enumerate(maze_str_lines):

            if i % 2 == 1: 

                formatted_line = ""
                for char_idx, char in enumerate(line):
                    if char_idx == 0 or char_idx == len(line) - 1: 
                        formatted_line += char + " "
                    elif char == '#': 
                        formatted_line += char + " "
                    else: 
                        formatted_line += char + " "
                print(formatted_line.strip()) 
            else: 
                print(" ".join(list(line)).strip())

        if player_position == maze.key_position and not has_key:
            has_key = True
            print("\nYou found the key!")



        if player_position == end_point:
            if has_key:
                print("\nCongratulations! You found the exit with the key!")
                print("Returning to main menu...")
                input("Press Enter to continue...")
                return
            else:
                print("\nYou reached the exit, but you need to find the key first!")

        move = input("Enter your move (U/D/L/R) or 'Q' to quit: ").strip().upper()

        if move == 'Q':
            print("Exiting game. Returning to main menu...")
            input("Press Enter to continue...")
            return

        next_position = player_position
        valid_move_made = False

        if move == 'U':
            next_position = (player_position[0] - 1, player_position[1])
        elif move == 'D':
            next_position = (player_position[0] + 1, player_position[1])
        elif move == 'L':
            next_position = (player_position[0], player_position[1] - 1)
        elif move == 'R':
            next_position = (player_position[0], player_position[1] + 1)
        else:
            print("Invalid input. Please use U, D, L, R, or Q.")
            input("Press Enter to try again...")
            continue 

        if maze.can_move(player_position, next_position):
            player_position = next_position
            valid_move_made = True
        else:
            print("You can't move there! There's a wall or it's out of bounds.")
            input("Press Enter to try again...")
            
def start_loop():
    for _ in range(20): 

        
        n = random.choice(range(11, 71, 2))  
        maze = GridMaze(n, n)
        maze.generate_maze()
        start_point = (0, 0)
        end_point = (maze.height - 1, maze.width - 1)
        
        data = maze.get_raw_maze() + "\nPath: "
        print(data)
        start_t = int(time.time())
        
        answer = input().strip().upper()
        
        end_t = int(time.time())
        solution = maze.solve_maze_with_key(start_point, end_point)
        
        if solution:
            path = maze.path_to_directions(solution)
            if end_t - start_t > 15:
                print(f"You took to long to find the path!")
                print(f"Expected path: {path}")
                print("Game over.")
                break 
            elif answer == path:
                continue
            else:
                print(f"Wrong path! Expected: {path}")
                print("Game over.")
                break
        else:
            print("Error: Could not find a solution for this maze. This shouldn't happen.")
            print("Game over.")
            break
    else: 
        print("Congratulations! You solved all mazes successfully.")
        print(f"Flag: {os.getenv('FLAG', 'FLAG{{example_flag}}')}") 
    
    return


def main():

    print(banner(), end='')
    response = input().strip()

    if response == '1':
        play_game()
        main() 
    elif response == '2':
        start_loop()

    else:
        print("Invalid choice")
        input("Press Enter to try again...")
        main() 

if __name__ == "__main__":
    main()