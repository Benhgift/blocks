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
    creature = {'position': {'row': 0, 'column': 0}}
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


# App
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.width = 4
        self.height = 4
        self.scale = 100
        self.win_width = self.width * self.scale
        self.win_height = self.height * self.scale
        self.size = self.win_width, self.win_height
        rand_color = lambda: randint(0, 255)
        blue = lambda: (0, 128, 255)
        grey = lambda: (randint(100, 120), 128, 128)
        self.color_map = {'blue': blue, 'grey': grey}
        self.grid = create_grid(self.width, self.height, self.color_map)
        self.creature = create_creature()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._paused = False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        self.handle_key_press(event)

    def on_loop(self):
        pass

    def on_render(self):
        scale_for_box = lambda x: int(self.scale / len(x))
        width = scale_for_box(self.grid[0])
        height = scale_for_box(self.grid)
        for i, row in enumerate(self.grid):
            for j, color in enumerate(row):
                x = j * self.scale
                y = i * self.scale
                pygame.draw.rect(self._display_surf, color, pygame.Rect(x, y, self.scale-5, self.scale-5))
        pygame.display.flip()

        if not self._paused:
            self.grid = move_creature(self.creature, self.grid, self.color_map)
        time.sleep(.1)

    def handle_key_press(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._running = False

            if event.key == K_p:
                self._paused = not self._paused

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init():
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
