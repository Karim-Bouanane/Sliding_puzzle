import copy  
import random


class Puzzle:

    def __init__(self, parent, matrix, empty_tile_index, moves=0):
        self.parent = parent                        # Save the reference of the parent object 
                                                    # so as to construct the path of the solution.
                                                    # The root puzzle has None parent
        self.matrix = matrix                        # Initialize the puzzle matrix
        self.size = len(matrix[0])                  # Get the matrix row size
        self.empty_tile_index = empty_tile_index    # Initialize the empty tile index
        self.moves = moves                          # Initialize the number of moves that has been done
                                                    # to create this puzzle state


    # Returns true if the goal state is reached, otherwise false
    # Goal state of 8-puzzle is:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    def is_goal(self):
        # In each index position we need to find the following value (i * row size) + j
        row_size = self.size
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != (i * row_size) + j:
                    return False    # matrix isn't ordered
        return True                 # matrix is well ordered    


    # Returns a list of puzzles after trying different actions
    def get_all_possible_actions(self):
        possible_actions = []

        move_right_action = self.move_right_action()
        if move_right_action != None:
            possible_actions.append(move_right_action)

        move_left_action = self.move_left_action()
        if move_left_action != None:
            possible_actions.append(move_left_action)

        move_up_action = self.move_up_action()
        if move_up_action != None:
            possible_actions.append(move_up_action)

        move_down_action = self.move_down_action()
        if move_down_action != None:
            possible_actions.append(move_down_action)

        return possible_actions


    # Move right action is like:
    # 4 1 6       4 1 6
    # 3 0 5   ->  0 3 5
    # 2 7 8       2 7 8
    def move_right_action(self):
        x, y = self.empty_tile_index    # Get the index of the empty tile
        # if empty tile is on the first column then there is nothing
        # on its left to move it right
        if y != 0:
            # make a copy of the current matrix so as to make changes on it.
            # Attention new_matrix = self.matrix will not make a copy, it will just store its reference,
            # and any changes on new_matrix will be applied on self.matrix (which is not what I want)
            # So I used copy.deepcopy.
            new_matrix = copy.deepcopy(self.matrix)
            # swap the empty tile index with its left element
            new_matrix[x][y-1], new_matrix[x][y] = new_matrix[x][y], new_matrix[x][y-1]
            # Return new Puzzle
            # self          : reference to the current object instance
            # (x, y-1)      : the empty tile is moved left so its column index is decremented
            # self.moves+1  : one action is added on the moves of this object
            return Puzzle(self, new_matrix, (x, y-1), self.moves+1)
        return None


    # Move left action is like:
    # 4 1 6       4 1 6
    # 3 0 5   ->  3 5 0
    # 2 7 8       2 7 8
    def move_left_action(self):
        x, y = self.empty_tile_index    # Get the index of the empty tile
        # if empty tile is on the last column then there is nothing
        # on its right to move it left
        if y != (self.size - 1):
            new_matrix = copy.deepcopy(self.matrix)
            # swap the empty tile index with its right element
            new_matrix[x][y+1], new_matrix[x][y] = new_matrix[x][y], new_matrix[x][y+1]
            # Return new Puzzle
            # self          : reference to the current object instance
            # (x, y-1)      : the empty tile is moved right so its column index is incremented
            # self.moves+1  : one action is added on the moves of this object
            return Puzzle(self, new_matrix, (x, y+1), self.moves+1)
        return None


    # Move up action is like:
    # 4 1 6       4 1 6
    # 3 0 5   ->  3 7 5
    # 2 7 8       2 0 8
    def move_up_action(self):
        x, y = self.empty_tile_index    # Get the index of the empty tile
        # if empty tile is on the last row then there is nothing
        # on its bottom to move it up
        if x != (self.size - 1):
            new_matrix = copy.deepcopy(self.matrix)
            # swap the empty tile index with its bottom element
            new_matrix[x+1][y], new_matrix[x][y] = new_matrix[x][y], new_matrix[x+1][y]
            # Return new Puzzle
            # self          : reference to the current object instance
            # (x, y-1)      : the empty tile is moved down so its row index is incremented
            # self.moves+1  : one action is added on the moves of this object
            return Puzzle(self, new_matrix, (x+1, y), self.moves+1)
        return None


    # Move down action is like:
    # 4 1 6       4 0 6
    # 3 0 5   ->  3 1 5
    # 2 7 8       2 7 8
    def move_down_action(self):
        x, y = self.empty_tile_index    # Get the index of the empty tile
        # if empty tile is on the first row then there is nothing
        # on its top to move it down
        if x != 0:
            new_matrix = copy.deepcopy(self.matrix)
            # swap the empty tile index with its top element
            new_matrix[x-1][y], new_matrix[x][y] = new_matrix[x][y], new_matrix[x-1][y]
            # Return new Puzzle
            # self          : reference to the current object instance
            # (x, y-1)      : the empty tile is moved up so its row index is decrelented
            # self.moves+1  : one action is added on the moves of this object
            return Puzzle(self, new_matrix, (x-1, y), self.moves+1)
        return None


    # Find the input value in the current puzzle and return its index in a typle of (i, j)
    def find_tile(self, value):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] == value:
                    return (i, j)


    # Returns the object reference that created this puzzle object instance
    def get_parent(self):
        return self.parent


    # Returns the number of moves to reach this puzzle state
    def get_moves(self):
        return self.moves


    # Print the puzzle matrix
    def print(self):
        n = self.size
        for i in range(n):
            for j in range(n):
                print(self.matrix[i][j], end=" ")
            print('')
        print('')


    def is_solvable(self):
        pass


    # This method allows the comparison of two puzzle instances by using the (less than) operator (Puzzle() < Puzzle()).
    # It is obligatory to define it because in the Priority Queue that is used in A_Star Class, it uses the priority 
    # value to insert elements in order in the queue. But when two elements have the same priority value, then their data 
    # which is a puzzle instance must to be compared so as the Priority Queue know where to insert the element. So in order 
    # to compare these two puzzle instance we need to define this method __it__.
    def __lt__(self, other):
        # matrix are 2d list and in python they can be compared with the less than operator
        return self.matrix < other.matrix


''' Those are global functions '''

# Find and return the empty tile index in a typle of (i, j)
def get_empty_tile_index(matrix):
    size = len(matrix[0]) 
    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 0:
                return (i,j)


# Generate and return the goal state matrix
def get_goal_matrix(size):
    goal_matrix = []                        # this will be a 2d list that contains the goal matrix
    for i in range(size):                   # construct rows
        row = []
        for j in range(size):               # construct columns
            row.append((i * size) + j)
        goal_matrix.append(row)

    return goal_matrix


# Generate and return a random puzzle
# The idea is to start with the goal state puzzle and apply random actions to it.
def get_random_puzzle(size):
    goal_matrix = get_goal_matrix(size)                 # Get the goal matrix
    puzzle = Puzzle(None, goal_matrix, (0,0))           # Construct the goal puzzle

    mutations = random.randrange(20,50)                 # This represents the number of random actions 
                                                        # to be applied on the goal state puzzle
    for i in range(mutations):                          
        actions = puzzle.get_all_possible_actions()     # Get all possible actions, its returns list of puzzle instances
        puzzle = random.choice(actions)                 # Choose one random action

    puzzle.parent = None                                # Remove the parent
    return puzzle                                       # Return the random puzzle
