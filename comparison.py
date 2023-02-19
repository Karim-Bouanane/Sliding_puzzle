from a_star import *
from bfs import *

# This function generate n puzzles (where n = sampling) with size = puzzle_size
# Each puzzle is solved with BFS, A* h1 and A* h2
# Then the average performance is printed out
def compare_bfs_h1_h2(puzzle_size, sampling):

    # local variables that sum the total results to be later averaged and printed 
    sum_time_bfs = 0
    sum_iterations_bfs = 0
    sum_nodes_bfs = 0
    sum_pathCost_bfs = 0

    sum_time_a_star_h1 = 0
    sum_iterations_a_star_h1 = 0
    sum_nodes_a_star_h1 = 0
    sum_pathCost_a_star_h1 = 0

    sum_time_a_star_h2 = 0
    sum_iterations_a_star_h2 = 0
    sum_nodes_a_star_h2 = 0
    sum_pathCost_a_star_h2 = 0

    timelimit = 60000              # equivalent to 1 minute
    bfs_timeout = False
    a_star_h2_timeout = False
    a_star_h1_timeout = False

    print("\n **************************** Puzzle Size: ", puzzle_size, " ****************************\n")

    for i in range(sampling):
        print("Iteration n°: ", i)

        rand_puzzle = get_random_puzzle(puzzle_size)

        # Run the BFS algo on the rand_puzzle
        bfs = BFS(rand_puzzle.matrix)
        if bfs_timeout == False:                 # checks if there isn't a previous timeout
            if bfs.solve(timelimit) == False:    # verify if timeout is reached
                bfs_timeout = True
        
        sum_time_bfs += bfs.getElapsedTime()
        sum_iterations_bfs += bfs.getIterations()
        sum_nodes_bfs += bfs.getTotalNodes()
        sum_pathCost_bfs += bfs.getPathCost()
        
        # Run the A* algo, first with h1 then with h2
        a_st = A_Star(rand_puzzle.matrix)

        # A* with h1
        if a_star_h1_timeout == False:                      # checks if there isn't a previous timeout
            if a_st.solve_with_h1(timelimit) == False:      # verify if timeout is reached
                a_star_h1_timeout = True

        sum_time_a_star_h1 += a_st.getElapsedTime()
        sum_iterations_a_star_h1 += a_st.getIterations()
        sum_nodes_a_star_h1 += a_st.getTotalNodes()
        sum_pathCost_a_star_h1 += a_st.getPathCost()

        # A* with h2
        if a_star_h2_timeout == False:                      # checks if there isn't a previous timeout
            if a_st.solve_with_h2(timelimit) == False:      # verify if timeout is reached
                a_star_h2_timeout = True

        sum_time_a_star_h2 += a_st.getElapsedTime()
        sum_iterations_a_star_h2 += a_st.getIterations()
        sum_nodes_a_star_h2 += a_st.getTotalNodes()
        sum_pathCost_a_star_h2 += a_st.getPathCost()


    ''' Print average performance '''
    print("\t\t\t bfs \t\t\t\t h1 \t\t\t\t h2 \n")

    if bfs_timeout ==  True:
        sum_time_bfs = 0
        sum_iterations_bfs = 0
        sum_nodes_bfs = 0
        sum_pathCost_bfs = 0

    if a_star_h1_timeout ==  True:
        sum_time_a_star_h1 = 0
        sum_iterations_a_star_h1 = 0
        sum_nodes_a_star_h1 = 0
        sum_pathCost_a_star_h1 = 0

    if a_star_h2_timeout ==  True:
        sum_time_a_star_h2 = 0
        sum_iterations_a_star_h2 = 0
        sum_nodes_a_star_h2 = 0
        sum_pathCost_a_star_h2 = 0


    print("time(ms): \t%15.1f" % (sum_time_bfs / sampling), 
                    "\t\t%15.1f" % (sum_time_a_star_h1 / sampling),
                    "\t\t%15.1f" % (sum_time_a_star_h2 / sampling))

    print("iterations: \t%15.1f" % (sum_iterations_bfs / sampling),
                    "\t\t%15.1f" % (sum_iterations_a_star_h1 / sampling),
                    "\t\t%15.1f" % (sum_iterations_a_star_h2 / sampling))

    print("nodes: \t\t%15.1f" % (sum_nodes_bfs / sampling),
                    "\t\t%15.1f" % (sum_nodes_a_star_h1 / sampling), 
                    "\t\t%15.1f" % (sum_nodes_a_star_h2 / sampling))

    print("pathCost: \t%15.1f" % (sum_pathCost_bfs / sampling),
                    "\t\t%15.1f" % (sum_pathCost_a_star_h1 / sampling), 
                    "\t\t%15.1f" % (sum_pathCost_a_star_h2 / sampling))


# Run the comparison function on different puzzle sizes
sampling = 5
for puzzle_size in range(3, 8):
    compare_bfs_h1_h2(puzzle_size, sampling)