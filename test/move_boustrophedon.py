from matplotlib import pyplot as plt
from random import randint
import cv2
import numpy as np
# def display_tracked_paths(input_im, x_coordinates,y_coordinates, cell_order):
#     # Assumption: Robot will start moving from left most point of each cell
#     # Cell order keeps the cell numbers in order, i.e. visit cell_order[0] first
#     fig_paths = plt.figure()
#     plt.show(block=False)
#     plt.ion()
#     # Image artist is needed to make drawing faster!  
#     ax = plt.gca() 
#     img_artist = ax.imshow(input_im)
#     input("Press Enter to Start the Movement of the Robot")
#     for i in range(len(cell_order)): #iterate through each cell in order
#         cell = cell_order[i]
#         print("Current cell: ", cell)
#         cell_color = [randint(0,255+1),randint(0,255+1),randint(0,255+1)]
#         # Robot will move vertical then move forward to next column 
#         x_start = x_coordinates[cell][0] #Starting point x
#         x_end = x_coordinates[cell][-1]  #Ending point x
#         robot_size = 5 #square in pixels
#         current_y_length = len(y_coordinates[cell])
#         # I will assume no need to modulate the starting point
#         x_end_modulated = x_end - (x_end % robot_size) 
#         for j in range(x_start,x_end_modulated+robot_size,robot_size): #iteration of x coordinates
#             # This if else structure is to fix the problem about implementation
#             # y_coordinates[cell][0] is sometimes list sometimes tuple depending on the cell
#             # If else is a straightforward solution for this --> This is not cheating at all! :D  
#             #current_y_length-robot_size for other y_start/end
#             try:
#                 y_ind = j%x_start
#                 if y_ind == current_y_length:
#                     y_ind = y_ind-robot_size
#             except ZeroDivisionError:
#                 y_ind = j
#             #print("Y index: ", y_ind)
#             if type(y_coordinates[cell][0]) is list:
#                 # Take the average of within robot size range since all the objects are not rectangular
#                 # for example y might be [(1,210),(1,211),(1,211),(1,212)]
#                 # Therefore, y_start will be (1+1)/2=1 and y_end will be (210+212)/2=211
#                 #print("y coordinates:: ",y_coordinates[cell][y_ind])
#                 y_start = y_coordinates[cell][y_ind][0][0]
#                 y_end = y_coordinates[cell][y_ind][0][1]
#                 #y_start = (y_coordinates[cell][y_ind][0][0]+y_coordinates[cell][y_ind+robot_size][0][0])//2
#                 #y_end = (y_coordinates[cell][y_ind][0][1]+y_coordinates[cell][y_ind+robot_size][0][1])//2
#             else:
#                 #print("y coordinates:: ",y_coordinates[cell][y_ind])
#                 y_start = y_coordinates[cell][y_ind][0]
#                 y_end = y_coordinates[cell][y_ind][1]
#                 #y_start = (y_coordinates[cell][y_ind][0]+y_coordinates[cell][y_ind+robot_size][0])//2
#                 #y_end = (y_coordinates[cell][y_ind][1]+y_coordinates[cell][y_ind+robot_size][1])//2
#             # TO DO: modulate y_start as well!
#             #print("y_start: ",y_start)
#             #print("y_end: ", y_end)
#             y_end_modulated = y_end - (y_end % robot_size)
#             if (j%2) == 0: #move down
#                 for k in range(y_start,y_end_modulated,robot_size): #iteration of y coordinates
#                     #input_in[y,x] --> It is weird, but related to opencv nothing to do! 
#                     #print("x coordinate: ", j)
#                     input_im[k:k+robot_size,j:j+robot_size] = cell_color  
#                     img_artist.set_data(input_im)
#                     plt.draw()
#                     plt.pause(0.00000000001)
#             else: #move up
#                 for k in range(y_end_modulated-robot_size,y_start-robot_size,-robot_size): #iteration of y coordinates
#                     #input_in[y,x] --> It is weird, but related to opencv nothing to do! 
#                     #print("x coordinate: ", j)
#                     input_im[k:k+robot_size,j:j+robot_size] = cell_color  
#                     img_artist.set_data(input_im)
#                     plt.draw()
#                     plt.pause(0.00000000001)

#             ## I am not sure indent of the below part and probably it needs to be changed
#             #if ((x_end % robot_size) != 0) or ((y_end % robot_size) != 0):
#             #    print("Last part is fixed!")
#             #    input_im[x_end_modulated+robot_size:x_end,y_end_modulated+robot_size:y_end] = [255,0,0]
#             #    img_artist.set_data(input_im)
        
