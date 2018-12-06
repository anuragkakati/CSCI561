counter = 0
global_max_efficiency_SPLA = 0
global_max_efficiency_LAHSA = 0
selected_by_SPLA = []
selected_by_LAHSA = []
next_applicant_SPLA = ''
global_LAHSA_dict = {}
global_SPLA_dict = {}

import time


# import logging

def remaining_applications(SPLA_chosen_list, LAHSA_chosen_list, total_applicant_list):
    for spla in SPLA_chosen_list:
        for total in total_applicant_list:
            if spla == total[:5]:
                total_applicant_list.remove(total)

    for lahsa in LAHSA_chosen_list:
        for total in total_applicant_list:
            if lahsa == total[:5]:
                total_applicant_list.remove(total)


def find_SPLA_eligible(total_applicant_list):
    eligible_list = []
    for applicant in total_applicant_list:
        medical = applicant[10]
        car = applicant[11]
        license = applicant[12]
        if medical == 'N' and car == 'Y' and license == 'Y':
            eligible_list.append(applicant)

    return eligible_list


def find_LAHSA_eligible(total_applicant_list):
    eligible_list = []
    for applicant in total_applicant_list:
        woman = applicant[5]
        age = int(applicant[6:9])
        pet = applicant[9]
        if woman == 'F' and age > 17 and pet == 'N':
            eligible_list.append(applicant)

    return eligible_list


def find_common_list(SPLA_eligible, LAHSA_eligible):
    common_list = []
    for spla in SPLA_eligible:
        if spla in LAHSA_eligible:
            common_list.append(spla)
    return common_list


def update_capacity(SPLA_chosen_list, LAHSA_chosen_list, total_applicant_list, capacity_SPLA, capacity_LAHSA):
    #print "SPLA chosen List:", SPLA_chosen_list
    #print "LAHSA chosen List:", LAHSA_chosen_list
    for spla_applicant in SPLA_chosen_list:
        for total_applicant in total_applicant_list:
            if spla_applicant == total_applicant[:5]:
                decrease_capacity(capacity_SPLA, total_applicant[13:])
    for lahsa_applicant in LAHSA_chosen_list:
        for total_applicant in total_applicant_list:
            if lahsa_applicant == total_applicant[:5]:
                decrease_capacity(capacity_LAHSA, total_applicant[13:])


def get_spots(applicant):
    spots = 0
    for i in range(13, len(applicant)):
        spots = spots + int(applicant[i])
    return spots


def get_total_SPLA_values(SPLA_eligible_list, capacity_SPLA):
    #print "get_total_SPLA_values: SPLA_eligible_list:", SPLA_eligible_list
    #print "capacity_SPLA:", capacity_SPLA
    temp_capacity_SPLA = capacity_SPLA[:]
    sum = 0
    for spla_applicant in SPLA_eligible_list:
        if is_eligible(spla_applicant, temp_capacity_SPLA):
            sum += get_spots(spla_applicant)
            decrease_capacity(temp_capacity_SPLA, spla_applicant[13:])

    return sum


def greedy_select_SPLA(common_list):
    max_spots_index = 0
    max_spots = 0
    for i in range(len(common_list)):
        req_spots = get_spots(common_list[i])
        if req_spots > max_spots:
            max_spots = req_spots
            max_spots_index = i

    return max_spots_index


def update_list(spla_applicant, SPLA_eligible_list, LAHSA_eligible_list):
    for item in SPLA_eligible_list:
        if spla_applicant == item:
            SPLA_eligible_list.remove(item)
            break
    for item in LAHSA_eligible_list:
        if spla_applicant == item:
            LAHSA_eligible_list.remove(item)
            break
    # print "updated lists :"
    # print "SPLA:", SPLA_eligible_list
    # print "LAHSA:", LAHSA_eligible_list


def is_eligible(applicant, capacity_list):
    global counter
    counter += 1
    # print "is_eligible: applicant, capacity_list :", applicant, capacity_list
    applicant_days = applicant[13:]
    for i in range(7):
        if int(applicant_days[i]) == 1 and capacity_list[i] == 0:
            return False
    # print "is_eligible: returning True"
    return True


