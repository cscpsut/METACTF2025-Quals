#!/usr/bin/env python3
from pwn import *
from collections import deque

def parse_maze(maze_text):
    """Parse the maze and find start, key, and exit positions"""
    lines = maze_text.strip().split('\n')
    
    # Find maze lines (lines that contain '#' and are part of the maze structure)
    maze_lines = []
    for line in lines:
        if '#' in line and len(line) > 20:  # Maze lines should be reasonably long
            maze_lines.append(line)
    
    if not maze_lines:
        print("No maze lines found")
        return None, None, None, None
    
    # Find positions
    start = None
    key = None
    exit_pos = None
    
    maze = []
    for i, line in enumerate(maze_lines):
        maze.append(list(line))
        for j, char in enumerate(line):
            if char == 'S':
                start = (i, j)
            elif char == '&':
                key = (i, j)
            elif char == '$':
                exit_pos = (i, j)
    
    return maze, start, key, exit_pos

def bfs_path(maze, start, target):
    """Find shortest path using BFS - sprite moves 2 steps at a time"""
    if not maze or not start or not target:
        return None
    
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, "")])
    visited = set([start])
    
    # Directions: Right, Down, Left, Up (each move is 2 steps)
    directions = [(0, 2, 'R'), (2, 0, 'D'), (0, -2, 'L'), (-2, 0, 'U')]
    
    while queue:
        (row, col), path = queue.popleft()
        
        if (row, col) == target:
            return path
        
        for dr, dc, move in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                (new_row, new_col) not in visited):
                
                # Check if both the intermediate cell and destination are passable
                mid_row, mid_col = row + dr//2, col + dc//2
                
                if (0 <= mid_row < rows and 0 <= mid_col < cols):
                    mid_cell = maze[mid_row][mid_col]
                    dest_cell = maze[new_row][new_col]
                    
                    # Both intermediate and destination must be passable
                    if mid_cell != '#' and dest_cell != '#':
                        visited.add((new_row, new_col))
                        queue.append(((new_row, new_col), path + move))
    
    return None

def solve_maze(maze_text):
    """Solve the maze puzzle"""
    maze, start, key, exit_pos = parse_maze(maze_text)
    
    if not all([maze, start, key, exit_pos]):
        print(f"Failed to parse maze. Start: {start}, Key: {key}, Exit: {exit_pos}")
        return None
    
    print(f"Maze size: {len(maze)}x{len(maze[0]) if maze else 0}")
    print(f"Start: {start}, Key: {key}, Exit: {exit_pos}")
    
    # Path from start to key
    path1 = bfs_path(maze, start, key)
    if not path1:
        print("No path from start to key")
        return None
    
    # Path from key to exit
    path2 = bfs_path(maze, key, exit_pos)
    if not path2:
        print("No path from key to exit")
        return None
    
    full_path = path1 + path2
    return full_path

def main():
    try:
        # Connect to remote
        conn = remote('localhost', 1337)

        conn.recvuntil(b'> ')
        conn.sendline(b'2')
        maze_data = conn.recvuntil(b'Path:')
        maze_text = maze_data.decode()

        while True:
            # Get maze
            print("=== MAZE RECEIVED ===") 
            
            solution = solve_maze(maze_text)
            
            if solution:
                conn.sendline(solution.encode())
                maze_data = conn.recvuntil(b'Path:')
                maze_text = maze_data.decode()
                
                if "METACTF" in maze_text:
                    print("FLAG FOUND!")
                    print(maze_text)
                    break
            else:
                print("Failed to solve maze")

    except:
        print(conn.recvall())

if __name__ == "__main__":
    main()