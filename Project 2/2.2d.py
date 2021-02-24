# Estimate the statistical accuracy
# Collect flow rate over 100 time steps
# Compute standard error of each flow rate, SE >= 0.01
# How long does the equilibration need to be to get accurate results?

import random, math
import numpy as np

class Car:
    """ Instance variables unique to each instance """
    def __init__(self, pos, vel):                               
        self.pos = pos
        self.vel = vel

    def update(self, vmax, carlist, myindex, p, roadlength):    
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
        if self.pos>=roadlength:
            self.pos = self.pos - roadlength

    def getpos(self):
        return self.pos

    def getvel(self):
        return self.vel


def flowrate(listofcars, roadlength):
    vellist = []
    for i in range(0, len(listofcars)):
        vellist.append(listofcars[i].getvel())
    return np.sum(vellist)/roadlength  


def run(numcars, roadlength, vmax, p, timestep):
    carlist = []
    for i in range(numcars):
        car_i = Car(i, 0)                                       # Create car i
        carlist.append(car_i)
    carlist.reverse()   

    frlist = []                                                 # List of flowrates with the length of the timestep                                         
    for j in range(timestep):                                   # Update 100 times for each car i
        for i in range(numcars):                                # Updates every car i so we get a 'new' carlist 
            carlist[i].update(vmax, carlist, i, p, roadlength)
        frnew = flowrate(carlist, roadlength)
        frlist.append(frnew)
    return frlist