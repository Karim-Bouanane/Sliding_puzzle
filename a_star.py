from math import inf
from puzzle import *
from queue import PriorityQueue
from time import time


class A_Star:

    def __init__(self, root_matrix):
        self.size = len(root_matrix[0])                                         # get the size of matrix row 
        empty_tile_index = get_empty_tile_index(root_matrix)                    # get the empty tile index
        self.root_puzzle = Puzzle(None, root_matrix, empty_tile_index)          # construct the root puzzle from the input matrix    

        # Initialize global variables
        self.elapsedTime = 0                                                    # represent the elapsed time during solving  
        self.iterations = 0                                                     # represent the number of iterations
        self.nodes = 0                                                          # represent the total nodes created
        self.path = []                                                          # represent the solution path
        self.pathCost = 0                                                       # represent the number of puzzles in the solution path
                                                                                # which mean the number of moves to reach the goal state puzzle

    def solve(self, heuristic, timelimit=inf):
            startTime = time()                                                  # get current time in seconds (float)

            visited = PriorityQueue()                                           # create a priority queue to store visited puzzles
                                                                                # the lowest priority value will be the first to be pulled out from the queue
            reached = {}                                                        # create dictionnary to store reached matrices
            iterations = 0                                                      # keep track of the number of iterations to reach the goal state

            visited.put((0, self.root_puzzle))
            const_matrix = str(self.root_puzzle.matrix)                         # convert the matrix list to string because lists can not be used
                                                                                # as a key in dictionnaries since they are not constant
            reached[const_matrix] = ''                                          # save string matrix to the dictionnary because it is fast to search

            while (not visited.empty()) and (int((time() - startTime) * 1000) < timelimit):

                iterations = iterations + 1                                     # increment iterations
                puzzle_priority, current_puzzle = visited.get()                 # pop from the visited queue the next puzzle

                if current_puzzle.is_goal() == True:                            # verify if the current puzzle is the goal state
                    endTime = time()                                            # get current time in seconds (float)
                    self.elapsedTime = int((endTime - startTime) * 1000)        # calculate elapsed time and convert it to milliseconds
                    self.iterations = iterations                                # save iterations value to its global variable
                    self.nodes = len(reached)                                   # save total nodes value to its global variable
                    self.path = self.findPath(current_puzzle)                   # get the solution path and save it to its global variable
                    self.pathCost = len(self.path) - 1                          # save the number of moves to reach the goal state
                                                                                # we decrement by -1 because our root puzzle is in the path
                                                                                # and we don't count it as a move.
                    return True                                                 # solution found
            
                for next_puzzle in current_puzzle.get_all_possible_actions():   # iterate though all possible puzzles created from the current vistied puzzle
                    const_matrix = str(next_puzzle.matrix)                      # convert matrix list to string so as to search for it in the reached dictionnary
                    if const_matrix not in reached:                             # verify if the matrix is not already reached
                        priority = next_puzzle.get_moves() + heuristic(next_puzzle)
                        visited.put((priority, next_puzzle))                    # add the new discovered puzzle to the visisted queue
                        reached[const_matrix] = ''                              # add the new discovered puzzle matrix to the reached dictionnary


            return False                                                        # timeout


    # Call the solve method with the h1_misplaced_tiles method
    def solve_with_h1(self, timelimit=inf):
        # Note: the self.h1_misplaced_tiles is a method
        return self.solve(self.h1_misplaced_tiles, timelimit)


    # Call the solve method with the h2_manhattan_distance method
    def solve_with_h2(self, timelimit=inf):
        # Note: the self.h2_manhattan_distance is a method
        return self.solve(self.h2_manhattan_distance, timelimit)


    # Return the total number of misplaced tiles
    def h1_misplaced_tiles(self, puzzle):
        matrix = puzzle.matrix      # only renames the variable
        size = puzzle.size          # only renames the variable
        misplaced = 0               # store the sum of misplaced tiles
        # iterate through each element of the matrix 
        for i in range(size):
            for j in range(size):
                # check if each element value is in it's goal position
                if matrix[i][j] != (i * size) + j:  
                    misplaced += 1
        
        return misplaced            # return sum of misplaced tiles


    # Return sum of manhattan distances
    def h2_manhattan_distance(self, puzzle):
        matrix = puzzle.matrix      # only rename the variable
        size = puzzle.size          # only rename the variable
        distance = 0                # store the sum of manhattan distances
        # The following loop, will iterate over each position (i, j) on the goal matrix
        # and get the goal value. Then find where is that goal value in the current puzzle.
        # Finally the manhattan distance is calculated as follow:
        # manhattan distance = |i - i1| + |j - j1|
        for i in range(size):
            for j in range(size):
                goal_value = (i * size) + j
                i1, j1 = puzzle.find_tile(goal_value)
    
                distance += abs(i - i1) + abs(j - j1)

                # for example in this 3 tile puzzle:
                # 2 3
                # 1 0
                # the sum of manhanttan distances is :
                # abs(0 - 1) + abs(0 - 1)   - Value 0 in goal state is in position (0,0), and in the current puzzle (1,1)
                # abs(0 - 1) + abs(1 - 0)   - Value 1 in goal state is in pos (0, 1) and in curr puzzle (1, 0) 
                # abs(1 - 0) + abs(0 - 0)   - Value 2 in goal state is in pos (1, 0) and in curr puzzle (0, 0)
                # abs(1 - 0) + abs(1 - 1)   - Value 3 in goal state is in pos (1, 1) and in curr puzzle (0, 1)
                # sum = 2 + 2 + 1 + 1 = 6

        return distance


    # Search for the solution path 
    def findPath(self, puzzle):
        path = []                           # store all matrices to the solution
        # trace puzzles from the goal state to the root puzzle
        parent = puzzle                     
        while parent != None:               # stop when the root puzzle is found
            path.append(parent.matrix)      # path contains only matrices without puzzle objects
            parent = parent.get_parent()    # get the puzzle parent
        return path


    # Iterate through the solution path, and print all matrices
    def printPath(self):
        # path contains matrices and not puzzle objects
        for puzzle_matrix in self.path:
            # print 2D list
            for i in range(self.size):
                for j in range(self.size):
                    print(puzzle_matrix[i][j], end=" ")
                print('')
            print('')


    ''' Getters '''
    def getIterations(self):
        return self.iterations

    def getTotalNodes(self):
        return self.nodes
    
    def getPath(self):
        return self.path
    
    def getPathCost(self):
        return self.pathCost

    def getElapsedTime(self):
        return self.elapsedTime