#         print("Following cell is completed: ", cell)
    
   ##-----------------------------------------   



    #print("X coordinates: ", x_coordinates[1])

    
    #fig_asdadasdas  = plt.figure()
    #input_im[25:25,25:25] = [255,0,0]
    #plt.show(block=False)
    #plt.imshow(input_im)
    #plt.draw()

    #for i in range(len(x_coordinates)):
    #    for j in range(len(y_coordinates)): 
    #        display_img[input_im == i, input_im == j] = [0,0,255] #Red color
    #        plt.imshow(display_img)
    #for i in range(300):    
    #    display_img[input_im == 10,i] = [0,0,255] #Red color
    #    plt.imshow(display_img)
    #for i in range(15):
    #    display_img[30+i,15]= [0,0,255]
    #    plt.plot(display_img)
##----------------------------------------------



##-------------------------------------------------------------------------------------
# def track_paths(original_im,cells_to_visit,cell_boundaries,nonneighbors):
#     """
#         Input: original_im --> Input map image without any preprocessing
#         Input: cells_to_visit --> It contains the order of cells to visit
#         Input: cell_boundaries --> It contains y coordinates of each cell
#             x coordinates will be calculated in this function based on 
#             cell number since first cell starts from the left and moves towards
#             right
#         Input: Nonneighbors --> This shows cels which are separated by the objects
#                 ,so these cells should have the same x coordinates!
#         Output: draw the executed path on the image
#             Path will be boustrophedonial --> zig,zag
#         Output: total travel time
#     """
#     ## TODO: Calculate the margin at the beginning and at the end for x coordinates
#             # They don't start at x=0 actually!


#     total_cell_number = len(cells_to_visit)

#     # Find the total length of the axises
#     size_x = original_im.shape[1]
#     size_y = original_im.shape[0]
    
#     # Calculate x coordinates of each cell
#     cells_x_coordinates = {}
#     width_accum_prev = 0
#     cell_idx = 1
#     while cell_idx <= total_cell_number:
#         #print("Cell index: ", cell_idx)
#         for subneighbor in nonneighbors:
#             #print("Subneighbor: ", subneighbor)
#             if subneighbor[0] == cell_idx: #current_cell, i.e. cell_idx is divided by the object(s)
#                 #print("Current cell is problematic")
#                 separated_cell_number = len(subneighbor) #contains how many cells are in the same vertical line 
#                 width_current_cell = len(cell_boundaries[cell_idx])
#                 #print("Width current cell: ", width_current_cell)
#                 for j in range(separated_cell_number):
#                     # All cells separated by the object(s) in this vertical line have same x coordinates 
#                     cells_x_coordinates[cell_idx+j] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
#                 width_accum_prev += width_current_cell
#                 #cell_idx = cell_idx + separated_cell_number 
#                 cell_idx += separated_cell_number
#                 break
        
#         #current cell is not separated by any object(s)
#         #print("Current cell is okay")
#         width_current_cell = len(cell_boundaries[cell_idx])
#         #print("Width current cell: ", width_current_cell)
#         cells_x_coordinates[cell_idx] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
#         width_accum_prev += width_current_cell

#         cell_idx = cell_idx + 1
#         # end of x calculation while loop
    
#     display_tracked_paths(original_im,cells_x_coordinates,cell_boundaries,cells_to_visit)
    
    ## Debug
    #print("##############DEBUG##########")
    #for i in range(total_cell_number):
    #    print("cell index: ", i+1)
    #    print("width: ", len(cell_boundaries[i+1]))
    ## Debug
    #print("##############DEBUG##########")
    #for i in range(total_cell_number):
    #    print("cell index: ", i+1)
    #    print("X coordinates: ", cells_x_coordinates[i+1])

    #for i in range(len(cells_to_visit)):
    #    current_cell = cells_to_visit[i]
    #    boundaries_current_cell = cell_boundaries[current_cell]





# def calculate_x_coordinates(x_size,y_size,cells_to_visit,cell_boundaries,nonneighbors):
#     """
#         Input: cells_to_visit --> It contains the order of cells to visit
#         Input: cell_boundaries --> It contains y coordinates of each cell
#             x coordinates will be calculated in this function based on 
#             cell number since first cell starts from the left and moves towards
#             right
#         Input: Nonneighbors --> This shows cels which are separated by the objects
#                 ,so these cells should have the same x coordinates!
#         Output: cells_x_coordinates --> x coordinates of each cell
#     """

