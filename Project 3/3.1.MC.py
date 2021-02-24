
import math as math
import numpy as np
from time import process_time
import random
import matplotlib.pyplot as plt

# Number of dimensions
numDims = 10
# Radius of the sphere
radius = 1
# numSamples_list is a list containing different numbers of random points that we want to generate in our MC method.
# Change it whichever way you like. Going past 1000000 doesn't seem to yield much better results
numSamples_list = range(10000, 1000000, 50000) 

run_times = np.zeros(len(numSamples_list))
errors = np.zeros(len(numSamples_list))
exact_solution = math.pi**(numDims/2)/math.gamma(numDims/2+1)*radius**numDims

def getRandVector(numD, r):
    retArray = np.zeros(numD, dtype="double")
    for i in range(numD):
        retArray[i] = random.random() * r * 2 - r
    return retArray

def calcIntegral(numD, r, numS):
    hit_or_miss = np.zeros(numS, dtype="double")
    for i in range(numS):
        vec = getRandVector(numD, r)
        if np.linalg.norm(vec) <= radius:
            hit_or_miss[i] = 1
    hit_rate = np.average(hit_or_miss)
    volume = hit_rate * (2 * r) ** numD
    return volume

# Below we run the integration for all the sample numbers in numSamples_list, calculate the absolute value of the errors
# and record the time it takes to perform the integration. The errors and run times are stored in lists and then plotted.
integralList = []
for i in range(len(numSamples_list)):
    for j in range(0, i):
        print("Running for numSamples =", numSamples_list[i], "...")
        t = process_time()
        integral = calcIntegral(numDims, radius, numSamples_list[i])
        integralList.append(integral)
        t = process_time() - t
        # errors[i] = abs(integral - exact_solution) # I have chosen to take the absolute of the error.
        run_times[i] = t
        # print("error =", round(errors[i], 6))

# Calculating error
fsqList, fsumList = [], []
for f in integralList:
    fsq = f**2
    fsqList.append(fsq)
    fsumList.append(f)

# <f^2>
fsqsum = sum(fsqList)/len(fsqList)

# <f>^2
fsqsum2 = (sum(fsumList)/len(fsumList)) ** 2

# sigma
sigma = fsqsum - fsqsum2
sigmasqrt = np.sqrt(sigma)

# standard error 
error = sigmasqrt/np.sqrt(len(fsumList))
print(error)

plt.figure()
plt.title("Error time dependence - Monte Carlo")
plt.plot(error, run_times, "b")
plt.plot(np.zeros(len(run_times)), run_times, color="k")
plt.xlabel("Time [s]")
plt.ylabel("Absolute error [m^10]")
plt.show()