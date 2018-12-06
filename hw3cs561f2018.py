import numpy as np

actions_list = ['UP', 'DOWN', 'RIGHT', 'LEFT']

def rotateLeft(action):
    if action == 'UP':
        return 'LEFT'
    elif action == 'DOWN':
        return 'RIGHT'
    elif action == 'RIGHT':
        return 'UP'
    else:
        return 'DOWN'

def rotateRight(action):
    if action == 'UP':
        return 'RIGHT'
    elif action == 'DOWN':
        return 'LEFT'
    elif action == 'RIGHT':
        return 'DOWN'
    else:
        return 'UP'

def get_new_location_reward(policy_grid, i, j, action):
    if action == 'UP':
        if i==0:
            return policy_grid[i][j][1]
        else:
            return policy_grid[i-1][j][1]
    elif action == 'DOWN':
        if i==grid_size-1:
            return policy_grid[i][j][1]
        else:
            return policy_grid[i+1][j][1]
    elif action == 'LEFT':
        if j==0:
            return policy_grid[i][j][1]
        else:
            return policy_grid[i][j-1][1]
    else:
        if j==grid_size-1:
            return policy_grid[i][j][1]
        else:
            return policy_grid[i][j+1][1]


def get_new_utility(policy_grid, i, j, action_index):
    util_70 = get_new_location_reward(policy_grid, i, j, actions_list[action_index])
    util_10_270 = get_new_location_reward(policy_grid, i, j, rotateLeft(actions_list[action_index]))
    util_10_90 = get_new_location_reward(policy_grid, i, j, rotateRight(actions_list[action_index]))
    util_10_180 = get_new_location_reward(policy_grid, i, j, rotateLeft(rotateLeft(actions_list[action_index])))

    return (0.7*util_70) + 0.1*(util_10_180+util_10_90+util_10_270)

def value_iteration(grid_size, states_reward_grid, policy_grid, policy_grid_dash, cars_finish_location_each):
    delta = 1.0
    gamma = 0.9
    limit = (0.1 * 0.1)/0.9
    while (delta>=limit):
        delta = 0
        policy_grid = [row[:] for row in policy_grid_dash]
        
        for i in range(grid_size):
            for j in range(grid_size):
                if i==cars_finish_location_each[0] and j==cars_finish_location_each[1]:
                    continue
                max_utility = []
                max_utility_action = 'UP'
                for action_index in range(len(actions_list)):
                    utility = get_new_utility(policy_grid, i, j, action_index)
                    
                    if action_index == 0:
                        max_utility.append(utility)
                        max_utility_action = actions_list[action_index]
                    elif utility > max_utility[0]:
                        max_utility[0] = utility
                        max_utility_action = actions_list[action_index]
                        
                policy_grid_dash[i][j] = [max_utility_action, states_reward_grid[i][j] + (gamma * max_utility[0])]
                
                if abs(policy_grid_dash[i][j][1]-policy_grid[i][j][1]) > delta:
                    delta = abs(policy_grid_dash[i][j][1]-policy_grid[i][j][1])

    return policy_grid

def get_policy(states_reward_grid, grid_size, obstacle_list, cars_start_location_each, cars_finish_location_each):
    policy_grid = []
    policy_grid_dash = []

    for i in range(grid_size):
        policy_grid_row = []
        for j in range(grid_size):
            if i==cars_finish_location_each[0] and j==cars_finish_location_each[1]:
                policy_grid_row.append(['', np.float64(99.0)])
            elif [i,j] in obstacle_list:
                policy_grid_row.append(['', -101.0])
            else:
                policy_grid_row.append(['', -1.0])
        policy_grid.append(policy_grid_row)
        policy_grid_dash.append(policy_grid_row)

    states_reward_grid[cars_finish_location_each[0]][cars_finish_location_each[1]] = 99

    policy_grid = value_iteration(grid_size, states_reward_grid, policy_grid, policy_grid_dash, cars_finish_location_each)
    states_reward_grid[cars_finish_location_each[0]][cars_finish_location_each[1]] = -1
    return policy_grid


