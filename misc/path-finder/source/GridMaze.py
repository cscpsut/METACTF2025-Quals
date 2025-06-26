import random
import collections
from typing import List, Tuple, Set, Dict, Optional
import sys
sys.setrecursionlimit(5000)



class GridMaze:
    def __init__(self, width: int = 0, height: int = 0): # Initialize with 0,0 to allow generating from string
        self.width = width
        self.height = height
        self.walls = {}
        self.visited = set()
        self.key_position = None

        if width > 0 and height > 0: # Only initialize walls if width/height are provided at creation
            # Initialize all walls as present
            for row in range(height):
                for col in range(width):
                    self.walls[(row, col)] = [True, True, True, True]  # N, E, S, W

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int, int]]:
        neighbors = []
        directions = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)]  # N, E, S, W

        for dr, dc, direction in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                neighbors.append((new_row, new_col, direction))

        return neighbors

    def remove_wall(
        self, cell1: Tuple[int, int], cell2: Tuple[int, int], direction: int
    ):
        self.walls[cell1][direction] = False
        opposite_direction = (direction + 2) % 4
        self.walls[cell2][opposite_direction] = False

    def generate_maze_recursive(self, row: int, col: int):
        current_cell = (row, col)
        self.visited.add(current_cell)

        neighbors = self.get_neighbors(row, col)
        random.shuffle(neighbors) # Shuffle neighbors to ensure random maze generation

        for neighbor_row, neighbor_col, direction in neighbors:
            neighbor_cell = (neighbor_row, neighbor_col)

            if neighbor_cell not in self.visited:
                self.remove_wall(current_cell, neighbor_cell, direction)
                self.generate_maze_recursive(neighbor_row, neighbor_col)

    def generate_maze(self, start_row: int = 0, start_col: int = 0):
        # Ensure walls are initialized for generation if not done in __init__
        if not self.walls or self.width * self.height == 0:
             for row in range(self.height):
                for col in range(self.width):
                    self.walls[(row, col)] = [True, True, True, True] # N, E, S, W

        self.visited.clear()
        self.generate_maze_recursive(start_row, start_col)

        # Place key randomly in maze (not at start or end)
        start = (start_row, start_col)
        end = (self.height - 1, self.width - 1)
        available_positions = [
            cell for cell in self.visited if cell != start and cell != end
        ]
        self.key_position = random.choice(available_positions)

    def can_move(self, from_cell: Tuple[int, int], to_cell: Tuple[int, int]) -> bool:
        from_row, from_col = from_cell
        to_row, to_col = to_cell

        if not (0 <= from_row < self.height and 0 <= from_col < self.width and
                0 <= to_row < self.height and 0 <= to_col < self.width):
            return False # Out of bounds

        # Determine direction
        if from_row - to_row == 1 and from_col == to_col: # North
            return not self.walls[from_cell][0]
        elif to_row - from_row == 1 and from_col == to_col: # South
            return not self.walls[from_cell][2]
        elif to_col - from_col == 1 and from_row == to_row: # East
            return not self.walls[from_cell][1]
        elif from_col - to_col == 1 and from_row == to_row: # West
            return not self.walls[from_cell][3]
        return False # Not an adjacent cell

    def solve_maze_with_key(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        # Get the raw maze representation to find the key position
        raw_maze_str = self.get_raw_maze()
        key_pos = self.find_key_position(raw_maze_str)

        if not key_pos:
            print("Error: Key position not found in the maze representation.")
            return None

        # First, find path from start to key
        path_to_key = self.bfs_path(start, key_pos)
        if not path_to_key:
            return None

        # Then, find path from key to end
        path_to_end = self.bfs_path(key_pos, end)
        if not path_to_end:
            return None

        # Combine paths (remove duplicate key position)
        full_path = path_to_key + path_to_end[1:]
        return full_path

    def bfs_path(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        queue = collections.deque([(start, [start])])
        visited = {start}

        while queue:
            current_cell, path = queue.popleft()

            if current_cell == end:
                return path

            current_row, current_col = current_cell
            # Manually check neighbors based on can_move
            for dr, dc, direction_idx in [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)]:
                neighbor_cell = (current_row + dr, current_col + dc)

                if (0 <= neighbor_cell[0] < self.height and
                    0 <= neighbor_cell[1] < self.width and
                    neighbor_cell not in visited and
                    self.can_move(current_cell, neighbor_cell)):
                    
                    visited.add(neighbor_cell)
                    new_path = path + [neighbor_cell]
                    queue.append((neighbor_cell, new_path))
        return None

    def path_to_directions(self, path: List[Tuple[int, int]]) -> str:
        """Convert path to direction string (R, L, U, D)"""
        if len(path) < 2:
            return ""

        directions = []
        for i in range(len(path) - 1):
            current_row, current_col = path[i]
            next_row, next_col = path[i + 1]

            row_diff = next_row - current_row
            col_diff = next_col - current_col

            if row_diff == -1:  # Moving up
                directions.append("U")
            elif row_diff == 1:  # Moving down
                directions.append("D")
            elif col_diff == 1:  # Moving right
                directions.append("R")
            elif col_diff == -1:  # Moving left
                directions.append("L")

        return "".join(directions)

    def print_maze_simple(self, solution_path: List[Tuple[int, int]] = None):
        """Print a simple, compact maze representation"""
        # Top border
        print("# " * (self.width * 2 + 1))

        for row in range(self.height):
            # Main row with cell contents and vertical walls
            line = "# "
            for col in range(self.width):
                cell = (row, col)

                # Cell content
                if cell == (0, 0):
                    content = "S "  # Start
                elif cell == (self.height - 1, self.width - 1):
                    content = "$ "  # Exit
                elif cell == self.key_position:
                    content = "& "  # Key
                elif solution_path and cell in solution_path:
                    content = "• "  # Solution path
                else:
                    content = "  "  # Empty

                line += content

                # Vertical wall or passage
                if col < self.width - 1:
                    if self.can_move(cell, (row, col + 1)):
                        line += "  "  # Open
                    else:
                        line += "# "  # Wall

            line += "# "
            print(line)

            # Horizontal walls between rows
            if row < self.height - 1:
                line = "# "
                for col in range(self.width):
                    cell = (row, col)
                    if self.can_move(cell, (row + 1, col)):
                        line += "  "  # Open
                    else:
                        line += "# "  # Wall

                    if col < self.width - 1:
                        line += "# "

                line += "# "
                print(line)

        # Bottom border
        print("# " * (self.width * 2 + 1))
        
    def get_raw_maze(self, solution_path: List[Tuple[int, int]] = None) -> str:
        """Returns a simple, compact maze representation as a string"""
        maze_str = ""
        
        # Top border
        maze_str += ("#" * (self.width * 2 + 1)) + "\n"

        for row in range(self.height):
            # Main row with cell contents and vertical walls
            line = "#"
            for col in range(self.width):
                cell = (row, col)

                # Cell content
                if cell == (0, 0):
                    content = "S"  # Start
                elif cell == (self.height - 1, self.width - 1):
                    content = "$"  # Exit
                elif cell == self.key_position:
                    content = "&"  # Key
                elif solution_path and cell in solution_path:
                    content = "•"  # Solution path
                else:
                    content = " "  # Empty

                line += content

                # Vertical wall or passage
                if col < self.width - 1:
                    # Check the wall to the East (direction 1)
                    if not self.walls[cell][1]: # If wall is removed
                        line += " "  # Open
                    else:
                        line += "#"  # Wall

            line += "#" + "\n" 
            maze_str += line

            # Horizontal walls between rows
            if row < self.height - 1:
                line = "#"
                for col in range(self.width):
                    cell = (row, col)
                    # Check the wall to the South (direction 2)
                    if not self.walls[cell][2]: # If wall is removed
                        line += " "  # Open
                    else:
                        line += "#"  # Wall

                    if col < self.width - 1:
                        line += "#"

                line += "#" + "\n"
                maze_str += line

        # Bottom border
        maze_str += "#" * (self.width * 2 + 1) 
        
        return maze_str

    def find_key_position(self, raw_maze_str: str) -> Optional[Tuple[int, int]]:
        """
        Parses the raw maze string to find the key's position ('&').
        Returns (row, col) or None if not found.
        """
        lines = raw_maze_str.strip().split('\n')
        
        # Determine height and width from the string
        # Number of content rows (maze_height) = (len(lines) - 1) // 2
        # Number of content cols (maze_width) = (len(lines[1]) - 1) // 2
        
        # Using self.height and self.width directly, assuming the maze object already
        # has its dimensions set, or they will be set by generate_from_raw_maze.
        # If calling this independently, the dimensions need to be inferred.
        
        # For simplicity, let's assume the GridMaze object calling this has correct dimensions.
        # If not, add logic to infer width/height from 'lines' here.

        for r in range(self.height):
            for c in range(self.width):
                line_idx = 2 * r + 1
                char_idx = 2 * c + 1
                
                if line_idx < len(lines) and char_idx < len(lines[line_idx]):
                    if lines[line_idx][char_idx] == '&':
                        return (r, c)
        return None

    def generate_from_raw_maze(self, raw_maze_str: str):
        """
        Reconstructs the maze's internal wall representation from a raw maze string.
        Also sets the width, height, and key_position based on the string.
        """
        lines = raw_maze_str.strip().split('\n')
        
        # Determine dimensions
        # Height: Number of maze content rows. There are (height * 2) + 1 lines in total,
        # where maze content lines are at odd indices (1, 3, 5...).
        # So, (total_lines - 1) / 2 = height
        self.height = (len(lines) - 1) // 2
        
        # Width: Number of maze content columns. Each content line is (width * 2) + 1 characters long.
        # So, (line_length - 1) / 2 = width
        # Take the length of the first content line (index 1)
        self.width = (len(lines[1]) - 1) // 2

        # Reinitialize all walls as present
        self.walls = {}
        for r in range(self.height):
            for c in range(self.width):
                self.walls[(r, c)] = [True, True, True, True] # N, E, S, W (initially all walls)

        self.key_position = None # Reset key position for new maze

        for r in range(self.height):
            # Process horizontal walls (between rows)
            # These are on even-indexed lines (2, 4, ...)
            if r < self.height - 1: # Only for rows that have a row below them
                horizontal_wall_line_idx = 2 * r + 2
                if horizontal_wall_line_idx < len(lines):
                    current_line = lines[horizontal_wall_line_idx]
                    for c in range(self.width):
                        # Wall char is at index 2*c + 1
                        wall_char_idx = 2 * c + 1
                        if wall_char_idx < len(current_line):
                            if current_line[wall_char_idx] == ' ': # Open passage
                                # Remove South wall of cell (r, c)
                                self.remove_wall((r, c), (r + 1, c), 2) # 2 for South

            # Process vertical walls (within rows) and cell content
            # These are on odd-indexed lines (1, 3, ...)
            maze_content_line_idx = 2 * r + 1
            if maze_content_line_idx < len(lines):
                current_line = lines[maze_content_line_idx]
                for c in range(self.width):
                    # Check cell content first (char_idx 2*c + 1)
                    cell_content_char_idx = 2 * c + 1
                    if cell_content_char_idx < len(current_line):
                        if current_line[cell_content_char_idx] == '&':
                            self.key_position = (r, c)

                    # Check vertical wall to the East (char_idx 2*c + 2)
                    if c < self.width - 1: # Only for columns that have a column to their right
                        vertical_wall_char_idx = 2 * c + 2
                        if vertical_wall_char_idx < len(current_line):
                            if current_line[vertical_wall_char_idx] == ' ': # Open passage
                                # Remove East wall of cell (r, c)
                                self.remove_wall((r, c), (r, c + 1), 1) # 1 for East

        # After reconstruction, clear visited set (not relevant for static maze)
        self.visited.clear()



def main():
    # 1. Generate a maze
    print("--- Generating a new maze (10x10) ---")
    n = 10 # A reasonable size for demonstration
    maze = GridMaze(width=n, height=n)
    maze.generate_maze(0, 0) # Start maze generation from (0,0)

    # 2. Print its simple representation
    print("\nMaze Layout:")
    maze.print_maze_simple()

    # 3. Find and print the key's internal position
    print(f"\nKey location (internally set): Row {maze.key_position[0]}, Column {maze.key_position[1]}")

    start_point = (0, 0)
    end_point = (maze.height - 1, maze.width - 1)

    # 4. Solve the maze (start to key, then key to end)
    print("\n--- Attempting to solve the maze ---")
    solution_path = maze.solve_maze_with_key(start_point, end_point)

    if solution_path:
        print(f"\nSolution found! Path length: {len(solution_path)} steps")

        # 5. Print the solved maze
        print("\nSolution Path on Maze:")
        maze.print_maze_simple(solution_path)

        # 6. Display the path as directions
        direction_string = maze.path_to_directions(solution_path)
        print(f"\nDirections: {direction_string}")

        # Break down the solution
        # Find the key position from the raw maze string (as solve_maze_with_key does)
        raw_maze_str_for_key_find = maze.get_raw_maze()
        key_pos_from_raw = maze.find_key_position(raw_maze_str_for_key_find)
        
        if key_pos_from_raw and key_pos_from_raw in solution_path:
            key_index = solution_path.index(key_pos_from_raw)
            path_to_key = solution_path[: key_index + 1]
            path_from_key_to_end = solution_path[key_index:]
            print(f"  - Steps to key: {len(path_to_key)} steps")
            print(f"  - Steps from key to exit: {len(path_from_key_to_end) - 1} steps")
        else:
            print("  - Could not determine separate path lengths to key and then to exit.")


    else:
        print("\nNo solution found for the maze!")

    # 7. Show the raw maze string (with solution if found)
    print("\n--- Raw Maze Representation ---")
    print("This is the compact string format for maze data.")
    print(maze.get_raw_maze(solution_path))


if __name__ == "__main__":
    main()