from competition import *
import problem
import json
import time


# test get team list
print("test get team list")
r = get_list()
# uuids_to_challenge = []
uuids = [i['uuid'] for i in r if i['author'] != 24]
for challenge in r:
    print(challenge)
    # if challenge['author'] != 24:
        # uuids.append(challenge['uuid'])
print('\n')
# print(uuids_to_challenge)
print(len(r))

# # test get team problem
# unsolved_problems = []
# print("test get unsolved problem")
# r = get_problem(teamid=24)
# for i in r:
#     unsolved_problems.append(
#         {
#             'author': i['author'],
#             'uuid': i['uuid']
#         }
#     )
#
# for unsolved_problem in unsolved_problems:
#     print(unsolved_problem)
# print("\n")
#
# print('get uuids of unsolved problem')
# uuids_to_challenge = [unsolved_problem['uuid'] for unsolved_problem in unsolved_problems]
# for uuid in uuids_to_challenge:
#     print(uuid)
# print('\n')


# print("problems to challenge")
# problems_to_challenge = [
#     {
#         "author": 31,
#         "uuid": "d128fd23-4b6b-4468-a21a-a8e0e99e1283"
#     },
#     {
#         "author": 42,
#         "uuid": "11a76f71-6bd1-430a-ab79-659ee01920c4"
#     },
#     {
#         "author": 44,
#         "uuid": "83991982-14bc-4b6a-ae05-5a14da745ad3"
#     },
#     {
#         "author": 40,
#         "uuid": "46cfe765-5870-4fb4-87e8-9ee58439948d"
#     },
#     {
#         "author": 43,
#         "uuid": "08a7c467-f6f8-42e9-a3c2-0c54c015ee91"
#     },
#     {
#         "author": 18,
#         "uuid": "b5c3045c-63ad-4dae-b5ef-e91a5be9624a"
#     },
#     {
#         "author": 7,
#         "uuid": "52a69932-c4bd-42fe-bbc3-4298801a37aa"
#     },
# ]
# for problem_to_challenge in problems_to_challenge:
#     print(problem_to_challenge)
# print('\n')

uuids_to_challenge = []
for uuid in uuids:
    record = get_record(uuid)
    found = False
    for i in range(min(len(record), 6)):
        if record[i]['owner'] == 24:
            found = True
            break
    if not found:
        print(uuid)
        uuids_to_challenge.append(uuid)
    time.sleep(1)

print('\n')

# # test get question record
# print("test get question record")
# r = get_record(challenge_uuid='faffa1cf-b298-452b-b469-d48f8ddf57a0')
# # print(r)
# for i in r:
#     print(i)
# print('\n')

# uuids = ["710e4174-168a-4685-9ae6-533f1c55e08a"]
# uuids_to_challenge = ['e8aaf981-7ba1-4d36-b80e-a6a16debe587']
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


# # test get teamdetail
# print("test get teamdetail")
# r = get_teamdetail(40)
# print(r)
# print("\n")



print('ok')