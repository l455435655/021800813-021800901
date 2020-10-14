import sys
import pygame



def main():

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FPS = 10




    print("START!")

    #init pygame
    pygame.init()

    # pygame.key.set_repeat(300, 10)

    system_screen_info = pygame.display.Info()
    system_screen_size = system_width, system_height = system_screen_info.current_w, system_screen_info.current_h
    print('screen_size =', system_screen_size)

    screen_size = width, height =(900, 600)


    # background_image
    background_image_path = r'02.PNG'
    background_image = pygame.image.load(background_image_path)
    background_image_rect = background_image.get_rect()
    print(background_image_rect)

    my_clock = pygame.time.Clock()
    my_title = u"数字华容道 v0.1"
    my_screen = pygame.display.set_mode(size=screen_size, flags=pygame.RESIZABLE)
    my_screen.fill((255, 255, 255))
    pygame.display.set_caption(my_title)


    while True:
        for event in pygame.event.get():

            # if quit
            if event.type == pygame.QUIT:
                print("QUIT")
                sys.exit(0)

            # if resize
            elif event.type == pygame.RESIZABLE:
                print("RESIZE")
                pygame.display.set_mode(size=event.size, flags=pygame.RESIZABLE)

            elif event.type == pygame.MOUSEMOTION:
                print("MOUSEMOTION")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSEBUTTONDOWN")

            elif event.type == pygame.MOUSEBUTTONUP:
                print("MOUSEBUTTONUP")


            # if keydown
            elif event.type == pygame.KEYDOWN:
                print("KEYDOWN")

                if event.key == pygame.K_ESCAPE:
                    print("<ESCAPE>")
                    sys.exit(0)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    print("<UP>")
                    background_image_rect = background_image_rect.move(0, -10)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    print("<DOWN>")
                    background_image_rect = background_image_rect.move(0, +10)
                    print(background_image.get_rect())
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    print("<LEFT>")
                    background_image_rect = background_image_rect.move(-10, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    print("<RIGHT>")
                    background_image_rect = background_image_rect.move(+10, 0)
                elif event.key == pygame.K_KP_ENTER:
                    print("<ENTER>")





        my_screen.fill(WHITE)
        my_screen.blit(background_image, background_image_rect)

        # fresh screen
        pygame.display.flip()
        my_clock.tick(FPS)



if __name__ == "__main__":
    main()