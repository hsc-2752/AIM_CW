import time
import copy
import random
import math
import sys


class Bin:
    def __init__(self, capacity):
        self.item_list = []
        self.capacity = capacity
        self.cap_left = capacity


class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.bin_list = []

    def get_objective(self):
        objective = 0
        for bin in self.bin_list:
            if bin.item_list:
                objective = objective + 1
        return objective

    def fitness(self):
        sum1 = 0.0
        sum2 = 0.0
        N = 0
        for bin in self.bin_list:
            if bin.item_list:
                N = N + 1
                sum1 = sum1 + bin.cap_left
                sum2 = sum2 + bin.cap_left ** 2
        mean = sum1 / N
        var = sum2 / N - mean ** 2
        return var


class Problem:
    def __init__(self, problem_Set, index):
        self.instance = problem_Set.all_instance[index]
        self.capacity = problem_Set.all_capacity[index]
        self.item_num = problem_Set.all_item_num[index]
        self.best_record = problem_Set.all_best_record[index]
        self.instance_id = problem_Set.all_instance_id[index]


class Problem_Set:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_instance = []
        self.all_capacity = []  # capacity of all instances in the file
        self.all_item_num = []  # item number of all instances in the file
        self.all_best_record = []  # best record of all instances in the file
        self.all_instance_id = []
        self.instance_num = 0
        self.load_problem()

    def load_problem(self):

        # read from the file
        fp = open(self.file_name)
        content = fp.readlines()
        fp.close()

        # process to get problem instance list
        self.instance_num = content[0]
        del content[0]

        start_flag = False

        current_instance = []
        for item in content:
            if item == '\n':
                break
            if item[0] == ' ' and item[1].isalpha():
                self.all_instance.append(current_instance)
                self.all_instance_id.append(item[1:])
                current_instance = []
                start_flag = True
            elif start_flag:
                start_flag = False
                if item[0] == " ":
                    item = item[1:]
                instance_info = item.split(' ')
                self.all_capacity.append(int(instance_info[0]))
                self.all_item_num.append(int(instance_info[1]))
                self.all_best_record.append(int(instance_info[2][:-1]))
            else:
                start_flag = False
                current_instance.append(int(item[:-1]))
        self.all_instance.append(current_instance)
        del self.all_instance[0]


class VNS:
    def __init__(self, problem):
        self.best_solution = None
        self.initial_solution = Solution(problem)
        self.start_time = time.time()
        self.get_initial_solution()

    def get_initial_solution(self):
        self.initial_solution.bin_list = greedy_search(self.initial_solution.problem.instance,
                                                       self.initial_solution.problem.capacity)

    def perform_local_search_best_descent(self, solution, neighbourhood_index):
        inner_i = 0
        neighbour_solution = copy.deepcopy(solution)

        while neighbour_solution.get_objective() >= solution.get_objective() and inner_i < 1000:
            inner_i = inner_i + 1
            neighbour_solution = copy.deepcopy(solution)

            if neighbourhood_index == 1:
                neighbour_solution.bin_list = shift(solution.bin_list, solution.problem.instance)

            if neighbourhood_index == 0:
                neighbour_solution.bin_list = largestBin_largestItem(solution.bin_list, solution.problem.instance)

            if neighbour_solution.fitness() > solution.fitness():
                solution = copy.deepcopy(neighbour_solution)

        return solution

    def stop(self):
        if (time.time() - self.start_time) >= max_time:
            return True
        else:
            if (self.best_solution.get_objective() - self.initial_solution.problem.best_record) <= 0:
                return True
        return False

    def perform_VNS_search(self):

        neighbourhood_num = 2
        neighbourhood_index = 0
        self.best_solution = copy.deepcopy(self.initial_solution)
        solution = copy.deepcopy(self.initial_solution)

        while not self.stop():
            while neighbourhood_index < neighbourhood_num and not self.stop():
                solution_prime = self.perform_local_search_best_descent(solution, neighbourhood_index)
                if solution_prime.get_objective() < solution.get_objective():
                    solution = copy.deepcopy(solution_prime)
                    neighbourhood_index = 0
                    continue
                else:
                    neighbourhood_index = neighbourhood_index + 1
            if solution.get_objective() <= self.best_solution.get_objective():
                self.best_solution = copy.deepcopy(solution)
            solution = shaking(solution)


def shaking(solution):
    shaking_random_bin_list = []
    for i in range(20):
        shaking_random_bin_list.append(randomBin_reshuffle(solution.bin_list, solution.problem.instance,
                                                           solution.problem.capacity))
    solution.bin_list = shaking_random_bin_list[random.randint(0, 19)]
    return solution


def clear_empty_bin(bin_list):
    processed_bin_list = []
    for bin in bin_list:
        if bin.item_list:
            processed_bin_list.append(bin)
    return processed_bin_list