#     total_cell_number = len(cells_to_visit)

#     # Find the total length of the axises
#     size_x = x_size
#     size_y = y_size
    
#     # Calculate x coordinates of each cell
#     cells_x_coordinates = {}
#     width_accum_prev = 0
#     cell_idx = 1
#     while cell_idx <= total_cell_number:
#         #print("Cell index: ", cell_idx)
#         for subneighbor in nonneighbors:
#             #print("Subneighbor: ", subneighbor)
#             if subneighbor[0] == cell_idx: #current_cell, i.e. cell_idx is divided by the object(s)
#                 #print("Current cell is problematic")
#                 separated_cell_number = len(subneighbor) #contains how many cells are in the same vertical line 
#                 width_current_cell = len(cell_boundaries[cell_idx])
#                 #print("Width current cell: ", width_current_cell)
#                 for j in range(separated_cell_number):
#                     # All cells separated by the object(s) in this vertical line have same x coordinates 
#                     cells_x_coordinates[cell_idx+j] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
#                 width_accum_prev += width_current_cell
#                 cell_idx = cell_idx + separated_cell_number 
#                 break
        
#         #current cell is not separated by any object(s)
#         #print("Current cell is okay")
#         width_current_cell = len(cell_boundaries[cell_idx])
#         #print("Width current cell: ", width_current_cell)
#         cells_x_coordinates[cell_idx] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
#         width_accum_prev += width_current_cell

#         cell_idx = cell_idx + 1
#         # end of x calculation while loop
    
#     return cells_x_coordinates
# -----------------------------------------------------

# def calculate_x_coordinates(x_size, y_size, cells_to_visit, cell_boundaries, nonneighbors):
#     """
#         Input: cells_to_visit --> It contains the order of cells to visit
#         Input: cell_boundaries --> It contains y coordinates of each cell
#             x coordinates will be calculated in this function based on 
#             cell number since first cell starts from the left and moves towards
#             right
#         Input: Nonneighbors --> This shows cels which are separated by the objects
#                 ,so these cells should have the same x coordinates!
#         Output: cells_x_coordinates --> x coordinates of each cell
#     """

#     total_cell_number = len(cells_to_visit)

#     # Find the total length of the axes
#     size_x = x_size
#     size_y = y_size
    
#     # Calculate x coordinates of each cell
#     cells_x_coordinates = {}
#     width_accum_prev = 0
#     cell_idx = 1
#     while cell_idx <= total_cell_number:
#         for subneighbor in nonneighbors:
#             if subneighbor[0] == cell_idx: # current_cell, i.e. cell_idx is divided by the object(s)
#                 separated_cell_number = len(subneighbor) # contains how many cells are in the same vertical line 
#                 width_current_cell = len(cell_boundaries[cell_idx])
#                 for j in range(separated_cell_number):
#                     # All cells separated by the object(s) in this vertical line have same x coordinates 
#                     cells_x_coordinates[cell_idx+j] = list(range(width_accum_prev, width_current_cell+width_accum_prev))
#                 width_accum_prev += width_current_cell
#                 cell_idx += separated_cell_number
#                 break
        
#         # current cell is not separated by any object(s)
#         if cell_idx not in cells_x_coordinates:  # Ensure this cell hasn't been processed in the above loop
#             width_current_cell = len(cell_boundaries[cell_idx])
#             cells_x_coordinates[cell_idx] = list(range(width_accum_prev, width_current_cell+width_accum_prev))
#             width_accum_prev += width_current_cell
#             cell_idx += 1
    
#     return cells_x_coordinates

