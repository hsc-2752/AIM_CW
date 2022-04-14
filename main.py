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

class Problem:
    def __init__(self,prolem_Set,index):
        self.instance = prolem_Set.all_instance[index]
        self.capacity = prolem_Set.all_capacity[index]
        self.item_num = prolem_Set.all_item_num[index]
        self.best_record = prolem_Set.all_best_record[index]

class Problem_Set:
    def __init__(self,file_name,max_time):
        self.file_name = file_name
        self.max_time = max_time
        self.all_instance = []
        self.all_capacity = []  # capacity of all instances in the file
        self.all_item_num = []  # item number of all instances in the file
        self.all_best_record = []  # best record of all instances in the file

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
            if item[0] == ' ' and item[1] == 'u':
                self.all_instance.append(current_instance)
                current_instance = []
                start_flag = True
            elif start_flag:
                start_flag = False
                if item[0] == " ":
                    item = item[1:]
                instance_info = item.split(' ')
                self.all_capacity.append(instance_info[0])
                self.all_item_num.append(instance_info[1])
                self.all_best_record.append(instance_info[2][:-1])
            else:
                start_flag = False
                current_instance.append(item[:-1])
        self.all_instance.append(current_instance)
        del self.all_instance[0]



class VNS:
    def __init__(self,problem):
        self.initial_solution = Solution(problem)
        self.neighbourhood_list = []

    def get_initial_solution(self):
        self.initial_solution.bin_list = greedy_search(self.initial_solution.problem.instance,self.initial_solution.problem.capacity)
        self.initial_solution.objective = len(self.initial_solution.bin_list)
        self.initial_solution.feasibility = True

    def get_neighbourhood_list(self):
        print("do not need any return")

    def perform_local_search(self):
        #return solution


    def stop(self):
        return False

    def f(self):


    def shaking(self,solution):


    def perform_VNS_search(self):
        neighbourhood_index = 0
        best_solution = self.initial_solution
        loop_temp_best_solution = self.initial_solution
        while self.stop() == False:
            while (neighbourhood_index <= len(self.neighbourhood_list)):
                temp_solution = self.perform_local_search(self.neighbourhood_list[neighbourhood_index])
                if(self.f(temp_solution)<self.f(loop_temp_best_solution)):
                    loop_temp_best_solution = temp_solution
                    neighbourhood_index = 1 #Strategies for changing neighbourhoods,might need to be changed
                    continue
                else:
                    neighbourhood_index = neighbourhood_index+1 #Strategies for changing neighbourhoods,might need to be changed
            if(self.f(loop_temp_best_solution)<self.f(best_solution)):
                best_solution = loop_temp_best_solution
            loop_temp_best_solution = self.shaking(loop_temp_best_solution)
        return best_solution

# This function searches in a list to find the index of the largest value(< capacity)
def search_max(list,banned_index_list,capacity):
    max_value = 0
    max_index = -2
    for i in range(len(list)):
        if not(i in banned_index_list) and capacity > list[i] > max_value:
            max_value = list[i]
            max_index = i
    return max_index,max_value


def greedy_search(item_list, capacity):
    all_bin = []
    #current_bin = []
    current_bin = Bin(capacity)
    placed_item_index = []
    #current_capacity = capacity
    while len(placed_item_index) != len(item_list):
        max_ind, max_val = search_max(item_list, placed_item_index, current_bin.cap_left)

        # The left capacity in this box can not contain any more item
        if max_val == 0:
            all_bin.append(current_bin)
            current_bin = Bin(capacity)
            #current_capacity = capacity
        else:
            current_bin.item_list.append(max_ind)
            current_bin.cap_left = current_bin.cap_left - max_val
            #current_capacity = current_capacity - max_val
            placed_item_index.append(max_ind)

    return all_bin


# input: a list of item to be put inside the bin_list([bin0,bin1,bin2...])
# output: new bin_list
# method: first fit
# 传一个problem进来，这里具体的还需修改
# item_list中保存的是item index, item体积需要访问(solution.)problem.instance
def reput_item(item_list,bin_list,problem):
    item_volume = problem.instance
    flag = False
    for item in item_list:
        #feasible_bin = []
        for bin in bin_list:
            if item_volume[item]<bin.cap_left:
                #feasible_bin.append(bin)
                bin.item_list.append(item)
                bin.cap_left = bin.cap_left-item_volume[item]
                flag = True
                break
        #哪都放不下，开个新的bin
        if not flag:
            new_bin = Bin(problem.capacity)
            new_bin.bin_list.append(item)
            new_bin.cap_left = new_bin.cap_left-item_volume[item]
            bin_list.append(new_bin)
    return bin_list









if __name__ == '__main__':
    file_name = "binpack1.txt"
    max_time = 30
    VNS(file_name, max_time)
