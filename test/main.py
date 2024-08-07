# Fix OpenCv2 configuration error with ROS
#import sys
#sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

import bcd  #The Boustrophedon Cellular decomposition
import dfs  #The Depth-first Search Algorithm
import os
import move_boustrophedon # Uses output of bcd cells in order to move the robot

import timeit


if __name__ == '__main__':
    os.chdir('/Users/haobo/UCL/FYP/bcd_py/results')
    # Read the original data
    original_map = bcd.cv2.imread("da.png")
    #original_map = cv2.imread("../data/example2.png")[:,0:350]
    
    # Show the original data
    fig1 = move_boustrophedon.plt.figure()
    move_boustrophedon.plt.imshow(original_map)

    move_boustrophedon.plt.title("Original Map Image")
    
    # We need binary image
    # 1's represents free space while 0's represents objects/walls
    if len(original_map.shape) > 2:
        print("Map image is converted to binary")
        single_channel_map = original_map[:, :, 0]
        _,binary_map = bcd.cv2.threshold(single_channel_map,127,1,bcd.cv2.THRESH_BINARY)

    # Call The Boustrophedon Cellular Decomposition function
    bcd_out_im, bcd_out_cells, cell_numbers, cell_boundaries, non_neighboor_cell_numbers = bcd.bcd(binary_map)
    # Show the decomposed cells on top of original map
    bcd.display_separate_map(bcd_out_im, bcd_out_cells)
    move_boustrophedon.plt.show(block=False)
    #non_nei= [[2,3,4],[4,5,6]]
    #print(cell_boundaries)
    print(non_neighboor_cell_numbers)
    def matrix_to_adj_list(matrix):
        adj_list = {}
        for i, row in enumerate(matrix): adj_list[i + 1] = [j + 1 for j, val in enumerate(row) if val == 1]
        return adj_list

    graph4 = matrix_to_adj_list(bcd.calculate_neighbour_matrix(cell_numbers, cell_boundaries, non_neighboor_cell_numbers))


    ######### DFS
    cleaned_DFS = [] #Keeps cleaned cell numbers in order
    iter_number = 1000
    #starting_cell_number = move_boustrophedon.randint(1,len(cell_numbers))
    starting_cell_number = 1
    print("Starting cell number: ", starting_cell_number)
    exec_time_dfs = timeit.timeit('dfs.dfs(cleaned_DFS, graph4, starting_cell_number)', \
        'from __main__ import dfs, cleaned_DFS, graph4, starting_cell_number',number = iter_number)
    exec_time_dfs = exec_time_dfs/iter_number
    print("DFS Cleaned cells in order", cleaned_DFS)
    print("Execution time of dfs in seconds: ", exec_time_dfs)

    def mean(input_list):
        output_mean = sum(input_list)/len(input_list)
        return output_mean

    def mean_double_list(input_double_list):
        length = len(input_double_list)
        total = 0 
        for i in range(length):
            total += mean(input_double_list[i])
        
        output_mean = total/length
        return output_mean

    def mean_d_double_list(input_double_list):
        length = len(input_double_list)
        total = 0 
        for i in range(length):
            total += mean(input_double_list[i][0])
        
        output_mean = total/length
        return output_mean
    


    x_length = original_map.shape[1]
    y_length = original_map.shape[0]

    x_coordinates = move_boustrophedon.calculate_x_coordinates(x_length, y_length, \
                    cell_numbers,cell_boundaries,non_neighboor_cell_numbers)
    y_coordinates = cell_boundaries

    # mean_x_coordinates = {}
    # mean_y_coordinates = {}
    # for i in range(len(x_coordinates)):
    #     cell_idx = i+1 #i starts from zero, but cell numbers start from 1
    #     mean_x_coordinates[cell_idx] = mean(x_coordinates[cell_idx])
    #     if type(y_coordinates[cell_idx][0]) is list:
    #         mean_y_coordinates[cell_idx] = mean_d_double_list(y_coordinates[cell_idx])
    #     else:
    #         mean_y_coordinates[cell_idx] = mean_double_list(y_coordinates[cell_idx])
    
    
    ########## Path Tracking
    ##DFS
    iter_number = 1
    dfs_path = cleaned_DFS

    path_time_dfs = timeit.timeit('move_boustrophedon.track_paths(original_map,dfs_path,cell_boundaries,non_neighboor_cell_numbers)', \
                                  'from __main__ import move_boustrophedon, \
                                  dfs_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    path_time_dfs = path_time_dfs/iter_number
    print("Total path tracking time of dfs in seconds: ", path_time_dfs)
  
    move_boustrophedon.plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    move_boustrophedon.plt.close("all")
