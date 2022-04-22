import time
import copy
import random
import math


class Bin:
    def __init__(self, capacity):
        self.item_list = []
        self.capacity = capacity
        self.cap_left = capacity


class Solution:
    def __init__(self, problem):
        self.problem = problem
        # self.objective = 0
        self.feasibility = False
        self.bin_list = []

    def get_objective(self):
        objective = 0
        for bin in self.bin_list:
            if bin.item_list:
                objective = objective + 1
        return objective


class Problem:
    def __init__(self, problem_Set, index):
        self.instance = problem_Set.all_instance[index]
        self.capacity = problem_Set.all_capacity[index]
        self.item_num = problem_Set.all_item_num[index]
        self.best_record = problem_Set.all_best_record[index]


class Problem_Set:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_instance = []
        self.all_capacity = []  # capacity of all instances in the file
        self.all_item_num = []  # item number of all instances in the file
        self.all_best_record = []  # best record of all instances in the file
        self.load_problem()

    def load_problem(self):

        # read from the file
        fp = open(self.file_name)
        content = fp.readlines()
        fp.close()

        # process to get problem instance list
        del content[0]

        start_flag = False

        current_instance = []
        for item in content:
            if item == '\n':
                break
            if item[0] == ' ' and item[1].isalpha():
                self.all_instance.append(current_instance)
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
        self.best_solution = None  # 不是说最优解，只是运行过程中的最优
        self.initial_solution = Solution(problem)
        # self.neighbourhood_list = []
        self.start_time = time.time()
        self.get_initial_solution()

    def get_initial_solution(self):
        self.initial_solution.bin_list = greedy_search(self.initial_solution.problem.instance,
                                                       self.initial_solution.problem.capacity)
        self.initial_solution.objective = len(self.initial_solution.bin_list)
        self.initial_solution.feasibility = True
        # print(len(self.initial_solution.bin_list) - self.initial_solution.problem.best_record)

    # def get_initial_solution(self):
    #     for item_index in range(len(self.initial_solution.problem.instance)):
    #         new_bin = Bin(self.initial_solution.problem.capacity)
    #         new_bin.item_list.append(item_index)
    #         new_bin.cap_left = new_bin.cap_left - self.initial_solution.problem.instance[item_index]
    #         self.initial_solution.bin_list.append(new_bin)
    #
    #     # self.initial_solution.objective = len(self.initial_solution.bin_list)
    #     self.initial_solution.feasibility = True

    # def get_neighbourhood_list(self):
    #     print("do not need any return")

    def perform_local_search(self, solution, neighbourhood_index):
        if neighbourhood_index != 0:
            # print("dsdfefe")
            solution.bin_list = randomBin_reshuffle(solution.bin_list, solution.problem.instance,
                                                    solution.problem.capacity)
        else:
            solution.bin_list = largestBin_largestItem(solution.bin_list, solution.problem.instance)
        #     total_times = 0
        #     no_improve_times = 0
        #     best_solution = copy.deepcopy(solution)
        #     while (no_improve_times < 20) and (total_times < math.pow(len(solution.bin_list), neighbourhood_index + 1)):
        #
        #         total_times = total_times + 1
        #         new_solution = copy.deepcopy(solution)
        #         to_be_reput_item_list = []
        #
        #         # 生成neighbourhood_index个随机数对应bin的index
        #         clear_bin_list = random.sample(range(0, len(new_solution.bin_list)), neighbourhood_index)
        #
        #         # 把这些bin里的item取出来合成一个list，把这些bin删掉
        #         for clear_bin_index in clear_bin_list:
        #             to_be_reput_item_list = to_be_reput_item_list + new_solution.bin_list[clear_bin_index].item_list
        #         new_bin_list = []
        #         for bin_index in range(len(new_solution.bin_list)):
        #             if (not (bin_index in clear_bin_list)) and new_solution.bin_list[bin_index].item_list:
        #                 new_bin_list.append(new_solution.bin_list[bin_index])
        #         new_solution.bin_list = new_bin_list
        #
        #         # 把item分配掉
        #         new_solution.bin_list = reput_item(to_be_reput_item_list, new_solution.bin_list, new_solution.problem)
        #         # new_solution.objective = len(new_solution.bin_list)
        #         # print(new_solution.objective)
        #
        #         # 如果有优化，则把当前solution作为下次开始的solution
        #         # solution = copy.deepcopy(new_solution)
        #         # print(solution.get_objective(),new_solution.get_objective())
        #         if new_solution.get_objective() < solution.get_objective():
        #             # solution = copy.deepcopy(new_solution)
        #             solution = copy.deepcopy(new_solution)
        #             no_improve_times = 0
        #         else:
        #             no_improve_times = no_improve_times + 1
        #
        # # print(len(solution.bin_list))
        # # for bin in solution.bin_list:
        # #     print(bin.item_list, end="")
        # # print("\n")
        # # print(best_solution.get_objective())
        return solution

    def stop(self):
        # 时间超过30s
        # 或 <= solution.problem.best_record
        if (time.time() - self.start_time) >= 30:
            print("time out!")
            return True
        else:
            if (self.best_solution.get_objective() - self.initial_solution.problem.best_record) <= 0:
                return True
        return False

    # def f(self,solution):
    #     return solution.objective

    # def shaking(self,solution):

    def perform_VNS_search(self):
        # temp
        neighbourhood_num = 3

        neighbourhood_index = 0
        # self.best_solution = self.initial_solution
        # loop_temp_best_solution = self.initial_solution
        # temp_solution = self.initial_solution
        # copy.deepcopy(solution)
        self.best_solution = copy.deepcopy(self.initial_solution)
        loop_temp_best_solution = copy.deepcopy(self.initial_solution)
        temp_solution = copy.deepcopy(self.initial_solution)

        while not self.stop():
            # print(self.best_solution.objective)
            # while neighbourhood_index <= neighbourhood_num:
            # print('194')
            temp_solution = self.perform_local_search(temp_solution, neighbourhood_index)

            # if(self.f(temp_solution)<self.f(loop_temp_best_solution)):
            if temp_solution.get_objective() <= loop_temp_best_solution.get_objective():
                # print(temp_solution.get_objective())

                loop_temp_best_solution = copy.deepcopy(temp_solution)
                neighbourhood_index = 1  # Strategies for changing neighbourhoods,might need to be changed
                continue
            else:

                neighbourhood_index = neighbourhood_index + 1  # Strategies for changing neighbourhoods,might need to be changed
        # if self.f(loop_temp_best_solution) < self.f(self.best_solution):
        if loop_temp_best_solution.get_objective() < self.best_solution.get_objective():
            self.best_solution = copy.deepcopy(loop_temp_best_solution)
            # loop_temp_best_solution = self.shaking(loop_temp_best_solution)
        # return best_solution


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
    # print(item_list)
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

    return all_bin


