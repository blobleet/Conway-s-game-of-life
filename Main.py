import pygame
from pygame.locals import *

pygame.init()

# ==== COLORS ====
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

unit_size = 20
width, height = screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game of Life")
running = True
game_started = False
main_clock = pygame.time.Clock()
live_spots = []
new_live_spots = []


def get_adjacent(pos):
    posx, posy = pos[0], pos[1]
    adj_pos = [(posx, posy - unit_size), (posx + unit_size, posy - unit_size), (posx + unit_size, posy),
               (posx + unit_size, posy + unit_size), (posx, posy + unit_size), (posx - unit_size, posy + unit_size),
               (posx - unit_size, posy), (posx - unit_size, posy - unit_size)]
    return adj_pos


def events():
    global game_started
    global live_spots
    global unit_size

    if not game_started:
        mouse_pos = pygame.mouse.get_pos()
        mouse_posx, mouse_posy = (int(mouse_pos[0] / unit_size) * unit_size,
                                  int(mouse_pos[1] / unit_size) * unit_size)
        mouse_pos = (mouse_posx, mouse_posy)

        if pygame.mouse.get_pressed(3)[0]:
            if mouse_pos not in live_spots:
                # print(mouse_pos)
                live_spots.append((mouse_posx, mouse_posy))
        elif pygame.mouse.get_pressed(3)[2]:
            if mouse_pos in live_spots:
                live_spots.remove(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = not game_started
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                unit_size += 1
            elif event.button == 5:
                unit_size -= 1


def update():
    global game_started
    global live_spots
    global new_live_spots

    if game_started:
        new_live_spots = live_spots.copy()
        for x in range(-100, width+100 + 1, unit_size):
            for y in range(-100, height+100 + 1, unit_size):
                curr_posx, curr_posy = curr_pos = (x, y)
                adjacent_pos = get_adjacent(curr_pos)
                live_cnt = 0

                for pos in adjacent_pos:  # Go through all adjacent positions and see how many are alive
                    if pos in live_spots:
                        live_cnt += 1

                if curr_pos in live_spots:
                    if live_cnt < 2:
                        new_live_spots.remove(curr_pos)
                    elif live_cnt > 3:
                        new_live_spots.remove(curr_pos)
                else:
                    if live_cnt == 3:
                        new_live_spots.append(curr_pos)
        live_spots = new_live_spots
        new_live_spots = None


def render():
    screen.fill(BLACK)
    pause_info = None
    if game_started:
        pause_info = pygame.font.SysFont("arial", 22).render("Running..", True, WHITE)
        screen.blit(pause_info, (10, 10))
    else:
        pause_info = pygame.font.SysFont("arial", 22).render("Paused..", True, WHITE)
        screen.blit(pause_info, (10, 10))
    for pos in live_spots:
        pygame.draw.rect(screen, WHITE, (pos, (unit_size, unit_size)))


while running:
    main_clock.tick(20)
    events()
    update()
    render()
    pygame.display.update()