# This function searches in a list to find the index of the largest value(< capacity)
def search_max(list, banned_index_list, capacity):
    max_value = 0
    max_index = -2
    for i in range(len(list)):
        if not (i in banned_index_list) and capacity > list[i] > max_value:
            max_value = list[i]
            max_index = i
    return max_index, max_value


def greedy_search(item_list, capacity):
    # print(len(item_list),"215")
    all_bin = []
    # current_bin = []
    current_bin = Bin(capacity)
    placed_item_index = []
    # current_capacity = capacity
    while len(placed_item_index) != len(item_list):
        # print(len(placed_item_index))
        max_ind, max_val = search_max(item_list, placed_item_index, current_bin.cap_left)
        # The left capacity in this box can not contain any more item
        if max_val == 0:
            all_bin.append(current_bin)
            current_bin = Bin(capacity)
            # current_capacity = capacity
        else:
            current_bin.item_list.append(max_ind)
            current_bin.cap_left = current_bin.cap_left - max_val
            # current_capacity = current_capacity - max_val
            placed_item_index.append(max_ind)
    all_bin.append(current_bin)

    return all_bin


def finMax_constrained(item_list_indexed, constraint, item_volume):
    max_index = 0
    flag = 0
    for item_index in item_list_indexed:
        if item_volume[item_index] < constraint:
            if item_volume[item_index] > item_volume[max_index]:
                max_index = item_index
            flag = 1
    return max_index, flag


def randomBin_reshuffle(bin_list, item_volume, capacity):
    bin_list = clear_empty_bin(bin_list)
    min_gap = capacity
    min_gap_item_selection = ''
    bin_1_index = ran_bin_by_proba(bin_list)
    bin_2_index = ran_bin_by_proba(bin_list)
    while not bin_list[bin_1_index].item_list:
        bin_1_index = ran_bin_by_proba(bin_list)

    while not bin_list[bin_2_index].item_list:
        bin_1_index = ran_bin_by_proba(bin_list)

    if bin_1_index == bin_2_index:
        return bin_list

    reshuffle_item_list = bin_list[bin_1_index].item_list + bin_list[bin_2_index].item_list

    for i in range(int(math.pow(2, len(reshuffle_item_list)))):
        i_bin = bin(i)[2:].zfill(len(reshuffle_item_list))
        weighted_list = []
        for j in range(len(reshuffle_item_list)):
            weighted_list.append(item_volume[reshuffle_item_list[j]] * int(i_bin[j]))
        if 0 < capacity - sum(weighted_list) < min_gap:
            min_gap = capacity - sum(weighted_list)
            min_gap_item_selection = i_bin
    bin_list[bin_1_index].item_list = []
    bin_list[bin_1_index].cap_left = capacity
    bin_list[bin_2_index].item_list = []
    bin_list[bin_2_index].cap_left = capacity
    for item_i in range(len(reshuffle_item_list)):
        if min_gap_item_selection[item_i] == '1':
            bin_list[bin_1_index].item_list.append(reshuffle_item_list[item_i])
            bin_list[bin_1_index].cap_left = bin_list[bin_1_index].cap_left - item_volume[reshuffle_item_list[item_i]]
        else:
            bin_list[bin_2_index].item_list.append(reshuffle_item_list[item_i])
            bin_list[bin_2_index].cap_left = bin_list[bin_2_index].cap_left - item_volume[reshuffle_item_list[item_i]]

    return clear_empty_bin(bin_list)


# give each bin a probability proportional to cap_left
def ran_bin_by_proba(bin_list):
    left_cap_list = []
    # generate a capacity left list[v1,v2,v3,v4,...,vn]
    for bin in bin_list:
        left_cap_list.append(bin.cap_left)

    # generate a random number between 1 to sum
    rand = random.randint(1, sum(left_cap_list))
    cap_index = 0
    while rand > 0:
        if rand <= left_cap_list[cap_index]:
            return cap_index
        else:
            rand = rand - left_cap_list[cap_index]
            cap_index = cap_index + 1


