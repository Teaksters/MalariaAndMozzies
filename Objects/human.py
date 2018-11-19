class Human(object):
    '''Class for humans in the preditor prey model.'''
    def __init__(self, coordinates):
        self.sick = False
        self.immune = False
        self.location = coordinates
