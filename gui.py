# Libraires
import os
from math import sqrt
from tkinter import *
from tkinter.filedialog import askopenfile

from puzzle import *
from bfs import *
from a_star import *


class GUI:
    

    # __init__ method is building the GUI interface with all components
    def __init__(self):
        ''' Initialize the global variables '''
        self.path = []                  # contains the whole path to the goal state
        self.matrix = []                # store the imported or generated matrix
        self.path_cost = 0              # store the number of states to reach the goal state
        self.current_instance_index = 0    # this variable tracks the current position inside the path array

        ''' Create the GUI window '''
        self.window = Tk()  # instantiate the tkinter object to create the GUI window

        # The GUI interface is divided into 3 frames. 
        # The top frame contains: - Generate and Upload Buttons, 
        #                         - Puzzle size and Time limit entries(text input),
        #                         - Algorithms buttons
        #                         - Output result details 
        # The middle frame or puzzle frame contains: only the puzzle matrix
        # The bottom frame contains: - Next and Previous buttons, 
        #                            - Index of current puzzle state inside the solution path

        self.top_frame = Frame(self.window, bg = '#FFFFFF')         # Create the top frame with white background
        self.puzzle_frame = Frame(self.window, bg = '#FFFFFF')      # Create the middle frame with white background
        self.bottom_frame = Frame(self.window, bg = '#FFFFFF')      # Create the bottom frame with withe background

        ''' Create all components for the TOP FRAME '''
        self.puzzle_size_entry = Entry(self.top_frame, bg = '#FFFFFF')                  # Create the text input for entring the puzzle size
        self.filename_label = Label(self.top_frame, bg = '#FFFFFF')                     # Create label for the uploaded filename
        self.error_message_label = Label(self.top_frame, bg = '#FFFFFF', fg='#FF0000')  # Create label to show the error messages
        self.generate_button = Button(self.top_frame)                                   # Create the generate button 
        self.upload_button = Button(self.top_frame)                                     # Create the upload button

        # Algorithms buttons
        self.algo_bfs_button = Button(self.top_frame)                   # Create the breadth first search algorithm button
        self.algo_Astar_h1_button = Button(self.top_frame)             # Create the A* with h1 search algorithm button
        self.algo_Astar_h2_button = Button(self.top_frame)             # Create the A* with h2 search algorithm button
        self.timelimit_label = Label(self.top_frame)                    # Create the timelimit label
        self.timelimit_entry = Entry(self.top_frame, bg = '#FFFFFF')    # Create the timelimit text input

        # Output Characteristics
        self.time_label = Label(self.top_frame, bg = '#FFFFFF')         # Create the label for the elapsed time of the execution
        self.iterations_label = Label(self.top_frame, bg = '#FFFFFF')   # Create the label for the number of iterations to reach the goal state
        self.nodes_label = Label(self.top_frame, bg = '#FFFFFF')        # Create the label for the total number of nodes created to reach the goal state
        self.path_cost_label = Label(self.top_frame, bg = '#FFFFFF')    # Create the label for the number of states in the solution path

        ''' Create all components for the BOTTOM FRAME '''
        self.current_instance_index_label = Label(self.bottom_frame)    # Create label to show the current instance in the solution path
        self.previous_instance_button = Button(self.bottom_frame)       # Create the previous instance button
        self.next_instance_button = Button(self.bottom_frame)           # Create the next instance button


    # run method is organizing and configuring all GUI components, and launch the GUI app
    def run(self):

        # Configure the window parameters
        self.window.title('Sliding Puzzle Solver')          # Configure window title
        self.window.geometry('700x600')                     # Configure window dimensions
        self.window.configure(bg = '#FFFFFF')               # Configure window background

        # Positionning Frames
        self.top_frame.pack(side = TOP)                     # Top frame is in the top side of the window
        self.puzzle_frame.pack(pady = 30)                   # Middle frame is below the top frame with a 30 pixel margin
        self.bottom_frame.pack(side = BOTTOM, pady = 25)    # Bottom frame is in the bottom side of the window

        ''' Top Frame '''
        # Generate Random Puzzle
        default_size_value = StringVar(self.top_frame, value='15')          # Default value to put inside the puzzle size text input
        self.puzzle_size_entry['textvariable'] = default_size_value         # Change the puzzle size text to the default size value
        self.puzzle_size_entry['width'] = 10                                # Configure the width of the puzzle size text input
        self.puzzle_size_entry.grid(row=0, column=0, padx=20, pady=5)       # Configure the position of the puzzle size text input

        self.generate_button['text'] = 'GENERATE'                           # Rename the generate button
        self.generate_button['command'] = self.generate_random_puzzle       # Associate generate_random_puzzle function to the click action
        self.generate_button.grid(row=1, column=0)                          # Configure the position of the generate button

        # Upload Puzzle
        self.filename_label['text'] = 'your_file.txt'                       # Rename the filename label
        self.filename_label.grid(row=0, column=1, padx=40)                  # Configure the position of the filename label

        self.upload_button['text'] = 'UPLOAD FILE'                          # Rename the upload button
        self.upload_button['command'] = self.upload_file                    # Associate upload_file function to the click action
        self.upload_button.grid(row=1, column=1)                            # Configure the position of the upload button 

        # Algorithms Buttons and timelimit input
        self.algo_bfs_button['text'] = 'Breadth First Search'               # Rename the bfs button
        self.algo_bfs_button['command'] = self.solve_with_bfs               # Associate the solve_with_bfs function to the click action
        self.algo_bfs_button.grid(row=0, column=2, sticky='ew')             # Configure the position of the bfs button

        self.algo_Astar_h1_button['text'] = 'A* h1 (Misplaced tiles)'      # Rename the Astar h1 button
        self.algo_Astar_h1_button['command'] = self.solve_with_a_star_h1   # Associate the solve_with_a_star function to the click action
        self.algo_Astar_h1_button.grid(row=1, column=2, sticky='ew')       # Configure the position of the Astar h1 button

        self.algo_Astar_h2_button['text'] = 'A* h2 (Manhattan distance)'   # Rename the Astar h2 button
        self.algo_Astar_h2_button['command'] = self.solve_with_a_star_h2   # Associate the solve_with_a_star_h2 function to the click action
        self.algo_Astar_h2_button.grid(row=2, column=2, sticky='ew')       # Configure the position of the Astar h2 button

        self.timelimit_label['text'] = "Time Limit(ms):"                    # Rename the timelimit label
        self.timelimit_label.grid(row=3, column=2, sticky='w')              # Configure the position of the timelimit label
        self.timelimit_entry['width'] = 10                                  # Configure the width of the timelimit entry
        self.timelimit_entry.grid(row=3, column=2, sticky='e')              # Configure the position of the timelimit entry

        # Output Characteristics
        self.time_label['text'] = "Time (ms):"                              # Rename the time label 
        self.time_label.grid(row=0, column=3, sticky='ew', padx=50)         # Configure the position of the time label

        self.iterations_label['text'] = "Iterations :"                      # Rename the iterations label
        self.iterations_label.grid(row=1, column=3, sticky='ew')            # Configure the position of the iterations label
        
        self.nodes_label['text'] = "Nodes:"                                 # Rename the nodes label
        self.nodes_label.grid(row=2, column=3, sticky='ew')                 # Configure the position of the nodes label

        self.path_cost_label['text'] = "Path cost:"                         # Rename the path cost label
        self.path_cost_label.grid(row=3, column=3, sticky='ew')             # Configure the position of the path cost label

        # Error Message
        self.error_message_label['text'] = 'ERROR MESSAGE: no error'                # Rename the error message label
        self.error_message_label.grid(row=4, pady=30, columnspan=4, sticky='ew')    # Configure the position of the error message label

        ''' Bottom Frame '''
        self.previous_instance_button['text'] = 'PREVIOUS'                          # Rename the previous instance button
        self.previous_instance_button['command'] = self.previous_puzzle_state       # Associate the previous_puzzle_state function with the click action
        self.previous_instance_button.grid(row=0, column=0)                         # Configure the position of the previous instance button

        self.current_instance_index_label['text'] = '0/0'                           # Rename the current instance index label
        self.current_instance_index_label.grid(row=0, column=1, padx=20)            # Configure the position of the current instance index label

        self.next_instance_button['text'] = 'NEXT'                                  # Rename the next instance button
        self.next_instance_button['command'] = self.next_puzzle_state               # Associate the next_puzzle_state function with the click action
        self.next_instance_button.grid(row=0, column=2)                             # Configure the position of the next instance button

        ''' Display a random puzzle at the application launch '''
        self.generate_random_puzzle()   # this will generate a random puzzle and draw it inside the puzzle frame

        ''' Run the GUI application '''
        self.window.mainloop()  


    # Generate a random puzzle and draw it in the puzzle frame
    def generate_random_puzzle(self):
        self.clear_output_results()                     # clear the output results before drawing new puzzle
        puzzle_size = self.puzzle_size_entry.get()      # retreive the input text from the puzzle size entry
        # verify if the input text contains only digits and it is a valid size
        if (puzzle_size.isnumeric() == True) and (self.verify_input_puzzle_size(int(puzzle_size)) == True):
            size = int(sqrt(int(puzzle_size) + 1))      # calculate the sqrt(size of the matrix)
                                                        # - int(puzzle_size) : convert string to integer
                                                        # - sqrt(int(puzzle_size)) + 1 : the sqrt of the whole matrix size gives
                                                        # the row, column size because they are same in the square matrix,
                                                        # and we are interrested only with the row size.
                                                        # - int(sqrt(int(puzzle_size)) + 1) :  convert float to int
            puzzle = get_random_puzzle(size)            # generate and return a random puzzle
            self.matrix = puzzle.matrix                 # store the generated puzzle matrix into the matrix global variable
            self.draw_puzzle(self.matrix)               # draw the generated matrix
        
        else:
            self.error_message_label.config(text = "ERROR MESSAGE: INVALID SIZE INPUT")
    

    # Upload new matrix from a file and draw it inside puzzle frame
    def upload_file(self):
        self.clear_output_results()                         # clear the output results before drawing new puzzle
        puzzle_file = askopenfile(mode ='r',                # open the file explorer window to search for a text file
                    filetypes =[('Text Files', '*.txt')])
        
        # verify if a file is selected
        if puzzle_file != None: 
            filename = os.path.basename(puzzle_file.name)   # retreive the filename from the file path
            self.filename_label.config(text = filename)     # rename the filename label with the uploaded filename

            self.matrix = []                                # clear the global matrix variable to put a new matrix
            lines = puzzle_file.readlines()                 # read all lines from the text file to iterate on them
            for line in lines:                              # iterate on every line
                row = []                                    # create new empty row
                list = line.rstrip('\n').split(' ')         # split line into numbers separated by a blank space
                for tile in list:                           # iterate through string numbers
                        row.append(int(tile))               # convert string numbers to int and add them to the row list
                self.matrix.append(row)                     # add row list to the matrix

            puzzle_file.close()                             # close file
            self.draw_puzzle(self.matrix)                   # draw matrix in the puzzle frame

        else:   # if no file is selected, then show the error message
            self.error_message_label.config(text = "ERROR MESSAGE: INVALID TEXT FILE")


    # Returns true if the input size is valid, otherwise false
    def verify_input_puzzle_size(self, number):
        # Check if the input number+1 is a square of an integer (input+1 = a * a) because the matrix is square.
        # For example: if the input is 8 then the matrix has 9 tiles and int(sqrt(8+1)) * int(sqrt(8+1)) = 3 * 3 = 8+1
        # but if the input is 7 then int(sqrt(7+1)) * int(sqrt(7+1)) = 2 * 2 = 4 which different of 7+1

        if number >= 3:    # matrix size need to be at least more than 3
            if(( int(sqrt(number + 1)) * int(sqrt(number + 1))) == (number + 1)):
                return True
        return False


    # Remove the puzzle matrix from the puzzle frame to put a new one
    def clear_puzzle(self):
        for widgets in self.puzzle_frame.winfo_children():  # iterate through every label in puzzle frame
            widgets.destroy()                               # destroy label


    # Draw the puzzle matrix in form of labels inside the puzzle frame
    def draw_puzzle(self, matrix):
        self.clear_puzzle()         # Clear the old displayed puzzle
        size = len(matrix[0])       # Get the matrix row size
        # Iterate through all elements of the matrix and create a new label for each
        for i in range(size):       
            for j in range(size):
                if matrix[i][j] != 0:
                    Label(self.puzzle_frame,                        # Create new label
                            text = str(matrix[i][j]),               # Rename the label by the element value
                            padx = 4,                               # Add top margin
                            bg = "#FFFFFF",                         # Change background color
                            borderwidth=1,                          # Change border line width
                            relief="solid",                         # Type of border line
                            font=("Arial", 20),                     # Change text font and size
                            width=2                                 # Expand label width
                        ).grid(row = i, column = j, sticky = 'ew')  # Configure the label position inside puzzle frame
                else:
                    Label(self.puzzle_frame,                        # Create new label
                            text = "",                              # Rename the label by the element value
                            padx = 4,                               # Add top margin
                            bg = "#FFFFFF",                         # Change background color
                            borderwidth=1,                          # Change border line width
                            relief="solid",                         # Type of border line
                            font=("Arial", 20),                     # Change text font and size
                            width=2                                 # Expand label width
                        ).grid(row = i, column = j, sticky = 'ew')  # Configure the label position inside puzzle frame

    # Return the user timelimit
    def get_timelimit(self):
        timelimit = self.timelimit_entry.get()                      # retreive the input text from the timelimit entry
        if timelimit.isnumeric() == True and int(timelimit) > 0:    # verify if the input text contains only digits
            return int(timelimit)                                   # convert string to int and return it
        return inf


    # This method is called when bfs button is clicked
    def solve_with_bfs(self):
        self.clear_output_results()             # Clear output results 
        self.draw_puzzle(self.matrix)           # Redraw the current puzzle matrix

        bfs = BFS(self.matrix)                  # Instantiate BFS class with the current matrix
        timelimit = self.get_timelimit()        # Get the user timelimit

        if bfs.solve(timelimit) == True:        # Find the solution path with breadth first search algo
            path = bfs.getPath()                # Get solution path
            pathCost = bfs.getPathCost()        # Get the number of actions to solve the puzzle
            time = bfs.getElapsedTime()         # Get elapsed time to solve the puzzle
            iterations = bfs.getIterations()    # Get number of iterations to solve the puzzle
            nodes = bfs.getTotalNodes()         # Get total nodes created during the solving

            self.set_output_results(path, pathCost, time, iterations, nodes) # Display output result
        
        else:
            self.error_message_label.config(text = "ERROR MESSAGE: TIMEOUT")


    # This method is called when A_star_h1 button is clicked
    def solve_with_a_star_h1(self):
        self.clear_output_results()                     # Clear output results 
        self.draw_puzzle(self.matrix)                   # Redraw the current puzzle matrix

        a_star = A_Star(self.matrix)                    # Instantiate A_Star class with the current matrix
        timelimit = self.get_timelimit()                # Get the user timelimit
        
        if a_star.solve_with_h1(timelimit) == True:     # Find the solution path with A* and h1 misplaced tiles algo
            path = a_star.getPath()                     # Get solution path
            pathCost = a_star.getPathCost()             # Get the number of actions to solve the puzzle
            time = a_star.getElapsedTime()              # Get elapsed time to solve the puzzle
            iterations = a_star.getIterations()         # Get number of iterations to solve the puzzle
            nodes = a_star.getTotalNodes()              # Get total nodes created during the solving

            self.set_output_results(path, pathCost, time, iterations, nodes) # Display output result

        else:
            self.error_message_label.config(text = "ERROR MESSAGE: TIMEOUT")


    # This method is called when A_star_h2 button is clicked
    def solve_with_a_star_h2(self):
        self.clear_output_results()                     # Clear output results 
        self.draw_puzzle(self.matrix)                   # Redraw the current puzzle matrix

        a_star = A_Star(self.matrix)                    # Instantiate A_Star class with the current matrix
        timelimit = self.get_timelimit()                # Get the user timelimit
        
        if a_star.solve_with_h2(timelimit) == True:     # Find the solution path with A* and h2 misplaced tiles algo
            path = a_star.getPath()                     # Get solution path
            pathCost = a_star.getPathCost()             # Get the number of actions to solve the puzzle
            time = a_star.getElapsedTime()              # Get elapsed time to solve the puzzle
            iterations = a_star.getIterations()         # Get number of iterations to solve the puzzle
            nodes = a_star.getTotalNodes()              # Get total nodes created during the solving

            self.set_output_results(path, pathCost, time, iterations, nodes) # Display output result
        
        else:
            self.error_message_label.config(text = "ERROR MESSAGE: TIMEOUT")


    # Display the solution details on the top right corner
    def set_output_results(self, path, pathCost, time, iterations, nodes):
        self.time_label.config(text = "Time(ms):\t" + str(time))                    # Change time label
        self.iterations_label.config(text = "Iterations:\t" + str(iterations))      # Change Iterations label
        self.nodes_label.config(text = "Nodes:\t\t" + str(nodes))                   # Change Nodes label
        self.current_instance_index_label.config(text= "0/" + str(pathCost))        # Change current instance label
        self.path_cost_label.config(text= "Path Cost:\t" + str(pathCost))           # Change Path Cost label
        self.path = path[::-1]                                                      # Inverse the path from current matrix to goal state matrix 
                                                                                    # and put it into its global variable
        self.path_cost = pathCost                                                   # Put pathCost value into its global variable


    # Reset the output results
    def clear_output_results(self):
        time = 0
        iterations = 0
        nodes = 0
        self.path = []
        self.path_cost = 0
        self.current_instance_index = 0
        self.set_output_results(self.path, self.path_cost, time, iterations, nodes)
        self.error_message_label.config(text = "")


    # This method is called when the previous instance button is clicked
    def previous_puzzle_state(self):
        previousIndex = self.current_instance_index - 1         # Decrement current instance index
        if previousIndex >= 0:                                  # Check if the index is valid (array begin with 0)
            puzzle = self.path[previousIndex]                   # Get the previous puzzle from the solution path
            self.draw_puzzle(puzzle)                            # Draw the previous puzzle matrix
            self.current_instance_index_label.config(text= str(previousIndex) + "/" + str(self.path_cost))
            self.current_instance_index = previousIndex         # Save previous index as current index


    # This method is called when the next instance button is clicked
    def next_puzzle_state(self):
        nextIndex = self.current_instance_index + 1             # Increment current instance index 
        if nextIndex <= self.path_cost:                         # Check if the index is valid (array end at pathCost value)
            puzzle = self.path[nextIndex]                       # Get the next puzzle from the solution path
            self.draw_puzzle(puzzle)                            # Draw the next puzzle matrix
            self.current_instance_index_label.config(text= str(nextIndex) + "/" + str(self.path_cost))  
            self.current_instance_index = nextIndex             # Save next index as current index