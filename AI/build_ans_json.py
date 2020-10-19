import json
from collections import deque

queue = deque()
move = {
    -1:'d',
    +1:'a',
    -3:'s',
    +3:'w'
}
dindexes = {
    1:[+1, +3],
    2:[-1, +3, +1],
    3:[-1, +3],
    4:[-3, +1, +3],
    5:[-3, -1, +1, +3],
    6:[-3, -1, +3],
    7:[-3, +1],
    8:[-3, -1, +1],
    9:[-3, -1]
}


def bfs():
    while len(queue) != 0:
        status, zero_index, answer = queue.popleft()

        if ans.get(status) is None:
            ans.update({status:answer})
        else:
            continue

        # swap item
        # direction: int
        for dindex in dindexes[zero_index]:
            next_status = list(status)
            next_index = zero_index + dindex
            next_status[next_index], next_status[zero_index] = next_status[zero_index], next_status[next_index]
            next_answer = answer + move[dindex]
            t = (''.join(next_status), next_index, next_answer)
            queue.append(t)


if __name__ == '__main__':
    orign_status = 's123456789'
    for i in range(1,10):
        ans = {}
        status = list(orign_status)
        status[i] = '0'
        queue.append((''.join(status), i, ''))
        bfs()
        ans = {status[1:]:step[::-1] for status,step in ans.items()}

        with open(r'.\data\answer\ans' + str(i) + '.json', 'w') as file:
            json.dump(ans,file)
        print("i =",i)
        print(len(ans))
        print("ok!")
