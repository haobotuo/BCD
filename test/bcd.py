# Import necessary libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt
from typing import Tuple, List
import random
import itertools


Slice = List[Tuple[int, int]]


def calc_connectivity(slice: np.ndarray) -> Tuple[int, Slice]:
    """
    Calculates the connectivity of a slice and returns the connected area of ​the slice.

    Args:
        slice: rows. A slice of map.

    Returns:
        The connectivity number and connectivity parts.
        connectivity --> total number of connected parts

    Examples:
        >>> data = np.array([0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,1,1,0])
        >>> print(calc_connectivity(data))
        (4, [(4, 7), (8, 9), (12, 14), (15, 17)])
        (4,7) --> 4 is the point where connectivity is started
              --> 7 is the point where it finished
    """
    connectivity = 0
    last_data = 0
    open_part = False
    connective_parts = []
    for i, data in enumerate(slice):
        if last_data == 0 and data == 1:
            open_part = True
            start_point = i
        elif last_data == 1 and data == 0 and open_part:
            open_part = False
            connectivity += 1
            end_point = i
            connective_parts.append((start_point, end_point))

        last_data = data
    return connectivity, connective_parts


def get_adjacency_matrix(parts_left: Slice, parts_right: Slice) -> np.ndarray:
    """
    Get adjacency matrix of 2 neighborhood slices.

    Args:
        slice_left: left slice
        slice_right: right slice

    Returns:
        [L, R] Adjacency matrix.
    """
    adjacency_matrix = np.zeros([len(parts_left), len(parts_right)])
    for l, lparts in enumerate(parts_left):
        for r, rparts in enumerate(parts_right):
            if min(lparts[1], rparts[1]) - max(lparts[0], rparts[0]) > 0:
                adjacency_matrix[l, r] = 1

    return adjacency_matrix

def remove_duplicates(in_list):
    """
        This function removes duplicates in the input list, where
        input list is composed of unhashable elements
        Example:
            in_list = [[1,2],[1,2],[2,3]]
            output = remove_duplicates(in_list)
            output --> [[1,2].[2,3]]
    """
    out_list = []
    in_list.sort()
    out_list = list(in_list for in_list,_ in itertools.groupby(in_list))
    #print("input_list: ", in_list)
    #print("output list: ",out_list)
    return out_list

