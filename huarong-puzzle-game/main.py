from huarong_puzele_game import *


def main():
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
                if click_chose_difficulty(pos=event.pos):
                    chose_difficulty_sound = pygame.mixer.Sound('./data/sound/move_0.wav')
                    chose_difficulty_sound.play()
                    game_mode += 1
                    game_mode = (game_mode - 1) % 3 + 1
                else:
                    pos = click_mouse(board=menu_board, pos=event.pos)
                    if pos:
                        play(screen=screen, game_mode=game_mode, image_num=(pos[0] - 1) * 3 + pos[1])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    play(screen=screen, game_mode=game_mode, image_num=event.key - pygame.K_0)
                elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                    play(screen=screen, game_mode=game_mode, image_num=event.key - pygame.K_KP0)

        screen.fill(BG_COLOR)
        # screen.blit(bg_image, (0, 0))
        display_game_menu(screen=screen, menu_board=menu_board, game_mode=game_mode)
        pygame.display.flip()


if __name__ == '__main__':
    main()
