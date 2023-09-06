#!/usr/bin/env python
# coding: utf-8

# In[1]:


import queue
import copy


# In[2]:


# Constructing some mazes to search
# Note to those using this code: you can add your own mazes and call that specific buildMaze function to test your own maze
def buildMaze():
    maze = []
    maze.append(['#','S','#'])
    maze.append(['#',' ','#'])
    maze.append(['T',' ','E'])
    maze.append(['#','#','#'])
    return maze   

def buildMaze2():
    maze = []
    maze.append(['#','#','S','#','#','#','#','#','#'])
    maze.append(['#','#',' ','#','#','#','#','E','#'])
    maze.append([' ','T',' ',' ',' ',' ',' ',' ','#'])
    maze.append(['#','#','#','#',' ','#','#','#','#'])
    return maze   

def buildMaze3():
    maze = []
    maze.append(['#','S','#','#','#','#','#','#','#','#','#','#'])
    maze.append(['#',' ','#',' ',' ',' ','#','#',' ',' ',' ','#'])
    maze.append(['#',' ',' ',' ','#',' ',' ',' ',' ','#',' ','#'])
    maze.append(['#',' ','#','#','#',' ','#','#','#','#',' ','#'])
    maze.append(['#',' ','#','#','#','T','#','T',' ',' ',' ','#'])
    maze.append(['#',' ','#','#','#','#','#','#','#','#',' ','#'])
    maze.append(['#',' ',' ','#',' ','#','#',' ','#','#',' ','#'])
    maze.append(['#','#','#','#',' ',' ',' ',' ',' ',' ',' ','#'])
    maze.append(['#','#','#','#','#','E','#','#','#','#','#','#'])
    return maze


# In[3]:


def printMaze(maze,best_path=''):
    for row in maze:
        print(' '.join(row))
 
# Finds the best (shortest) path of all successful paths, accounting for treasure found
def findBestPath(maze,successful_paths):
    best_path = []
    best_path_value = 1000000
    for path in successful_paths:
        # The default value of a path is the number of "steps," which means the number of coordinates visited
        path_value = len(path)
        
        # Applying the concept of "hidden treasure"; if a 'T' cell was found, which signifies treasure, this makes the path more valuable in this proposed simulation
        # Thus, 7 "steps" will be removed from the path per each treasure found; this is just an example value
        for item in path:
            i, j = item
            if maze[i][j]=='T':
                path_value-=7
         
        # Store the best path
        if path_value<best_path_value:
            best_path = path
            best_path_value = path_value
    
    printPaths(maze,[best_path],True)

def printPaths(maze,successful_paths,best_path = False):
    print('The original maze:')
    printMaze(maze)

    for i, path in enumerate(successful_paths):
        # If the best path is passed to this function, print accordingly
        if best_path:
            print('\n')
            print('The best path (accounting for steps and treasure found) is as follows:')
            
        else:
            print('\n')
            print(f'Successful path {i+1}:')
        
        # Create a deep copy of the maze so that the original maze can continue being used as an unchanged reference for all iterations 
        copy_maze = copy.deepcopy(maze)
        
        # Mark coordinates of path with '|' to signify traversal
        for i in range(len(copy_maze)):
            for j in range(len(copy_maze[0])):
                if (i,j) in path:
                    copy_maze[i][j] = '|'
        
        # Print the path in the maze
        printMaze(copy_maze)

def findStart(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j]=='S':
                return (i,j)
            
def findEnd(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j]=='E':
                return (i,j)


# In[4]:


def bfs(maze,paths,end):
    successful_paths = []
    while not paths.empty():
        
        # Pop a path from the Queue
        reference = paths.get()
        
        # Check if the end point is in the current path; if so, store the path as a success and continue
        if end in reference:
            successful_paths.append(reference)
            continue
       
        # Gather i and j coordinates of current point
        i = reference[-1][0]
        j = reference[-1][1]
      
        # Keep booleans for validity of move in each direction
        up, paths = validMove(i-1,j,maze,reference,paths)
        down, paths = validMove(i+1,j,maze,reference,paths)
        left, paths = validMove(i,j-1,maze,reference,paths)
        right, paths = validMove(i,j+1,maze,reference,paths)
           
        # If no move is valid, backtrack to the last item in the path that has a non-explored, valid move 
        if not (up or down or left or right):
            add = reference[:]
            backtracked_path = backtrack(maze,add)
            paths.put(backtracked_path)
            
    return successful_paths


# In[5]:


def validMove(i,j,maze,reference,paths):
    if 0<=i<len(maze) and 0<=j<len(maze[0]) and maze[i][j]!='#' and (i,j) not in reference:
        add = reference[:]
        add.append((i,j))
        paths.put(add)
        return True, paths
    return False, paths


# In[6]:


def backtrack(maze,path):
    copy_path = path[:]
    skip = True
    
    # Traverse the passed path backwards, adding each point (besides the starting point) that does not have an unexplored, valid move to the path (simulating backtracking)
    for item in reversed(copy_path):
        # Skip the first iteration since we do not need to check the current point once more (which was done in the bfs function)
        if skip:
            skip = False
            continue
        
        # Add the coordinates of the current item to the path since backtracking is taking place
        i, j = item
        path.append((i,j))
        
        # If this current item has an unexplored, valid move in any direction, append it to the path and return the path
        # This could be tailored to use the "validMove" function like my "bfs" function does; however, since this function is returning a singular path, it is a bit easier for me to understand this way
        if i-1>=0 and maze[i-1][j]!='#' and (i-1,j) not in path:
            path.append((i-1,j))
            return path
        
        if i+1<len(maze) and maze[i+1][j]!='#' and (i+1,j) not in path:
            path.append((i+1,j))
            return path
        
        if j-1>=0 and maze[i][j-1]!='#' and (i,j-1) not in path:
            path.append((i,j-1))
            return path    
        
        if j+1<len(maze[0]) and maze[i][j+1]!='#' and (i,j+1) not in path:
            path.append((i,j+1))
            return path   
        
    return path


# In[7]:


# Construct the maze from one of the preset options; note that any maze can be passed though as long as it has a start and end
#maze = buildMaze()
#maze = buildMaze2()
maze = buildMaze3() 

# Display the maze
print('The maze is as follows:')
printMaze(maze)

# Gather the start and end coordinates
start = findStart(maze)
end = findEnd(maze)

# Create the Queue that keeps track of paths in the bfs function
paths = queue.Queue()

# Add the starting coordinates (tuple) inside of a list to the Queue 
paths.put([start])


# In[8]:


# Call bfs (breadth-first search) to find all possible successful paths for the maze
successful_paths = bfs(maze,paths,end)


# In[9]:


# Display the coordinates of each successful path
print('The successful paths are as follows:')
for path in successful_paths:
    print(path)


# In[10]:


# Print the original maze as well as all the possible successful paths (that finish going a direction they start) marked in the maze
printPaths(maze,successful_paths)


# In[11]:


# Print and display the best path; keep note that finding treasure removes 7 steps from a path's step value
# See the "findBestPath" function for more comments 
findBestPath(maze,successful_paths)

