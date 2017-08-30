from lib import blocks


def test_the_creation_of_a_grid():
    # A grid holds the colors of the squares

    # We need a map to return the color for the grid. It starts off grey so that's all we need. It's a function in case we want to randomize it for fun
    color_map = {'grey': lambda: (1, 128, 1)}

    assert(len(blocks.create_grid(3, 3, color_map)) == 3)


def test_move_a_creature_around():
    # create a creature and a grid and make it move around
    
    # a creature is just a position right now
    creature = blocks.create_creature()

    grid = blocks.create_grid(3, 3, _make_some_colors())

    # now move the creature a few times and see if it explodes
    for _ in range(10):
        blocks.move_creature(creature, grid, _make_some_colors())
    assert(creature)


def _make_some_colors():
    color_map = {'grey': lambda: (1, 128, 1), 'blue': lambda: (1, 1, 1)}
    return color_map
