import pygame

pygame.init()

screen = pygame.display.set_mode((600, 500))


done = False

player_color = (150, 0, 150)
comp_color = (255, 255, 255)

player_paddle_width = 75
player_paddle_height = 20
player_x = 175
player_y = screen.get_height() - player_paddle_height

comp_width = 15
comp_height = 15
comp_x = 150
comp_y = 150

clock = pygame.time.Clock()

x_dir = True
y_dir = True

font = pygame.font.Font(None, 25)

strike_counter = 0


def draw_player(paddle_width=75, paddle_height=20):
    return pygame.draw.rect(screen,
            player_color,
            pygame.Rect(player_x,
                player_y,
                paddle_width,
                paddle_height))

def draw_ball(size=15):
    return pygame.draw.rect(screen,
            comp_color,
            pygame.Rect(comp_x,
                comp_y,
                size,
                size))

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_LEFT]
        and player_x > 0):
            player_x -= 5

        if (pressed[pygame.K_RIGHT]
        and player_x < screen.get_width()
                    - player_paddle_width):
            player_x += 5



        screen.fill((0, 0, 0))
        draw_player()
        draw_ball()

        paddle_x_zone = (player_x + 1,
                        player_x + player_paddle_width + 1)

        comp_in_zone = (comp_x > paddle_x_zone[0]
                        and comp_x < paddle_x_zone[1])

        comp_in_contact = (comp_in_zone
                        and comp_y == screen.get_height()
                                    - player_paddle_height
                                    - comp_height)
        comp_below_contact = (comp_y > screen.get_height()
                                        - player_paddle_height
                                        - comp_height)

        if (comp_in_zone
        and comp_in_contact):
            y_dir = not y_dir
            strike_counter += 1
        elif (comp_in_zone
        and comp_below_contact):
            print comp_x, comp_y
            x_dir = not x_dir

        text = font.render("Current Score: %d"%strike_counter,
                True,
                (0, 255,255))

        screen.blit(text,
        (screen.get_width() - (text.get_width() + 15), 15))

        if (x_dir
        and y_dir):
            comp_x += 5
            comp_y += 5
        elif (not x_dir
        and not y_dir):
            comp_x -= 5
            comp_y -= 5
        elif (x_dir
        and not y_dir):
            comp_x += 5
            comp_y -= 5
        elif (not x_dir
        and y_dir):
            comp_x -= 5
            comp_y += 5

        if comp_x >= screen.get_width() - 15:
            x_dir = not x_dir
        elif comp_x <= 0:
            x_dir = not x_dir

        if comp_y >= screen.get_height() - 15:
            y_dir = not y_dir
        elif comp_y <= 0:
            y_dir = not y_dir

        pygame.display.flip()
        clock.tick(60)