def calculate_x_coordinates(x_size, y_size, cells_to_visit, cell_boundaries, nonneighbors):
    """
    Calculate x coordinates for each cell.

    Parameters:
        x_size (int): Total size of the x-axis.
        y_size (int): Total size of the y-axis.
        cells_to_visit (list): Order of cells to visit.
        cell_boundaries (dict): Contains y coordinates of each cell.
        nonneighbors (list): Cells separated by objects.

    Returns:
        dict: x coordinates of each cell.
    """
    total_cell_number = len(cells_to_visit)
    cells_x_coordinates = {}
    width_accum_prev = 0
    cell_idx = 1

    while cell_idx <= total_cell_number:
        for subneighbor in nonneighbors:
            if subneighbor[0] == cell_idx:
                separated_cell_number = len(subneighbor)
                if cell_idx in cell_boundaries:
                    width_current_cell = len(cell_boundaries[cell_idx])
                    for j in range(separated_cell_number):
                        cells_x_coordinates[cell_idx + j] = list(range(width_accum_prev, width_current_cell + width_accum_prev))
                    width_accum_prev += width_current_cell
                    cell_idx += separated_cell_number
                else:
                    print(f"Warning: Cell index {cell_idx} not found in cell_boundaries.")
                    cell_idx += separated_cell_number
                break
        else:
            if cell_idx in cell_boundaries:
                width_current_cell = len(cell_boundaries[cell_idx])
                cells_x_coordinates[cell_idx] = list(range(width_accum_prev, width_current_cell + width_accum_prev))
                width_accum_prev += width_current_cell
                cell_idx += 1
            else:
                print(f"Warning: Cell index {cell_idx} not found in cell_boundaries.")
                cell_idx += 1

    return cells_x_coordinates



def track_paths(original_im, cells_to_visit, cell_boundaries, nonneighbors):
    """
        Input: original_im --> Input map image without any preprocessing
        Input: cells_to_visit --> It contains the order of cells to visit
        Input: cell_boundaries --> It contains y coordinates of each cell
            x coordinates will be calculated in this function based on 
            cell number since first cell starts from the left and moves towards
            right
        Input: Nonneighbors --> This shows cels which are separated by the objects
                ,so these cells should have the same x coordinates!
        Output: draw the executed path on the image
            Path will be boustrophedonial --> zig,zag
        Output: total travel time
    """

    total_cell_number = len(cells_to_visit)
    size_x = original_im.shape[1]
    size_y = original_im.shape[0]

    cells_x_coordinates = calculate_x_coordinates(size_x, size_y, cells_to_visit, cell_boundaries, nonneighbors)
    
    display_tracked_paths(original_im, cells_x_coordinates, cell_boundaries, cells_to_visit)

def draw_cell_boundary(img, x, y_start, y_end, color=[255, 255, 255], thickness=1):
    """Draw a vertical line to represent cell boundary"""
    cv2.line(img, (x, y_start), (x, y_end), color, thickness)

def is_free_space(img, x, y):
    return np.all(img[y, x] != [0, 0, 0])  # 假设障碍物是黑色的

def display_tracked_paths(input_im, x_coordinates, y_coordinates, cell_order):
    fig_paths = plt.figure()
    plt.show(block=False)
    plt.ion()
    ax = plt.gca() 
    img_artist = ax.imshow(input_im)
    input("Press Enter to Start the Movement of the Robot")

    robot_size = 5
    path_color = [255, 0, 0]  # Green color for the path

    for i, cell in enumerate(cell_order):
        print("Current cell: ", cell)
        x_start, x_end = x_coordinates[cell][0], x_coordinates[cell][-1]
        x_end_modulated = x_end - (x_end % robot_size)

        for j in range(x_start, x_end_modulated + robot_size, robot_size):
            y_ind = (j - x_start) % len(y_coordinates[cell])
            
            if type(y_coordinates[cell][0]) is list:
                y_start, y_end = y_coordinates[cell][y_ind][0][0], y_coordinates[cell][y_ind][0][1]
            else:
                y_start, y_end = y_coordinates[cell][y_ind][0], y_coordinates[cell][y_ind][1]
            
            y_end_modulated = y_end - (y_end % robot_size)

            if (j % (2 * robot_size)) == 0:  # move down
                for k in range(y_start, y_end_modulated, robot_size):
                    input_im[k:k+robot_size, j:j+robot_size] = path_color
            else:  # move up
                for k in range(y_end_modulated - robot_size, y_start - robot_size, -robot_size):
                    input_im[k:k+robot_size, j:j+robot_size] = path_color

            img_artist.set_data(input_im)
            plt.draw()
            plt.pause(0.00000000001)

        # # Draw cell boundary
        # if i < len(cell_order) - 1:
        #     draw_cell_boundary(input_im, x_end, 0, input_im.shape[0])
        #     img_artist.set_data(input_im)
        #     plt.draw()
        #     plt.pause(0.00000000001)

        print("Following cell is completed: ", cell)

    plt.title("Path with Cell Boundaries")
    plt.tight_layout()
    plt.show()


