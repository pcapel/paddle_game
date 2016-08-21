import pygame

pygame.init()

right_edge = 600
left_edge = 0
bottom_edge = 500
top_edge = 0
screen = pygame.display.set_mode((right_edge, bottom_edge))

done = False

player_color = (150, 0, 150)
comp_color = (255, 255, 255)

player_paddle_width = 75
player_paddle_height = 20
player_x = 175
player_y = bottom_edge - player_paddle_height

comp_width = 15
comp_height = 15
comp_x = 150
comp_y = 150

clock = pygame.time.Clock()

x_dir = True
y_dir = True

paddle_strike = True

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        pressed = pygame.key.get_pressed()

        if (pressed[pygame.K_LEFT]
        and player_x > left_edge):
            player_x -= 5

        if (pressed[pygame.K_RIGHT]
        and player_x < right_edge
                    - player_paddle_width):
            player_x += 5

        screen.fill((0, 0, 0))
        #player rect
        pygame.draw.rect(screen,
        player_color,
        pygame.Rect(player_x,
            player_y,
            player_paddle_width,
            player_paddle_height))
        #comp rect
        pygame.draw.rect(screen,
        comp_color,
        pygame.Rect(comp_x,
            comp_y,
            comp_width,
            comp_height))

        paddle_x_zone = (player_x,
                        player_x + player_paddle_width)

        comp_in_zone = (comp_x > paddle_x_zone[0]
                        and comp_x < paddle_x_zone[1])

        comp_in_contact = (comp_in_zone
                        and comp_y == bottom_edge
                                    - player_paddle_height
                                    - comp_height)

        if (comp_in_zone
        and comp_in_contact):
            y_dir = not y_dir

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

        if comp_x >= right_edge - 15:
            x_dir = not x_dir
        elif comp_x <= left_edge:
            x_dir = not x_dir

        if comp_y >= bottom_edge - 15:
            y_dir = not y_dir
        elif comp_y <= top_edge:
            y_dir = not y_dir

        pygame.display.flip()
        clock.tick(60)
