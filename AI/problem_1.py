import requests
import heapq
import json
import img


class Problem:

    def __init__(self, url_to_get_problem: str, url_to_post_answer: str):
        self.__url_to_get_problem = url_to_get_problem
        self.__url_to_post_answer = url_to_post_answer

        self.__answers_dicts = []
        self.__answers_dicts.append({})
        for i in range(1, 10):
            with open(r'.\data\answer\ans' + str(i) + '.json', 'r') as answer_file:
                self.__answers_dicts.append(json.load(answer_file))

        self.__img = img.Img()

        # get problem from url-------------------------
        self.__problem_dict = requests.get(self.__url_to_get_problem).json()

        # self.__img = img.Img(b64str=self.__problem_dict['img'], path='./data/img/problem.png')
        # self.__img_status = self.__img.get_status()

        self.__img.load(b64str=self.__problem_dict['img'], path='./data/img/problem.png')
        self.__img_status = self.__img.get_status()

        self.__step = self.__problem_dict['step']
        self.__swap = self.__problem_dict['swap']
        self.__uuid = self.__problem_dict['uuid']
        self.__data_to_post = {
            "uuid": self.__uuid,
            "answer": {}
        }

        self.__caculate_ans()

    def __caculate_ans(self):
        status_type = 0
        for i in range(1, 10):
            if str(i) not in list(self.__img_status):
                status_type = i
                break

        operations = self.__answers_dicts[status_type].get(self.__img_status, 'w' * 100)

        if len(operations) <= self.__step:
            print("no forced swap")
            self.__data_to_post["answer"]["operations"] = operations
            self.__data_to_post["answer"]["swap"] = []
            print(self.__data_to_post)
        else:
            print("forced swap")
            self.__data_to_post["answer"]["operations"], self.__data_to_post["answer"]["swap"] = \
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
        close_list = []
        open_list = []
        step = 0
        f = h(orign_status, target_status)
        # f = step
        operations = ''
        status = orign_status
        heapq.heappush(open_list, (f, status, zero_index, step, operations))

        # search
        while open_list:
            f, status, zero_index, step, operations = heapq.heappop(open_list)
            if status in vis or step > step_to_swap:
                continue
            else:
                vis.add(status)
                heapq.heappush(close_list, (f, status, zero_index, step, operations))
            for dindex in dindexes[zero_index]:
                next_zero_index = zero_index + dindex
                next_status = swap_image(status, next_zero_index, zero_index)
                next_operations = operations + operation[dindex]

                f = h(next_status, target_status)
                # f = step + 1

                heapq.heappush(open_list, (f, next_status, next_zero_index, step + 1, next_operations))

        # traverse close_list
        open_list = []
        close_list.sort(key=lambda x: x[0])
        for i in range(min(len(close_list), len(close_list))):
            f, status, zero_index, step, operations = close_list[i]
            if (step_to_swap - step) % 2 == 0:
                operations = operations + (operation[dindexes[zero_index][0]] + reverse_operation[
                    operation[dindexes[zero_index][0]]]) * ((step_to_swap - step) // 2)
                open_list.append((swap_image(status, force_swap[0], force_swap[1]), operations))

        operations_before_swap = ''
        min_operations = 'w' * 100
        free_swap = []
        # status: status aafter forced swap
        for status, operations in open_list:
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
            min_operations += " "
        print("operations_before_swap:", operations_before_swap)
        print("all_operations:", min_operations)
        print("free_swap:", free_swap)
        return min_operations, free_swap

    def post_ans(self) -> dict:
        return requests.post(url=self.__url_to_post_answer, json=self.__data_to_post).json()
