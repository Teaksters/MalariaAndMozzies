import matplotlib.pyplot as plt
import numpy as np


class Model:
    def __init__(self, width=50, height=50, nHuman=20, nMosquito=1000,
                 initMosquitoHungry=0.5,
                 initHumanInfected=0.5,
                 humanInfectionProb=0.7,
                 mosquitoInfectionProb=0.7,
                 biteProb=0.9,
                 mosquitoHungryProb=0.2,
                 humanCureProb = 0.005,
                 humanSickDieProb = 0.005,
                 humanDieProb = 0.005):
        """
        Model parameters
        Initialize the model with the width and height parameters.
        """
        self.height = height
        self.width = width
        self.nHuman = nHuman
        self.nMosquito = nMosquito
        self.humanInfectionProb = humanInfectionProb
        self.mosquitoInfectionProb = mosquitoInfectionProb
        self.biteProb = biteProb
        self.presentHumans = set()
        self.mosquitoHungryProb = mosquitoHungryProb
        self.humanCureProb = humanCureProb
        self.humanSickDieProb = humanSickDieProb
        self.humanDieProb = humanDieProb


        """
        Population setters
        Make a data structure in this case a list with the humans and mosquitos.
        """
        self.humanPopulation = self.set_human_population(initHumanInfected)
        self.mosquitoPopulation = self.set_mosquito_population(initMosquitoHungry)

    def set_human_population(self, initHumanInfected):
        """
        This function makes the initial human population, by iteratively adding
        an object of the Human class to the humanPopulation list.
        The position of each Human object is randomized. A number of Human
        objects is initialized with the "infected" state.
        """
        humanPopulation = []
        for i in range(self.nHuman):
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            '''Place humans only on human free spots randomly.'''
            while True:
                # If location is not taken place human
                if (x, y) not in self.presentHumans:
                    if (i / self.nHuman) <= initHumanInfected:
                        state = 'I'  # I for infected
                    else:
                        state = 'S'  # S for susceptible
                    humanPopulation.append(Human(x, y, state))
                    self.presentHumans.add((x, y))
                    break
                # Try again for new location
                x = np.random.randint(self.width)
                y = np.random.randint(self.height)
        return humanPopulation

    def set_mosquito_population(self, initMosquitoHungry):
        """
        This function makes the initial mosquito population, by iteratively
        adding an object of the Mosquito class to the mosquitoPopulation list.
        The position of each Mosquito object is randomized.
        A number of Mosquito objects is initialized with the "hungry" state.
        """
        mosquitoPopulation = []
        for i in range(self.nMosquito):
            x = np.random.randint(self.width)
            y = np.random.randint(self.height)
            if (i / self.nMosquito) <= initMosquitoHungry:
                hungry = True
            else:
                hungry = False
            mosquitoPopulation.append(Mosquito(x, y, hungry))
        

        return mosquitoPopulation

    def update(self):
        """
        Perform one timestep:
        1.  Update mosquito population. Move the mosquitos. If a mosquito is
            hungry it can bite a human with a probability biteProb.
            Update the hungry state of the mosquitos.
        2.  Update the human population. If a human dies remove it from the
            population, and add a replacement human.
        """

        for m in self.mosquitoPopulation:
            m.move(width = self.width, height = self.height)
            for h in self.humanPopulation:
                if m.position == h.position and m.hungry and np.random.uniform() <= self.biteProb:
                    m.bite(h, m, self.humanInfectionProb, self.mosquitoInfectionProb)
            
            '''Each musquito has a chance to get hungry'''
            if np.random.uniform() <= self.mosquitoHungryProb:
                m.hungry = True
        
        humanInfectedCount = 0
        humanDeathCount = 0
        humanResistentCount = 0
        for h in self.humanPopulation:
            if h.state == 'D':
                humanDeathCount += 1
                ''''respawn human!'''
                h.state = 'S'
            if np.random.uniform() <= self.humanDieProb:
                h.state = 'D'
            if h.state == 'I':
                humanInfectedCount += 1
                if np.random.uniform() <= self.humanCureProb:
                    h.state = 'R'
                if np.random.uniform() <= self.humanSickDieProb:
                    h.state = 'D'
            if h.state == 'R':
                humanResistentCount +=1

        """
        To implement: update the data/statistics e.g. infectedCound,
                      deathCount, etc.
        """

        return humanInfectedCount, humanDeathCount, humanResistentCount, len(self.mosquitoPopulation)


class Mosquito:
    def __init__(self, x, y, hungry):
        """
        Class to model the mosquitos. Each mosquito is initialized with a random
        position on the grid. Mosquitos can start out hungry or not hungry.
        All mosquitos are initialized infection free (this can be modified).
        """
        self.position = [x, y]
        self.hungry = hungry
        self.infected = False
        self.timeSinceFeed = 0

    def bite(self, human, musquito, humanInfectionProb, mosquitoInfectionProb):
        """
        Function that handles the biting. If the mosquito is infected and the
        target human is susceptible, the human can be infected.
        If the mosquito is not infected and the target human is infected, the
        mosquito can be infected.
        After a mosquito bites it is no longer hungry.
        """
        if self.infected and human.state == 'S':
            if np.random.uniform() <= humanInfectionProb:
                human.state = 'I'
        elif not self.infected and human.state == 'I':
            if np.random.uniform() <= mosquitoInfectionProb:
                self.infected = True
        musquito.hungry = False


    def move(self, width, height):
        """
        Moves the mosquito one step in a random direction.
        """
        deltaX = np.random.randint(-1, 2)
        deltaY = np.random.randint(-1, 2)

        '''set movement boundries'''
        if (self.position[0] + deltaX) < 0:
            deltaX = 1
        if (self.position[1] + deltaY) < 0:
            deltaY = 1
        if (self.position[0] + deltaX) > width:
            deltaX = -1
        if (self.position[1] + deltaY) > height:
            deltaY = -1

        self.position[0] += deltaX
        self.position[1] += deltaY

class Human:
    def __init__(self, x, y, state):
        """
        Class to model the humans. Each human is initialized with a random
        position on the grid. Humans can start out susceptible or infected
        (or immune).
        """
        self.position = [x, y]
        self.state = state


if __name__ == '__main__':
    """
    Simulation parameters
    """
    fileName = 'simulation'
    timeSteps = 1000
    t = 0
    plotData = True
    """
    Run a simulation for an indicated number of timesteps.
    """
    file = open(fileName + '.csv', 'w')
    sim = Model()
    print('Starting simulation')
    while t < timeSteps:
        # print("calculating t = ", t)
        [humanInfectedCount, humanDeathCount, humanResistentCount, nmosquitos] = sim.update()  # Catch the data
        line = str(t) + ',' + str(humanInfectedCount) + ',' + str(humanDeathCount) + ',' + str(humanResistentCount) + ',' + str(nmosquitos)  + '\n'  # Separate the data with commas
        file.write(line)  # Write the data to a .csv file

        t += 1
    file.close()

    if plotData:
        """
        Make a plot by from the stored simulation data.
        """
        data = np.loadtxt(fileName + '.csv', delimiter=',')
        time = data[:, 0]
        humanInfectedCount = data[:, 1]
        humanDeathCount = data[:, 2]
        humanResistentCount = data[:, 3]
        nmosquitos = data[:, 4]
        plt.plot(time, humanInfectedCount, label='humanInfectedCount')
        plt.plot(time, humanDeathCount, label='humanDeathCount')
        plt.plot(time, humanResistentCount, label='humanResistentCount')
        plt.legend()
        plt.show()