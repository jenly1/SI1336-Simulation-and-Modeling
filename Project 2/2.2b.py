# Estimate the statistical accuracy
# Collect flow rate over 100 time steps
# Compute standard error of each flow rate, SE >= 0.01
# How long does the equilibration need to be to get accurate results?

import random, math
import pylab as plt
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


def listofcars(numcars, roadlength, vmax, p):
    carlist = []
    for i in range(numcars):
        car_i = Car(i, 0)                                           # Create car i
        carlist.append(car_i)
    carlist.reverse()   
                                   
    for j in range(50):                                             # Update 50 times for each car i so that initial conditons doesnt affect it
        for i in range(numcars):                                    # Updates every car i so we get a 'new' carlist 
            carlist[i].update(vmax, carlist, i, p, roadlength)
    return carlist

roadlength = 50
numcars= 25
vmax = 2
p = 0.5

def standardError(N):
    flowrateArray = []      
    flowrateArray_nCars = []
    for n in range(N):                                              # N=number of simulations
        carlist = listofcars(numcars, roadlength, vmax, p)          # Generates different values for 25 cars
        flowRate = flowrate(carlist, roadlength)                    # Calculates the flowrate for 25 cars 
        flowrateArray_nCars.append(flowRate)                        # The flowrate will be added to                          
    flowrateArray.append(flowrateArray_nCars[:])
    error = np.std(flowrateArray)/np.sqrt(N)                        # std = standard deviation
    return error
    

def output():
    standardErrorArray = []
    simulationArray = range(2000, 10000, 200)
    for i in simulationArray:
        se = standardError(i)
        standardErrorArray.append(round(se,5))    # round the number iwth 5 decimals
        if se >= 0.001:
            pass
        else:
            print("The number of simulations needed to be done before getting a standard error of 0.001 is approximately "+str(i)+"-"+str(i+200))
            x = range(2000, i+200, 200)
            break
        print((round(standardError(i),5)))
        
    plt.ticklabel_format(style='plain', axis='x', useOffset=False)
    plt.plot(x,standardErrorArray, 'b')
    plt.title("Standard error for flow rate")
    plt.xlabel("Number of simulations")
    plt.ylabel("Standard error")
    plt.show()

output()