import random
import mosquito as m
import human as h


def place_agents(grid, amount, mosquito=False, malaria_rate=0.0):
    '''Places a human or moquito and infects the later according to given
    malaria rate.'''
    for i in range(amount):
        # Keep tryin untill you find empty spot
        while True:
            row = random.randint(0, len(grid) - 1)
            column = random.randint(0, len(grid[0]) - 1)
            if grid[row][column] is 0:
                # If mosquito place mosquito
                if mosquito:
                    grid[row][column] = m.Mosquito()
                    # Infect mosquitos according to chance
                    if random.uniform(0, 1) <= malaria_rate:
                        grid[row][column].infected = True
                # If human place human
                else:
                    grid[row][column] = h.Human()
                break
