from lib import blocks
from lib import creature as cre


def test_the_creation_of_a_grid():
    # A grid holds the colors of the squares

    # We need a map to return the color for the grid. It starts off grey so that's all we need. It's a function in case we want to randomize it for fun
    color_map = {'grey': lambda: (1, 128, 1)}

    assert(len(blocks.create_grid(3, 3, color_map)) == 3)


def test_move_a_creature_around():
    # create a creature and a grid and make it move around

    # a creature is just a position right now
    creature = cre.create_creature()

    grid = blocks.create_grid(3, 3, _make_some_colors())

    # now move the creature a few times and see if it explodes
    for _ in range(10):
        grid, creature = blocks.move_creature(creature, grid, _make_some_colors())
    assert(creature)


def test_creature_moving_onto_food_heals(monkeypatch):
    creature = cre.create_creature()
    color_map = _make_some_colors()
    grid = blocks.create_grid(3, 3, _make_some_colors())
    food = cre.create_creature(0, 1)
    foods_map = {(0, 1): food}

    # put the food on the grid
    grid = blocks.set_food_onto_grid(grid, foods_map, color_map)

    # make the creature move to the right, where we put the food
    def move_right(creature):
        return 'right'
    monkeypatch.setattr(cre, '_ask_creature_where_to_move_to', move_right)

    grid, creature = blocks.move_creature(creature, grid, _make_some_colors())

    # eat
    creature, foods_map, new_food = cre.handle_eating(creature, foods_map)
    assert(creature['hp'] == 550)


def _make_some_colors():
    color_map = {
        'yellow': lambda: (1, 1, 1),
        'grey': lambda: (1, 128, 1),
        'blue': lambda: (1, 1, 1)
    }
    return color_map
