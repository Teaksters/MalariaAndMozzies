import helpers as hp


class Grid(object):
    def __init__(self, width, height, humans, mosquitos, malaria_rate):
        self.gridH = [[0 for i in range(width)] for j in range(height)]
        self.gridM = [[0 for i in range(width)] for j in range(height)]
        went_fine = self.place_agents(humans, mosquitos, malaria_rate)
        if not went_fine:
            exit()

    def plot(self):
        '''Plot functie'''
        pass

    ###################################################################
    # Initialisation helperfunctions
    ###################################################################

    def place_agents(self, humans, mosquitos, malaria_rate):
        '''Randomly places humans and mosquitos on the grid according to given
        amount. Also has a chance of infecting the mosquitos with malaria
        according to the given malaria rate.
        If succesful returns True, else returns False.'''

        if self.legal_amounts(humans) and self.legal_amounts(mosquitos):
            hp.place_agents(self.gridH, humans)
            hp.place_agents(self.gridM, mosquitos, True, malaria_rate)
            return True
        # If illegal return false
        print("No legal amount of humans or mosquitos given.")
        return False

    def legal_amounts(self, agents):
        '''Checks if it is possible to place this amount of agents
        (humans or mosquitos) in the grid.'''
        if agents >= 0 and type(agents) == int:
            max = len(self.gridH) * len(self.gridH[0])
            if max > agents:
                return True
            return False
        return False
