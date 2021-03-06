# copy paste from original cgp for now 
### arguments.py

# packages
import numpy as np
from numpy import random as r
#import random
from copy import copy

# other python scripts
from configuration import perc_args, streamData


### Mutation Methods
'''
    Define a set of mutation methods to be called on to mutate all/any of the argument classes.
    Consider limiting them to be strictly positive or non-negative
'''

def mut_uniform(value):
    if value == 0:
        return r.uniform(0,5)
    else:
        low = value*.85
        high = value * 1.15
        return r.uniform(low,high)

def mut_normal(value):
    if value == 0:
        return r.normal(3, 3*.1)
    else:
        mean = value
        sd = value * .1
        return r.normal(mean, sd)




### Argument Classes
    '''
    Define the various argument classes with an __init__() and mutate() function.
    Make sure that there is also a self.value attribute, and a self.num_samples
    attribute to define how many samples of that argument object type to create
    in the argument skeleton (see below)
    class ArgumentType(object):
        def __init__(self):
            self.num_samples = #
            self.value = #######
            self.mutate()
        def mutate(self):
            roll = r.random_integers(0,#)
            if roll == 0:
                self.value = #######
            elif roll == 1:
                self.value = #######
            ...
    
    Once an Argument Class is defined, at it to the list of arguments.
    The argument skeleton is filled by sampling from this list so even if
    an Arg Class is defined but not added to the list, it will not be used.
    '''
arguments = []


class argBool(object):

    def __init__(self, value=None):
        if value is None:
            self.value = True
            self.num_samples = 10
            self.mutate()
        else:
            self.value = value
            self.num_samples = 10

    def mutate(self):
        self.value = r.choice([True, False])
        # or should i force it to pick whatever it isn't...true-->false, false-->true?
arguments.append(argBool)


class argFloat(object):

    def __init__(self, value=None):
        if value is None:
            roll = r.random_integers(0,2)
            if roll == 0:
                self.value = 5.0
            elif roll == 1:
                self.value = 50.0
            elif roll == 2:
                self.value = 100.0
            self.num_samples = 10
            self.mutate()
        else:
            self.value = value
            self.num_samples = 10

    def mutate(self):
        roll = r.random_integers(0,2)
        if roll == 0:
            self.value = mut_normal(self.value)
        elif roll == 1:
            self.value = mut_uniform(self.value)
        else:
            pass
        if self.value < 0:
            self.value *= -1
        else:
            pass
arguments.append(argFloat)


class argInt(object):

    def __init__(self, value=None):
        if value is None:    
            roll = r.random_integers(0,2)
            if roll == 0:
                self.value = 5
            elif roll == 1:
                self.value = 50
            elif roll == 2:
                self.value = 100
            self.num_samples = 10
            self.mutate()
        else:
            self.value = value
            self.num_samples = 10

    def mutate(self):
        roll = r.random_integers(0,2)
        if roll == 0:
            self.value = mut_normal(self.value)
        elif roll == 1:
            self.value = mut_uniform(self.value)
        else:
            pass
        if self.value < 1:
            self.value = 1
        else:
            pass
        self.value = int(self.value)
arguments.append(argInt)