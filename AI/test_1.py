import problem_1

if __name__ == '__main__':
    total_time = 0.0
    for i in range(50):
        print("----------test_1 start----------")
        p = problem_1.Problem(url_to_get_problem="http://47.102.118.1:8089/api/problem?stuid=021800813",
                              url_to_post_answer="http://47.102.118.1:8089/api/answer")
        result = p.post_ans()
        total_time += result['time']
        # print("i =", i)
        print(result)
        print("----------test_1 end----------", end='\n\n')

    print("total_time =", total_time)
