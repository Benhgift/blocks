import pygame
from pygame.locals import *
from random import randint
import time


# Grid
def create_grid(width, height, colors):
    column = lambda: [colors['grey']() for _ in range(width)]
    rows = [column() for _ in range(height)]

    return rows


def move_to_pos(grid, row, column, creature, color_map):
    grid[row][column] = color_map['blue']()
    return grid


# Creature
def create_creature():
    creature = {
        'position': {'row': 0, 'column': 0}, 
        'facing': 'south',
    }
    return creature


def ask_creature_where_to_move_to(creature):
    return ['up', 'down', 'left', 'right'][randint(0, 3)]


def move_creature(creature, grid, color_map):
    #import pdb; pdb.set_trace()
    row = creature['position']['row']
    column = creature['position']['column']
    direction = ask_creature_where_to_move_to(creature)
    grid[row][column] = color_map['grey']()
    new_pos = [row, column]
    if row > 0 and direction == 'up':
        new_pos = [row-1, column]
    elif row < (len(grid) - 1) and direction == 'down':
        new_pos = [row+1, column]
    elif column > 0 and direction == 'left':
        new_pos = [row, column-1]
    elif column < (len(grid[0]) - 1) and direction == 'right':
        new_pos = [row, column+1]
    creature['position']['row'] = new_pos[0]
    creature['position']['column'] = new_pos[1]
    grid = move_to_pos(grid, new_pos[0], new_pos[1], creature, color_map)
    return grid


# App globals config
def create_config():
    return {
        'width': 8,
        'height': 8,
        'scale': 100
    }


def create_default_color_map():
    blue = lambda: (0, 128, 255)
    grey = lambda: (128, randint(90, 130), 128)
    return {'blue': blue, 'grey': grey}



def main_loop():
    app = App(create_config())

    color_map = create_default_color_map()
    grid = create_grid(app.width, app.height, color_map)
    creature = create_creature()
    app = handle_events(app)

    while app._running:
        render(app, grid)

        if not app._paused:
            grid = move_creature(creature, grid, color_map)

        if not app._running:
            pygame.quit()

        app = handle_events(app)
        time.sleep(.03)


# App
class App:
    def __init__(self, config = create_config()):
        _running = True
        _paused = False
        _display_surf = None
        width, height, scale = create_config().values()
        win_width = width * scale
        win_height = height * scale
        size = win_width, win_height
        pygame.init()
        _display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.__dict__.update(locals())


def render(app, grid):
    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            x = j * app.scale
            y = i * app.scale
            pygame.draw.rect(app._display_surf, color, pygame.Rect(x, y, app.scale-5, app.scale-5))
    pygame.display.flip()


def handle_events(app):
    for event in pygame.event.get():
        app = handle_key_press(app, event)
    return app


def handle_key_press(app, event):
    if event.type == pygame.QUIT:
        app._running = False
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            app._running = False

        if event.key == K_p:
            app._paused = not app._paused
    return app