def make_state_grid(grid_size, obstacle_list):
    states_reward_grid = []

    for i in range(grid_size):
        states_grid_row = []
        for j in range(grid_size):
            states_grid_row.append(-1)
        states_reward_grid.append(states_grid_row)

    for i in range(len(obstacle_list)):
        states_reward_grid[obstacle_list[i][0]][obstacle_list[i][1]] = -101

    return states_reward_grid


def make_move(grid_size, move, current_position):
    if move == 'UP':
        if current_position[0]==0:
            return current_position
        else:
            return [current_position[0]-1, current_position[1]]
    elif move == 'DOWN':
        if current_position[0]==grid_size-1:
            return current_position
        else:
            return [current_position[0]+1, current_position[1]]
    elif move == 'LEFT':
        if current_position[1]==0:
            return current_position
        else:
            return [current_position[0], current_position[1]-1]
    else:
        if current_position[1]==grid_size-1:
            return current_position
        else:
            return [current_position[0], current_position[1]+1]


def calculate_mean(simulated_rewards_per_car):
    sum = 0
    for reward_each in simulated_rewards_per_car:
        sum = sum + reward_each

    return int(np.floor(sum/10))


def run_simulation(grid_size, policies, cars_start_location_list, cars_finish_location_list):
    final_simulation_results = []
    for i in range(len(cars_finish_location_list)):
        states_reward_grid = make_state_grid(grid_size, obstacle_list)
        states_reward_grid[cars_finish_location_list[i][0]][cars_finish_location_list[i][1]] = 99
        
        simulated_rewards_per_car = []
        for j in range(10):
            current_position = cars_start_location_list[i]
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k=0
            simulation_rewards = 0
            source_dest_same=False
            
            while current_position[0] != cars_finish_location_list[i][0] or \
                  current_position[1] != cars_finish_location_list[i][1]:
                source_dest_same=True
                move = policies[i][current_position[0]][current_position[1]][0]
               
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = rotateLeft(rotateLeft(move))
                        else:
                            move = rotateRight(move)
                    else:
                        move = rotateLeft(move)

                current_position = make_move(grid_size, move, current_position)
                simulation_rewards += states_reward_grid[current_position[0]][current_position[1]]

                k = k+1
            if source_dest_same == False:
                simulation_rewards=100
            simulated_rewards_per_car.append(simulation_rewards)
            
        final_simulation_results.append(calculate_mean(simulated_rewards_per_car))
        
    return final_simulation_results

if __name__ == '__main__':
    inputFP = open('input.txt', 'r')
    grid_size = int(inputFP.readline().rstrip())
    num_of_cars = int(inputFP.readline().rstrip())
    num_of_obstacles = int(inputFP.readline().rstrip())

    obstacle_list=[]
    cars_start_location_list = []
    cars_finish_location_list = []

    for i in range(num_of_obstacles):
        coordinates = map(int, inputFP.readline().rstrip().split(',')[::-1])
        obstacle_list.append(coordinates)

    for i in range(num_of_cars):
        coordinates = map(int, inputFP.readline().rstrip().split(',')[::-1])
        cars_start_location_list.append(coordinates)

    for i in range(num_of_cars):
        coordinates = map(int, inputFP.readline().rstrip().split(',')[::-1])
        cars_finish_location_list.append(coordinates)

    inputFP.close()

    policies = []

    states_reward_grid = make_state_grid(grid_size, obstacle_list)
    for i in range(num_of_cars):
        policy = get_policy(states_reward_grid, grid_size, obstacle_list, cars_start_location_list[i], cars_finish_location_list[i])
        policies.append(policy)

    mean_reward_list = run_simulation(grid_size, policies, cars_start_location_list, cars_finish_location_list)
    
    outputFP = open('output.txt', 'w')
    for mean_reward_each in mean_reward_list:
        outputFP.write(str(mean_reward_each)+'\n')
    outputFP.close()
