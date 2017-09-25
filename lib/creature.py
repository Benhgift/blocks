import numpy as np
from random import randint
from itertools import chain


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


def _normalize_what_it_can_see(creature):
    seeable = chain.from_iterable(creature['what_it_can_see'])
    seeable = [x if x != 'I' else 1 for x in seeable]
    seeable = [x if x != 'o' else 2 for x in seeable]
    seeable = [x if x != '|' else 3 for x in seeable]
    seeable = [x if x != 'f' else 4 for x in seeable]
    print(seeable)
    return seeable


def _can_it_even_see_food(creature):
    seeable = chain.from_iterable(creature['what_it_can_see'])
    return 'f' in seeable


def _ask_creature_where_to_move_to(creature):
    #seeable = _normalize_what_it_can_see(creature)
    print(_can_it_even_see_food(creature))
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

