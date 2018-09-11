from src.input_box import InputBox
import src.const as CONST
import src.data_harvest as data_harvest
import pygame

class GameMenu():
    def __init__(self):

        pygame.mixer.init()
        pygame.mixer.music.load('sounds/back4.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)


        background = pygame.image.load("img/menu.jpg")

        screen = pygame.display.set_mode((CONST.DISPLAY_SIZE_X, CONST.DISPLAY_SIZE_Y), pygame.FULLSCREEN)
        COLOR_INACTIVE = pygame.Color('lightskyblue3')
        COLOR_ACTIVE = pygame.Color('dodgerblue2')
        FONT = pygame.font.SysFont('Comic Sans MS', 45)
        clock = pygame.time.Clock()
        input_box = InputBox(400, 600, 140, 32)

        done = False

        while not done:

            for event in pygame.event.get():
                # pega as teclas pressionadas
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_ESCAPE]:
                    quit(0)
                if pressed[pygame.K_RETURN]:
                    data_harvest.player_name = input_box.text
                    done = True

                if event.type == pygame.QUIT:
                    quit(0)
                    done = True
                input_box.handle_event(event)

            input_box.update()

            screen.fill((0, 0, 0))
            screen.blit(background,(0,70))
            input_box.draw(screen)

            pygame.display.flip()
            clock.tick(60)