def largestBin_largestItem(bin_list, item_volume):
    bin_list = clear_empty_bin(bin_list)

    # selects the largest item from the bin with the largest cap_left
    max_cap_left = 0
    for bin_index in range(len(bin_list)):
        # print((bin_list[bin_index].cap_left))
        if bin_list[bin_index].cap_left > max_cap_left:
            max_cap_left = bin_list[bin_index].cap_left
            max_cap_left_bin_index = bin_index
    largest_item_volume = 0
    for item_index in bin_list[max_cap_left_bin_index].item_list:
        if item_volume[item_index] > largest_item_volume:
            largest_item_volume = item_volume[item_index]
            largest_item_index = item_index
    # randomly select a bin
    random_bin_index = random.randint(0, len(bin_list) - 1)
    while random_bin_index == max_cap_left_bin_index:
        random_bin_index = random.randint(0, len(bin_list) - 1)

    random_item_index = bin_list[random_bin_index].item_list[
        random.randint(0, len(bin_list[random_bin_index].item_list) - 1)]

    if not (item_volume[random_item_index] < item_volume[largest_item_index] < bin_list[random_bin_index].cap_left +
            item_volume[random_item_index]):
        return bin_list

    # swap

    bin_list[max_cap_left_bin_index].item_list.remove(largest_item_index)
    bin_list[max_cap_left_bin_index].cap_left = bin_list[max_cap_left_bin_index].cap_left + item_volume[
        largest_item_index]

    bin_list[max_cap_left_bin_index].item_list.append(random_item_index)
    bin_list[max_cap_left_bin_index].cap_left = bin_list[max_cap_left_bin_index].cap_left - item_volume[
        random_item_index]

    bin_list[random_bin_index].item_list.remove(random_item_index)
    bin_list[random_bin_index].cap_left = bin_list[random_bin_index].cap_left + item_volume[random_item_index]

    bin_list[random_bin_index].item_list.append(largest_item_index)
    bin_list[random_bin_index].cap_left = bin_list[random_bin_index].cap_left - item_volume[largest_item_index]

    return clear_empty_bin(bin_list)


# Split: this heuristic simply moves half the items (randomly selected from) the current bin to a new bin
#        if the number of items in the current bin exceeds the average item numbers per bin.

def split(bin_list, average_item_number, capacity, volume_list, bin_index=None):
    # randomly choose a bin in which the number of items exceeds the average item numbers per bin
    if bin_index is None:
        bin_index = random.randint(0, len(bin_list) - 1)
        while bin_list[bin_index].cap_left <= average_item_number:
            bin_index = random.randint(0, len(bin_list) - 1)
    new_bin = Bin(capacity)
    random_item_index_list = random.sample(bin_list[bin_index].item_list, int(len(bin_list[bin_index].item_list) / 2))
    for random_item_index in random_item_index_list:
        bin_list[bin_index].item_list.remove(random_item_index)
        bin_list[bin_index].cap_left = bin_list[bin_index].cap_left + volume_list[random_item_index]
        new_bin.item_list.append(random_item_index)
        new_bin.cap_left = new_bin.cap_left - volume_list[random_item_index]
    bin_list.append(new_bin)
    return bin_list


# selects each item from the bin with the largest residual capacity and
# tries to move the items to the rest of the bins using the best fit descent
def shift(bin_list, volume_list):
    max_cap_left = 0
    for bin_index in range(len(bin_list)):
        if bin_list[bin_index].cap_left > max_cap_left:
            max_cap_left = bin_list[bin_index].cap_left
            max_cap_left_bin_index = bin_index
    for item in bin_list[max_cap_left_bin_index].item_list:
        min_gap = 10000
        flag = 0
        for bin_index_best_fit in range(len(bin_list)):
            if 0 < bin_list[bin_index_best_fit].cap_left - volume_list[item] < min_gap and bin_index_best_fit != max_cap_left_bin_index:
                min_gap_index = bin_index_best_fit
                min_gap = bin_list[bin_index_best_fit].cap_left - volume_list[item]
                flag = 1
        if flag:
            bin_list[max_cap_left_bin_index].item_list.remove(item)
            bin_list[max_cap_left_bin_index].cap_left = bin_list[max_cap_left_bin_index].cap_left + volume_list[item]
            bin_list[min_gap_index].item_list.append(item)
            bin_list[min_gap_index].cap_left = bin_list[min_gap_index].cap_left - volume_list[item]
    return clear_empty_bin(bin_list)


# write solution of single problem to the file
def write_to_file(solution):
    # file_handle = open(solution_file_name,mode = 'a')
    file_handle.write(solution.problem.instance_id)
    file_handle.write(" obj=   " + str(solution.get_objective()) + '\t' + str(
        solution.get_objective() - solution.problem.best_record))
    file_handle.write('\n')
    for bin in solution.bin_list:
        if not bin.item_list:
            continue
        for item in bin.item_list:
            file_handle.write(str(item) + ' ')
        file_handle.write('\n')


if __name__ == '__main__':
    global max_time
    file_name = sys.argv[2]
    solution_file_name = sys.argv[4]
    max_time = int(sys.argv[-1])
    current_problem_set = Problem_Set(file_name)
    file_handle = open(solution_file_name, mode='a')
    file_handle.write(str(current_problem_set.instance_num))
    for i in range(len(current_problem_set.all_instance)):
        current_problem = Problem(current_problem_set, i)
        vns = VNS(current_problem)
        vns.perform_VNS_search()
        write_to_file(vns.best_solution)
        print(vns.best_solution.get_objective() - vns.initial_solution.problem.best_record)
    file_handle.close()
