# As the roadlength shortens, when do the fundamental diagram start to deviate from those of long roadlengths?

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
            nextcarpos += roadLength
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
    for i in listofcars:
        vellist.append(i.getvel())
    flowrate = np.sum(vellist)/roadLength
    return flowrate


def run(numcars, roadLength, vmax, p):
    carlist = []
    for i in range(numcars):
        car_i = Car(i, 0)                                                           # Create cars 
        carlist.append(car_i)
    carlist.reverse()   

    for t in range(100):                                                            # Update 100 times for each car i 
        for i in range(numcars):
            carlist[i].update(vmax, carlist, i, p, roadLength)
    return flowrate(carlist, roadLength)


def output(roadLength, density):                                                    # density = #cars / roadlength
    carnumberlist = []                                                              
    for d in density:
        numbcars = int(d*roadLength)
        carnumberlist.append(numbcars)                                              # #cars = density * roadlength
        print(numbcars)

    meanFlowrate = []
    for numbcars in carnumberlist:                                            
        flowrate_list = []
        for k in range(50):                                                         # number of simulations
            flowrate = run(numbcars, roadLength, 2, 0.5)                            # create 50 flowrates per number of cars
            flowrate_list.append(flowrate)                      
        meanFlowrate.append(np.mean(flowrate_list))                                 # get the average flowrate per number of cars
    
    return meanFlowrate


density = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# plt.plot(density, output(48, density))
# plt.show()
plt.figure(1)
plt.title('Fundamental diagram: Flow rate vs density for different road lengths')
roadLength = [5, 10, 15, 20, 30, 40, 50, 80, 100, 150]
jet = plt.get_cmap('jet')
colors = iter(jet(np.linspace(0,1,len(roadLength))))
for rl in roadLength:
    meanfr = output(rl, density)
    plt.plot(density, meanfr, 'b', color=next(colors), label='L = '+str(rl))
plt.xlabel('Car density')
plt.ylabel('Flow rate')
plt.legend()
plt.show()

# plt.figure(2)
# plt.title('Fundamental diagram: Flow rate vs density')
# density50, meanfr50 = output(50)
# plt.plot(density50, meanfr50, 'b', label='L = 50')
# plt.xlabel('Car density')
# plt.ylabel('Flow rate')
# plt.legend()
# plt.savefig('tester4')

# 2.2e
# plt.figure(3)
# plt.title('Fundamental diagram: Flow rate vs density for different probabilities p')
# roadLength = 50
# colors = ["b", "darkturquoise"]
# p = [0.2, 0.8]
# for i, j in zip(colors, p):
#     density, meanfr = output(roadLength, j)
#     plt.plot(density, meanfr, color=i, label='p = '+str(j))
# plt.xlabel('Car density')
# plt.ylabel('Flow rate')
# plt.legend()
# plt.savefig('tester8')
# plt.show()



