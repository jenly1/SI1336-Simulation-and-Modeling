# A 2D random walk with single steps along x or y
# Generate many random walks for step: range(N)
# Determime the root mean squared end-to-end distance: sqrt(<R^2>)
# Plot the estimate of the root-mean-square fluctuation: sqrt((<R^2>)-<R>^2)*#walks/(#walks-1)
# Plot the standard error estimate 

import pylab, random, numpy, math

def randomwalk(step):
    # Arrays with the same size as the number of steps
    x = numpy.zeros(step)
    y = numpy.zeros(step)

    # Random-walk generator
    for i in range(step):
        n = random.randint(0,3)

        if n == 0:
            x[i] = x[i-1] + 1
            y[i] = y[i-1] 

        elif n == 1:
            x[i] = x[i-1] - 1
            y[i] = y[i-1] 

        elif n == 2: 
            x[i] = x[i-1] 
            y[i] = y[i-1] + 1

        elif n == 3:
            x[i] = x[i-1] 
            y[i] = y[i-1] - 1

    # Distances R^2, R
    d = (x[step-1]-x[0])**2 + (y[step-1]-y[0])**2
    dsqrt = math.sqrt((x[step-1]-x[0])**2 + (y[step-1]-y[0])**2)

    return d, dsqrt


N = range(1, 200)
rmsd_list = []
rmsf_list = []
see_list = []

for step in N:                              # For step N
    d_list = []
    dsqrt_list = []

    for walk in range(1000):                 # Generate 100 different walks per step
        d, dsqrt = randomwalk(step)
        d_list.append(d)
        dsqrt_list.append(dsqrt)

    # Average <R^2>, <R>
    d_mean = numpy.average(d_list)
    dsqrt_mean = numpy.average(dsqrt_list)
    
    # Variance V = <R^2> - <R>^2
    var = d_mean - dsqrt_mean**2

    # Root-mean-square fluctuation 
    rmsf = math.sqrt(var * 1000 / 999)
    rmsf_list.append(rmsf)

    # Standard error estimate
    see = math.sqrt(var / 999)
    see_list.append(see)

    # Root-mean-square end-to-end distance 
    rmsd = math.sqrt(d_mean)
    rmsd_list.append(rmsd)
    #print("The rmsd for step "+str(step)+" is:", rmsd)

# Plot rmsf and see against the step number 
# pylab.figure(1)
# pylab.title("Root-mean-square fluctuation (RMSF) dependence on step N")
# pylab.xlabel("Step N")
# pylab.ylabel("RMSF")
# pylab.plot(N, rmsf_list,"r",label = "RMSF")

# pylab.figure(2)
# pylab.title("Standard error estimate (SEE) dependence on step N")
# pylab.xlabel("Step N")
# pylab.ylabel("SEE")
# pylab.plot(N, see_list,"g", label ="SEE")

pylab.figure(3)
pylab.title("Root-mean-square distance (RMSD) dependence on step N")
pylab.xlabel("Step N")
pylab.ylabel("RMSD")
pylab.plot(N, rmsd_list,"b", label ="SEE")
pylab.plot(N, [numpy.sqrt(i) for i in N],color="deepskyblue", label="sqrt(N)")
pylab.legend()



pylab.show()