def get_max_SPLA_id(SPLA_eligible_list, capacity_SPLA):
    max_SPLA_id = ''
    max_sum = 0
    for spla_applicant in SPLA_eligible_list:
        if is_eligible(spla_applicant, capacity_SPLA):
            if get_spots(spla_applicant) > max_sum:
                max_sum = get_spots(spla_applicant)
                max_SPLA_id = spla_applicant[:5]
    return max_SPLA_id


def get_slots_from_applicant_request(spla_applicant):
    sum = 0
    days = spla_applicant[13:]
    for i in range(7):
        sum += int(days[i])

    return sum


def decrease_capacity(capacity_list, applicant):
    for i in range(7):
        capacity_list[i] -= int(applicant[i])


def increase_capacity(capacity_list, applicant):
    for i in range(7):
        capacity_list[i] += int(applicant[i])


def calculate_efficiency_SPLA(SPLA_eligible_list, capacity_list):
    sum = 0
    for spla_applicant in selected_by_SPLA:
        sum += get_spots(spla_applicant)
    for spla_applicant in SPLA_eligible_list:
        if is_eligible(spla_applicant, capacity_list):
            sum += get_spots(spla_applicant)
    # print "calculate_efficiency_SPLA: sum:", sum
    return sum


def calculate_efficiency_LAHSA(LAHSA_eligible_list, capacity_list):
    sum = 0
    for lahsa_applicant in selected_by_LAHSA:
        sum += get_spots(lahsa_applicant)
    for lahsa_applicant in LAHSA_eligible_list:
        if is_eligible(lahsa_applicant, capacity_list):
            sum += get_spots(lahsa_applicant)
    # print "calculate_efficiency_LAHSA: sum:", sum
    return sum


def get_maximized_LAHSA(spla_spots):
    max = 0
    return_list = []
    for max_max_list in global_LAHSA_dict.values():
        if max_max_list[1] > max:
            max = max_max_list[1]
            return_list = max_max_list
    return_list[0] += spla_spots
    return return_list


def get_maximized_SPLA():
    max = 0
    next_SPLA_id = '99999'
    for spla_id, max_max_list in global_SPLA_dict.iteritems():
        if max_max_list[0] > max or (max_max_list[0] == max and int(spla_id) < int(next_SPLA_id)):
            max = max_max_list[0]
            next_SPLA_id = spla_id

    return next_SPLA_id


# exactly a mirror of recurse_SPLA
def recurse_LAHSA(lahsa_applicant, SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA, current_sum):
    # print "LAHSA selects", lahsa_applicant
    # print "LAHSA_eligible_list", LAHSA_eligible_list
    update_list(lahsa_applicant, SPLA_eligible_list, LAHSA_eligible_list)
    global selected_by_SPLA, global_max_efficiency_SPLA, next_applicant_SPLA, global_max_efficiency_LAHSA
    for spla_applicant in SPLA_eligible_list:
        if is_eligible(spla_applicant, capacity_SPLA):
            current_sum += get_slots_from_applicant_request(spla_applicant)
            selected_by_SPLA.append(spla_applicant)
            # print "Selected Applicant : ", spla_applicant
            decrease_capacity(capacity_SPLA, spla_applicant[13:])
            current_sum = recurse_SPLA(spla_applicant, SPLA_eligible_list[:], LAHSA_eligible_list[:], capacity_SPLA,
                                       capacity_LAHSA, current_sum)
            # logging.basicConfig()
            # logging.debug()
            # print "recurse_LAHSA: SPLA_eligible_list:", SPLA_eligible_list, "LAHSA_eligible_list", LAHSA_eligible_list

    if len(SPLA_eligible_list) == 0 or len(LAHSA_eligible_list) == 0:
        local_max_SPLA = calculate_efficiency_SPLA(SPLA_eligible_list, capacity_SPLA)
        local_max_LAHSA = calculate_efficiency_LAHSA(LAHSA_eligible_list, capacity_LAHSA)
        # print "calculate_efficiencyL: eligible:", SPLA_eligible_list, "selected", selected_by_SPLA
        # print "local_max_SPLA and global_max :", local_max_SPLA, global_max_efficiency_SPLA
        # if local_max_LAHSA > global_max_efficiency_LAHSA:

        if local_max_SPLA > global_max_efficiency_SPLA:
            # print "updating global_max from", global_max_efficiency_SPLA, "to", local_max_SPLA
            # print "next_applicant_SPLA:", selected_by_SPLA
            global_max_efficiency_SPLA = local_max_SPLA
            global_max_efficiency_LAHSA = local_max_LAHSA
            next_applicant_SPLA = selected_by_SPLA[0][:5]
    applicant = selected_by_LAHSA.pop()
    # print "recurse_LAHSA: popped applicant:", applicant
    # print "LAHSA_eligible_list:", LAHSA_eligible_list
    # print "SPLA_eligible_list", SPLA_eligible_list
    increase_capacity(capacity_LAHSA, applicant[13:])
    # del selected_by_LAHSA[-1]
    # selected_by_LAHSA.remove(-1)
    return current_sum