# input: a list of item to be put inside the bin_list([bin0,bin1,bin2...])
# output: new bin_list
# method: first fit
# 传一个problem进来，这里具体的还需修改
# item_list中保存的是item index, item体积需要访问(solution.)problem.instance
def reput_item(item_list, bin_list, problem):
    item_volume = problem.instance

    for item in item_list:
        flag = False

        for bin in bin_list:
            if item_volume[item] < bin.cap_left:
                bin.item_list.append(item)
                bin.cap_left = bin.cap_left - item_volume[item]
                flag = True
                break
        # 哪都放不下，开个新的bin
        if not flag:
            new_bin = Bin(problem.capacity)
            new_bin.item_list.append(item)
            new_bin.cap_left = new_bin.cap_left - item_volume[item]
            bin_list.append(new_bin)
    return bin_list


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
    min_gap = capacity
    min_gap_item_selection = ''
    bin_1_index = ran_bin_by_proba(bin_list)
    bin_2_index = ran_bin_by_proba(bin_list)
    while bin_1_index == bin_2_index:
        bin_2_index = ran_bin_by_proba(bin_list)

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
    bin_list[bin_2_index].item_list = []
    for item_i in range(len(reshuffle_item_list)):
        if min_gap_item_selection[item_i] == '1':
            bin_list[bin_1_index].item_list.append(reshuffle_item_list[item_i])
        else:
            bin_list[bin_2_index].item_list.append(reshuffle_item_list[item_i])
    return bin_list


