import time
import copy
import random
import math


class Bin:
    def __init__(self, capacity):
        self.item_list = []
        self.capacity = capacity
        self.cap_left = capacity

    # def cal_cap_left(self):
    #     self.cap_left = self.capacity - sum(self.item_list)


class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.objective = 0
        self.feasibility = False
        self.bin_list = []

    # def copy(self,solution):
    #     self.problem = solution.problem
    #     self.objective = solution.objective
    #     self.feasibility = solution.feasibility
    #     self.bin_list = solution.bin_list


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
        # print(len(self.initial_solution.bin_list))

    # def get_neighbourhood_list(self):
    #     print("do not need any return")

    def perform_local_search(self, solution, neighbourhood_index):

        total_times = 0
        no_improve_times = 0

        while (no_improve_times < 20) and (total_times < math.pow(len(solution.bin_list), neighbourhood_index)):
            total_times = total_times + 1
            new_solution = copy.deepcopy(solution)
            to_be_reput_item_list = []

            # 生成neighbourhood_index个随机数对应bin的index
            clear_bin_list = random.sample(range(0, len(new_solution.bin_list)), neighbourhood_index)

            # 把这些bin里的item取出来合成一个list，把这些bin删掉
            for clear_bin_index in clear_bin_list:
                to_be_reput_item_list = to_be_reput_item_list + new_solution.bin_list[clear_bin_index].item_list
            new_bin_list = []
            for bin_index in range(len(new_solution.bin_list)):
                if not (bin_index in clear_bin_list):
                    new_bin_list.append(new_solution.bin_list[bin_index])
            new_solution.bin_list = new_bin_list

            # print("-----------new bin list-------------------------")
            # # bin_item_list_list = []
            # # for bin in new_bin_list:
            # #     bin_item_list_list.append(bin.item_list)
            # print(to_be_reput_item_list)
            # print("---end---")

            # 把item分配掉
            new_solution.bin_list = reput_item(to_be_reput_item_list, new_solution.bin_list, new_solution.problem)
            new_solution.objective = len(new_solution.bin_list)
            # print(new_solution.objective)

            # 如果有优化，则把当前solution作为下次开始的solution
            if new_solution.objective < solution.objective:
                solution = new_solution
                no_improve_times = 0
            else:
                no_improve_times = no_improve_times + 1

        return solution

    def stop(self):
        # 时间超过30s
        # 或 <= solution.problem.best_record
        if (time.time() - self.start_time) >= 30:
            # print("time out!")
            return True
        else:
            if (self.best_solution.objective - self.initial_solution.problem.best_record) <= 0:
                return True
        return False

    # def f(self,solution):
    #     return solution.objective

    # def shaking(self,solution):

    def perform_VNS_search(self):
        # temp
        neighbourhood_num = 10
        neighbourhood_index = 0
        self.best_solution = self.initial_solution
        loop_temp_best_solution = self.initial_solution
        temp_solution = self.initial_solution
        while not self.stop():
            # print(self.best_solution.objective)
            while neighbourhood_index <= neighbourhood_num:
                temp_solution = self.perform_local_search(temp_solution, neighbourhood_index)

                # if(self.f(temp_solution)<self.f(loop_temp_best_solution)):
                if temp_solution.objective < loop_temp_best_solution.objective:
                    loop_temp_best_solution = temp_solution
                    neighbourhood_index = 1  # Strategies for changing neighbourhoods,might need to be changed
                    continue
                else:
                    neighbourhood_index = neighbourhood_index + 1  # Strategies for changing neighbourhoods,might need to be changed
            # if self.f(loop_temp_best_solution) < self.f(self.best_solution):
            if loop_temp_best_solution.objective < self.best_solution.objective:
                self.best_solution = loop_temp_best_solution
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
        min_gap = 10000
        min_gap_bin_index = -2
        for bin_index in range(len(bin_list)):
            if item_volume[item] < bin_list[bin_index].cap_left:
                #bin.item_list.append(item)
                #bin.cap_left = bin.cap_left - item_volume[item]
                if(bin_list[bin_index].cap_left-item_volume[item]) < min_gap:
                    min_gap_bin_index = bin_index
                    min_gap = bin_list[bin_index].cap_left
                flag = True
                #break
        # 哪都放不下，开个新的bin
        bin_list[min_gap_bin_index].item_list.append(item)
        bin_list[min_gap_bin_index].cap_left = bin_list[min_gap_bin_index].cap_left - item_volume[item]
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
    return max_index,flag


# def reput_item(item_list, bin_list, problem):
#     item_volume = problem.instance
#
#     for bin in bin_list: #
#         max_fit_item_index, flag = finMax_constrained(item_list, bin.cap_left, item_volume)
#         while flag:
#             bin.item_list.append(max_fit_item_index)
#             bin.cap_left = bin.cap_left - item_volume(max_fit_item_index)
#             item_list.pop(max_fit_item_index)






if __name__ == '__main__':
    file_name = "binpack3.txt"
    # max_time =
    current_problem_set = Problem_Set(file_name)
    for i in range(len(current_problem_set.all_instance)):
        current_problem = Problem(current_problem_set, i)
        vns = VNS(current_problem)
        vns.perform_VNS_search()
        print(vns.best_solution.objective - vns.best_solution.problem.best_record)

# 可能有些地方对象赋值有问题
