from random import randint


# Creature
def create_creature(row=0, column=0):
    creature = {
        'row': row,
        'column': column,
        'facing': 'south',
        'nutrition': 5,
        'hp': 500,
        'moved': False,
        'color': (randint(0, 255), randint(0, 255), randint(0, 255)),
        'what_it_can_see': [
            ['o', 'o', 'o'],
            ['o', 'I', 'o'],
            ['o', 'o', 'o'],
        ]
    }
    return creature


def _ask_creature_where_to_move_to(creature):
    return ['up', 'down', 'left', 'right'][randint(0, 3)]


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