# 给bin赋概率 剩余空间越多的bin概率越低 --- 剩余体积list[v1,v2,v3,v4,...,vn] 生成一个1到sum之间的随机数，判断在哪
def ran_bin_by_proba(bin_list):
    left_cap_list = []
    for bin in bin_list:
        left_cap_list.append(bin.cap_left)

    rand = random.randint(1, sum(left_cap_list))
    cap_index = 0
    while rand > 0:
        if rand <= left_cap_list[cap_index]:
            return cap_index
        else:
            rand = rand - left_cap_list[cap_index]
            cap_index = cap_index + 1


def largestBin_largestItem(bin_list, item_volume):
    # selects the largest item from the bin with the largest cap_left
    min_cap_left = 100000
    for bin_index in range(len(bin_list)):
        # print((bin_list[bin_index].cap_left))
        if bin_list[bin_index].cap_left < min_cap_left:
            min_cap_left = bin_list[bin_index].cap_left
            min_cap_left_bin_index = bin_index
    largest_item_volume = 0
    for item_index in bin_list[min_cap_left_bin_index].item_list:
        if item_volume[item_index] > largest_item_volume:
            largest_item_volume = item_volume[item_index]
            largest_item_index = item_index
    # randomly select a bin
    random_bin_index = random.randint(0, len(bin_list) - 1)
    while random_bin_index == min_cap_left_bin_index:
        random_bin_index = random.randint(0, len(bin_list) - 1)
    # randomly select an item smaller than that largest item in this bin
    random_item_index = bin_list[random_bin_index].item_list[
        random.randint(0, len(bin_list[random_bin_index].item_list) - 1)]
    # print(len(bin_list[random_bin_index].item_list))
    while item_volume[random_item_index] < item_volume[largest_item_index] < bin_list[random_bin_index].cap_left:
        random_item_index = bin_list[random_bin_index].item_list[
            random.randint(0, len(bin_list[random_bin_index].item_list) - 1)]
    # swap
    bin_list[min_cap_left_bin_index].item_list.remove(largest_item_index)
    bin_list[min_cap_left_bin_index].item_list.append(random_item_index)
    bin_list[random_bin_index].item_list.remove(random_item_index)
    bin_list[random_bin_index].item_list.append(largest_item_index)
    return bin_list


# Split: this heuristic simply moves half the items (randomly selected from) the current bin to a new bin
#        if the number of items in the current bin exceeds the average item numbers per bin.
# use for shaking
def split(bin_list, average_item_number, capacity, volume_list, bin_index=None):
    # randomly choose a bin in which the number of items exceeds the average item numbers per bin
    if bin_index is None:
        bin_index = random.randint(0, len(bin_list) - 1)
        while bin_list[bin_index].cap_left <= average_item_number:
            bin_index = random.randint(0, len(bin_list) - 1)
    new_bin = Bin(capacity)
    random_item_index_list = random.sample(bin_list[bin_index].item_list, int(len(bin_list[bin_index].item_list) / 2))
    for random_item_index in random_item_index_list:
        new_bin.item_list.append(random_item_index)
        new_bin.cap_left = new_bin.cap_left - volume_list[random_item_index]
    bin_list.append(new_bin)
    return new_bin


if __name__ == '__main__':
    file_name = "binpack3.txt"
    # max_time =
    current_problem_set = Problem_Set(file_name)
    for i in range(len(current_problem_set.all_instance)):
        current_problem = Problem(current_problem_set, i)
        vns = VNS(current_problem)
        vns.perform_VNS_search()
        print(vns.best_solution.get_objective() - vns.initial_solution.problem.best_record)


