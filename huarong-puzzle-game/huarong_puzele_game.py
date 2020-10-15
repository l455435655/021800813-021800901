import pygame
import sys
import json
import random
import time

BG_COLOR = (245, 222, 179)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 10

SCREEN_SIZE = (900, 600)

CELL_WIDTH = 200
CELL_HEIGHT = 200
TITLE = "华容道 v0.1"

FONT_FILE_PATH_0 = './data/font/zhakukuaile2016.ttf'
FONT_FILE_PATH_1 = './data/font/simhei.ttf'


def get_orign_status(mode: int) -> str:
    ranges = [
        (0, 181439),
        (50, 1000),
        (1001, 10000),
        (10001, 181439)
    ]
    answer_file_path = './data/answer/ans9.json'
    with open(answer_file_path, 'r') as answer_file:
        answer = json.load(answer_file)
    return list(answer)[random.randint(ranges[mode][0], ranges[mode][1])]


def init_board(status: str) -> list:
    board = [
        [{}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}]
    ]
    for r in range(1, 4):
        for c in range(1, 4):
            index = (r - 1) * 3 + c
            board[r][c].update({'num': status[index - 1], 'position': ((c - 1) * CELL_WIDTH, (r - 1) * CELL_HEIGHT)})
    return board


def load_images(image_type: int, image_num: int) -> list:
    images = [pygame.image.load('./data/image/white.jpg')]
    for i in range(1, 4):
        for j in range(1, 4):
            image_path = './data/image/{0}/{1}{2}{3}.jpg'.format(image_type, image_num, i, j)
            images.append(pygame.image.load(image_path))
    return images


def load_answer() -> dict:
    answer_file_path = './data/answer/ans9.json'
    with open(answer_file_path, 'r') as answer_file:
        answer = json.load(answer_file)
    return answer


def swap_num(board: list, position_1: tuple, position_2: tuple):
    move_sound = pygame.mixer.Sound('./data/sound/move_1.wav')
    move_sound.play()
    board[position_1[0]][position_1[1]]["num"], board[position_2[0]][position_2[1]]["num"] = \
        board[position_2[0]][position_2[1]]["num"], board[position_1[0]][position_1[1]]["num"]


def show_board_info(board: list):
    for i in range(1, 4):
        for j in range(1, 4):
            print(board[i][j], end=' ')
        print('')


def is_click_image(board: list, pos: tuple):
    for r in range(1, 4):
        for c in range(1, 4):
            if pos[0] in range(board[r][c]['position'][0], board[r][c]['position'][0] + CELL_WIDTH + 1) and \
                    pos[1] in range(board[r][c]['position'][1], board[r][c]['position'][1] + CELL_HEIGHT + 1):
                return (r, c)


def move_blank_image(board: list, pos: tuple) -> bool:
    d = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    for dr, dc in d:
        r = pos[0] + dr
        c = pos[1] + dc
        if board[r][c].get('num') == '0':
            swap_num(board=board, position_1=pos, position_2=(r, c))
            return True
    return False


def move_blank_image_by_keyboard(board: list, operation) -> bool:
    white_image_pos = get_white_image_pos(board=board)
    if operation == 'w':
        if white_image_pos[0] - 1 in range(1, 4):
            swap_num(board=board,
                     position_1=white_image_pos,
                     position_2=(white_image_pos[0] - 1, white_image_pos[1]))
            return True

    elif operation == 's':
        if white_image_pos[0] + 1 in range(1, 4):
            swap_num(board=board,
                     position_1=white_image_pos,
                     position_2=(white_image_pos[0] + 1, white_image_pos[1]))
            return True

    elif operation == 'a':
        if white_image_pos[1] - 1 in range(1, 4):
            swap_num(board=board,
                     position_1=white_image_pos,
                     position_2=(white_image_pos[0], white_image_pos[1] - 1))
            return True

    elif operation == 'd':
        if white_image_pos[1] + 1 in range(1, 4):
            swap_num(board=board,
                     position_1=white_image_pos,
                     position_2=(white_image_pos[0], white_image_pos[1] + 1))
            return True
    return False


def is_click_chose_difficulty(pos: tuple) -> bool:
    if pos[0] in range(650, 650 + 202) and pos[1] in range(400, 400 + 31):
        return True
    else:
        return False


def is_click_top5(pos: tuple) -> bool:
    if pos[0] in range(675, 675 + 150) and pos[1] in range(475, 475 + 31):
        return True
    else:
        return False


