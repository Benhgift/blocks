import pygame
from pygame.locals import *


# App globals config
def create_config():
    return {
        'width': 8,
        'height': 8,
        'scale': 100
    }


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
        pygame.display.set_caption('■ BLOCKS ■')
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
