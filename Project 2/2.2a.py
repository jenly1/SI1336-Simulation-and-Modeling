# Cellular automaton traffic model 
# Condition 1: vi < vmax    => vi = vi-1
# Condition 2: vi >= d      => vi = vi-d, d=distance between current car and other car
# Condition 3: vi > 0       => vi -> vi-1 with probability p (randomizer)
# Condition 4: xi(t+1) = xi(t)+vi 

import matplotlib, random, math
import numpy as np
import pylab as plt
from matplotlib import animation

class Car:
    """ Instance variables unique to each instance """
    def __init__(self, pos, vel):                               
        self.pos = pos
        self.vel = vel

    def update(self, vmax, carlist, myindex, p, roadLength):    
        """ Updates the instances based on given conditions """
        if self.vel < vmax:                                     # Condition 1
            self.vel = min(self.vel+1, vmax)

        nextcarpos = carlist[myindex-1].getpos()                
        mypos = self.getpos()  
        d = nextcarpos-mypos
        if nextcarpos >= mypos:                                 
            if self.vel >= d:                                   # Condition 2
                self.vel = max(d-1,0)
        elif nextcarpos < mypos:
            nextcarpos += 50
            dnew = nextcarpos-mypos
            if self.vel >= dnew:
                self.vel = max(dnew-1,0)

        comparisonnumber = np.random.rand()                     # Generates random float in the range [0.0, 1.0)
        if p > comparisonnumber and self.vel > 0:               # Condition 3
            self.vel = max(self.vel-1, 0)

        self.pos = self.pos + self.vel                          # Condition 4
        if self.pos>=roadLength:
            self.pos = self.pos - roadLength

    def getpos(self):
        return self.pos

    def getvel(self):
        return self.vel


def flowrate(listofcars, roadLength):
    vellist = []
    for i in range(0, len(listofcars)):
        vellist.append(listofcars[i].getvel())
    return np.sum(vellist)/roadLength


def run(numcars, roadLength, numFrames, vmax, p, distr):
    carlist = []
    for i in range(numcars):
        car_i = Car(i*distr, 0)                                 # Create cars 
        carlist.append(car_i)
    carlist.reverse()   

    for t in range(500):                                        # Update 500 times for each car i 
        for i in range(numcars):
            carlist[i].update(vmax, carlist, i, p, roadLength)

    return flowrate(carlist, roadLength)

rl = 50
carnumberlist = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35]
averagelist = []

for i in range(len(carnumberlist)):
    listfornow = []
    for k in range(500):                                        # 500 simulations
        listfornow.append(run(carnumberlist[i], rl, 500, 2, 0.5, 1))
    averagelist.append(np.mean(listfornow))


plt.clf()
plt.figure(1)
plt.title('Fundamental diagram: Flow rate vs density')
plt.plot(np.array(carnumberlist)/rl, averagelist, 'b', label="Flow rate")
plt.xlabel('Car density')
plt.ylabel('Flow rate')
plt.legend(fontsize=12)
plt.savefig('tester')
plt.show()
