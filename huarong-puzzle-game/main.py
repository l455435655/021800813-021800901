from huarong_puzele_game import *


def main():
    pygame.init()
    pygame.mixer.init()
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
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                    play(screen=screen, image_num=event.key - pygame.K_0)
                elif event.key in range(pygame.K_KP1, pygame.K_KP9 + 1):
                    play(screen=screen, image_num=event.key - pygame.K_KP0)

        screen.fill(BG_COLOR)
        # screen.blit(bg_image, (0, 0))
        display_game_menu(screen=screen, board=menu_board)
        pygame.display.flip()


if __name__ == '__main__':
    main()