from math import inf
from puzzle import *
from queue import Queue
from time import time


class BFS:

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

    # Return True if there is a solution, or False if there is a timeout
    def solve(self, timelimit=inf):
            startTime = time()                                                  # get current time in seconds (float)

            visited = Queue()                                                   # create a queue to store visited puzzles
            reached = {}                                                        # create dictionnary to store reached matrices
            iterations = 0                                                      # keep track of the number of iterations to reach the goal state

            visited.put(self.root_puzzle)                                       # insert root puzzle into the visited queue
            const_matrix = str(self.root_puzzle.matrix)                         # convert the matrix list to string because lists can not be used 
                                                                                # as a key in dictionnaries since they are not constant
            reached[const_matrix] = ''                                          # save string matrix to the dictionnary because it is fast to search
                                                                                # for it. Complexity O(1)

            while (not visited.empty()) and (int((time() - startTime) * 1000) < timelimit):

                iterations = iterations + 1                                     # increment iterations
                current_puzzle = visited.get()                                  # pop from the visited queue the next puzzle

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
                        visited.put(next_puzzle)                                # add the new discovered puzzle to the visisted queue
                        reached[const_matrix] = ''                              # add the new discovered puzzle matrix to the reached dictionnary

            return False                                                        # timeout


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
        for matrix in self.path:    
            # print 2D list
            for i in range(self.size):
                for j in range(self.size):
                    print(matrix[i][j], end=" ")
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