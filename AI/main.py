from competition import *
import problem
import json
import time


uuids_to_challenge = ['e8aaf981-7ba1-4d36-b80e-a6a16debe587']
for uuid in uuids_to_challenge:
    q = problem.Problem()
    # test post challenge start
    print("test post challenge start")
    challenge = post_start(question_uuid=uuid)

    # print(challenge)
    challenge_uuid = challenge["uuid"]
    # print("\n")

    # test post submit answer
    # print("test post submit answer")
    q.load(chellenge_data=challenge["data"])
    answer = q.get_answer()
    # print("answer =", answer)
    r = post_submit(uuid=challenge_uuid, answer=answer)
    print(r)
    # print(challenge)
    print("\n")

print('\n')


print("test get rank")
r = get_rank()
for i in r:
    print(i)
print("\n")



print('ok')