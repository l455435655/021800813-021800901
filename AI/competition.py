import requests

url = "http://47.102.118.1:8089"
api_challenge_list = "/api/challenge/list"
api_challenge_record = "/api/challenge/record/"
api_challenge_create = "/api/challenge/create"
api_challenge_start ="/api/challenge/start/"
api_challenge_submit = "/api/challenge/submit"
api_rank = "/api/rank"
api_teamdetail = "/api/teamdetail/"
api_team_problem = "/api/team/problem/"

token = "334d857d-efa6-4087-bcb5-7a6eb1e62d6b"
my_teamid = 24



def get_list() -> list:
    return requests.get(url + api_challenge_list).json()

def get_record(challenge_uuid: str) -> list:
    return requests.get(url + api_challenge_record + challenge_uuid).json()

def post_create(question) -> dict:
    return requests.post(url=url + api_challenge_create, json=question).json()

def post_start(question_uuid: str) -> dict:
    data = {
        "teamid": my_teamid,
        "token": token
    }
    return requests.post(url=url + api_challenge_start + question_uuid, json=data).json()

def post_submit(uuid: str, answer: dict) -> dict:
    data = {
        "uuid": uuid,
        "teamid": my_teamid,
        "token": token,
        "answer": answer
    }
    return requests.post(url=url + api_challenge_submit, json=data).json()

def get_rank() -> list:
    return requests.get(url + api_rank).json()

def get_teamdetail(teamid: int) -> dict:
    return requests.get(url + api_teamdetail + str(teamid)).json()

def get_problem(teamid: int) -> list:
    return requests.get(url + api_team_problem + str(teamid)).json()