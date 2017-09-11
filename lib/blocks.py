import pygame
from pygame.locals import *
from random import randint
import time
import lib.creature as cre
import lib.gui_and_inputs as gui


# Grid
def create_grid(width, height, colors):
    column = lambda: [colors['grey']() for _ in range(width)]
    rows = [column() for _ in range(height)]
    return rows


def move_to_pos(grid, row, column, creature, color):
    grid[row][column] = color
    return grid


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
    direction = cre._ask_creature_where_to_move_to(creature)
    grid[row][column] = color_map['grey']()
    new_pos = _make_new_position_but_stay_in_bounds(row, column, direction, grid)
    if new_pos[0] != creature['row']:
        creature['moved'] = True
    creature['row'] = new_pos[0]
    creature['column'] = new_pos[1]
    grid = move_to_pos(grid, new_pos[0], new_pos[1], creature, creature['color'])
    return grid, creature


def _create_default_color_map():
    blue = lambda: (0, 128, 255)
    grey = lambda: (128, randint(90, 130), 128)
    yellow = lambda: (200, randint(0, 130), 255)
    return {'blue': blue, 'grey': grey, 'yellow': yellow}


def main_loop():
    app = gui.App()

    color_map = _create_default_color_map()
    grid = create_grid(app.width, app.height, color_map)
    creature = cre.create_creature()
    food_maker = lambda: cre.create_creature(randint(0, len(grid)-1), randint(0, len(grid[0])-1))
    foods_map = {}
    for x in range(len(grid)):
        food = food_maker()
        foods_map[(food['row'], food['column'])] = food

    for food in foods_map.values():
        grid = move_to_pos(grid, food['row'], food['column'], creature, color_map['yellow']())

    app = gui.handle_events(app)

    while app._running:
        gui.render(app, grid)

        if not app._paused:
            grid, creature = move_creature(creature, grid, color_map)
            creature, foods_map, new_food = cre.handle_eating(creature, foods_map)
            if new_food:
                food = food_maker()
                while (food['row'], food['column']) in foods_map:
                    food = food_maker()
                grid = move_to_pos(grid, food['row'], food['column'], creature, color_map['yellow']())
                foods_map[(food['row'], food['column'])] = food

            if creature['moved']:
                creature = cre.hurt_creature(creature)
            if creature['hp'] < 1:
                creature = cre.create_creature()

        if not app._running:
            pygame.quit()

        app = gui.handle_events(app)
        time.sleep(.1)