####
def is_click_back_to_menu(pos: tuple) -> bool:
    if pos[0] in range(635, 635 + 100) and pos[1] in range(485, 485 + 26):
        return True
    else:
        return False


def is_click_get_hint(pos: tuple) -> bool:
    if pos[0] in range(765, 765 + 100) and pos[1] in range(485, 485 + 26):
        return True
    else:
        return False


def is_click_disrupt(pos: tuple) -> bool:
    if pos[0] in range(635, 635 + 100) and pos[1] in range(525, 525 + 26):
        return True
    else:
        return False


def is_click_restart(pos: tuple) -> bool:
    if pos[0] in range(765, 765 + 100) and pos[1] in range(525, 525 + 26):
        return True
    else:
        return False


def is_win(board: list) -> bool:
    for i in range(1, 9):
        r = (i - 1) // 3 + 1
        c = (i - 1) % 3 + 1
        if board[r][c]['num'] != str(i):
            return False
    return True


def get_white_image_pos(board: list) -> tuple:
    for r in range(1, 4):
        for c in range(1, 4):
            if board[r][c]['num'] == '0':
                return r, c


def get_board_status(board: list) -> str:
    status = ''
    for r in range(1, 4):
        for c in range(1, 4):
            status += board[r][c]['num']
    return status


def record_game_history(game_mode: int, time_cost: float, step: int, tips_cnt: int):
    history = {
        'time': time_cost,
        'step': step,
        'tips_cnt': tips_cnt
    }

    with open('./data/history/{0}.json'.format(game_mode), 'r') as history_file:
        histories = json.load(history_file)

    histories.append(history)
    histories.sort(key=lambda x: (x['tips_cnt'], x['step'], x['time']))

    with open('./data/history/{0}.json'.format(game_mode), 'w') as history_file:
        json.dump(histories, history_file)


def load_game_history(game_mode: int) -> list:
    with open('./data/history/{0}.json'.format(game_mode), 'r') as history_file:
        histories = json.load(history_file)
    return histories


def blit_images(screen, board: list, images: list):
    for r in range(1, 4):
        for c in range(1, 4):
            screen.blit(images[int(board[r][c]['num'])], board[r][c]['position'])


def blit_game_info(screen, image, time_cost: float, step: int, tips_cnt: int):
    screen.blit(image, (650, 50))

    my_font_1 = pygame.font.Font(FONT_FILE_PATH_0, 30)
    time_surface = my_font_1.render('时间: {0}'.format(time.strftime("%M:%S", time.localtime(time_cost))), True, BLACK)
    step_surface = my_font_1.render('步数: %d' % step, True, BLACK)
    tips_cnt_surface = my_font_1.render('提示: %d' % tips_cnt, True, BLACK)
    screen.blit(time_surface, (675, 300))
    screen.blit(step_surface, (675, 350))
    screen.blit(tips_cnt_surface, (675, 400))

    # my_font_2 = pygame.font.Font(FONT_FILE_PATH_0, 20)
    # help_info_surface_1 = my_font_2.render('鼠标或方向键移动白块', True, BLACK)
    # help_info_surface_2 = my_font_2.render('   按<T>获取提示   ', True, BLACK)
    # help_info_surface_3 = my_font_2.render('  按<ESC>重新开始  ', True, BLACK)
    # screen.blit(help_info_surface_1, (650, 500))
    # screen.blit(help_info_surface_2, (650, 525))
    # screen.blit(help_info_surface_3, (650, 550))

    my_font_3 = pygame.font.Font(FONT_FILE_PATH_0, 25)

    button_surface_1 = my_font_3.render('返回菜单', True, BLACK)
    screen.blit(button_surface_1, (635, 485))

    button_surface_2 = my_font_3.render('获取提示', True, BLACK)
    screen.blit(button_surface_2, (765, 485))

    button_surface_3 = my_font_3.render('重新打乱', True, BLACK)
    screen.blit(button_surface_3, (635, 525))

    button_surface_4 = my_font_3.render('重新开始', True, BLACK)
    screen.blit(button_surface_4, (765, 525))


def blit_game_over(screen):
    my_font = pygame.font.Font(FONT_FILE_PATH_0, 100)
    win_surface = my_font.render('你赢啦', True, (121, 205, 205))
    screen.blit(win_surface, (150, 250))