def recurse_SPLA(spla_applicant, SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA, current_sum):
    # print "SPLA selects", spla_applicant
    # print "SPLA_eligible_list:", SPLA_eligible_list
    update_list(spla_applicant, SPLA_eligible_list, LAHSA_eligible_list)
    global selected_by_LAHSA, global_max_efficiency_SPLA, next_applicant_SPLA, global_max_efficiency_LAHSA
    # recurse for each remaining LAHSA
    for lahsa_applicant in LAHSA_eligible_list:
        if is_eligible(lahsa_applicant, capacity_LAHSA):
            selected_by_LAHSA.append(lahsa_applicant)
            # current_sum += get_slots_from_applicant_request(lahsa_applicant)
            decrease_capacity(capacity_LAHSA, lahsa_applicant[13:])
            # ignore current_sum, it is for older code
            # important to send SPLA_eligible_list[:] by value and not reference
            current_sum = recurse_LAHSA(lahsa_applicant, SPLA_eligible_list[:], LAHSA_eligible_list[:], capacity_SPLA,
                                        capacity_LAHSA, current_sum)
            # print "recurse_SPLA: SPLA_eligible_list:", SPLA_eligible_list, "LAHSA_eligible_list", LAHSA_eligible_list

    # Recursion for LAHSA ended, no more to select for LAHSA so need to calculate efficiencies for both
    if len(SPLA_eligible_list) == 0 or len(LAHSA_eligible_list) == 0:
        local_max_SPLA = calculate_efficiency_SPLA(SPLA_eligible_list, capacity_SPLA)
        local_max_LAHSA = calculate_efficiency_LAHSA(LAHSA_eligible_list, capacity_LAHSA)
        # print "calculate_efficiencyS: eligible:", SPLA_eligible_list, "selected", selected_by_SPLA
        # print "local_max_SPLA and global_max :", local_max_SPLA, global_max_efficiency_SPLA
        # if local_max_LAHSA > global_max_efficiency_LAHSA:

        # print "local_max_LAHSA and global_max :", local_max_LAHSA, global_max_efficiency_LAHSA

        # need to maximize just SPLA so check only if local maximum of SPLA is > global maximum
        # but update both global maxima since we need both later for maximax
        if local_max_SPLA > global_max_efficiency_SPLA:
            # print "updating global_max from", global_max_efficiency_SPLA, "to", local_max_SPLA
            # print "next_applicant_SPLA:", selected_by_SPLA
            global_max_efficiency_SPLA = local_max_SPLA
            global_max_efficiency_LAHSA = local_max_LAHSA
            next_applicant_SPLA = selected_by_SPLA[0][:5]

    # returning from this function, hence undo selection of selected applicant and return
    applicant = selected_by_SPLA.pop()
    # print "recurse_SPLA: popped applicant:", applicant
    # print "LAHSA_eligible_list:", LAHSA_eligible_list
    # print "SPLA_eligible_list", SPLA_eligible_list
    increase_capacity(capacity_SPLA, applicant[13:])
    # del selected_by_SPLA[-1]
    # selected_by_SPLA.remove(-1)

    # ignore current_sum
    return current_sum


