import matplotlib.pyplot as plt
import numpy as np

# progressbar, copied from:
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


class Model:
    def __init__(self, width=50, height=50, nHuman=50, nMosquito=2000,
                 initMosquitoHungry=0.5,
                 initHumanInfected=0.5,
                 humanInfectionProb=0.7,
                 mosquitoInfectionProb=0.7,
                 mosquitoHungryDieProb=0.01,
                 biteProb=0.7,
                 mosquitoHungryProb=0.2,
                 humanCureProb = 0.002,
                 humanSickDieProb = 0.01,
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
        self.mosquitoHungryDieProb = mosquitoHungryDieProb
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

    def update(self, SimulateMosquitonets, SimulateMosquitonetsAftertimeSteps,TimeStep):
        """
        Perform one timestep:
        1.  Update mosquito population. Move the mosquitos. If a mosquito is
            hungry it can bite a human with a probability biteProb.
            Update the hungry state of the mosquitos.
        2.  Update the human population. If a human dies remove it from the
            population, and add a replacement human.
        """

        MosquitoInfectedCount = 0
        MosquitoHungryCount = 0
        for m in self.mosquitoPopulation:
            m.move(width = self.width, height = self.height)
            for h in self.humanPopulation:
                if m.position == h.position and m.hungry and np.random.uniform() <= self.biteProb:
                    # simulate mosquitonets if 
                    if SimulateMosquitonets == True:
                        if TimeStep > SimulateMosquitonetsAftertimeSteps:
                            if np.random.uniform() <= 0.2:
                                m.bite(h, m, self.humanInfectionProb, self.mosquitoInfectionProb)
                        else:
                            m.bite(h, m, self.humanInfectionProb, self.mosquitoInfectionProb)
                    else:
                        m.bite(h, m, self.humanInfectionProb, self.mosquitoInfectionProb)
            
            '''Each mosquito has a chance to die when hungry, and suddenly a new mosquito respawns!'''
            if np.random.uniform() <= self.mosquitoHungryDieProb:
                m.infected = False
                m.hungry = False

            '''Each musquito has a chance to get hungry'''
            if np.random.uniform() <= self.mosquitoHungryProb:
                m.hungry = True

            if m.infected == True:
                MosquitoInfectedCount += 1
            if m.hungry == True:
                MosquitoHungryCount += 1
        
        humanInfectedCount = 0
        humanSusceptibleCount = 0
        humanResistentCount = 0
        for h in self.humanPopulation:
            if h.state == 'S':
                humanSusceptibleCount += 1
            if h.state == 'D':
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

        return humanInfectedCount, humanResistentCount, humanSusceptibleCount, MosquitoInfectedCount, MosquitoHungryCount


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
    SimulateMosquitonets = True
    SimulateMosquitonetsAftertimeSteps = 500
    plotData = True
    """
    Run a simulation for an indicated number of timesteps.
    """
    file = open(fileName + '.csv', 'w')
    sim = Model()
    print('Starting simulation')

    while t < timeSteps:
        [humanInfectedCount, humanResistentCount, humanSusceptibleCount, MosquitoInfectedCount, MosquitoHungryCount] = sim.update(SimulateMosquitonets, SimulateMosquitonetsAftertimeSteps, TimeStep = t)  # Catch the data
        line = str(t) + ',' + str(humanInfectedCount) + ',' + str(humanResistentCount) + ',' + str(humanSusceptibleCount) + ',' + str(MosquitoInfectedCount) + ',' + str(MosquitoHungryCount)   + '\n'  # Separate the data with commas
        file.write(line)  # Write the data to a .csv file
        t += 1
        printProgressBar(t, timeSteps, prefix = 'Calculating simulation:', suffix = 'Complete', length = 50) # print progress
    file.close()

    if plotData:
        """
        Make a plot by from the stored simulation data.
        """
        data = np.loadtxt(fileName + '.csv', delimiter=',')
        time = data[:, 0]
        humanInfectedCount = data[:, 1]
        humanResistentCount = data[:, 2]
        humanSusceptibleCount = data[:, 3]
        MosquitoInfectedCount = data[:, 4]
        MosquitoHungryCount = data[:, 5]

        # subplot human data
        plt.subplot(2, 1, 1)
        plt.plot(time, humanInfectedCount, label='humanInfectedCount')
        plt.plot(time, humanResistentCount, label='humanResistentCount')
        plt.plot(time, humanSusceptibleCount, label='humanSusceptibleCount')
        if SimulateMosquitonets == True:
            plt.axvline(SimulateMosquitonetsAftertimeSteps)
        plt.legend()

        # subplot mosquito data
        plt.subplot(2, 1, 2)
        plt.plot(time, MosquitoInfectedCount, label='MosquitoInfectedCount')
        plt.plot(time, MosquitoHungryCount, label='MosquitoHungryCount')
        if SimulateMosquitonets == True:
            plt.axvline(SimulateMosquitonetsAftertimeSteps)
        plt.legend()

        # plot plot
        plt.show()