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
        'brain': Neural_Network(),
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



# X = (hours studying, hours sleeping), y = score on test, xPredicted = 4 hours studying & 8 hours sleeping (input data for prediction)
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
xPredicted = np.array(([4,8]), dtype=float)

# scale units
X = X/np.amax(X, axis=0) # maximum of X array
xPredicted = xPredicted/np.amax(xPredicted, axis=0) # maximum of xPredicted (our input data for the prediction)
y = y/100 # max test score is 100

class Neural_Network(object):
  def __init__(self):
    #parameters
    self.inputSize = 2
    self.outputSize = 1
    self.hiddenSize = 3

    #weights
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize) # (3x2) weight matrix from input to hidden layer
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer

  def forward(self, X):
    #forward propagation through our network
    self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
    o = self.sigmoid(self.z3) # final activation function
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))

  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def backward(self, X, y, o):
    # backward propgate through the network
    self.o_error = y - o # error in output
    self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error

    self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
    self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error

    self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
    self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights

  def train(self, X, y):
    o = self.forward(X)
    self.backward(X, y, o)

  def saveWeights(self):
    np.savetxt("w1.txt", self.W1, fmt="%s")
    np.savetxt("w2.txt", self.W2, fmt="%s")