def blit_game_menu(screen, menu_board: list, game_mode: int):
    images = [pygame.image.load('./data/image/white.jpg')]
    for i in range(1, 10):
        image_path = './data/image/{0}/{1}s.jpg'.format(game_mode, i)
        images.append(pygame.image.load(image_path))
    blit_images(screen=screen, board=menu_board, images=images)

    my_font_1 = pygame.font.Font(FONT_FILE_PATH_0, 50)
    text_surface_1 = my_font_1.render('点击图片', True, BLACK)
    text_surface_2 = my_font_1.render('开始游戏', True, BLACK)
    screen.blit(text_surface_1, (650, 125))
    screen.blit(text_surface_2, (650, 225))

    modes = [
        '随机',
        '简单',
        '普通',
        '困难'
    ]
    my_font_2 = pygame.font.Font(FONT_FILE_PATH_0, 30)
    text_surface_3 = my_font_2.render('切换难度: ' + modes[game_mode], True, BLACK)
    text_surface_4 = my_font_2.render('查看排行榜', True, BLACK)
    screen.blit(text_surface_3, (650, 400))
    screen.blit(text_surface_4, (675, 475))


def blit_top5(screen, game_mode: int, histories: list):
    my_font_1 = pygame.font.Font(FONT_FILE_PATH_0, 80)
    text_surface_0 = my_font_1.render('排', True, BLACK)
    text_surface_1 = my_font_1.render('行', True, BLACK)
    text_surface_2 = my_font_1.render('榜', True, BLACK)
    screen.blit(text_surface_0, (715, 50))
    screen.blit(text_surface_1, (715, 150))
    screen.blit(text_surface_2, (715, 250))

    modes = [
        '随机',
        '简单',
        '普通',
        '困难'
    ]
    my_font_2 = pygame.font.Font(FONT_FILE_PATH_0, 30)
    text_surface_3 = my_font_2.render('切换难度: ' + modes[game_mode], True, BLACK)
    text_surface_4 = my_font_2.render('关闭排行榜', True, BLACK)
    screen.blit(text_surface_3, (650, 400))
    screen.blit(text_surface_4, (675, 475))

    my_font_3 = pygame.font.Font(FONT_FILE_PATH_0, 30)
    my_font_4 = pygame.font.Font(FONT_FILE_PATH_0, 50)

    text_surface_5 = my_font_4.render('TOP 5', True, BLACK)
    screen.blit(text_surface_5, (250, 30))

    for i in range(min(5, len(histories))):
        step = histories[i]['step']
        time_cost = time.strftime("%M:%S", time.localtime(histories[i]['time']))
        tips_cnt = histories[i]['tips_cnt']
        game_info_surface = my_font_3.render('步数: {0}  时间: {1}  提示: {2}'.format(step, time_cost, tips_cnt),
                                             True, BLACK)

        screen.blit(game_info_surface, (100, i * 90 + 120))


def press_key_to_continue():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return


def ready(screen, image_type: int, image_num: int):
    image = pygame.image.load('./data/image/{0}/{1}.jpg'.format(image_type, image_num))

    my_font = pygame.font.Font(FONT_FILE_PATH_0, 150)
    text_color = BLACK
    text_bgcolor = WHITE
    text_pos_1 = (230, 225)
    text_pos_2 = (200, 200)

    three_surface = my_font.render('3', True, text_color)
    screen.blit(image, (0, 0))
    screen.blit(three_surface, text_pos_1)
    pygame.display.flip()
    time.sleep(1)

    two_surface = my_font.render('2', True, text_color)
    screen.blit(image, (0, 0))
    screen.blit(two_surface, text_pos_1)
    pygame.display.flip()
    time.sleep(1)

    one_surface = my_font.render('1', True, text_color)
    screen.blit(image, (0, 0))
    screen.blit(one_surface, text_pos_1)
    pygame.display.flip()
    time.sleep(1)

    start_surface = my_font.render('开始', True, text_color)
    screen.blit(image, (0, 0))
    screen.blit(start_surface, text_pos_2)
    pygame.display.flip()
    start_sound = pygame.mixer.Sound('./data/sound/start.wav')
    start_sound.play()
    time.sleep(1)


def display_top5(screen):
    histories = [[], [], [], []]
    for i in range(1, 4):
        histories[i] = load_game_history(game_mode=i)

    game_mode = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_click_top5(event.pos):
                    chose_difficulty_sound = pygame.mixer.Sound('./data/sound/move_0.wav')
                    chose_difficulty_sound.play()
                    return
                elif is_click_chose_difficulty(event.pos):
                    chose_difficulty_sound = pygame.mixer.Sound('./data/sound/move_0.wav')
                    chose_difficulty_sound.play()
                    game_mode += 1
                    game_mode = (game_mode - 1) % 3 + 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        screen.fill(BG_COLOR)
        blit_top5(screen=screen, game_mode=game_mode, histories=histories[game_mode])
        pygame.display.flip()