def bcd(erode_img: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Boustrophedon Cellular Decomposition

    Args:
        erode_img: [H, W], eroded map. The pixel value 0 represents obstacles and 1 for free space.

    Returns:
        [H, W], separated map. The pixel value 0 represents obstacles and others for its' cell number.
        current_cell and seperate_img is for display purposes --> which is used to show
        decomposed cells into a separate figure
        all_cell_numbers --> contains all cell index numbers
        cell_boundaries --> contains all cell boundary coordinates (only y coordinate)
        non_neighboor_cells --> contains cell index numbers of non_neighboor_cells, i.e.
        cells which are separated by the objects
    """
    
    assert len(erode_img.shape) == 2, 'Map should be single channel.'
    last_connectivity = 0
    last_connectivity_parts = []
    current_cell = 1
    current_cells = []
    separate_img = np.copy(erode_img)
    cell_boundaries = {}
    non_neighboor_cells = []

    for col in range(erode_img.shape[1]):
        current_slice = erode_img[:, col]
        connectivity, connective_parts = calc_connectivity(current_slice)
        
        if last_connectivity == 0:
            current_cells = []
            for i in range(connectivity):
                current_cells.append(current_cell)
                current_cell += 1
        elif connectivity == 0:
            current_cells = []
            continue
        elif connectivity == 1:
            if last_connectivity == 1:
                current_cells = [current_cells[0]]
            else:
                current_cells = [current_cell]
                current_cell += 1
        elif connectivity == 2:
            if last_connectivity == 1:
                current_cells = [current_cell, current_cell + 1]
                current_cell += 2
            elif last_connectivity == 2:
                current_cells = current_cells
            
            else:
                current_cells = [current_cell, current_cell + 1]
                current_cell += 2
        else:  # connectivity > 2
            if last_connectivity == connectivity:
                # If connectivity remains the same, keep the same cells
                current_cells = current_cells
            # elif last_connectivity == 3:
            #     # Keep the first two cells from the last iteration
            #     # and add a new cell for the additional connectivity
            #     current_cells = current_cells[:2] + [current_cell]
            #     current_cell += 1
            else:
            # For other cases, create new cells for each connected part
                current_cells = []
                for i in range(connectivity):
                    current_cells.append(current_cell)
                    current_cell += 1
        # Draw the partition information on the map.
        for cell, slice in zip(current_cells, connective_parts):
            #print("Debug")
            #print(current_cells, connective_parts)
            separate_img[slice[0]:slice[1], col] = cell
        
            # print('Slice {}: connectivity from {} to {}'.format(col, last_connectivity, connectivity))
        last_connectivity = connectivity
        last_connectivity_parts = connective_parts

        #print("Debug")
        #print(current_cells,connective_parts)
        
        #print("Current cell: ", current_cell)
        if len(current_cells) == 1: #no object in this cell
            ## cell_index = current_cell -1  # cell index starts from 1
            ## cell_boundaries.setdefault(cell_index,[])
            ## cell_boundaries[cell_index].append(connective_parts)
            cell_index = current_cells[0]
            cell_boundaries.setdefault(cell_index, [])
            cell_boundaries[cell_index].append((connective_parts[0][0], connective_parts[-1][1]))
        elif len(current_cells) > 1: ##cells separated by the object
            # cells separated by the objects are not neighbor to each other
            non_neighboor_cells.append(current_cells)
            # non_neighboor_cells will contain many duplicate values, but we 
            # will get rid of duplicates at the end

            # in this logic, all other cells must be neighboor to each other
            # if their cell number are adjacent to each other
            # like cell1 is neighboor to cell2

            for i in range(len(current_cells)):
                # current cells list doesn't need cell -1 operation 
                # it is already in the proper form
                cell_index = current_cells[i]
                # connective_parts and current_cells contain more than one
                # cell info which are separated by the object ,so we are iterating
                # with the for loop to reach all the cells
                cell_boundaries.setdefault(cell_index,[])
                ##cell_boundaries[cell_index].append(connective_parts[i])
                cell_boundaries[cell_index].append((connective_parts[i][0], connective_parts[i][1]))
     
    # Cell 1 is the left most cell and cell n is the right most cell
    # where n is the total cell number
    all_cell_numbers = cell_boundaries.keys()
    non_neighboor_cells = remove_duplicates(non_neighboor_cells)
    
    return separate_img, current_cell, list(all_cell_numbers), cell_boundaries, non_neighboor_cells

def display_separate_map(separate_map, cells):
    display_img = np.empty([*separate_map.shape, 3], dtype=np.uint8)
    random_colors = np.random.randint(0, 255, [cells, 3])
    for cell_id in range(1, cells):
        display_img[separate_map == cell_id, :] = random_colors[cell_id, :]
    fig_new = plt.figure()
    plt.imshow(display_img)

# def calculate_neighboor_matrix(cells,boundaries,nonneighboor_cells):
#     # Adjacent cells
#     """
#         This function creates adjacency matrix for the decomposed cells
#         Output: Matrix composed of zeros and ones
#                 output.shape --> total_cell_number x total_cell_number
#         Assumption: One cell is not neighboor with itself, so diagonal elements
#                     are always zero!        
#         Example: let's say we have 3 cells: cell1 and cell2 are only neighboors
#                 adjacency_matrix = [ [0 1 0] #cell1 is neighboor with cell2 
#                                      [1 0 0] #cell2 is neighboor with cell1
#                                      [0 0 0]  ]
#     """
#     """
#     adjacency_graph = {}
#     total_cell_number = len(cells)
#     for i in range(total_cell_number): #Iterate through all the cells
#         if (nonneighboor_cells[0][0] != cells[0]): #if first cell doesn't contain any objects
#             # previous cell is located at the left side of cells which are divided by the object(s)
#             current_cell = cells[i]
#             print("Current_cell: ", current_cell)
#             next_cell = cells[i]+1
#             for subneighboor in nonneighboor_cells:
#                 print("subneighboor: ", subneighboor)
#                 if subneighboor[0] == next_cell: #next cell is divided by an object
#                     print("next cell sikintili")
#                     adjacency_graph[current_cell] = subneighboor
#                     for k in range(len(subneighboor)):
#                         #if we already assigned something to subneighboord k
#                         if adjacency_graph.get(subneighboor[k]):
#                             print("debug")
#                             print(subneighboor[k]) 
#                             #adjacency_graph[subneighboor[k]].append(current_cell)
#                         #else: #we are assigning for the first time
#                             #adjacency_graph[subneighboor[k]] = current_cell
#                     break #we already found so break out subneighboor loop
#                 else:  #current cell and next cell doesn't have object
#                     adjacency_graph[current_cell] = next_cell
#                     adjacency_graph[next_cell] = current_cell #bidirectional way
#         #elif (nonneighboor_cells[0][0] == cells[0]):
#     """
# def calculate_neighbour_matrix(cells, boundaries, nonneighbour_cells):
#     total_cell_number = len(cells)
#     adjacency_matrix = [[0] * total_cell_number for _ in range(total_cell_number)]

#     for i in range(total_cell_number):
#         for j in range(total_cell_number):
#             if i != j:
#                 cell_i = cells[i]
#                 cell_j = cells[j]

#                 if not any(set(pair) == {cell_i, cell_j} for pair in nonneighbour_cells):
#                     if cell_i in boundaries and cell_j in boundaries:
#                         if are_cells_adjacent(boundaries[cell_i], boundaries[cell_j]):
#                             adjacency_matrix[i][j] = 1
#                             adjacency_matrix[j][i] = 1

#     return adjacency_matrix


# def are_cells_adjacent(boundary1, boundary2):
#     for b1 in boundary1:
#         for b2 in boundary2:
#             if len(b1) < 2 or len(b2) < 2:
#                 print(f"Invalid boundary pair: {b1}, {b2}")
#                 continue
#             if min(b1[1], b2[1]) - max(b1[0], b2[0]) > 0:
#                 return True
#     return False
def calculate_neighbour_matrix(cells, boundaries, nonneighbour_cells):
    total_cell_number = len(cells)
    adjacency_matrix = [[0] * total_cell_number for _ in range(total_cell_number)]

    # Create a mapping from cell number to its index
    cell_to_index = {cell: idx for idx, cell in enumerate(cells)}

    for i in range(total_cell_number):
        current_cell = cells[i]
        
        if current_cell not in cell_to_index:
            continue
        
        current_index = cell_to_index[current_cell]

        # Check all other cells to determine adjacency
        for j in range(total_cell_number):
            if i == j:
                continue

            other_cell = cells[j]
            
            if other_cell not in cell_to_index:
                continue

            other_index = cell_to_index[other_cell]

            # Skip if cells are explicitly marked as non-neighbours
            if [current_cell, other_cell] in nonneighbour_cells or [other_cell, current_cell] in nonneighbour_cells:
                continue

            # Check if the boundaries of the two cells overlap
            if are_cells_adjacent(boundaries[current_cell], boundaries[other_cell]):
                adjacency_matrix[current_index][other_index] = 1
                adjacency_matrix[other_index][current_index] = 1

    return adjacency_matrix

# def are_cells_adjacent(boundary1, boundary2):
#     for b1 in boundary1:
#         for b2 in boundary2:
#             if isinstance(b1, tuple) and isinstance(b2, tuple) and len(b1) == 2 and len(b2) == 2:
#                 if min(b1[1], b2[1]) - max(b1[0], b2[0]) > 0:
#                     return True
#     return False
def are_cells_adjacent(boundary1, boundary2):
    for b1 in boundary1:
        for b2 in boundary2:
            # 确保每个边界都是有效的元组，并且长度为2
            if isinstance(b1, tuple) and isinstance(b2, tuple) and len(b1) == 2 and len(b2) == 2:
                # 检查边界是否有重叠
                if max(b1[0], b2[0]) < min(b1[1], b2[1]):
                    return True
            else:
                print(f"Invalid boundary pair: {b1}, {b2}")
    return False

#print("Debug")
#print("Total cell number: ", total_cell_number)
#print("Boundaries: ", boundaries)
#print("Non-neighboor cells: ", nonneighboor_cells)