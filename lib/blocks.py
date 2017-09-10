import pygame
from pygame.locals import *
from random import randint
import time


# Grid
def create_grid(width, height, colors):
    column = lambda: [colors['grey']() for _ in range(width)]
    rows = [column() for _ in range(height)]
    return rows


def move_to_pos(grid, row, column, creature, color):
    grid[row][column] = color
    return grid


# Creature
def create_creature(row=0, column=0):
    creature = {
        'row': row,
        'column': column,
        'facing': 'south',
        'nutrition': 5,
        'hp': 500,
        'moved': False,
        'color': (randint(0, 255), randint(0, 255), randint(0, 255))
    }
    return creature


def _ask_creature_where_to_move_to(creature):
    return ['up', 'down', 'left', 'right'][randint(0, 3)]


def _make_new_position_but_stay_in_bounds(row, column, direction, grid):
    new_pos = [row, column]
    if row > 0 and direction == 'up':
        new_pos = [row-1, column]
    elif row < (len(grid) - 1) and direction == 'down':
        new_pos = [row+1, column]
    elif column > 0 and direction == 'left':
        new_pos = [row, column-1]
    elif column < (len(grid[0]) - 1) and direction == 'right':
        new_pos = [row, column+1]
    return new_pos


def move_creature(creature, grid, color_map):
    row = creature['row']
    column = creature['column']
    direction = _ask_creature_where_to_move_to(creature)
    grid[row][column] = color_map['grey']()
    new_pos = _make_new_position_but_stay_in_bounds(row, column, direction, grid)
    if new_pos[0] != creature['row']:
        creature['moved'] = True
    creature['row'] = new_pos[0]
    creature['column'] = new_pos[1]
    grid = move_to_pos(grid, new_pos[0], new_pos[1], creature, creature['color'])
    return grid, creature


# App globals config
def create_config():
    return {
        'width': 8,
        'height': 8,
        'scale': 100
    }


def _create_default_color_map():
    blue = lambda: (0, 128, 255)
    grey = lambda: (128, randint(90, 130), 128)
    yellow = lambda: (200, randint(0, 130), 255)
    return {'blue': blue, 'grey': grey, 'yellow': yellow}


def hurt_creature(creature):
    creature['hp'] -= 5
    if creature['moved']:
        creature['hp'] -= 10
        creature['moved'] = False
    return creature


def handle_eating(creature, foods_map):
    pos = (creature['row'], creature['column'])
    new_food = False
    if pos in foods_map:
        del foods_map[pos]
        creature['hp'] += 50
        new_food = True
    return creature, foods_map, new_food


def main_loop():
    app = App(create_config())

    color_map = _create_default_color_map()
    grid = create_grid(app.width, app.height, color_map)
    creature = create_creature()
    food_maker = lambda: create_creature(randint(0, len(grid)-1), randint(0, len(grid[0])-1))
    foods_map = {}
    for x in range(len(grid)):
        food = food_maker()
        foods_map[(food['row'], food['column'])] = food

    for food in foods_map.values():
        grid = move_to_pos(grid, food['row'], food['column'], creature, color_map['yellow']())

    app = handle_events(app)

    while app._running:
        render(app, grid)

        if not app._paused:
            grid, creature = move_creature(creature, grid, color_map)
            creature, foods_map, new_food = handle_eating(creature, foods_map)
            if new_food:
                food = food_maker()
                while (food['row'], food['column']) in foods_map:
                    food = food_maker()
                grid = move_to_pos(grid, food['row'], food['column'], creature, color_map['yellow']())
                foods_map[(food['row'], food['column'])] = food

            if creature['moved']:
                creature = hurt_creature(creature)
            if creature['hp'] < 1:
                creature = create_creature()

        if not app._running:
            pygame.quit()

        app = handle_events(app)
        time.sleep(.1)


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