#
# def exhaustive_select_SPLA(total_applicant_list, SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA) :
#     #print "exhaustive_select_SPLA"
#     max_efficiency = 0
#     applicant_id = ''
#     global selected_by_SPLA
#     for spla_applicant in SPLA_eligible_list :
#         temp_max = 0
#         if is_eligible(spla_applicant, capacity_SPLA) == True :
#             #print "exhaustive_select_SPLA: eligible", spla_applicant
#             temp_max += get_slots_from_applicant_request(spla_applicant)
#             selected_by_SPLA.append(spla_applicant)
#             decrease_capacity(capacity_SPLA, spla_applicant[13:])
#             temp_max = recurse_SPLA(spla_applicant, SPLA_eligible_list[:], LAHSA_eligible_list[:], capacity_SPLA, capacity_LAHSA, temp_max)
#             print "exhaustive_select_SPLA: temp_max:", temp_max
#             if temp_max > max_efficiency :
#                 max_efficiency = temp_max
#                 applicant_id = spla_applicant[:5]
#         print "if SPLA first selects", spla_applicant, "max_efficiency:", max_efficiency
#         print "selected_by_SPLA:", selected_by_SPLA
#         if len(selected_by_SPLA)>0 :
#             applicant = selected_by_SPLA.pop()
#             #del selected_by_SPLA[-1]
#             increase_capacity(capacity_SPLA, applicant[13:])
#         #selected_by_SPLA.remove(-1)
#     return applicant_id

def lets_play_the_game(SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA):
    for spla_applicant in SPLA_eligible_list:
        if is_eligible(spla_applicant, capacity_SPLA):
            selected_by_SPLA.append(spla_applicant)
            decrease_capacity(capacity_SPLA, spla_applicant[13:])
            # recursion for each SPLA applicant
            recurse_SPLA(spla_applicant, SPLA_eligible_list[:], LAHSA_eligible_list[:], capacity_SPLA, capacity_LAHSA,
                         0)
            # selected_by_SPLA.remove(spla_applicant)