def play(screen, game_mode: int, image_num: int):
    clock = pygame.time.Clock()
    target_image = pygame.image.load('./data/image/{0}/{1}s.jpg'.format(game_mode, image_num))
    images = load_images(image_type=game_mode, image_num=image_num)
    answer = load_answer()
    orign_status = get_orign_status(mode=game_mode)


    while True:
        print("START NEW GAME!")

        # bg_image = pygame.image.load('./data/image/background.jpg')

        board = init_board(status=orign_status)
        print("orign_status:", get_board_status(board=board))

        start_sound = pygame.mixer.Sound('./data/sound/start.wav')
        start_sound.play()

        step = 0
        tips_cnt = 0
        time_start = time.time()
        restart = False


        # ready(screen=screen, image_type=game_mode, image_num=image_num)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("<MOUSEBUTTONDOWN>")
                    print(event.pos)

                    image_position = is_click_image(board=board, pos=event.pos)
                    if image_position:
                        if move_blank_image(board=board, pos=image_position):
                            step += 1

                    elif is_click_back_to_menu(pos=event.pos):
                        return

                    elif is_click_get_hint(pos=event.pos):
                        move_blank_image_by_keyboard(board=board, operation=answer[get_board_status(board=board)][0])
                        tips_cnt += 1
                        step += 1

                    elif is_click_disrupt(pos=event.pos):
                        orign_status = get_orign_status(mode=game_mode)
                        restart = True

                    elif is_click_restart(pos=event.pos):
                        restart = True


                elif event.type == pygame.KEYDOWN:
                    print('<KEYDOWN>')
                    if event.key == pygame.K_ESCAPE:
                        return

                    elif event.key == pygame.K_t:
                        print("<T>")
                        move_blank_image_by_keyboard(board=board, operation=answer[get_board_status(board=board)][0])
                        tips_cnt += 1
                        step += 1
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        if move_blank_image_by_keyboard(board=board, operation='w'):
                            step += 1
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        if move_blank_image_by_keyboard(board=board, operation='s'):
                            step += 1
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        if move_blank_image_by_keyboard(board=board, operation='a'):
                            step += 1
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        if move_blank_image_by_keyboard(board=board, operation='d'):
                            step += 1

            if is_win(board=board):
                win_sound = pygame.mixer.Sound('./data/sound/win.wav')
                win_sound.play()
                record_game_history(game_mode=game_mode, time_cost=time.time() - time_start, step=step, tips_cnt=tips_cnt)

                screen.fill(BG_COLOR)
                # screen.blit(bg_image, (0, 0))
                blit_images(screen=screen, board=board, images=images)
                blit_game_info(screen=screen, image=target_image, time_cost=time.time() - time_start,
                               step=step, tips_cnt=tips_cnt)
                blit_game_over(screen=screen)
                pygame.display.flip()

                time.sleep(2)
                press_key_to_continue()
                restart = True



            screen.fill(BG_COLOR)
            # screen.blit(bg_image, (0, 0))
            blit_images(screen=screen, board=board, images=images)
            blit_game_info(screen=screen, image=target_image, time_cost=time.time() - time_start,
                           step=step, tips_cnt=tips_cnt)


            pygame.display.flip()
            clock.tick(FPS)

            if restart:
                break


def run():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)

    menu_board = init_board('123456789')
    game_mode = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_click_chose_difficulty(pos=event.pos):
                    click_button_sound = pygame.mixer.Sound('./data/sound/move_0.wav')
                    click_button_sound.play()
                    game_mode += 1
                    game_mode = (game_mode - 1) % 3 + 1
                elif is_click_top5(pos=event.pos):
                    click_button_sound = pygame.mixer.Sound('./data/sound/move_0.wav')
                    click_button_sound.play()
                    display_top5(screen=screen)
                else:
                    image_position = is_click_image(board=menu_board, pos=event.pos)
                    if image_position:
                        play(screen=screen, game_mode=game_mode,
                             image_num=(image_position[0] - 1) * 3 + image_position[1])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    play(screen=screen, game_mode=game_mode, image_num=event.key - pygame.K_0)
                elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                    play(screen=screen, game_mode=game_mode, image_num=event.key - pygame.K_KP0)

        screen.fill(BG_COLOR)
        # screen.blit(bg_image, (0, 0))
        blit_game_menu(screen=screen, menu_board=menu_board, game_mode=game_mode)
        pygame.display.flip()
