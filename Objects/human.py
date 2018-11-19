class Human(object):
    '''Class for humans in the preditor prey model.'''
    def __init__(self, coordinates):
        self.status = 0
        self.location = coordinates
