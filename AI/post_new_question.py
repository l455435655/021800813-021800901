# test post new question
from competition import *


print("test post new question")

question = {
    "teamid": my_teamid,
    "data": {
        "letter": "X",
        "exclude": 9,
        "challenge": [
            [3, 6, 7],
            [2, 5, 4],
            [8, 1, 0]
        ],
        "step": 20,
        "swap": [4, 9]
    },
    "token": token
}

r = post_create(question)
print(r)