def exhaustive_select_SPLA(SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA, common_list):
    global global_max_efficiency_LAHSA, global_max_efficiency_SPLA
    for spla_applicant in SPLA_eligible_list:  # Fix each applicant first for SPLA
        selected_by_SPLA_local = []
        if is_eligible(spla_applicant, capacity_SPLA):  # Prerequisite for SPLA
            selected_by_SPLA_local.append(spla_applicant)
            decrease_capacity(capacity_SPLA, spla_applicant[13:])
            # update_list(spla_applicant, SPLA_eligible_list, LAHSA_eligible_list)
            # print "LAHSA_eligible_list:", LAHSA_eligible_list
            any_lahsa_eligible = False
            for lahsa_applicant in LAHSA_eligible_list:  # Fix each applicant first for LAHSA
                selected_by_LAHSA_local = []
                # print "exhaustive_select_SPLA: Pairs to compare are: SPLA", spla_applicant, "LAHSA", lahsa_applicant
                if lahsa_applicant != spla_applicant and is_eligible(lahsa_applicant, capacity_LAHSA):
                    if is_eligible(lahsa_applicant, capacity_LAHSA):
                        any_lahsa_eligible = True
                    selected_by_LAHSA_local.append(lahsa_applicant)  # Prerequisite for LAHSA
                    decrease_capacity(capacity_LAHSA, lahsa_applicant[13:])
                    # update_list(lahsa_applicant, SPLA_eligible_list, LAHSA_eligible_list)
                    # print "LAHSA ELi : " , LAHSA_eligible_list
                    # print "exhaustive_select_SPLA: Pairs to compare are: SPLA", spla_applicant, "LAHSA", lahsa_applicant

                    # create copies to send to avoid inconsistencies after update_list
                    copy_SPLA_eligible_list = SPLA_eligible_list[:]
                    copy_LAHSA_eligible_list = LAHSA_eligible_list[:]
                    update_list(spla_applicant, copy_SPLA_eligible_list, copy_LAHSA_eligible_list)
                    update_list(lahsa_applicant, copy_SPLA_eligible_list, copy_LAHSA_eligible_list)
                    # print "Updated lists: SPLA:", copy_SPLA_eligible_list, "LAHSA:", copy_LAHSA_eligible_list
                    # the game begins with 1 applicant fixe for each SPLA and LAHSA
                    #print "play start"
                    lets_play_the_game(copy_SPLA_eligible_list[:], copy_LAHSA_eligible_list[:], capacity_SPLA,
                                       capacity_LAHSA)
                    #print "play ends"
                    # global_max_efficiency_LAHSA += get_spots(lahsa_applicant)
                    if spla_applicant[:5] in global_LAHSA_dict:
                        #print global_max_efficiency_LAHSA + get_spots(lahsa_applicant), 'check', \
                        global_LAHSA_dict[spla_applicant[:5]][1]
                        if global_max_efficiency_LAHSA + get_spots(lahsa_applicant) > \
                                global_LAHSA_dict[spla_applicant[:5]][1]:
                            global_LAHSA_dict[spla_applicant[:5]] = [global_max_efficiency_SPLA,
                                                                     global_max_efficiency_LAHSA + get_spots(
                                                                         lahsa_applicant)]
                    else:
                        global_LAHSA_dict[spla_applicant[:5]] = [global_max_efficiency_SPLA,
                                                                 global_max_efficiency_LAHSA + get_spots(
                                                                     lahsa_applicant)]
                    #print "exhaustive_select_SPLA: Pairs to compare are: SPLA", spla_applicant, "LAHSA", lahsa_applicant
                    #print "global_LAHSA_dict:", global_LAHSA_dict
                    global_max_efficiency_LAHSA = 0
                    global_max_efficiency_SPLA = 0
                    increase_capacity(capacity_LAHSA, lahsa_applicant[13:])

            # if spla_applicant[:5] not in global_LAHSA_dict :
            #     print "global_SPLA_dict[spla_applicant[:5]] is set to :", [get_total_SPLA_values(SPLA_eligible_list, capacity_SPLA),0]
            #     global_SPLA_dict[spla_applicant[:5]] = [get_total_SPLA_values(SPLA_eligible_list, capacity_SPLA),0]

            if (len(common_list) == 1 and spla_applicant == common_list[0]) or not any_lahsa_eligible:
                # print "In common list:", common_list
                global_SPLA_dict[spla_applicant[:5]] = [get_total_SPLA_values(SPLA_eligible_list, capacity_SPLA), 0]
                if len(common_list)>0:
                    common_list.pop()
            elif len(SPLA_eligible_list) == 1:
                return SPLA_eligible_list[0][:5]
            else:
                # print "global_LAHSA_dict:", global_LAHSA_dict, "spla_applicant:", spla_applicant
                new_list_max = global_LAHSA_dict[spla_applicant[:5]]
                new_list_max[0] += get_spots(spla_applicant)
                global_SPLA_dict[spla_applicant[:5]] = new_list_max
        increase_capacity(capacity_SPLA, spla_applicant[13:])
        # get_maximized_LAHSA(get_spots(spla_applicant))
        # if spla_applicant[:5] in global_SPLA_dict:
        #     if global_max_efficiency_SPLA+get_spots(spla_applicant) > global_SPLA_dict[spla_applicant[:5][0]]:
        #         global_SPLA_dict[spla_applicant[:5]] = [global_max_efficiency_SPLA+get_spots(spla_applicant),
        #                                                 global_max_efficiency_LAHSA]
        # else:
        #     global_SPLA_dict[spla_applicant[:5]] = get_maximized_LAHSA(get_spots(spla_applicant))
        # print "global_SPLA_dict:", global_SPLA_dict

    next_SPLA_id = get_maximized_SPLA()
    #print "global_SPLA_dict:", global_SPLA_dict
    return next_SPLA_id


