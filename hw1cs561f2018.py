import pandas as pd
import numpy as np

#global_max
global_maximum_activity = 0

#Form a NxN grid and calculate frequency of each cell
def construct_frequency(grid_size, num_of_scooters, route_map) :
    grid_frequency = {}

    for i in range(grid_size) :
        for j in range(grid_size) :
            grid_frequency[str(i)+','+str(j)] = 0

    for i in range(num_of_scooters*12) :
        grid_frequency[route_map[i]] += 1

    return grid_frequency

#Read input from the file
def readInput() :
    inputFP = open('input.txt','r')

    grid_size = 0
    num_of_officers = 0
    num_of_scooters = 0
    route_map = []

    line_num = 0
    for line in inputFP :
        if line_num == 0 :
            grid_size = int(line.rstrip('\r\n'))
        elif line_num == 1 :
            num_of_officers = int(line.rstrip('\r\n'))
        elif line_num == 2 :
            num_of_scooters = int(line.rstrip('\r\n'))
        else :
            route_map.append((line.rstrip('\r\n')))
        line_num+=1

    inputFP.close()

    return grid_size, num_of_officers, num_of_scooters, route_map

#form a DataFrame from dictionary
def form_data_frame(grid_frequency) :
    return pd.DataFrame({'cell':grid_frequency.keys(),
                         'frequency':grid_frequency.values()})

#sort the DataFrame based on frequency in a decreasing order
def sort_dataframe(grid_dataframe) :
    return grid_dataframe.sort_values('frequency', ascending=False)#, inplace=True)

#check for collision of officer location, similar to N Queen
def check_collision(valid_officer_list, new_location) :
    if len(valid_officer_list) == 0 :
        return False
    #print "collision test :", valid_officer_list, new_location
    new_x, new_y = new_location.split(',')
    for item in valid_officer_list :
        item_x, item_y = map(int, item.split(','))
        if int(new_x) == item_x or int(new_y) == item_y or \
           abs(int(new_x)-item_x) == abs(int(new_y) - item_y) :
            return True
    return False

#Function to calculate best path
def find_max_activity(grid_dataframe, grid_size, num_of_officers) :
    stack = []
    local_max_activity = 0
    i = 0
    rows = grid_dataframe.shape[0]
    global global_maximum_activity
    while i<grid_size*grid_size or len(stack)!=0 :
        if num_of_officers == 0 or i == grid_size*grid_size :
            if num_of_officers==0 and global_maximum_activity < local_max_activity :
		#print stack, local_max_activity
	        global_maximum_activity = local_max_activity

            cell = stack.pop() 
	    
	    index = 0
            #index = int(grid_dataframe[grid_dataframe['cell']==cell].index.values[0]) 
            for i in range(rows) :
	        if grid_dataframe[i,0]==cell :
		    index = i
		    break
	    #print np.where((grid_dataframe[0]==cell))
            num_of_officers = num_of_officers+1
            local_max_activity = local_max_activity - grid_dataframe[index,1]
            i = index+1
            continue

        if (local_max_activity+(num_of_officers*grid_dataframe[i,1])) <= global_maximum_activity :
            #print local_max_activity+(num_of_officers*grid_dataframe.iloc[i][1]), global_maximum_activity
            i = i+1
            continue

        if (check_collision(stack, grid_dataframe[i,0]) == False) :
            stack.append(grid_dataframe[i,0])
            num_of_officers = num_of_officers-1
            local_max_activity = local_max_activity + grid_dataframe[i,1]

        i = i+1

#Main function starts
if __name__ == "__main__" :
    grid_size, num_of_officers, num_of_scooters, route_map = readInput()
    grid_frequency = construct_frequency(grid_size, num_of_scooters, route_map)

    grid_dataframe = form_data_frame(grid_frequency) 
    grid_frequency.clear()
    grid_dataframe = sort_dataframe(grid_dataframe)

    grid_dataframe['ind'] = [i for i in range(grid_size*grid_size)]
    grid_dataframe = grid_dataframe.set_index('ind')
    
    #print grid_dataframe[['frequency']].values
    grid_dataframe = grid_dataframe.values
    #print grid_dataframe
    #print grid_dataframe.shape
    find_max_activity(grid_dataframe, grid_size, num_of_officers)

    writeFP = open('output.txt', 'w')
    writeFP.write(str(global_maximum_activity)+"\n")
    writeFP.close()
