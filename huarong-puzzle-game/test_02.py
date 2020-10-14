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

# FONT_FILE_PATH = './data/font/simhei.ttf'
FONT_FILE_PATH = './data/font/zhakukuaile2016.ttf'


def get_orign_status() -> str:
    answer_file_path = './data/answer/ans9.json'
    with open(answer_file_path, 'r') as answer_file:
        answer = json.load(answer_file)
    return random.choice(list(answer))

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

def load_images(image_num: int) -> list:
    images = []
    images.append(pygame.image.load('./data/image/white.jpg'))
    for i in range(1, 4):
        for j in range(1, 4):
            image_path = './data/image/' +  str(image_num) + str(i) + str(j) + '.jpg'
            images.append(pygame.image.load(image_path))
    return images

def load_answer() -> dict:
    answer_file_path = './data/answer/ans9.json'
    with open(answer_file_path, 'r') as answer_file:
        answer = json.load(answer_file)
    return answer

def swap_num(board: list, position_1: tuple, position_2: tuple):
    board[position_1[0]][position_1[1]]["num"], board[position_2[0]][position_2[1]]["num"] = \
        board[position_2[0]][position_2[1]]["num"], board[position_1[0]][position_1[1]]["num"]

def show_board_info(board: list):
    for i in range(1, 4):
        for j in range(1, 4):
            print(board[i][j], end=' ')
        print('')

def click_mouse(board, pos: tuple):
    for r in range(1, 4):
        for c in range(1, 4):
            if pos[0] in range(board[r][c]['position'][0], board[r][c]['position'][0] + CELL_WIDTH + 1) and \
                    pos[1] in range(board[r][c]['position'][1], board[r][c]['position'][1] + CELL_HEIGHT + 1):
                return (r, c)

def move_blank_image(board, pos: tuple) -> bool:
    if pos:
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

def move_blank_image_by_keyboard(board, operation) -> bool:
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

def is_win(board) -> bool:
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
                return (r, c)

def get_board_status(board) -> str:
    status = ''
    for r in range(1, 4):
        for c in range(1, 4):
            status += board[r][c]['num']
    return status

def display_images(screen, board: list, images: list):
    for r in range(1, 4):
        for c in range(1, 4):
            # if board[r][c]['num'] == '0':
            #     continue
            screen.blit(images[int(board[r][c]['num'])], board[r][c]['position'])

def display_game_info(screen, image_num, time_cost, step: int, tips_cnt: int):
    img = pygame.image.load('./data/image/' + str(image_num) + 's.jpg')
    my_font_1 = pygame.font.Font(FONT_FILE_PATH, 30)
    my_font_2 = pygame.font.Font(FONT_FILE_PATH, 20)

    time_surface = my_font_1.render('时间: %s' %(time.strftime("%M:%S", time.localtime(time_cost))), True, BLACK)
    step_surface = my_font_1.render('步数: %d' % (step), True, BLACK)
    tips_cnt_surface = my_font_1.render('提示: %d' % (tips_cnt), True, BLACK)

    help_info_surface_1 = my_font_2.render('鼠标或方向键移动白块', True, BLACK)
    help_info_surface_2 = my_font_2.render('   按<T>获取提示   ', True, BLACK)
    help_info_surface_3 = my_font_2.render('  按<ESC>重新开始  ', True, BLACK)

    screen.blit(img, (650, 50))
    screen.blit(time_surface, (675, 300))
    screen.blit(step_surface, (675, 350))
    screen.blit(tips_cnt_surface, (675, 400))
    screen.blit(help_info_surface_1, (650, 500))
    screen.blit(help_info_surface_2, (650, 525))
    screen.blit(help_info_surface_3, (650, 550))

def display_game_over(screen):
    my_font = pygame.font.Font(FONT_FILE_PATH, 100)
    win_surface = my_font.render('你赢啦', True, (121, 205, 205))
    screen.blit(win_surface, (150, 250))

def display_game_menu(screen, board):
    images = []
    images.append(pygame.image.load('./data/image/white.jpg'))
    for i in range(1, 10):
        image_path = './data/image/' + str(i) + "s.jpg"
        images.append(pygame.image.load(image_path))
    display_images(screen=screen, board=board, images=images)


    my_font = pygame.font.Font(FONT_FILE_PATH, 50)
    text_surface_1 = my_font.render('选择图片', True, BLACK)
    text_surface_2 = my_font.render('开始游戏', True, BLACK)
    screen.blit(text_surface_1, (650, 250))
    screen.blit(text_surface_2, (650, 350))

def play(screen, image_num: int):
    print("START NEW GAME!")
    board = init_board(status=get_orign_status())
    clock = pygame.time.Clock()
    images = load_images(image_num=image_num)
    bg_image = pygame.image.load('./data/image/background.jpg')
    answer = load_answer()

    print("orign_status:", get_board_status(board=board))

    step = 0
    tips_cnt = 0
    time_start = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("<QUIT>")
                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("<MOUSEBUTTONDOWN>")
                print(event.pos)
                if move_blank_image(board=board, pos=click_mouse(board=board, pos=event.pos)):
                    step += 1

            elif event.type == pygame.KEYDOWN:
                print('<KEYDOWN>')
                if event.key == pygame.K_ESCAPE:
                    return

                elif event.key == pygame.K_t:
                    print("<tips>")
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
            screen.fill(BG_COLOR)
            # screen.blit(bg_image, (0, 0))
            display_images(screen=screen, board=board, images=images)
            display_game_info(screen=screen, image_num=image_num, time_cost=time.time() - time_start, step=step, tips_cnt=tips_cnt)
            display_game_over(screen=screen)
            pygame.display.flip()
            time.sleep(2)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                        return


        screen.fill(BG_COLOR)
        # screen.blit(bg_image, (0, 0))
        display_images(screen=screen, board=board, images=images)
        display_game_info(screen=screen, image_num=image_num, time_cost=time.time() - time_start, step=step, tips_cnt=tips_cnt)
        ############################################################################################

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(TITLE)
    menu_board = init_board('123456789')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = click_mouse(board=menu_board, pos= event.pos)
                if pos:
                    play(screen=screen, image_num=(pos[0] - 1) * 3 + pos[1])

            elif event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    play(screen=screen, image_num=event.key - pygame.K_0)
                elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                    play(screen=screen, image_num=event.key - pygame.K_KP0)

        screen.fill(BG_COLOR)
        # screen.blit(bg_image, (0, 0))
        display_game_menu(screen=screen, board=menu_board)
        pygame.display.flip()