'''Main function starts'''
if __name__ == "__main__":
    start_time = time.time()
    LAHSA_chosen_list = []
    SPLA_chosen_list = []
    total_applicant_list = []

    line_num = 1
    inputFP = open('input.txt', 'r')

    '''Read input begin'''
    LAHSA_beds = int(inputFP.readline().rstrip('\n'))
    SPLA_spots = int(inputFP.readline().rstrip('\n'))
    LAHSA_chosen_num = int(inputFP.readline().rstrip('\n'))
    for i in range(LAHSA_chosen_num):
        LAHSA_chosen_list.append(inputFP.readline().rstrip('\n'))
    SPLA_chosen_num = int(inputFP.readline().rstrip('\n'))
    for i in range(SPLA_chosen_num):
        SPLA_chosen_list.append(inputFP.readline().rstrip('\n'))
    total_applicant_num = int(inputFP.readline().rstrip('\n'))
    for i in range(total_applicant_num):
        total_applicant_list.append(inputFP.readline().rstrip('\n'))

    if inputFP.readline() == '':
        inputFP.close()
    '''Read input end'''

    capacity_SPLA = [SPLA_spots for i in range(7)]
    capacity_LAHSA = [LAHSA_beds for i in range(7)]

    '''print 'LAHSA beds :', LAHSA_beds
    print 'SPLA spots :', SPLA_spots
    print 'LAHSA chose', LAHSA_chosen_num, 'of applicants'
    print 'LAHSA chosen applicants :', LAHSA_chosen_list
    print 'SPLA chose', SPLA_chosen_num, 'of applicants'
    print 'SPLA chosen applicants :', SPLA_chosen_list
    print 'total applicants :', total_applicant_num
    print 'total applicants list :', total_applicant_list '''

    update_capacity(SPLA_chosen_list, LAHSA_chosen_list, total_applicant_list, capacity_SPLA, capacity_LAHSA)

    remaining_applications(SPLA_chosen_list, LAHSA_chosen_list, total_applicant_list)
    # print 'After removal, total_applicants :', total_applicant_list

    SPLA_eligible_list = find_SPLA_eligible(total_applicant_list)
    LAHSA_eligible_list = find_LAHSA_eligible(total_applicant_list)

    #print "SPLA eligible List :", SPLA_eligible_list
    #print "LAHSA eligible List :", LAHSA_eligible_list

    common_list = find_common_list(SPLA_eligible_list, LAHSA_eligible_list)
    #print "Common List :", common_list

    if (len(common_list) == 0 or len(LAHSA_eligible_list) == 0) and (len(SPLA_eligible_list) <= SPLA_spots and len(LAHSA_eligible_list) <= LAHSA_beds):
        next_SPLA_id = get_max_SPLA_id(SPLA_eligible_list, capacity_SPLA)
        outputFP = open('output.txt', 'w')
        outputFP.write(next_SPLA_id + '\n')
        outputFP.close()

    elif len(SPLA_eligible_list) <= SPLA_spots and len(LAHSA_eligible_list) <= LAHSA_beds :
        next_SPLA_id = greedy_select_SPLA(common_list)
        #print common_list[next_SPLA_id][:5]

        outputFP = open('output.txt', 'w')
        outputFP.write(common_list[next_SPLA_id][:5] + '\n')
        outputFP.close()
    else :
        next_SPLA_id = exhaustive_select_SPLA(SPLA_eligible_list, LAHSA_eligible_list, capacity_SPLA, capacity_LAHSA,
                                          common_list)
        # print "next_SPLA_id :", next_SPLA_id
        # print "next_SPLA_id_new:", next_applicant_SPLA
        # print "global_max_efficiency_SPLA:", global_max_efficiency_SPLA
        outputFP = open('output.txt', 'w')
        outputFP.write(next_SPLA_id)
        outputFP.close()

    # print "counter:", counter
    # print time.time() - start_time