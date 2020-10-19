import requests
import heapq
import json
import img
from collections import deque

class Problem:

    def __init__(self):
        self.__challenge_data = {}
        self.__answers_dicts = []
        self.__answers_dicts.append({})
        for i in range(1, 10):
            with open(r'.\data\answer\ans' + str(i) + '.json', 'r') as answer_file:
                self.__answers_dicts.append(json.load(answer_file))

        self.__img = img.Img()

        self.__answer = {
            "operations": '',
            "swap": []
        }


    def load(self, chellenge_data):
        self.__challenge_data = chellenge_data

        self.__img.load(b64str=self.__challenge_data['img'], path='./data/img/problem.png')
        self.__img_status = self.__img.get_status()
        self.__step = self.__challenge_data['step']
        self.__swap = self.__challenge_data['swap']

        self.__caculate_answer()


    def __caculate_answer(self):
        status_type = 0
        for i in range(1, 10):
            if str(i) not in list(self.__img_status):
                status_type = i
                break

        operations = self.__answers_dicts[status_type].get(self.__img_status, 'w' * 100)

        if len(operations) <= self.__step:
            print("no forced swap")
            self.__answer["operations"] = operations
            self.__answer["swap"] = []
        else:
            print("forced swap")
            self.__answer["operations"], self.__answer["swap"] = \
                self.__caculate_operations(
                    stauts_type=status_type,
                    orign_status=self.__img_status,
                    force_swap=self.__swap,
                    step_to_swap=self.__step)

    def __caculate_operations(self, stauts_type: int, orign_status: str, force_swap: list, step_to_swap: int) -> tuple:
        answers = self.__answers_dicts[stauts_type]
        operation = {
            -1: 'a',
            +1: 'd',
            -3: 'w',
            +3: 's'
        }
        dindexes = {
            1: [+1, +3],
            2: [-1, +3, +1],
            3: [-1, +3],
            4: [-3, +1, +3],
            5: [-3, -1, +1, +3],
            6: [-3, -1, +3],
            7: [-3, +1],
            8: [-3, -1, +1],
            9: [-3, -1]
        }
        reverse_operation = {
            'a': 'd',
            'd': 'a',
            'w': 's',
            's': 'w'
        }

        def swap_image(status, num_1, num_2) -> str:
            status = list(status)
            status[num_1], status[num_2] = status[num_2], status[num_1]
            return ''.join(status)

        def diff(status: str, target_status: str) -> int:
            cnt = 0
            for i in range(len(status)):
                if status[i] != target_status[i]:
                    cnt += 1
            return cnt

        def h(status: str, target_status: str) -> int:
            return diff(swap_image(status, force_swap[0], force_swap[1]), target_status)

        orign_status = 's' + orign_status
        target_status = 's' + ''.join([str(i) if i != stauts_type else '0' for i in range(1, 10)])

        # zero_index
        zero_index = 0
        for i in range(1, 10):
            if orign_status[i] == '0':
                zero_index = i
                break

        print("orign_status:", orign_status)
        print("target_status:", target_status)
        print("forced_swap:", force_swap)
        print("step_to_swap:", step_to_swap)

        vis = set()
        close_table = []

        # open_table = []
        open_table = deque()

        step = 0
        # f = h(orign_status, target_status)
        f = step
        operations = ''
        status = orign_status
        # heapq.heappush(open_table, (f, status, zero_index, step, operations))
        open_table.append((f, status, zero_index, step, operations))

        # search
        while open_table:
            # f, status, zero_index, step, operations = heapq.heappop(open_table)
            f, status, zero_index, step, operations = open_table.popleft()

            if status in vis or step > step_to_swap:
                continue
            else:
                vis.add(status)
                # heapq.heappush(close_table, (f, status, zero_index, step, operations))
                close_table.append((f, status, zero_index, step, operations))

            for dindex in dindexes[zero_index]:
                next_zero_index = zero_index + dindex
                next_status = swap_image(status, next_zero_index, zero_index)
                next_operations = operations + operation[dindex]

                # f = h(next_status, target_status)
                f = step + 1

                # heapq.heappush(open_table, (f, next_status, next_zero_index, step + 1, next_operations))
                open_table.append((f, next_status, next_zero_index, step + 1, next_operations))

        # traverse close_table
        open_table = []
        # close_table.sort(key=lambda x: x[0])
        for i in range(min(len(close_table), len(close_table))):
            f, status, zero_index, step, operations = close_table[i]
            if (step_to_swap - step) % 2 == 0:
                operations = operations + (operation[dindexes[zero_index][0]] + reverse_operation[
                    operation[dindexes[zero_index][0]]]) * ((step_to_swap - step) // 2)
                open_table.append((swap_image(status, force_swap[0], force_swap[1]), operations))

        operations_before_swap = ''
        min_operations = 'w' * 100
        free_swap = []
        # status: status aafter forced swap
        for status, operations in open_table:
            if answers.get(status[1:]):
                all_operations = operations + answers.get(status[1:])
                if len(all_operations) < len(min_operations):
                    operations_before_swap = operations
                    min_operations = all_operations
                    free_swap = []
            else:
                for i in range(1, 10):
                    for j in range(i + 1, 10):
                        all_operations = operations + answers.get(swap_image(status, i, j)[1:], 'w' * 100)
                        if len(all_operations) < len(min_operations):
                            operations_before_swap = operations
                            min_operations = all_operations
                            free_swap = [i, j]

        if min_operations == operations_before_swap:
            min_operations += ' '

        print("operations_before_swap:", operations_before_swap)
        print("all_operations:", min_operations)
        print("free_swap:", free_swap)
        return min_operations, free_swap

    def get_answer(self):
        return self.__answer

    def get_orign_status(self):
        return self.__img_status